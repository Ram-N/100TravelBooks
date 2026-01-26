#!/usr/bin/env python3
"""
update_status.py - Sync database Status field with completed writeups

Scans book-writeups/ directory for completed .md files and updates the
master-candidates.csv database to mark those books as "Completed".

Usage:
    python update_status.py                 # Dry run (preview changes)
    python update_status.py --apply         # Apply changes to database
    python update_status.py --status-to Completed  # Custom status value
"""

import argparse
import csv
import re
import sys
import shutil
import unicodedata
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# FILENAME MATCHING (same logic as recommend_next.py)
# ═══════════════════════════════════════════════════════════════════════════

def normalize_for_filename(text: str) -> str:
    """Normalize text for filename matching."""
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Strip subtitles (anything after colon or em-dash)
    text = re.split(r'[:\u2014]', text)[0]

    # Normalize Unicode characters to ASCII equivalents (ś→s, ñ→n, etc.)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove common articles at the start
    text = re.sub(r'^(the|a|an)\s+', '', text)

    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s-]', '', text)

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Strip leading/trailing hyphens
    text = text.strip('-')

    return text


def generate_filename_candidates(title: str, author: str) -> List[str]:
    """Generate possible filename patterns for matching."""
    candidates = []

    # Normalize title and author
    title_norm = normalize_for_filename(title)
    author_norm = normalize_for_filename(author)

    # Generate title variations:
    # 1. Remove articles only
    title_no_articles = re.sub(r'\b(the|a|an)\b', '', title_norm)
    title_no_articles = re.sub(r'-+', '-', title_no_articles).strip('-')

    # 2. Remove both articles AND common prepositions (more forgiving)
    title_minimal = re.sub(r'\b(the|a|an|at|of|in|on|from|to|with|by|for)\b', '', title_norm)
    title_minimal = re.sub(r'-+', '-', title_minimal).strip('-')

    # Extract author last name (assume last word)
    author_parts = author_norm.split('-')
    author_lastname = author_parts[-1] if author_parts else author_norm

    # Generate all pattern variations
    variations = []

    # Full title (with articles/prepositions)
    variations.append((title_norm, 'full'))

    # No articles
    if title_no_articles != title_norm:
        variations.append((title_no_articles, 'no_articles'))

    # Minimal (no articles or prepositions)
    if title_minimal != title_norm and title_minimal != title_no_articles:
        variations.append((title_minimal, 'minimal'))

    # Generate candidates for each variation
    for title_var, var_type in variations:
        if not title_var:
            continue

        # Pattern: title-author
        if author_norm:
            candidates.append(f"{title_var}-{author_norm}")

        # Pattern: title-lastname
        if author_lastname and author_lastname != author_norm:
            candidates.append(f"{title_var}-{author_lastname}")

        # Pattern: title only
        candidates.append(title_var)

    # Remove duplicates while preserving order
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    return unique_candidates


def fuzzy_match_score(candidate: str, filename: str) -> float:
    """
    Calculate fuzzy match score between candidate and filename.

    Returns a score from 0.0 (no match) to 1.0 (perfect match).
    Score is based on word overlap percentage.
    """
    # Split into words
    candidate_words = set(candidate.split('-'))
    filename_words = set(filename.split('-'))

    # Remove empty strings, very short words, and common prepositions (noise)
    stop_words = {'in', 'on', 'at', 'to', 'of', 'the', 'a', 'an', 'up', 'down', 'by', 'with', 'from', 'for'}
    candidate_words = {w for w in candidate_words if len(w) > 1 and w not in stop_words}
    filename_words = {w for w in filename_words if len(w) > 1 and w not in stop_words}

    if not candidate_words or not filename_words:
        return 0.0

    # Calculate overlap with exact matches
    overlap = candidate_words & filename_words

    # Also check for partial word matches (handles singular/plural, typos)
    partial_matches = 0
    for c_word in candidate_words - overlap:
        for f_word in filename_words - overlap:
            # Check if one word is a substring of the other (handles valley/valleys)
            # OR if they're very similar (handles typos like assasins/assassins)
            if c_word in f_word or f_word in c_word:
                partial_matches += 1
                break
            # Check Levenshtein-like similarity (allow 1-2 char difference)
            if len(c_word) >= 4 and len(f_word) >= 4:
                if abs(len(c_word) - len(f_word)) <= 2:
                    # Simple character overlap check
                    common_chars = sum((set(c_word) & set(f_word)).__len__() for _ in [1])
                    if common_chars >= min(len(c_word), len(f_word)) - 2:
                        partial_matches += 0.5
                        break

    # Score based on what percentage of candidate words appear in filename
    total_matches = len(overlap) + partial_matches
    score = total_matches / len(candidate_words) if candidate_words else 0.0

    return score


def is_book_completed(title: str, author: str, completed_files: List[str]) -> bool:
    """Check if a book has been completed based on filename matching."""
    candidates = generate_filename_candidates(title, author)

    for candidate in candidates:
        # Check for exact match
        if candidate in completed_files:
            return True

        # Check for substring match (handles variations)
        for completed in completed_files:
            if candidate in completed or completed in candidate:
                return True

            # Fuzzy match: if 75%+ of candidate words appear in filename, it's a match
            score = fuzzy_match_score(candidate, completed)
            if score >= 0.75:
                return True

    return False


# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════

