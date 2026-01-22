# The 100 Greatest Travel Books Ever Written

A curated guide to the finest travel literature, designed as an ebook (PDF/EPUB) for publication. This repository contains the **tools, templates, and schemas** used to organize and produce the book.

**Note:** The actual book content (writeups, manuscripts, data) is kept private and not included in this repository.

## Project Overview

This is a reference guide to 100 essential travel books, with each entry getting a two-page spread containing:
- Author biography and context
- Book summary and significance
- Geographic coverage
- Further reading recommendations
- Memorable quotes
- Atmospheric pairings

**Target Audience:** Readers and vicarious travelers - armchair explorers and literary enthusiasts

**Format:** PDF and EPUB for Amazon KDP

## Repository Structure

```
100TravelBooks/
├── scripts/              # Python tools for data management
│   ├── migrate_add_columns.py   # CSV schema migration utility
│   └── safety_check.py          # Pre-commit safety checks
│
├── templates/            # Writing templates
│   └── entry_template.md        # Standard format for book entries
│
├── schemas/              # Data structure definitions
│   ├── master_candidates.schema.md    # Complete field documentation
│   └── master_candidates.header.csv   # CSV header specification
│
├── docs/                 # Documentation
│   ├── workflow.md              # Project workflow and timeline
│   └── database_guide.md        # How to use the candidate database
│
├── data_samples/         # Example data (safe for public repo)
│   └── master_candidates.sample.csv   # Sample with fake entries
│
└── private/              # GITIGNORED - Your actual content lives here
    ├── data/             # Real candidate database
    ├── manuscript/       # Book writeups and drafts
    ├── exports/          # Generated PDFs and EPUBs
    ├── research/         # Research materials
    └── planning/         # Planning documents
```

## Key Features

### Candidate Database Schema
Track ~150 candidate books with comprehensive metadata:
- **Identity tracking**: Author gender, BIPOC representation, indigenous voices
- **Geographic indexing**: Multi-continent journeys with pipe-separated tags
- **Selection workflow**: Status field (Candidate/Selected/Cut/HonorableMention)
- **Quality tiers**: 4-tier system from bestsellers to wildcards
- **Source tracking**: Multiple AI and human curation sources

See `schemas/master_candidates.schema.md` for complete field documentation.

### Selection Criteria
Balanced across multiple dimensions:
- **Literary merit** - Writing quality and stylistic innovation
- **Geographic diversity** - All continents represented
- **Era representation** - 19th century classics through contemporary
- **Voice diversity** - 30%+ women authors, 20%+ BIPOC voices, indigenous perspectives
- **Genre mix** - Memoir, adventure, literary, journalistic, philosophical

### Entry Template
Standardized two-page format including:
- The Essentials (genre, keywords, traveler profile)
- Author biography
- Book significance and journey details
- Destinations explored
- Further reading pairings
- Signature quotes
- Atmospheric pairing (drink, soundtrack, setting)

See `templates/entry_template.md` for the complete structure.

## Tools

### Migration Script
Schema evolution tool for the candidate database:
```bash
python scripts/migrate_add_columns.py
```
- Auto-detects private data vs sample data
- Preserves existing content
- Auto-populates derived fields

### Safety Check
Pre-commit validation to prevent accidentally committing private content:
```bash
python scripts/safety_check.py
```
Blocks files matching:
- Anything in `private/`
- Book formats (.epub, .pdf, .docx)
- Manuscript/draft keywords in paths

**Recommended:** Run before every commit or set up as a git pre-commit hook.

## Getting Started

### For Contributors (Public Repo)
1. Clone the repository
2. Explore the sample data in `data_samples/`
3. Review the template and schema documentation
4. Scripts will use sample data automatically if private data isn't present

### For Project Owner (With Private Data)
1. Your real content stays in `private/` (gitignored)
2. Scripts automatically prefer `private/data/` over samples
3. Always run `safety_check.py` before committing
4. Only commit changes to scripts, templates, schemas, and docs

## Timeline

**Week 1:** Finalize the 100 books from 150 candidates
**Week 2-3:** Write all 100 entries (split between human and AI)
**Week 4:** Layout design, index compilation, EPUB/PDF generation

## Contributing

This is primarily a personal project, but suggestions and improvements to the tools and templates are welcome via issues or pull requests.

## License

Tools and templates: MIT License
Book content: All rights reserved (not included in this repository)

---

**Last Updated:** 2026-01-22
