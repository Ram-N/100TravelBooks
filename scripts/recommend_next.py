#!/usr/bin/env python3
"""
recommend_next.py - Intelligent book recommendation engine

Analyzes the 100 Greatest Travel Books database and recommends the next books to
write entries for, prioritizing diversity gaps, geographic coverage, and tier
classification.

Usage:
    python recommend_next.py                    # Top 5 (default)
    python recommend_next.py --limit 10         # Top 10
    python recommend_next.py --focus diversity  # Prioritize diversity
    python recommend_next.py --show-all-scores  # Full ranked list
    python recommend_next.py --export recs.csv  # Export to CSV
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple
from collections import Counter


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION - Scoring Weights
# ═══════════════════════════════════════════════════════════════════════════

# Base tier scores (mutually exclusive)
TIER_SCORES = {
    '1': 10,  # Global bestsellers
    '2': 7,   # Travel canon
    '3': 4,   # Deep divers
    '4': 2,   # Wildcards
}

# Diversity bonuses (stackable)
WOMEN_BONUS = 8
BIPOC_BONUS = 15          # Critical gap
INDIGENOUS_BONUS = 15     # Severe gap

# Geographic bonuses (stackable)
CARIBBEAN_BONUS = 12      # Critical - only 1 book
SOUTH_AMERICA_BONUS = 8   # Low representation
AFRICA_BONUS = 6          # Low representation
OCEANIA_BONUS = 5         # Very low - 2 books
MIDDLE_EAST_BONUS = 4     # Low representation

# Other bonuses
POST_2010_BONUS = 3       # Contemporary voices
NEW_AUTHOR_BONUS = 5      # Author diversity

# Focus mode multipliers
FOCUS_MULTIPLIERS = {
    'balanced': {
        'diversity': 1.0,
        'geography': 1.0,
        'tier': 1.0,
    },
    'diversity': {
        'diversity': 2.0,
        'geography': 1.0,
        'tier': 1.0,
    },
    'geography': {
        'diversity': 1.0,
        'geography': 2.0,
        'tier': 1.0,
    },
    'tier': {
        'diversity': 1.0,
        'geography': 1.0,
        'tier': 1.5,
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════════════

def load_database(db_path: Path) -> List[Dict[str, Any]]:
    """Load the CSV database."""
    if not db_path.exists():
        print(f"Error: Database file not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    books = []
    with open(db_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        books = list(reader)

    return books


def get_completed_files(writeups_dir: Path) -> List[str]:
    """Get list of completed writeup filenames (without .md extension)."""
    if not writeups_dir.exists():
        print(f"Warning: Writeups directory not found: {writeups_dir}", file=sys.stderr)
        return []

    # Get all .md files and remove extension
    completed = [f.stem for f in writeups_dir.glob('*.md')]
    return completed


# ═══════════════════════════════════════════════════════════════════════════
# FILENAME MATCHING
# ═══════════════════════════════════════════════════════════════════════════

def normalize_for_filename(text: str) -> str:
    """Normalize text for filename matching."""
    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

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

    # Extract author last name (assume last word)
    author_parts = author_norm.split('-')
    author_lastname = author_parts[-1] if author_parts else author_norm

    # Pattern 1: title-author
    if title_norm and author_norm:
        candidates.append(f"{title_norm}-{author_norm}")

    # Pattern 2: title-lastname
    if title_norm and author_lastname:
        candidates.append(f"{title_norm}-{author_lastname}")

    # Pattern 3: title only
    if title_norm:
        candidates.append(title_norm)

    return candidates


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

    return False


# ═══════════════════════════════════════════════════════════════════════════
# FILTERING
# ═══════════════════════════════════════════════════════════════════════════

def filter_candidates(
    books: List[Dict[str, Any]],
    completed_files: List[str]
) -> List[Dict[str, Any]]:
    """Filter to only 'Candidate' status books that haven't been completed."""
    candidates = []

    for book in books:
        # Must have Candidate status
        status = book.get('Status', '').strip()
        if status != 'Candidate':
            continue

        # Must not be completed
        title = book.get('Title', '')
        author = book.get('Author', '')

        if not is_book_completed(title, author, completed_files):
            candidates.append(book)

    return candidates


# ═══════════════════════════════════════════════════════════════════════════
# SCORING ENGINE
# ═══════════════════════════════════════════════════════════════════════════