def get_completed_files(writeups_dir: Path) -> List[str]:
    """Get list of completed writeup filenames (without .md extension)."""
    if not writeups_dir.exists():
        print(f"Warning: Writeups directory not found: {writeups_dir}", file=sys.stderr)
        return []

    # Get all .md files and remove extension
    # Exclude workspace files and other non-book files
    completed = []
    for f in writeups_dir.glob('*.md'):
        # Skip workspace files and other non-book files
        if f.stem not in ['workspace', 'README', 'TEMPLATE']:
            completed.append(f.stem)

    return completed


def load_database(db_path: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Load the CSV database and return (fieldnames, rows)."""
    if not db_path.exists():
        print(f"Error: Database file not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    with open(db_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    return fieldnames, rows


def save_database(db_path: Path, fieldnames: List[str], rows: List[Dict[str, Any]]):
    """Save the database to CSV."""
    with open(db_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_backup(db_path: Path) -> Path:
    """Create timestamped backup of database."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = db_path.parent / f"{db_path.stem}-backup-{timestamp}.csv"
    shutil.copy2(db_path, backup_path)
    return backup_path


# ═══════════════════════════════════════════════════════════════════════════
# UPDATE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def update_status(
    rows: List[Dict[str, Any]],
    completed_files: List[str],
    target_status: str = 'Completed'
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Update Status field for completed books.

    Returns:
        (updated_rows, changes) where changes is a list of dicts with update info
    """
    updated_rows = []
    changes = []

    for row in rows:
        title = row.get('Title', '')
        author = row.get('Author', '')
        current_status = row.get('Status', '').strip()

        # Check if this book has a completed writeup
        if is_book_completed(title, author, completed_files):
            # Update if status is NOT already "Completed"
            if current_status != target_status:
                # Create updated row
                updated_row = row.copy()
                updated_row['Status'] = target_status
                updated_rows.append(updated_row)

                # Track the change
                changes.append({
                    'title': title,
                    'author': author,
                    'old_status': current_status,
                    'new_status': target_status,
                })
            else:
                # Already has correct status, keep as-is
                updated_rows.append(row)
        else:
            # Not completed, keep as-is
            updated_rows.append(row)

    return updated_rows, changes


# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTING
# ═══════════════════════════════════════════════════════════════════════════

def format_changes(changes: List[Dict[str, Any]], dry_run: bool = True) -> str:
    """Format changes for display."""
    if not changes:
        return "No changes needed - all completed books already have correct status."

    lines = []

    if dry_run:
        lines.append("═" * 70)
        lines.append("  DRY RUN - Preview of changes (use --apply to save)")
        lines.append("═" * 70)
    else:
        lines.append("═" * 70)
        lines.append("  CHANGES APPLIED")
        lines.append("═" * 70)

    lines.append("")
    lines.append(f"Total books to update: {len(changes)}")
    lines.append("")

    for i, change in enumerate(changes, 1):
        lines.append(f"{i}. {change['title']} by {change['author']}")
        lines.append(f"   Status: {change['old_status']} → {change['new_status']}")
        lines.append("")

    lines.append("═" * 70)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# MAIN CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Sync database Status field with completed writeups',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Dry run (preview changes)
  %(prog)s --apply                   # Apply changes to database
  %(prog)s --status-to Completed     # Use custom status value
  %(prog)s --db my-database.csv      # Use different database file
        """
    )

    # Main options
    parser.add_argument(
        '--apply',
        action='store_true',
        help='Apply changes to database (default is dry run)'
    )
    parser.add_argument(
        '--status-to',
        default='Completed',
        help='Status value to set for completed books [default: Completed]'
    )

    # Data source options
    parser.add_argument(
        '--db',
        default='master-candidates.csv',
        help='Database file to update [default: master-candidates.csv]'
    )
    parser.add_argument(
        '--writeups-dir',
        help='Path to book-writeups directory [default: ../book-writeups]'
    )

    args = parser.parse_args()

    # Resolve paths
    db_path = Path(__file__).parent.parent / 'database' / args.db

    if args.writeups_dir:
        writeups_dir = Path(args.writeups_dir)
    else:
        writeups_dir = Path(__file__).parent.parent / 'book-writeups'

    # Load data
    print(f"Loading database: {db_path}")
    fieldnames, rows = load_database(db_path)
    print(f"Total books in database: {len(rows)}")

    print(f"\nScanning completed writeups: {writeups_dir}")
    completed_files = get_completed_files(writeups_dir)
    print(f"Completed writeup files found: {len(completed_files)}")

    if not completed_files:
        print("\nNo completed writeup files found. Nothing to update.")
        sys.exit(0)

    # Perform update
    print(f"\nAnalyzing status changes (target status: '{args.status_to}')...")
    updated_rows, changes = update_status(rows, completed_files, args.status_to)

    # Display results
    print("\n")
    output = format_changes(changes, dry_run=not args.apply)
    print(output)

    # Apply changes if requested
    if args.apply and changes:
        # Create backup
        print("\nCreating backup...")
        backup_path = create_backup(db_path)
        print(f"Backup saved: {backup_path}")

        # Save updated database
        print(f"\nSaving updated database: {db_path}")
        save_database(db_path, fieldnames, updated_rows)
        print(f"✓ Database updated successfully!")
        print(f"  {len(changes)} book(s) marked as '{args.status_to}'")
    elif not args.apply and changes:
        print("\nTo apply these changes, run:")
        print(f"  python {Path(__file__).name} --apply")

    print()


if __name__ == '__main__':
    main()
