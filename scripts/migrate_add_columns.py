#!/usr/bin/env python3
"""
Migration script to add 5 new columns to master-candidates.csv

New columns:
1. author_gender (after Author)
2. author_indigenous (after author_gender)
3. author_person_of_color (after author_indigenous)
4. author_identity_notes (after author_person_of_color)
5. travel_continents (after Primary_Region)

Old header (9 columns):
ID,Status,Title,Author,Year,Primary_Region,Tier,Source,Notes

New header (14 columns):
ID,Status,Title,Author,author_gender,author_indigenous,author_person_of_color,author_identity_notes,Year,Primary_Region,travel_continents,Tier,Source,Notes
"""

import csv
import sys
from pathlib import Path

def map_region_to_continents(region):
    """Auto-populate travel_continents from Primary_Region where obvious."""
    if not region:
        return ""

    region_lower = region.lower()

    # Direct mappings
    if region_lower == "europe":
        return "Europe"
    elif region_lower == "south america":
        return "South America"
    elif region_lower == "antarctica":
        return "Antarctica"
    elif region_lower == "north america":
        return "North America"
    elif region_lower == "africa":
        return "Africa"
    elif region_lower == "asia":
        return "Asia"
    elif region_lower == "oceania":
        return "Oceania"
    elif region_lower == "arctic":
        return "Arctic"
    elif region_lower == "caribbean":
        return "Central America"

    # Check for specific mentions
    elif "europe" in region_lower:
        continents = ["Europe"]
        if "asia" in region_lower or "middle east" in region_lower:
            continents.append("Asia")
        return "|".join(continents)
    elif "middle east" in region_lower:
        return "Asia"
    elif "pacific" in region_lower:
        return "Oceania"
    elif "islamic world" in region_lower:
        return ""  # Too broad to auto-assign
    elif "multiple" in region_lower:
        return ""  # User will fill in manually
    elif "/" in region:
        # Region contains a slash, try to extract continent
        base = region.split("/")[0].strip().lower()
        if base == "europe":
            return "Europe"
        elif base == "africa":
            return "Africa"
        elif base == "asia":
            return "Asia"
        elif base == "north america":
            return "North America"
        elif base == "south america":
            return "South America"
        elif base == "oceania":
            return "Oceania"
        elif base == "middle east":
            return "Asia"

    return ""

def migrate_csv(input_path, output_path):
    """Migrate CSV by adding 5 new columns."""

    with open(input_path, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Verify expected columns
        expected_cols = ['ID', 'Status', 'Title', 'Author', 'Year', 'Primary_Region', 'Tier', 'Source', 'Notes']
        if list(reader.fieldnames) != expected_cols:
            print(f"ERROR: Unexpected columns in input CSV")
            print(f"Expected: {expected_cols}")
            print(f"Found: {list(reader.fieldnames)}")
            sys.exit(1)

        # New column order
        new_fieldnames = [
            'ID', 'Status', 'Title', 'Author',
            'author_gender', 'author_indigenous', 'author_person_of_color', 'author_identity_notes',
            'Year', 'Primary_Region', 'travel_continents',
            'Tier', 'Source', 'Notes'
        ]

        # Read all rows
        rows = []
        for row in reader:
            # Add new columns with default values
            new_row = {
                'ID': row['ID'],
                'Status': row['Status'],
                'Title': row['Title'],
                'Author': row['Author'],
                'author_gender': 'unknown',
                'author_indigenous': 'unknown',
                'author_person_of_color': 'unknown',
                'author_identity_notes': '',
                'Year': row['Year'],
                'Primary_Region': row['Primary_Region'],
                'travel_continents': map_region_to_continents(row['Primary_Region']),
                'Tier': row['Tier'],
                'Source': row['Source'],
                'Notes': row['Notes']
            }
            rows.append(new_row)

        # Write migrated CSV
        with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print(f"✓ Migration complete!")
        print(f"  Input:  {input_path}")
        print(f"  Output: {output_path}")
        print(f"  Rows processed: {len(rows)}")
        print(f"  Old columns: {len(expected_cols)}")
        print(f"  New columns: {len(new_fieldnames)}")

if __name__ == "__main__":
    # Find project root (parent of scripts/)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Try private data first, fall back to sample
    private_csv = project_root / "private" / "data" / "master-candidates.csv"
    sample_csv = project_root / "data_samples" / "master_candidates.sample.csv"

    if private_csv.exists():
        input_csv = private_csv
        output_csv = project_root / "private" / "data" / "master-candidates-migrated.csv"
        print(f"Using private data file: {input_csv}")
    elif sample_csv.exists():
        input_csv = sample_csv
        output_csv = project_root / "data_samples" / "master_candidates.sample.migrated.csv"
        print(f"Private data not found. Using sample file: {input_csv}")
    else:
        print(f"ERROR: No input file found!")
        print(f"  Tried: {private_csv}")
        print(f"  Tried: {sample_csv}")
        sys.exit(1)

    migrate_csv(input_csv, output_csv)

    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("1. Review the migrated file: " + str(output_csv.name))
    print("2. If it looks good, replace the original:")
    if private_csv.exists():
        print("   cd private/data && mv master-candidates-migrated.csv master-candidates.csv")
    else:
        print("   cd data_samples && mv master_candidates.sample.migrated.csv master_candidates.sample.csv")
    print("="*60)