def score_book(
    book: Dict[str, Any],
    completed_authors: set,
    focus_mode: str = 'balanced'
) -> Tuple[int, List[str], List[str]]:
    """
    Calculate score for a book with reasoning.

    Returns:
        (score, reasons, warnings) tuple
    """
    score = 0
    reasons = []
    warnings = []

    multipliers = FOCUS_MULTIPLIERS[focus_mode]

    # ─────────────────────────────────────────────────────────────────────
    # TIER SCORE (base quality indicator)
    # ─────────────────────────────────────────────────────────────────────
    tier = book.get('Tier', '').strip()
    if tier in TIER_SCORES:
        tier_score = int(TIER_SCORES[tier] * multipliers['tier'])
        score += tier_score
        tier_labels = {
            '1': 'Tier 1 - Global bestseller',
            '2': 'Tier 2 - Travel canon',
            '3': 'Tier 3 - Deep dive',
            '4': 'Tier 4 - Wildcard',
        }
        reasons.append(f"{tier_labels[tier]} (+{tier_score})")

    # ─────────────────────────────────────────────────────────────────────
    # DIVERSITY BONUSES
    # ─────────────────────────────────────────────────────────────────────

    # Women authors
    gender = book.get('author_gender', '').strip().lower()
    if gender == 'female' or gender == 'f':
        women_score = int(WOMEN_BONUS * multipliers['diversity'])
        score += women_score
        reasons.append(f"Women author (+{women_score})")
    elif gender == 'unknown' or not gender:
        warnings.append("⚠ Gender unknown - manual review recommended")

    # BIPOC authors (critical gap)
    poc = book.get('author_person_of_color', '').strip().lower()
    if poc == 'yes' or poc == 'y' or poc == 'true':
        bipoc_score = int(BIPOC_BONUS * multipliers['diversity'])
        score += bipoc_score
        reasons.append(f"BIPOC author - CRITICAL GAP (+{bipoc_score})")
    elif poc == 'unknown' or not poc:
        warnings.append("⚠ BIPOC status unknown - manual review recommended")

    # Indigenous authors (severe gap)
    indigenous = book.get('author_indigenous', '').strip().lower()
    if indigenous == 'yes' or indigenous == 'y' or indigenous == 'true':
        indigenous_score = int(INDIGENOUS_BONUS * multipliers['diversity'])
        score += indigenous_score
        reasons.append(f"Indigenous author - SEVERE GAP (+{indigenous_score})")
    elif indigenous == 'unknown' or not indigenous:
        warnings.append("⚠ Indigenous status unknown - manual review recommended")

    # ─────────────────────────────────────────────────────────────────────
    # GEOGRAPHIC BONUSES
    # ─────────────────────────────────────────────────────────────────────

    primary_region = book.get('Primary_Region', '').strip().lower()
    continents = book.get('travel_continents', '').strip().lower()

    # Caribbean (critical gap - only 1 book)
    if 'caribbean' in primary_region or 'caribbean' in continents:
        caribbean_score = int(CARIBBEAN_BONUS * multipliers['geography'])
        score += caribbean_score
        reasons.append(f"Caribbean - CRITICAL GAP (+{caribbean_score})")

    # South America
    if 'south america' in primary_region or 'south america' in continents:
        sa_score = int(SOUTH_AMERICA_BONUS * multipliers['geography'])
        score += sa_score
        reasons.append(f"South America - low representation (+{sa_score})")

    # Africa
    if 'africa' in primary_region or 'africa' in continents:
        africa_score = int(AFRICA_BONUS * multipliers['geography'])
        score += africa_score
        reasons.append(f"Africa - low representation (+{africa_score})")

    # Oceania
    if 'oceania' in primary_region or 'oceania' in continents or 'australia' in primary_region:
        oceania_score = int(OCEANIA_BONUS * multipliers['geography'])
        score += oceania_score
        reasons.append(f"Oceania - very low representation (+{oceania_score})")

    # Middle East
    if 'middle east' in primary_region or 'middle east' in continents:
        me_score = int(MIDDLE_EAST_BONUS * multipliers['geography'])
        score += me_score
        reasons.append(f"Middle East - low representation (+{me_score})")

    # ─────────────────────────────────────────────────────────────────────
    # OTHER BONUSES
    # ─────────────────────────────────────────────────────────────────────

    # Post-2010 (contemporary voices)
    year = book.get('Year', '').strip()
    if year and year.isdigit() and int(year) >= 2010:
        score += POST_2010_BONUS
        reasons.append(f"Contemporary (post-2010) (+{POST_2010_BONUS})")

    # New author (not in completed books)
    author = book.get('Author', '').strip()
    if author and author not in completed_authors:
        score += NEW_AUTHOR_BONUS
        reasons.append(f"New author to collection (+{NEW_AUTHOR_BONUS})")

    return score, reasons, warnings


