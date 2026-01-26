# Scripts Reference

Quick reference guide for all scripts in the 100 Greatest Travel Books project.

## Main Dashboard

### `status.sh`
Project status dashboard showing book selection progress, writing completion, and diversity metrics. Displays summary by default, with options to filter by category (candidates, completed, honorable mentions, cut, maybe, duplicates).

**Usage:**
```bash
./status.sh                     # Show full dashboard
./status.sh --view completed    # List completed entries
./status.sh --view candidates   # List final 100 candidates
./status.sh --help              # Show all options
```

---

## Python Scripts (in scripts/)

### `check_book.py`
Search and query tool for the master-candidates.csv database. Supports flexible search modes (substring, tokens, regex) across multiple fields with CSV export capability.

**Usage:**
```bash
python scripts/check_book.py "morocco"                          # Simple search
python scripts/check_book.py --q "Bruce" --mode tokens          # Multi-word search
python scripts/check_book.py --q "^The" --mode regex            # Regex search
python scripts/check_book.py "railway" --export results.csv     # Export results
```

### `recommend_next.py`
Intelligent recommendation engine that analyzes the database and suggests which books to write next. Prioritizes diversity gaps (BIPOC, indigenous, women authors) and geographic coverage (Caribbean, South America, Africa, Oceania). Includes tier-based quality scoring and author diversity tracking.

**Usage:**
```bash
python scripts/recommend_next.py                    # Top 5 (default)
python scripts/recommend_next.py --limit 10         # Top 10
python scripts/recommend_next.py --focus diversity  # Prioritize diversity
python scripts/recommend_next.py --show-all-scores  # Full ranked list
python scripts/recommend_next.py --export recs.csv  # Export to CSV
```

### `update_status.py`
Synchronizes the database Status field with actual completed writeups in book-writeups/. Automatically detects which books have finished entries and updates their status to "Completed". Creates timestamped backups before making changes.

**Usage:**
```bash
python scripts/update_status.py                # Dry run (preview changes)
python scripts/update_status.py --apply        # Apply changes to database
python scripts/update_status.py --status-to Completed  # Custom status value
```

### `migrate_add_columns.py`
One-time database migration script that adds diversity tracking columns (author_gender, author_indigenous, author_person_of_color, author_identity_notes, travel_continents) to the master-candidates.csv file. Auto-populates travel_continents from Primary_Region where possible.

**Usage:**
```bash
python scripts/migrate_add_columns.py  # Migrates and creates new file
```

### `safety_check.py`
Git commit safety checker that prevents accidentally committing private content (manuscript files, PDFs, EPUBs, or anything in private/ directory) to the public repository. Can be used manually or as a pre-commit hook.

**Usage:**
```bash
python scripts/safety_check.py  # Check currently staged files
```

---

## Workflow

**Typical workflow:**
1. Run `./status.sh` to see current progress
2. Run `python scripts/recommend_next.py` to see next recommended books
3. Write book entries in book-writeups/
4. Run `python scripts/update_status.py --apply` to sync database
5. Search with `python scripts/check_book.py "<query>"` as needed
6. Use `python scripts/safety_check.py` before committing to git

---

**Last Updated:** 2026-01-25
