#!/usr/bin/env python3
"""
change_status.py - Flexible book status changer for 100 Travel Books project

Changes book status between: Candidate, Completed, HonorableMention, Cut, Maybe

Usage:
    # Interactive mode - search for book and choose new status
    python change_status.py

    # Command-line mode - change by book title
    python change_status.py "The Salt Path" --to Completed

    # Command-line mode - change by ID
    python change_status.py --id 45 --to HonorableMention --reason "One book per author rule"

    # List all books with a specific status
    python change_status.py --list Candidate
"""

import argparse
import csv
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple


# Valid status values
VALID_STATUSES = ['Candidate', 'Completed', 'HonorableMention', 'Cut', 'Maybe', 'Duplicate']


# ═══════════════════════════════════════════════════════════════════════════
# FILE PATHS
# ═══════════════════════════════════════════════════════════════════════════

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_master_db_path() -> Path:
    """Get path to master-candidates.csv."""
    return get_project_root() / 'database' / 'master-candidates.csv'


def get_honorable_db_path() -> Path:
    """Get path to honorable-mentions.csv."""
    return get_project_root() / 'database' / 'honorable-mentions.csv'


# ═══════════════════════════════════════════════════════════════════════════
# DATABASE I/O
# ═══════════════════════════════════════════════════════════════════════════