def get_completed_authors(books: List[Dict[str, Any]], completed_files: List[str]) -> set:
    """Get set of authors who already have completed writeups."""
    completed_authors = set()

    for book in books:
        title = book.get('Title', '')
        author = book.get('Author', '')

        if is_book_completed(title, author, completed_files):
            completed_authors.add(author.strip())

    return completed_authors


# ═══════════════════════════════════════════════════════════════════════════
# RECOMMENDATION GENERATOR
# ═══════════════════════════════════════════════════════════════════════════

def generate_recommendations(
    candidates: List[Dict[str, Any]],
    completed_authors: set,
    focus_mode: str = 'balanced',
    limit: int = 5,
    show_all: bool = False
) -> List[Dict[str, Any]]:
    """Score all candidates and return top N recommendations."""

    scored_books = []

    for book in candidates:
        score, reasons, warnings = score_book(book, completed_authors, focus_mode)

        scored_books.append({
            'book': book,
            'score': score,
            'reasons': reasons,
            'warnings': warnings,
        })

    # Sort by score (descending)
    scored_books.sort(key=lambda x: x['score'], reverse=True)

    # Return top N or all
    if show_all:
        return scored_books
    else:
        return scored_books[:limit]


# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTERS
# ═══════════════════════════════════════════════════════════════════════════

def format_output(recommendations: List[Dict[str, Any]], limit: int) -> str:
    """Format recommendations as ASCII table with reasoning."""

    lines = []

    # Header
    lines.append("═" * 70)
    lines.append(f"  TOP {min(limit, len(recommendations))} RECOMMENDED BOOKS TO WRITE NEXT")
    lines.append("═" * 70)
    lines.append("")

    # Individual recommendations
    for i, rec in enumerate(recommendations[:limit], 1):
        book = rec['book']
        score = rec['score']
        reasons = rec['reasons']
        warnings = rec['warnings']

        title = book.get('Title', 'Unknown')
        author = book.get('Author', 'Unknown')
        tier = book.get('Tier', '?')
        year = book.get('Year', '?')
        region = book.get('Primary_Region', 'Unknown')

        # Book header
        lines.append(f"{i}. {title} by {author} (Tier {tier}, {year}, {region})")
        lines.append(f"   Score: {score} points")
        lines.append("")

        # Reasoning
        if reasons:
            lines.append("   Why recommended:")
            for reason in reasons:
                lines.append(f"   • {reason}")

        # Warnings
        if warnings:
            for warning in warnings:
                lines.append(f"   {warning}")

        # Notes
        notes = book.get('Notes', '').strip()
        if notes:
            lines.append(f"   📝 Notes: {notes}")

        lines.append("")

    # Impact summary
    lines.append("═" * 70)
    lines.append("📊 IMPACT SUMMARY")
    lines.append("═" * 70)
    lines.append("")

    # Calculate statistics for top recommendations
    top_recs = recommendations[:limit]

    # Diversity stats
    women_count = sum(
        1 for r in top_recs
        if r['book'].get('author_gender', '').strip().lower() in ['female', 'f']
    )
    bipoc_count = sum(
        1 for r in top_recs
        if r['book'].get('author_person_of_color', '').strip().lower() in ['yes', 'y', 'true']
    )

    lines.append("Diversity Impact:")
    lines.append(f"  • BIPOC authors: {bipoc_count} of {len(top_recs)} ({bipoc_count*100//len(top_recs) if top_recs else 0}%)")
    lines.append(f"  • Women authors: {women_count} of {len(top_recs)} ({women_count*100//len(top_recs) if top_recs else 0}%)")
    lines.append("")

    # Geographic stats
    region_counter = Counter()
    for r in top_recs:
        region = r['book'].get('Primary_Region', '').strip()
        if 'Caribbean' in region or 'caribbean' in region.lower():
            region_counter['Caribbean'] += 1
        elif 'South America' in region or 'south america' in region.lower():
            region_counter['South America'] += 1
        elif 'Africa' in region or 'africa' in region.lower():
            region_counter['Africa'] += 1
        elif 'Oceania' in region or 'oceania' in region.lower() or 'Australia' in region:
            region_counter['Oceania'] += 1
        elif 'Middle East' in region or 'middle east' in region.lower():
            region_counter['Middle East'] += 1

    if region_counter:
        lines.append("Geographic Coverage:")
        for region, count in region_counter.most_common():
            lines.append(f"  • {region}: {count} book{'s' if count > 1 else ''}")
        lines.append("")

    # Tier distribution
    tier_counter = Counter()
    for r in top_recs:
        tier = r['book'].get('Tier', '?').strip()
        tier_counter[tier] += 1

    lines.append("Tier Distribution:")
    tier_labels = {'1': 'global bestsellers', '2': 'travel canon', '3': 'deep dives', '4': 'wildcards'}
    for tier in ['1', '2', '3', '4']:
        count = tier_counter.get(tier, 0)
        if count > 0:
            label = tier_labels.get(tier, 'unknown')
            lines.append(f"  • Tier {tier}: {count} ({label})")

    lines.append("═" * 70)

    return "\n".join(lines)


