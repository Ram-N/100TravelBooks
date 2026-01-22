# CLAUDE.md

This file provides guidance to Claude Code when working on **The 100 Greatest Travel Books Ever Written** project.

## Project Overview

A curated guide to the finest travel literature, designed as an ebook (PDF/EPUB) for sale on Amazon KDP. Each of the 100 books gets a two-page spread with rich detail to help readers discover their next great travel read.

**Timeline**: 1 month to production
**Target Audience**: Vicarious travelers who are readers - armchair explorers and literary enthusiasts
**Format**: PDF and EPUB for Amazon KDP
**Current Status**: Planning and early content creation phase

## Core Concept

This is NOT a personal memoir of reading. It's an encyclopedic yet engaging reference guide with:
- Literary merit as the primary selection criterion
- Mix of classic exploration narratives, modern travel memoirs, journalistic accounts
- Last 200 years of travel writing (with modern bias)
- Global geographic coverage
- Multiple indexing systems (region, genre, era, travel mode, themes)

## Project Structure

```
/home/ram/projects/100TravelBooks/
├── CLAUDE.md                    # This file
├── PROJECT-GUIDE.md             # Project overview and workflow
├── TEMPLATE.md                  # Standard template for book entries
├── candidate-books/             # AI-generated and curated candidate lists
│   ├── chatgpt100.md
│   └── gemini100.md            # Comprehensive 100-book list with tier analysis
├── book-writeups/              # Completed book entries (target: 100)
│   ├── in-patagonia-chatwin.md
│   ├── wild-cheryl-strayed.md
│   ├── valley-of-the-assasins.md
│   ├── south-ernest-shackleton.md
│   └── there-and-then-thubron.md
├── author-writeups/            # Author biographical sketches
│   └── freya-stark.md
├── planning/                   # Strategic planning documents
│   ├── book-high-concept.md
│   ├── book-structure.md
│   ├── 2-page-layout-take2.md
│   └── book-addon-ideas.md
├── database/                   # To be created - tracking spreadsheet
└── assets/                     # To be created - images, covers, etc.
```

## Writing Style & Tone

- **Encyclopedic but engaging**: Not personal memoir, but not dry academic prose
- **Accessible**: Should work for both serious travelers and casual readers
- **Rich with context**: Historical, cultural, literary significance
- **Practical guidance**: Help readers decide if this book is for them
- **NO emojis** unless explicitly requested
- **Concise**: Two-page limit per book (approximately 300-500 words)

## Entry Template Structure

Each book entry follows a consistent format (see TEMPLATE.md for full details):

### Required Sections:
1. **Title & Author** - with memorable quote
2. **The Essentials** - Genre, keywords, traveler profile
3. **The Author** - Brief biographical sketch, why they matter
4. **The Book** - Journey details, what makes it significant
5. **Destinations Explored** - Geographic coverage
6. **Further Reading** - Pairings both within and outside the 100
7. **The Signature Line** - A defining quote from the book
8. **The Perfect Pairing** - Atmospheric details (drink, soundtrack, setting)

### Entry Length:
- Target: 300-500 words (excluding quotes and bullet points)
- Fits on two-page spread with formatting

## Selection Criteria

We're narrowing ~150 candidates to 100 using these balanced criteria:

### Must Include:
- **Literary merit**: Writing quality, stylistic innovation
- **Historical significance**: Impact on travel writing genre
- **Geographic diversity**: Representation across continents
- **Era representation**: 19th century classics through contemporary
- **Voice diversity**: Women travelers, BIPOC voices, varied perspectives
- **Genre mix**: Memoir, adventure, literary, journalistic, philosophical

### Nice to Have:
- Commercial success (but not required)
- Modern relevance
- Accessibility for general readers

### Four-Tier System (from gemini100.md):
1. **Global Bestsellers** - Household names, major films
2. **The Travel Canon** - Serious traveler essentials
3. **The Deep Divers** - Literary darlings, intellectually dense
4. **The Wildcards** - Obscure, niche, or "questionable" works

## Multiple Index System

Each book can belong to multiple categories. Planned indexes:

### Geographic:
- Europe, Asia, Africa, Americas, Oceania, Antarctica, Global/Multiple

### Genre/Type:
- Literary travelogue, memoir, adventure, journalistic reportage, philosophical, humor, survival, spiritual