def load_csv(filepath: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Load CSV file and return (fieldnames, rows)."""
    if not filepath.exists():
        return [], []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    return fieldnames, rows


def save_csv(filepath: Path, fieldnames: List[str], rows: List[Dict[str, Any]]):
    """Save data to CSV file."""
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def create_backup(filepath: Path) -> Path:
    """Create timestamped backup of a file."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup_path = filepath.parent / f"{filepath.stem}-backup-{timestamp}.csv"
    shutil.copy2(filepath, backup_path)
    return backup_path


# ═══════════════════════════════════════════════════════════════════════════
# SEARCH & LOOKUP
# ═══════════════════════════════════════════════════════════════════════════

def normalize_for_search(text: str) -> str:
    """Normalize text for case-insensitive searching."""
    return ' '.join(text.lower().split())


def find_book_by_title(title: str, rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find a book by title (case-insensitive, fuzzy)."""
    normalized_search = normalize_for_search(title)

    # Try exact match first
    for row in rows:
        if normalize_for_search(row.get('Title', '')) == normalized_search:
            return row

    # Try partial match
    for row in rows:
        if normalized_search in normalize_for_search(row.get('Title', '')):
            return row

    return None


def find_book_by_id(book_id: str, rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Find a book by ID."""
    for row in rows:
        if row.get('ID') == str(book_id):
            return row
    return None


def search_books(query: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Search for books by title or author (returns multiple matches)."""
    normalized_query = normalize_for_search(query)
    matches = []

    for row in rows:
        title = normalize_for_search(row.get('Title', ''))
        author = normalize_for_search(row.get('Author', ''))

        if normalized_query in title or normalized_query in author:
            matches.append(row)

    return matches


# ═══════════════════════════════════════════════════════════════════════════
# STATUS CHANGE LOGIC
# ═══════════════════════════════════════════════════════════════════════════

def change_book_status(
    book: Dict[str, Any],
    new_status: str,
    reason: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Change a book's status.

    Returns (success, message).
    """
    if new_status not in VALID_STATUSES:
        return False, f"Invalid status: {new_status}. Must be one of {VALID_STATUSES}"

    old_status = book.get('Status', 'Unknown')
    title = book.get('Title', 'Unknown')

    # Handle HonorableMention status (requires moving between files)
    if new_status == 'HonorableMention' or old_status == 'HonorableMention':
        return False, "Moving to/from HonorableMention requires special handling. Use --to-honorable flag."

    # Simple status change within master-candidates.csv
    book['Status'] = new_status

    message = f"Changed '{title}' from {old_status} → {new_status}"
    if reason:
        message += f"\n  Reason: {reason}"

    return True, message


def move_to_honorable_mentions(
    book: Dict[str, Any],
    reason: str
) -> Dict[str, Any]:
    """
    Convert a master-candidates book entry to honorable-mentions format.

    Returns the new honorable mention row.
    """
    return {
        'ID': book.get('ID'),
        'Title': book.get('Title'),
        'Author': book.get('Author'),
        'Year': book.get('Year'),
        'Primary_Region': book.get('Primary_Region'),
        'Tier': book.get('Tier'),
        'Reason_For_Honorable_Mention': reason
    }


def move_from_honorable_mentions(
    hm_book: Dict[str, Any],
    new_status: str,
    master_fieldnames: List[str]
) -> Dict[str, Any]:
    """
    Convert an honorable mention to a master-candidates entry.

    Returns the new master-candidates row.
    """
    # Create new row with master-candidates structure
    new_row = {field: '' for field in master_fieldnames}

    # Copy over the fields that exist in both
    new_row['ID'] = hm_book.get('ID')
    new_row['Title'] = hm_book.get('Title')
    new_row['Author'] = hm_book.get('Author')
    new_row['Year'] = hm_book.get('Year')
    new_row['Primary_Region'] = hm_book.get('Primary_Region')
    new_row['Tier'] = hm_book.get('Tier')
    new_row['Status'] = new_status
    new_row['Source'] = 'restored-from-hm'
    new_row['Notes'] = hm_book.get('Reason_For_Honorable_Mention', '')

    return new_row


# ═══════════════════════════════════════════════════════════════════════════
# INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════════════════

def interactive_mode():
    """Run in interactive mode."""
    print("═" * 70)
    print("  📚 Book Status Changer - Interactive Mode")
    print("═" * 70)
    print()

    # Load master database
    master_path = get_master_db_path()
    master_fieldnames, master_rows = load_csv(master_path)

    if not master_rows:
        print("Error: Could not load master-candidates.csv")
        return

    # Search for book
    print("Search for a book by title or author:")
    query = input("  → ").strip()

    if not query:
        print("No search query provided. Exiting.")
        return

    matches = search_books(query, master_rows)

    if not matches:
        print(f"\nNo books found matching '{query}'")
        return

    # Display matches
    if len(matches) > 1:
        print(f"\nFound {len(matches)} matches:")
        for i, book in enumerate(matches, 1):
            print(f"  {i}. {book['Title']} by {book['Author']} [{book.get('Status', 'Unknown')}]")

        choice = input(f"\nSelect book (1-{len(matches)}): ").strip()
        try:
            idx = int(choice) - 1
            if idx < 0 or idx >= len(matches):
                print("Invalid selection.")
                return
            selected_book = matches[idx]
        except ValueError:
            print("Invalid selection.")
            return
    else:
        selected_book = matches[0]

    # Display current status
    print()
    print("═" * 70)
    print(f"Book: {selected_book['Title']}")
    print(f"Author: {selected_book['Author']}")
    print(f"Current Status: {selected_book.get('Status', 'Unknown')}")
    print("═" * 70)
    print()

    # Choose new status
    print("Available statuses:")
    for i, status in enumerate(VALID_STATUSES, 1):
        print(f"  {i}. {status}")

    status_choice = input(f"\nSelect new status (1-{len(VALID_STATUSES)}): ").strip()
    try:
        status_idx = int(status_choice) - 1
        if status_idx < 0 or status_idx >= len(VALID_STATUSES):
            print("Invalid selection.")
            return
        new_status = VALID_STATUSES[status_idx]
    except ValueError:
        print("Invalid selection.")
        return

    # Get reason if moving to HonorableMention
    reason = None
    if new_status == 'HonorableMention':
        reason = input("\nReason for honorable mention: ").strip()
        if not reason:
            print("Reason required for honorable mentions.")
            return

    # Confirm
    print()
    print(f"Change '{selected_book['Title']}' from {selected_book.get('Status')} → {new_status}?")
    confirm = input("Confirm (y/n): ").strip().lower()

    if confirm != 'y':
        print("Cancelled.")
        return

    # Apply change
    if new_status == 'HonorableMention':
        # Move to honorable-mentions.csv
        hm_path = get_honorable_db_path()
        hm_fieldnames, hm_rows = load_csv(hm_path)

        # Create backup
        backup = create_backup(master_path)
        print(f"\nBackup created: {backup.name}")

        if hm_fieldnames:
            hm_backup = create_backup(hm_path)
            print(f"Backup created: {hm_backup.name}")

        # Remove from master and add to honorable
        master_rows = [r for r in master_rows if r['ID'] != selected_book['ID']]
        new_hm_entry = move_to_honorable_mentions(selected_book, reason)

        if not hm_fieldnames:
            hm_fieldnames = ['ID', 'Title', 'Author', 'Year', 'Primary_Region', 'Tier', 'Reason_For_Honorable_Mention']

        hm_rows.append(new_hm_entry)

        # Save both files
        save_csv(master_path, master_fieldnames, master_rows)
        save_csv(hm_path, hm_fieldnames, hm_rows)

        print(f"\n✓ Moved '{selected_book['Title']}' to Honorable Mentions")

    else:
        # Simple status change in master-candidates.csv
        success, message = change_book_status(selected_book, new_status, reason)

        if not success:
            print(f"\nError: {message}")
            return

        # Create backup and save
        backup = create_backup(master_path)
        print(f"\nBackup created: {backup.name}")

        save_csv(master_path, master_fieldnames, master_rows)

        print(f"\n✓ {message}")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# COMMAND-LINE MODE
# ═══════════════════════════════════════════════════════════════════════════

def list_books_by_status(status: str):
    """List all books with a given status."""
    master_path = get_master_db_path()
    _, master_rows = load_csv(master_path)

    if status == 'HonorableMention':
        hm_path = get_honorable_db_path()
        _, hm_rows = load_csv(hm_path)

        print(f"\n{'═' * 70}")
        print(f"  Honorable Mentions ({len(hm_rows)} books)")
        print('═' * 70)

        for book in hm_rows:
            print(f"{book['ID']:>4}. {book['Title']:<45} {book['Author']}")
        print()
        return

    matching = [r for r in master_rows if r.get('Status') == status]

    print(f"\n{'═' * 70}")
    print(f"  {status} ({len(matching)} books)")
    print('═' * 70)

    for book in matching:
        print(f"{book['ID']:>4}. {book['Title']:<45} {book['Author']}")
    print()


def cli_change_status(
    book_id: Optional[str] = None,
    title: Optional[str] = None,
    new_status: str = None,
    reason: Optional[str] = None
):
    """Change status via command-line arguments."""
    master_path = get_master_db_path()
    master_fieldnames, master_rows = load_csv(master_path)

    if not master_rows:
        print("Error: Could not load master-candidates.csv")
        return

    # Find the book
    if book_id:
        book = find_book_by_id(book_id, master_rows)
    elif title:
        book = find_book_by_title(title, master_rows)
    else:
        print("Error: Must provide --id or book title")
        return

    if not book:
        print(f"Error: Book not found")
        return

    print(f"\nFound: {book['Title']} by {book['Author']}")
    print(f"Current status: {book.get('Status', 'Unknown')}")
    print(f"New status: {new_status}")
    if reason:
        print(f"Reason: {reason}")

    # Handle HonorableMention special case
    if new_status == 'HonorableMention':
        if not reason:
            print("\nError: --reason required when moving to HonorableMention")
            return

        hm_path = get_honorable_db_path()
        hm_fieldnames, hm_rows = load_csv(hm_path)

        # Create backups
        backup = create_backup(master_path)
        print(f"\nBackup created: {backup.name}")

        if hm_fieldnames:
            hm_backup = create_backup(hm_path)
            print(f"Backup created: {hm_backup.name}")

        # Remove from master and add to honorable
        master_rows = [r for r in master_rows if r['ID'] != book['ID']]
        new_hm_entry = move_to_honorable_mentions(book, reason)

        if not hm_fieldnames:
            hm_fieldnames = ['ID', 'Title', 'Author', 'Year', 'Primary_Region', 'Tier', 'Reason_For_Honorable_Mention']

        hm_rows.append(new_hm_entry)

        # Save both files
        save_csv(master_path, master_fieldnames, master_rows)
        save_csv(hm_path, hm_fieldnames, hm_rows)

        print(f"\n✓ Moved '{book['Title']}' to Honorable Mentions")

    else:
        # Simple status change
        success, message = change_book_status(book, new_status, reason)

        if not success:
            print(f"\nError: {message}")
            return

        # Create backup and save
        backup = create_backup(master_path)
        print(f"\nBackup created: {backup.name}")

        save_csv(master_path, master_fieldnames, master_rows)

        print(f"\n✓ {message}")

    print()


# ═══════════════════════════════════════════════════════════════════════════
# MAIN CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='Change book status in 100 Travel Books project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  # Interactive mode
  %(prog)s

  # Change by title
  %(prog)s "The Salt Path" --to Completed

  # Change by ID
  %(prog)s --id 45 --to HonorableMention --reason "One book per author"

  # List all books with a status
  %(prog)s --list Candidate

Valid statuses: {', '.join(VALID_STATUSES)}
        """
    )

    parser.add_argument(
        'title',
        nargs='?',
        help='Book title to change (optional if using --id)'
    )

    parser.add_argument(
        '--id',
        help='Book ID to change (alternative to title)'
    )

    parser.add_argument(
        '--to',
        help=f'New status ({", ".join(VALID_STATUSES)})'
    )

    parser.add_argument(
        '--reason',
        help='Reason for change (required for HonorableMention)'
    )

    parser.add_argument(
        '--list',
        metavar='STATUS',
        help='List all books with given status'
    )

    args = parser.parse_args()

    # List mode
    if args.list:
        list_books_by_status(args.list)
        return

    # No arguments - interactive mode
    if not args.title and not args.id and not args.to:
        interactive_mode()
        return

    # Command-line mode
    if not args.to:
        print("Error: --to <status> required in command-line mode")
        parser.print_help()
        sys.exit(1)

    cli_change_status(
        book_id=args.id,
        title=args.title,
        new_status=args.to,
        reason=args.reason
    )


if __name__ == '__main__':
    main()
