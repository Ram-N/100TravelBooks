#!/usr/bin/env python3
"""
check_book.py - Search the travel books database

Search for books by keyword(s) in various fields with flexible matching modes.

Usage:
    python check_book.py "mountain"
    python check_book.py --q "morocco" --fields title,author,region --limit 10
    python check_book.py --q "Bruce" --mode tokens --case-sensitive
    python check_book.py --q "^The" --mode regex --export results.csv
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from typing import List, Dict, Any


def normalize_text(text: str, case_sensitive: bool = False) -> str:
    """Normalize text for comparison."""
    if text is None:
        return ""
    text = str(text).strip()
    if not case_sensitive:
        text = text.lower()
    return text


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


def search_contains(query: str, text: str, case_sensitive: bool) -> bool:
    """Simple substring match."""
    query_norm = normalize_text(query, case_sensitive)
    text_norm = normalize_text(text, case_sensitive)
    return query_norm in text_norm


def search_tokens(query: str, text: str, case_sensitive: bool) -> bool:
    """Split query into tokens and require all tokens appear (AND logic)."""
    query_norm = normalize_text(query, case_sensitive)
    text_norm = normalize_text(text, case_sensitive)

    # Split query into tokens
    tokens = query_norm.split()

    # All tokens must appear in text
    return all(token in text_norm for token in tokens)


def search_regex(query: str, text: str, case_sensitive: bool) -> bool:
    """Regex match."""
    try:
        flags = 0 if case_sensitive else re.IGNORECASE
        text = str(text) if text else ""
        return bool(re.search(query, text, flags))
    except re.error as e:
        print(f"Error: Invalid regex pattern: {e}", file=sys.stderr)
        sys.exit(1)


def search_books(
    books: List[Dict[str, Any]],
    query: str,
    mode: str,
    case_sensitive: bool,
    search_fields: List[str]
) -> List[Dict[str, Any]]:
    """Search books based on query and mode."""

    search_func = {
        'contains': search_contains,
        'tokens': search_tokens,
        'regex': search_regex
    }[mode]

    results = []
    for book in books:
        # Search across specified fields
        match = False
        for field in search_fields:
            if field in book:
                if search_func(query, book[field], case_sensitive):
                    match = True
                    break

        if match:
            results.append(book)

    return results


def format_table(books: List[Dict[str, Any]], display_fields: List[str]) -> str:
    """Format books as a text table."""
    if not books:
        return "No matches found."

    # Calculate column widths
    widths = {}
    for field in display_fields:
        # Header width
        widths[field] = len(field)
        # Data width
        for book in books:
            value = str(book.get(field, ''))
            widths[field] = max(widths[field], len(value))

    # Build table
    lines = []

    # Header
    header = " | ".join(f"{field:<{widths[field]}}" for field in display_fields)
    lines.append(header)
    lines.append("-" * len(header))

    # Rows
    for book in books:
        row = " | ".join(
            f"{str(book.get(field, '')):<{widths[field]}}"
            for field in display_fields
        )
        lines.append(row)

    return "\n".join(lines)


def export_csv(books: List[Dict[str, Any]], output_path: Path, display_fields: List[str]):
    """Export results to CSV."""
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=display_fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(books)

    print(f"\nExported {len(books)} results to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Search the travel books database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "mountain"
  %(prog)s --q "morocco" --fields title,author,region
  %(prog)s --q "Bruce Chatwin" --mode tokens
  %(prog)s --q "^The" --mode regex --case-sensitive
  %(prog)s --q "railway" --limit 20 --export results.csv
        """
    )

    # Query argument (positional or --q)
    parser.add_argument(
        'query',
        nargs='?',
        help='Search query (keyword or pattern)'
    )
    parser.add_argument(
        '--q',
        dest='query_flag',
        help='Search query (alternative to positional)'
    )

    # Search options
    parser.add_argument(
        '--mode',
        choices=['contains', 'regex', 'tokens'],
        default='contains',
        help='Search mode: contains (substring), tokens (all words), regex (pattern) [default: contains]'
    )
    parser.add_argument(
        '--case-sensitive',
        action='store_true',
        help='Enable case-sensitive search [default: case-insensitive]'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Maximum number of results to display [default: 50]'
    )

    # Field options
    parser.add_argument(
        '--fields',
        default='title,author,year,primary_region,status,tier,source',
        help='Comma-separated fields to display [default: title,author,year,primary_region,status,tier,source]'
    )
    parser.add_argument(
        '--search-fields',
        default='title,author,notes',
        help='Comma-separated fields to search in [default: title,author,notes]'
    )

    # Output options
    parser.add_argument(
        '--export',
        metavar='FILE',
        help='Export results to CSV file'
    )
    parser.add_argument(
        '--db',
        default='master-candidates.csv',
        help='Database file to search [default: master-candidates.csv]'
    )
    parser.add_argument(
        '--sort-by',
        default='title',
        help='Field to sort results by [default: title]'
    )

    args = parser.parse_args()

    # Get query from either positional or --q flag
    query = args.query or args.query_flag
    if not query:
        parser.print_help()
        print("\nError: Query is required", file=sys.stderr)
        sys.exit(1)

    # Parse field lists
    display_fields = [f.strip() for f in args.fields.split(',')]
    search_fields = [f.strip() for f in args.search_fields.split(',')]

    # Normalize field names (handle case variations)
    field_map = {
        'primary_region': 'Primary_Region',
        'region': 'Primary_Region',
        'travel_continents': 'travel_continents',
        'continents': 'travel_continents',
        'id': 'ID',
        'status': 'Status',
        'title': 'Title',
        'author': 'Author',
        'year': 'Year',
        'tier': 'Tier',
        'source': 'Source',
        'notes': 'Notes',
        'author_gender': 'author_gender',
        'gender': 'author_gender',
        'author_indigenous': 'author_indigenous',
        'indigenous': 'author_indigenous',
        'author_person_of_color': 'author_person_of_color',
        'poc': 'author_person_of_color',
        'author_identity_notes': 'author_identity_notes',
        'identity': 'author_identity_notes',
    }

    display_fields = [field_map.get(f.lower(), f) for f in display_fields]
    search_fields = [field_map.get(f.lower(), f) for f in search_fields]

    # Resolve database path (from scripts/ to database/)
    db_path = Path(__file__).parent.parent / 'database' / args.db

    # Load database
    print(f"Loading database: {db_path}")
    books = load_database(db_path)
    print(f"Total books in database: {len(books)}")

    # Search
    print(f"\nSearching for: '{query}'")
    print(f"Mode: {args.mode}")
    print(f"Search fields: {', '.join(search_fields)}")
    print(f"Case-sensitive: {args.case_sensitive}")

    results = search_books(books, query, args.mode, args.case_sensitive, search_fields)

    # Sort results
    if args.sort_by in results[0] if results else False:
        results.sort(key=lambda x: str(x.get(args.sort_by, '')))

    # Limit results
    limited_results = results[:args.limit] if args.limit > 0 else results

    # Display results
    print(f"\n{'='*60}")
    print(f"Found {len(results)} matches")
    if len(results) > args.limit and args.limit > 0:
        print(f"Displaying first {args.limit} results")
    print(f"{'='*60}\n")

    if results:
        print(format_table(limited_results, display_fields))

        # Export if requested
        if args.export:
            export_path = Path(args.export)
            export_csv(results, export_path, display_fields)
    else:
        print("No matches found.")

    print()


if __name__ == '__main__':
    main()