### Era:
- 19th century, Early 20th (1900-1945), Postwar (1946-1989), Contemporary (1990+)

### Travel Mode:
- On foot, bicycle, train, sea, air, motorcycle, animal, road trip

### Themes:
- Solitude, food/culinary, spiritual journeys, political, nature/wilderness, cultural immersion, expat life, war/conflict zones

### Author Identity:
- Women travelers, BIPOC voices, LGBTQ+ perspectives

## Workflow (1 Month Timeline)

### Week 1: Foundation
- Finalize the 100 books from 150 candidates
- Build comprehensive database/spreadsheet with all metadata
- Create taxonomy and indexing system
- Identify research gaps

### Week 2-3: Content Creation
- Write all 100 entries (split between human and AI)
- Research books not yet read
- Gather quotes, publication details
- Create "further reading" pairings

### Week 4: Production
- Layout design in Canva
- Index compilation
- Introduction/front matter
- EPUB and PDF generation
- Final polish and proofreading

## Important Constraints

### Book Covers:
- **NO book cover images** unless Creative Commons/open source
- Design will be text-based or use alternative visual elements
- Cannot screenshot from Amazon for commercial use

### Fair Use:
- Keep quotes short (1-2 sentences maximum)
- Always attribute properly
- This is transformative commentary/criticism (defensible fair use)

### Dependencies:
- User has ~150 candidates across multiple lists
- User has written 5 sample entries (good style reference)
- User has planning documents with layout specs
- Need to consolidate all candidate lists into single database

## Current Candidates Summary

From gemini100.md, we have a comprehensive tier-sorted list of 100 books. Additional candidates exist in:
- chatgpt100.md
- User's personal shortlist (shared in conversation)

**Status**: Need to consolidate into single master database with metadata.

## Key Authors Already Identified

### Older Classics:
Robert Byron, Eric Newby, Freya Stark, John Steinbeck, Mark Twain

### Middle Classics:
Paul Theroux, Pico Iyer, Peter Matthiessen, Simon Winchester, Bruce Chatwin, Colin Thubron, Bill Bryson, Ryszard Kapuściński, William Dalrymple, Redmond O'Hanlon

### Modern Classics:
Rory Stewart, Jon Krakauer, Cheryl Strayed

### Women Writers:
Jan Morris, Dervla Murphy, Cheryl Strayed, Rebecca West, Beryl Markham, Robyn Davidson, and others

### Notable Gaps to Research:
- More BIPOC voices
- More non-Western perspectives
- More contemporary (2010+) works
- More South American, African authors

## Commands & Tools

### For Book Research:
- Use WebSearch for publication details, quotes, critical reception
- Read planning documents before suggesting changes
- Check existing book-writeups/ for style consistency

### For Database Management:
- When creating spreadsheet, include ALL metadata fields for indexing
- Track: title, author, year, region, genre, era, travel mode, themes, status (read/unread), tier, keywords

### For Content Creation:
- Always reference TEMPLATE.md for structure
- Match tone/style from existing entries
- Keep within word count limits
- Prioritize literary/historical context over plot summary

## Working Principles

1. **Simplicity first**: Warn if simpler options exist
2. **Stay organized**: Use TodoWrite for multi-step tasks
3. **Batch operations**: When possible, work on multiple entries in parallel
4. **Preserve user's voice**: Don't over-edit existing writeups
5. **Research thoroughly**: For unfamiliar books, gather context before writing
6. **Balance the list**: Consider diversity across all dimensions when selecting final 100

## Notes & Reminders

- User wants to sell on Amazon KDP - keep commercial viability in mind
- PDF and EPUB both needed - design must work for both formats
- Two-page spreads need to work in digital format (scrolling)
- User is open to suggestions but has strong vision - collaborate, don't dictate
- Timeline is tight (1 month) - prioritize efficiency
- User has ~150 candidates, need to cut to 100 - expect difficult choices

## Questions to Resolve

These will be addressed as project progresses:
- Final 100 selection criteria weights
- Exact layout specifications for Canva
- Introduction/front matter content
- Back matter (indexes, reading lists, acknowledgments)
- Cover design approach
- Pricing strategy for KDP

---

**Last Updated**: 2026-01-21
**Project Phase**: Planning & Early Content Creation
