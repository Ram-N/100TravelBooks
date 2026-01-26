#!/usr/bin/env python3
"""
update_status.py - Sync database Status field with completed writeups

Scans book-writeups/ directory for completed .md files, reads the actual title
from inside each file, and updates the master-candidates.csv database to mark
those books as "Completed".

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
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# TITLE EXTRACTION FROM WRITEUP FILES
# ═══════════════════════════════════════════════════════════════════════════

def extract_title_from_writeup(filepath: Path) -> str:
    """
    Extract the book title from a writeup .md file.

    Looks for patterns like:
    - # **# [Entry Number] — Title**
    - # XX — Title
    - # Title

    Returns the title, or None if not found.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read first 20 lines (title should be near the top)
            for i, line in enumerate(f):
                if i > 20:
                    break

                line = line.strip()

                # Skip empty lines and horizontal rules
                if not line or line.startswith('---'):
                    continue

                # Look for markdown headers - must be single # (not ## or ###)
                # Pattern: # **# [Entry Number] — Title** or # XX — Title or # Title
                if line.startswith('# '):
                    # Skip author sections and other metadata
                    if any(keyword in line.lower() for keyword in ['the author', 'author:', 'essentials', 'book:']):
                        continue

                    # Skip lines with birth/death years like (1902–1986)
                    if re.search(r'\(\d{4}[–-]\d{4}\)', line):
                        continue

                    # Check for em-dash separator (—)
                    if '—' in line:
                        # Extract everything after the em-dash
                        parts = line.split('—', 1)
                        if len(parts) == 2:
                            title = parts[1].strip()
                            # Remove markdown formatting and brackets
                            title = re.sub(r'\*+', '', title)
                            title = re.sub(r'\[.*?\]', '', title)
                            title = title.strip()
                            if title and len(title) > 2:
                                return title

                    # No separator - just take the header text as-is
                    else:
                        title = line.lstrip('#').strip()
                        # Remove markdown formatting and brackets
                        title = re.sub(r'\*+', '', title)
                        title = re.sub(r'\[.*?\]', '', title)
                        # Remove placeholder entry numbers like "XX:" or "XX :" or "##:"
                        title = re.sub(r'^[X#]+\s*:\s*', '', title)
                        title = title.strip()
                        # Make sure it's a reasonable title (not just "XX" or similar)
                        if title and len(title) > 3 and not re.match(r'^[IVX]+$', title):
                            return title

        return None

    except Exception as e:
        print(f"Warning: Could not read {filepath.name}: {e}", file=sys.stderr)
        return None


def normalize_title_for_matching(title: str) -> str:
    """
    Normalize a title for case-insensitive matching.
    Removes extra whitespace and standardizes quotes.
    """
    if not title:
        return ""

    # Normalize whitespace
    title = ' '.join(title.split())

    # Normalize quotes
    title = title.replace('"', '"').replace('"', '"')
    title = title.replace(''', "'").replace(''', "'")

    return title.strip()


def find_book_in_database(title: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Find a book in the database by exact title match (case-insensitive).
    Also matches if the main title matches (ignoring subtitles after colon).

    Returns the matching row, or None if not found.
    """
    normalized_title = normalize_title_for_matching(title).lower()

    # Also create version without subtitle (everything before colon)
    title_no_subtitle = normalized_title.split(':')[0].strip()

    for row in rows:
        db_title = normalize_title_for_matching(row.get('Title', '')).lower()
        db_title_no_subtitle = db_title.split(':')[0].strip()

        # Match either full title or main title (without subtitle)
        if normalized_title == db_title or title_no_subtitle == db_title_no_subtitle:
            return row

    return None


# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════

def get_completed_titles(writeups_dir: Path) -> Dict[str, Path]:
    """
    Get titles from completed writeup files by reading them.

    Returns dict mapping title -> filepath.
    """
    if not writeups_dir.exists():
        print(f"Warning: Writeups directory not found: {writeups_dir}", file=sys.stderr)
        return {}

    completed_titles = {}

    for filepath in writeups_dir.glob('*.md'):
        # Skip workspace files and other non-book files
        if filepath.stem in ['workspace', 'README', 'TEMPLATE', 'INDEX']:
            continue

        title = extract_title_from_writeup(filepath)
        if title:
            completed_titles[title] = filepath
        else:
            print(f"Warning: Could not extract title from {filepath.name}", file=sys.stderr)

    return completed_titles


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
    completed_titles: Dict[str, Path],
    target_status: str = 'Completed'
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Update Status field for completed books.

    Args:
        rows: Database rows
        completed_titles: Dict mapping title -> filepath
        target_status: Status to set for completed books

    Returns:
        (updated_rows, changes) where changes is a list of dicts with update info
    """
    updated_rows = []
    changes = []

    for row in rows:
        title = row.get('Title', '')
        author = row.get('Author', '')
        current_status = row.get('Status', '').strip()

        # Check if this book has a completed writeup (by exact title match)
        matching_book = find_book_in_database(title, [{'Title': t} for t in completed_titles.keys()])

        if matching_book:
            # Found a matching writeup file
            matched_title = matching_book['Title']
            filepath = completed_titles[matched_title]

            # Update if status is NOT already the target status
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
                    'file': filepath.name,
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
        lines.append(f"   File:   {change['file']}")
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
    completed_titles = get_completed_titles(writeups_dir)
    print(f"Completed writeup files found: {len(completed_titles)}")

    if not completed_titles:
        print("\nNo completed writeup files found. Nothing to update.")
        sys.exit(0)

    # Show what titles were extracted
    if completed_titles:
        print("\nExtracted titles from writeups:")
        for title in sorted(completed_titles.keys()):
            print(f"  • {title}")
        print()

    # Perform update
    print(f"Analyzing status changes (target status: '{args.status_to}')...")
    updated_rows, changes = update_status(rows, completed_titles, args.status_to)

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
