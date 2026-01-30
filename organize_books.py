#!/usr/bin/env python3
"""
Organize book writeups into category directories based on CSV data.
Matches files by reading Title and Author from markdown frontmatter.
"""

import csv
import os
import re
import shutil

# Category mapping from CSV to directory names
CATEGORY_MAP = {
    "I. First Routes and Foundational Journeys": "1_first_routes",
    "II. Exploration at the Edge": "2_exploration",
    "III. Slow Routes and Long Ways Through": "3_slow_routes",
    "IV. Frontiers and Frictions": "4_frontiers",
    "V. Humbled by the World": "5_humbled",
    "VI. Institutional Constraints": "6_institutional",
    "VII. Inhabited Landscapes": "7_inhabited_landscapes",
    "VIII. Political Moral and Historical Reckonings": "8_political",
    "IX. Self-Reckoning Through Movement": "9_self_reckoning",
}

def extract_frontmatter(filepath):
    """Extract Title and Author from markdown heading."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Title formats:
    # 1. # **# [Entry Number] — TITLE**
    # 2. # XX — TITLE
    # 3. # TITLE (simple format)
    title_match = re.search(r'^#\s+\*\*#\s+\[Entry Number\]\s+—\s+(.+?)\*\*', content, re.MULTILINE)
    if not title_match:
        title_match = re.search(r'^#\s+XX\s+—\s+(.+?)$', content, re.MULTILINE)
    if not title_match:
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)

    # Author format: ### **[ The Author: AUTHOR (years) ]**
    # Or sometimes just: ### *By AUTHOR*
    # Also extract from quote attribution: — *AUTHOR*
    author_match = re.search(r'###\s+\*\*\[\s*The Author:\s+(.+?)\s*\(', content, re.MULTILINE)
    if not author_match:
        author_match = re.search(r'###\s+\*By\s+(.+?)\*', content, re.MULTILINE)
    if not author_match:
        # Try to find author in quote attribution: — *Author Name*
        author_match = re.search(r'—\s+\*(.+?)\*\s*$', content, re.MULTILINE)

    title = title_match.group(1).strip() if title_match else None
    author = author_match.group(1).strip() if author_match else None

    # Clean up title: remove XX: or number prefixes, leading/trailing punctuation
    if title:
        title = re.sub(r'^XX\s*:\s*', '', title)
        title = re.sub(r'^\d+\s*—\s*', '', title)  # Remove "52 —" style prefixes
        title = title.strip()

    # Strip titles from author names (Sir, Lady, etc.)
    if author:
        author = re.sub(r'^(Sir|Lady|Dr\.|Professor)\s+', '', author)

    return title, author

def normalize_string(s):
    """Normalize string for comparison (lowercase, remove extra spaces and punctuation)."""
    # Remove common punctuation and normalize
    s = s.lower()
    s = re.sub(r'[,:\'\"\.\-]', '', s)  # Remove commas, colons, quotes, periods, hyphens
    s = re.sub(r'\s+', ' ', s)  # Normalize whitespace
    return s.strip()

def main():
    base_dir = "/home/ram/projects/100TravelBooks"
    csv_path = os.path.join(base_dir, "database/final_selection_with_new_categories.csv")
    writeups_dir = os.path.join(base_dir, "book-writeups")

    # Author aliases for matching
    AUTHOR_ALIASES = {
        'che guevara': 'ernesto guevara',
        'ernesto guevara': 'che guevara',
    }

    # Read CSV data
    print("Reading CSV...")
    books_data = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row['Title'].strip()
            author = row['Author'].strip()
            category = row['New_Category'].strip()

            # Strip titles from author names
            author_clean = re.sub(r'^(Sir|Lady|Dr\.|Professor)\s+', '', author)

            # Store multiple keys for flexible matching
            # 1. Full title + author
            key = (normalize_string(title), normalize_string(author_clean))
            books_data[key] = {
                'title': title,
                'author': author,
                'category': category,
                'target_dir': CATEGORY_MAP.get(category)
            }

            # 2. Title without subtitle (before colon) + author
            title_short = title.split(':')[0].strip()
            if title_short != title:
                key_short = (normalize_string(title_short), normalize_string(author_clean))
                books_data[key_short] = books_data[key]

            # 3. Add author alias keys if applicable
            author_norm = normalize_string(author_clean)
            if author_norm in AUTHOR_ALIASES:
                alias_author = AUTHOR_ALIASES[author_norm]
                key_alias = (normalize_string(title), alias_author)
                books_data[key_alias] = books_data[key]
                if title_short != title:
                    key_alias_short = (normalize_string(title_short), alias_author)
                    books_data[key_alias_short] = books_data[key]

    # Count unique books (not just keys)
    unique_books = set()
    for book_info in books_data.values():
        unique_books.add((book_info['title'], book_info['author']))
    print(f"Found {len(unique_books)} unique books in CSV ({len(books_data)} total keys)")

    # Get all .md files in writeups directory
    md_files = [f for f in os.listdir(writeups_dir)
                if f.endswith('.md') and os.path.isfile(os.path.join(writeups_dir, f))]

    print(f"Found {len(md_files)} .md files in book-writeups/")
    print()

    # Process each file
    matched = 0
    unmatched = []

    for filename in md_files:
        filepath = os.path.join(writeups_dir, filename)
        title, author = extract_frontmatter(filepath)

        if not title or not author:
            print(f"⚠️  Could not extract title/author from {filename}")
            unmatched.append(filename)
            continue

        # Look up in CSV data - try multiple variations
        keys_to_try = [
            (normalize_string(title), normalize_string(author)),
            # Try without subtitle (before colon)
            (normalize_string(title.split(':')[0].strip()), normalize_string(author)),
            # Try without " of [Author]" suffix patterns
            (normalize_string(re.sub(r'\s+of\s+.+$', '', title)), normalize_string(author)),
        ]

        book_info = None
        for key in keys_to_try:
            if key in books_data:
                book_info = books_data[key]
                break

        if book_info:
            target_dir = book_info['target_dir']

            if not target_dir:
                print(f"⚠️  No directory mapping for category: {book_info['category']}")
                unmatched.append(filename)
                continue

            # Move the file
            target_path = os.path.join(writeups_dir, target_dir, filename)
            shutil.move(filepath, target_path)
            print(f"✓ Moved {filename} → {target_dir}/")
            matched += 1
        else:
            # Debug: show keys we tried
            keys_tried_str = ' | '.join([f"('{k[0]}', '{k[1]}')" for k in keys_to_try])
            print(f"⚠️  No CSV match for: {title} by {author}")
            print(f"    Tried keys: {keys_tried_str}")
            print(f"    File: {filename}")
            unmatched.append(filename)

    print()
    print(f"Summary: {matched} files moved, {len(unmatched)} unmatched")

    if unmatched:
        print("\nUnmatched files:")
        for f in unmatched:
            print(f"  - {f}")

if __name__ == "__main__":
    main()
