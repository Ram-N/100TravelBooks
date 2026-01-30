# Manuscript Validation Summary

## Critical Issues to Fix

### 1. DUPLICATE CONTENT - IMMEDIATE ACTION REQUIRED

**File:** `book-writeups/5_humbled/great-railway-bazaar-theroux.md`
- **Problem:** This file contains "From Heaven Lake" by Vikram Seth content
- **Action:** DELETE this file (it's a duplicate of `from-heaven-lake-vikram-seth.md`)

### 2. MISSING BOOK - NEEDS WRITEUP

**Book:** "The Great Railway Bazaar" by Paul Theroux (1975)
- **Category:** VI. Institutional Constraints
- **Status:** No writeup file exists
- **Expected filename:** `book-writeups/6_institutional/great-railway-bazaar-theroux.md`

## Extra Books (Not in Final 98 List)

These files exist but are NOT in the final_category_list.md:

1. **Terra Incognita** — Sara Wheeler
   - Location: `book-writeups/2_exploration/terra-incognita-sara-wheeler.md`
   - Action: Decide if this should replace another book or be removed

2. **The Narrow Road to the Deep North** — Matsuo Bashō
   - Location: `book-writeups/3_slow_routes/the-narrow-road-basho.md`
   - Action: Decide if this should replace another book or be removed

3. **Jupiter's Travels** — Ted Simon
   - Location: `book-writeups/6_institutional/jupiters-travels-ted-simon.md`
   - Action: Decide if this should replace another book or be removed

## Book Count Status

- **Expected:** 98 books (per final_category_list.md)
- **Files found:** 101 markdown files (excluding category intros)
- **After cleanup:** Will be 97 books (if you delete the duplicate and don't add the missing Theroux book)

## Recommended Actions

### Immediate (Before Manuscript Finalization):

1. **Delete duplicate:** `book-writeups/5_humbled/great-railway-bazaar-theroux.md`

2. **Decide on extra books:** Keep or remove the 3 books not in your final list:
   - Terra Incognita (Wheeler)
   - The Narrow Road (Bashō)
   - Jupiter's Travels (Simon)

3. **Write missing entry:** Create writeup for "The Great Railway Bazaar" by Paul Theroux

### Optional (Formatting Polish):

Many files have placeholder "XX" for entry numbers. If you want numbered entries in your final manuscript, you'll need to:
- Replace "# XX —" with actual numbers (1-98)
- Can be done with a simple find/replace script if needed

## Notes on Title Variations

The validation script flagged many books as "missing" because of minor title variations between the expected list and file content. These are NOT actual problems - the files exist, just with slight subtitle differences. For example:

- Expected: "The Travels"
- File contains: "XX — The Travels" (correct)

- Expected: "Personal Narrative"
- File contains: "XX — Personal Narrative of a Journey to the Equinoctial Regions of the New Continent" (full subtitle - also correct)

These variations are fine and don't need fixing.

---

**Generated:** 2026-01-29
