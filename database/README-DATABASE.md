# Database Files Guide

## Files in this directory

### master-candidates.csv
**Complete list of ~150 candidate books** with essential metadata:
- All candidates from gemini100.md, chatgpt100.md, and user shortlist
- Consolidated and de-duplicated
- Status: All marked as "Candidate" initially
- Source tracking shows where each book came from

**Fields:**
- ID (1-150)
- Status (all "Candidate" for now - change to "Selected" or "Cut" as you decide)
- Title
- Author
- **author_gender** - Values: `male`, `female`, `nonbinary`, `unknown` (default: unknown)
- **author_indigenous** - Values: `yes`, `no`, `unknown` (default: unknown)
- **author_person_of_color** - Values: `yes`, `no`, `unknown` (default: unknown)
- **author_identity_notes** - Free text for provenance (e.g., "official bio", "publisher page", "interview")
- Year (when known)
- Primary_Region
- **travel_continents** - Pipe-separated list (e.g., "Europe|Asia"). Auto-populated from Primary_Region where obvious. Values: Africa, Asia, Europe, North America, South America, Oceania, Antarctica, Middle East, Central America
- Tier (1-4 system from gemini analysis)
- Source (gemini/chatgpt/user)
- Notes

### How to use:

**Option 1: Local CSV editing**
- Open in Excel, LibreOffice, or Numbers
- Sort and filter as needed
- Change Status column to "Selected" for final 100
- Change Status to "Cut" for eliminated books

**Option 2: Google Sheets (recommended for collaboration)**
- Upload to Google Drive
- Import as Google Sheet
- Enables filtering, sorting, comments
- Can share with collaborators if needed

## Selection Process

### Step 1: Quick First Pass
Sort by Tier and mark obvious includes:
- Tier 1 bestsellers you love → "Selected"
- Tier 4 wildcards you're unsure about → maybe mark "Unlikely"
- Books you know you don't want → "Cut"

### Step 2: Balance Check
Filter by Status = "Selected" and check:
- Geographic distribution (all continents? Use travel_continents column)
- Era mix (not too many from one period?)
- Author diversity:
  - Use author_gender column (target: 30%+ female)
  - Use author_person_of_color column (target: 20%+ yes)
  - Use author_indigenous column (include indigenous voices)
- Genre variety (not all memoir, not all adventure?)

### Step 3: Fill Gaps
Based on what's missing, select from remaining candidates:
- Need more Africa? Look for Africa in Primary_Region
- Need more women? Look for female authors
- Need more contemporary? Look for Year > 2000

### Step 4: Final Cuts
When you have ~110-120 "Selected":
- Make hard choices between similar books
- Consider: Do we need 3 Theroux books? Or just 2?
- Eliminate duplicates (same journey, different books)
- Get to exactly 100

## Notes on Incomplete Entries

These entries need research/clarification:
- ID 132: "India" by Geoffrey Moorehead - need to verify
- ID 148: Jonathan Raban - placeholder for his works
- ID 149: Evelyn Waugh in Morocco - need exact title
- ID 150: Walking with Abel - need full author name

Can fill these in later or skip if not essential.

## Populating Author Identity Fields

The new author identity columns (author_gender, author_indigenous, author_person_of_color) currently default to "unknown" for all entries. Populate these fields using:

**Priority 1: Completed entries (5 books)**
- Start with books that already have writeups
- Use official author bios, Wikipedia, publisher pages
- Document source in author_identity_notes

**Priority 2: Well-known authors**
- Research from published biographies, official websites
- Note source in author_identity_notes field

**Priority 3: Remaining candidates**
- Leave as "unknown" until research phase
- Research systematically during selection process

**Best Practices:**
- Always cite your source in author_identity_notes
- Use "unknown" rather than guessing
- Be respectful and use author's self-identification when available
- For historical figures, use established biographical sources

## Adding Additional Custom Fields

If you want to expand the CSV further, consider adding:
- Read_Status (Read / Unread / To Read)
- Own_Copy (Y/N)
- Priority (High / Medium / Low)
- Entry_Writer (Ram / Claude / Both)
- Writing_Status (Not Started / Drafting / Complete)

But keep it simple for now - focus on selection and identity data first!

## Next Steps

1. Open master-candidates.csv in your preferred tool
2. Do a quick scan - any obvious errors or duplicates?
3. Start marking Status column ("Selected" / "Unlikely" / "Cut")
4. Use filters to check balance as you go
5. Get to exactly 100 "Selected" entries
6. Then we can create the final working list and start writing!

---

**Last Updated:** 2026-01-22 (Schema expanded from 9 to 14 columns - added author identity and geographic tracking fields)
