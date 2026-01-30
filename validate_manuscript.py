#!/usr/bin/env python3
"""
Validate the manuscript files for mismatches, duplicates, and missing entries.
"""

import re
from pathlib import Path
from collections import defaultdict


def extract_title_from_content(filepath):
    """
    Extract the book title from the first heading in the markdown file.
    Expected format: # XX — Title or # Title
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') and not line.startswith('##'):
                    # Remove the # and any leading numbers/dashes
                    title = line.lstrip('#').strip()
                    # Remove number prefix like "XX — "
                    title = re.sub(r'^\d+\s*[—–-]\s*', '', title)
                    return title
    except Exception as e:
        return f"ERROR: {e}"
    return "NO TITLE FOUND"


def normalize_title(title):
    """
    Normalize title for comparison (lowercase, remove punctuation, etc.)
    """
    # Remove quotes, colons, and normalize spacing
    normalized = title.lower()
    normalized = re.sub(r'[:"''\']', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized.strip()


def extract_author_from_content(filepath):
    """
    Extract author name from the markdown content.
    Expected format: ### *Author Name* right after title
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith('###') and '*' in line:
                    # Extract text between asterisks
                    author = re.search(r'\*([^*]+)\*', line)
                    if author:
                        return author.group(1).strip()
    except Exception as e:
        return f"ERROR: {e}"
    return "NO AUTHOR FOUND"