def export_to_csv(recommendations: List[Dict[str, Any]], output_path: Path, limit: int):
    """Export recommendations to CSV."""

    fieldnames = ['Rank', 'Score', 'Title', 'Author', 'Year', 'Tier', 'Primary_Region', 'Reasoning']

    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for i, rec in enumerate(recommendations[:limit], 1):
            book = rec['book']

            writer.writerow({
                'Rank': i,
                'Score': rec['score'],
                'Title': book.get('Title', ''),
                'Author': book.get('Author', ''),
                'Year': book.get('Year', ''),
                'Tier': book.get('Tier', ''),
                'Primary_Region': book.get('Primary_Region', ''),
                'Reasoning': ' | '.join(rec['reasons']),
            })

    print(f"\nExported {min(limit, len(recommendations))} recommendations to: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════
# MAIN CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Intelligent book recommendation engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Top 5 recommendations
  %(prog)s --limit 10                # Top 10 recommendations
  %(prog)s --focus diversity         # Prioritize diversity gaps
  %(prog)s --focus geography         # Prioritize geographic gaps
  %(prog)s --show-all-scores         # Show all candidates ranked
  %(prog)s --export recs.csv         # Export to CSV
        """
    )

    # Main options
    parser.add_argument(
        '--limit',
        type=int,
        default=5,
        help='Number of recommendations to show [default: 5]'
    )
    parser.add_argument(
        '--focus',
        choices=['balanced', 'diversity', 'geography', 'tier'],
        default='balanced',
        help='Focus mode for scoring emphasis [default: balanced]'
    )
    parser.add_argument(
        '--show-all-scores',
        action='store_true',
        help='Show all candidates with scores (not just top N)'
    )

    # Data source options
    parser.add_argument(
        '--db',
        default='master-candidates.csv',
        help='Database file to use [default: master-candidates.csv]'
    )

    # Output options
    parser.add_argument(
        '--export',
        metavar='FILE',
        help='Export recommendations to CSV file'
    )

    args = parser.parse_args()

    # Resolve paths (from scripts/ to database/ and book-writeups/)
    db_path = Path(__file__).parent.parent / 'database' / args.db
    writeups_dir = Path(__file__).parent.parent / 'book-writeups'

    # Load data
    print(f"Loading database: {db_path}")
    all_books = load_database(db_path)
    print(f"Total books in database: {len(all_books)}")

    print(f"Loading completed writeups from: {writeups_dir}")
    completed_files = get_completed_files(writeups_dir)
    print(f"Completed writeups: {len(completed_files)}")

    # Filter candidates
    candidates = filter_candidates(all_books, completed_files)
    print(f"Candidate books remaining: {len(candidates)}")

    if not candidates:
        print("\nNo candidate books found!")
        sys.exit(0)

    # Get completed authors for scoring
    completed_authors = get_completed_authors(all_books, completed_files)

    # Generate recommendations
    print(f"\nGenerating recommendations (focus: {args.focus})...")
    recommendations = generate_recommendations(
        candidates,
        completed_authors,
        focus_mode=args.focus,
        limit=args.limit if not args.show_all_scores else len(candidates),
        show_all=args.show_all_scores
    )

    # Display results
    print("\n")
    output = format_output(recommendations, args.limit if not args.show_all_scores else len(recommendations))
    print(output)

    # Export if requested
    if args.export:
        export_path = Path(args.export)
        export_to_csv(recommendations, export_path, args.limit if not args.show_all_scores else len(recommendations))

    print()


if __name__ == '__main__':
    main()