def parse_expected_list():
    """
    Parse the final_category_list.md to get expected books by category.
    """
    list_file = Path('/home/ram/projects/100TravelBooks/assembly/final_category_list.md')

    expected = {}
    current_category = None
    category_map = {
        'I.': '1_first_routes',
        'II.': '2_exploration',
        'III.': '3_slow_routes',
        'IV.': '4_frontiers',
        'V.': '5_humbled',
        'VI.': '6_institutional',
        'VII.': '7_inhabited_landscapes',
        'VIII.': '8_political',
        'IX.': '9_self_reckoning'
    }

    with open(list_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Check for category header
            for roman, category in category_map.items():
                if line.startswith(f'## {roman}'):
                    current_category = category
                    expected[current_category] = []
                    break

            # Check for book entry (numbered list)
            if current_category and re.match(r'^\d+\.', line):
                # Extract title and author
                match = re.match(r'^\d+\.\s+(.+?)\s+—\s+(.+?)\s+\((\d{4})\)', line)
                if match:
                    title = match.group(1).strip()
                    author = match.group(2).strip()
                    year = match.group(3)
                    expected[current_category].append({
                        'title': title,
                        'author': author,
                        'year': year,
                        'normalized_title': normalize_title(title)
                    })

    return expected


def main():
    """
    Main validation function.
    """
    base_path = Path('/home/ram/projects/100TravelBooks/book-writeups')

    print("=" * 80)
    print("MANUSCRIPT VALIDATION REPORT")
    print("=" * 80)
    print()

    # Parse expected list
    print("Loading expected book list from final_category_list.md...")
    expected_books = parse_expected_list()

    total_expected = sum(len(books) for books in expected_books.values())
    print(f"Expected total: {total_expected} books\n")

    # Track all files and their content
    all_files = {}
    title_to_files = defaultdict(list)

    categories = [
        '1_first_routes',
        '2_exploration',
        '3_slow_routes',
        '4_frontiers',
        '5_humbled',
        '6_institutional',
        '7_inhabited_landscapes',
        '8_political',
        '9_self_reckoning'
    ]

    print("-" * 80)
    print("SCANNING FILES...")
    print("-" * 80)
    print()

    category_stats = {}

    for category in categories:
        category_path = base_path / category

        if not category_path.exists():
            print(f"⚠ WARNING: Category directory not found: {category}")
            continue

        # Get all markdown files except category_intro.md
        md_files = [f for f in category_path.glob('*.md') if f.name != 'category_intro.md']

        category_stats[category] = {
            'found': len(md_files),
            'expected': len(expected_books.get(category, [])),
            'files': []
        }

        for filepath in md_files:
            filename = filepath.name
            title = extract_title_from_content(filepath)
            author = extract_author_from_content(filepath)
            normalized_title = normalize_title(title)

            file_info = {
                'filename': filename,
                'title': title,
                'author': author,
                'normalized_title': normalized_title,
                'category': category,
                'path': filepath
            }

            all_files[str(filepath)] = file_info
            title_to_files[normalized_title].append(file_info)
            category_stats[category]['files'].append(file_info)

    # Report 1: Files with duplicate content
    print("=" * 80)
    print("REPORT 1: DUPLICATE CONTENT")
    print("=" * 80)
    print()

    duplicates_found = False
    for normalized_title, files in title_to_files.items():
        if len(files) > 1:
            duplicates_found = True
            print(f"⚠ DUPLICATE: '{files[0]['title']}'")
            for f in files:
                print(f"  - {f['category']}/{f['filename']}")
            print()

    if not duplicates_found:
        print("✓ No duplicate content found.\n")

    # Report 2: Filename vs Content mismatches
    print("=" * 80)
    print("REPORT 2: FILENAME vs CONTENT MISMATCHES")
    print("=" * 80)
    print()

    mismatches_found = False
    for filepath, info in all_files.items():
        filename = info['filename'].replace('.md', '').replace('-', ' ')
        title = info['normalized_title']

        # Simple check: does the title appear in the filename or vice versa?
        # This is imperfect but catches obvious mismatches
        filename_words = set(filename.lower().split())
        title_words = set(title.lower().split())

        # Calculate overlap
        common_words = filename_words & title_words

        # Exclude common words
        excluded = {'a', 'an', 'the', 'of', 'in', 'to', 'and', 'with', 'on', 'from', 'by'}
        significant_common = common_words - excluded

        # If there are fewer than 2 significant common words, it's likely a mismatch
        if len(significant_common) < 2:
            mismatches_found = True
            print(f"⚠ MISMATCH:")
            print(f"  Filename: {info['filename']}")
            print(f"  Content title: {info['title']}")
            print(f"  Author: {info['author']}")
            print(f"  Category: {info['category']}")
            print()

    if not mismatches_found:
        print("✓ No obvious filename/content mismatches found.\n")

    # Report 3: Missing books by category
    print("=" * 80)
    print("REPORT 3: MISSING BOOKS")
    print("=" * 80)
    print()

    total_missing = 0
    for category in categories:
        expected = expected_books.get(category, [])
        found_titles = set(f['normalized_title'] for f in category_stats[category]['files'])

        missing = []
        for book in expected:
            if book['normalized_title'] not in found_titles:
                missing.append(book)

        if missing:
            total_missing += len(missing)
            print(f"📂 {category.replace('_', ' ').title()}")
            print(f"   Expected: {len(expected)}, Found: {len(found_titles)}, Missing: {len(missing)}")
            for book in missing:
                print(f"   ⚠ Missing: {book['title']} — {book['author']} ({book['year']})")
            print()

    if total_missing == 0:
        print("✓ No missing books! All expected entries found.\n")

    # Report 4: Extra books (files that don't match expected list)
    print("=" * 80)
    print("REPORT 4: EXTRA/UNEXPECTED FILES")
    print("=" * 80)
    print()

    extra_found = False
    for category in categories:
        expected_titles = set(book['normalized_title'] for book in expected_books.get(category, []))
        found_files = category_stats[category]['files']

        extras = []
        for file_info in found_files:
            if file_info['normalized_title'] not in expected_titles:
                extras.append(file_info)

        if extras:
            extra_found = True
            print(f"📂 {category.replace('_', ' ').title()}")
            for extra in extras:
                print(f"   ⚠ Extra: {extra['filename']}")
                print(f"      Title: {extra['title']}")
                print(f"      Author: {extra['author']}")
            print()

    if not extra_found:
        print("✓ No extra files found.\n")

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    total_found = sum(stats['found'] for stats in category_stats.values())

    print(f"Total expected: {total_expected} books")
    print(f"Total found: {total_found} files")
    print(f"Missing: {total_missing} books")
    print()

    for category in categories:
        stats = category_stats[category]
        status = "✓" if stats['found'] == stats['expected'] else "⚠"
        print(f"{status} {category.replace('_', ' ').title()}: {stats['found']}/{stats['expected']}")

    print()
    print("=" * 80)
    print("END OF REPORT")
    print("=" * 80)


if __name__ == '__main__':
    main()
