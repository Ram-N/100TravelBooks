# Database Schema for 100 Greatest Travel Books

This document defines the structure for the master spreadsheet/database used to track all candidate and selected books.

---

## Spreadsheet Structure

**Recommended Tool:** Google Sheets (for collaboration) or Excel

**Main Sheets:**
1. **MASTER LIST** - All candidates (~150) with full metadata
2. **FINAL 100** - Selected books only
3. **INDEXES** - Pivot tables and reference lists
4. **PROGRESS TRACKER** - Content creation status

---

## MASTER LIST - Column Definitions

### Core Information (Columns A-L)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| A | **ID** | Number | Unique identifier (1-150) | 1 |
| B | **Status** | Dropdown | Selection status | Selected / Maybe / Cut |
| C | **Entry_Number** | Number | Final position in book (1-100) | 23 |
| D | **Title** | Text | Full book title | In Patagonia |
| E | **Subtitle** | Text | Subtitle if any | - |
| F | **Author_Full_Name** | Text | Author's complete name | Bruce Chatwin |
| G | **Author_Last_Name** | Text | For sorting | Chatwin |
| H | **Author_Years** | Text | Birth-death or birth-present | 1940-1989 |
| I | **Publication_Year** | Number | Year first published | 1977 |
| J | **Journey_Year** | Text | When journey occurred | 1974-1975 |
| K | **Page_Count** | Number | Book length | 204 |
| L | **ISBN** | Text | Current edition ISBN | 978-0142437841 |

### Classification (Columns M-T)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| M | **Tier** | Dropdown | 1-4 tier system | 2 - Travel Canon |
| N | **Primary_Genre** | Dropdown | Main genre category | Literary Travelogue |
| O | **Sub_Genres** | Multi-select | 2-3 additional genres | Quest Narrative, Cultural History |
| P | **Keywords** | Text | 5-7 evocative keywords | Nomadic, Elliptical, Mythic, Desolate, Fragments |
| Q | **Traveler_Profile** | Text | Reader archetype | The Intellectual Explorer |
| R | **Writing_Style** | Dropdown | Prose characteristics | Literary, Dense, Poetic |
| S | **Tone** | Multi-select | Overall mood | Contemplative, Adventurous, Melancholic |
| T | **Difficulty** | Dropdown | Reader accessibility | Moderate |

### Geographic Data (Columns U-Y)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| U | **Primary_Region** | Dropdown | Main geographic focus | South America |
| V | **Countries** | Text | Specific countries visited | Argentina, Chile |
| W | **Continents** | Multi-select | All continents touched | South America |
| X | **Urban_Rural** | Dropdown | Setting type | Rural, Remote |
| Y | **Specific_Places** | Text | Notable locations | Buenos Aires, Patagonian Steppe, Tierra del Fuego |

### Temporal & Thematic (Columns Z-AH)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| Z | **Era_Category** | Dropdown | Historical period | Postwar (1946-1989) |
| AA | **Travel_Mode** | Multi-select | Method of travel | On Foot |
| AB | **Duration_of_Journey** | Text | How long the journey took | 6 months |
| AC | **Theme_1** | Dropdown | Primary theme | Solitude & Self-Discovery |
| AD | **Theme_2** | Dropdown | Secondary theme | Historical Pilgrimage |
| AE | **Theme_3** | Dropdown | Tertiary theme | Cultural Immersion |
| AF | **Narrative_Type** | Dropdown | Story structure | Non-linear, Vignettes |
| AG | **Purpose_of_Journey** | Text | Why they traveled | Quest for family relic, explore myth |
| AH | **Key_Insight** | Text | Main takeaway | Why humans wander |

### Author Identity & Diversity (Columns AI-AM)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| AI | **Author_Gender** | Dropdown | M / F / NB / Unknown | M |
| AJ | **Author_Nationality** | Text | Country of origin | British |
| AK | **Author_Ethnicity** | Text | Cultural background | White European |
| AL | **BIPOC** | Checkbox | Author is BIPOC | ☐ |
| AM | **Women_Writer** | Checkbox | Author identifies as woman | ☐ |
| AN | **LGBTQ** | Checkbox | LGBTQ+ perspective | ☑ |
| AO | **Non_Western** | Checkbox | Non-Western author | ☐ |

### Content Elements (Columns AP-AW)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| AP | **Opening_Quote** | Text | Memorable quote for header | "Walking is a virtue, tourism is a deadly sin." |
| AQ | **Signature_Quote** | Text | Defining quote from book | "Travel doesn't merely broaden the mind..." |
| AR | **First_Line** | Text | Opening line of book | - |
| AS | **Similar_Book_1** | Text | Pairing within the 100 | The Songlines - Chatwin |
| AT | **Similar_Book_2** | Text | Pairing outside the 100 | The Old Ways - Macfarlane |
| AU | **Drink_Pairing** | Text | Perfect drink | Bitter maté or rugged Malbec |
| AV | **Soundtrack_Pairing** | Text | Music/sounds | Low whistle of cold wind or lone cello |
| AW | **Setting_Pairing** | Text | Where to read | Remote cabin with wood stove during storm |

### Index Tags (Columns AX-BD)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| AX | **Geographic_Index** | Multi-select | Which geo indexes | South America |
| AY | **Genre_Index** | Multi-select | Which genre indexes | Literary Travelogue, Quest Narrative |
| AZ | **Era_Index** | Dropdown | Which era index | Postwar |
| BA | **Mode_Index** | Multi-select | Which mode indexes | On Foot |
| BB | **Theme_Index** | Multi-select | Which theme indexes | Solitude, Historical Pilgrimage |
| BC | **Identity_Index** | Multi-select | Which identity indexes | LGBTQ+ |
| BD | **Special_Lists** | Multi-select | Featured in special sections | Cult Classics, British Writers |

### Production Status (Columns BE-BM)

| Column | Field Name | Type | Description | Example |
|--------|------------|------|-------------|---------|
| BE | **Read_Status** | Dropdown | Has author read it? | Read |
| BF | **Research_Status** | Dropdown | Research progress | Complete |
| BG | **Draft_Status** | Dropdown | Writing progress | Completed |
| BH | **Word_Count** | Number | Entry length | 487 |
| BI | **Fact_Checked** | Checkbox | Verified accuracy | ☑ |
| BJ | **Entry_File** | Text | Markdown filename | in-patagonia-chatwin.md |
| BK | **Last_Updated** | Date | Most recent edit | 2026-01-21 |
| BL | **Assigned_To** | Dropdown | Who's writing | Ram / Claude / Both |
| BM | **Notes** | Text | Any special notes | Classic, must include |

---

## Dropdown Options

### Status (Column B)
- Selected
- Strong Maybe
- Maybe
- Unlikely
- Cut

### Tier (Column M)
- 1 - Global Bestseller
- 2 - Travel Canon
- 3 - Deep Diver
- 4 - Wildcard

### Primary_Genre (Column N)
- Literary Travelogue
- Travel Memoir
- Adventure Narrative
- Journalistic Reportage
- Philosophical Travel
- Survival Story
- Spiritual Journey
- Expat Memoir
- Culinary Travel
- Nature Writing
- War/Conflict Reportage
- Humor/Satire
- Historical Travel
- Quest Narrative

### Primary_Region (Column U)
- Africa (North)
- Africa (Sub-Saharan)
- Antarctica
- Asia (East)
- Asia (South)
- Asia (Southeast)
- Asia (Central)
- Europe (Western)
- Europe (Eastern)
- Europe (Mediterranean)
- Europe (Nordic)
- Middle East
- North America
- South America
- Oceania
- Multiple/Global

### Era_Category (Column Z)
- 19th Century (1800-1899)
- Early Modern (1900-1945)
- Postwar (1946-1989)
- Contemporary (1990-2009)
- Recent (2010-Present)

### Travel_Mode (Column AA - multi-select)
- On Foot / Hiking
- Bicycle
- Train / Railway
- Sea / Sailing
- River / Boat
- Air / Aviation
- Motorcycle
- Animal (Horse, Camel, etc.)
- Road Trip / Car
- Public Transport
- Mixed / Various

### Themes (Columns AC-AE - dropdowns)
- Solitude & Self-Discovery
- Food & Culinary
- Spiritual Journey
- Political & War
- Nature & Wilderness
- Cultural Immersion
- Expat Life
- Quest / Search
- Historical Pilgrimage
- Urban Exploration
- Family / Roots
- Language & Communication
- Art & Literature
- Science & Natural History
- Humor & Satire
- Romance & Relationships
- Poverty & Inequality
- Adventure & Danger
- Transformation & Healing

### Difficulty (Column T)
- Easy (Light, accessible, popular)
- Moderate (Some literary demands)
- Challenging (Dense, academic, long)
- Very Challenging (Experimental, difficult)

### Read_Status (Column BE)
- Read
- Partially Read
- Not Read (Researched)
- To Read

### Research_Status (Column BF)
- Not Started
- In Progress
- Complete

### Draft_Status (Column BG)
- Not Started
- Outlined
- First Draft
- Revised
- Completed
- Final

### Assigned_To (Column BL)
- Ram
- Claude
- Both
- Unassigned

---

## FINAL 100 Sheet

This sheet is a filtered view of the MASTER LIST showing only books where:
- Status = "Selected"
- Entry_Number is assigned (1-100)

**Sort by:** Entry_Number (ascending)

**Purpose:** Working list for production, ensures exactly 100 books

---

## INDEXES Sheet

Create pivot tables or reference lists for quick filtering:

### By Geographic Region
Groups all books by Primary_Region, shows count per region

### By Genre
Groups by Primary_Genre and Sub_Genres

### By Era
Groups by Era_Category, chronological distribution

### By Travel Mode
Groups by Travel_Mode tags

### By Theme
Groups by Theme_1, Theme_2, Theme_3

### By Author Identity
Counts of:
- Women writers (%)
- BIPOC authors (%)
- LGBTQ+ perspectives (%)
- Non-Western authors (%)

### By Tier
Distribution across 4 tiers

### Diversity Dashboard
Summary stats:
- Total books: 100
- Women: X (X%)
- BIPOC: X (X%)
- LGBTQ+: X (X%)
- Non-Western: X (X%)
- Continents represented: X
- Countries covered: X
- Era distribution: chart
- Genre distribution: chart

---

## PROGRESS TRACKER Sheet

Simple Kanban-style view:

| Not Started | Research | Drafting | Revision | Complete |
|-------------|----------|----------|----------|----------|
| Title - Author | Title - Author | Title - Author | Title - Author | Title - Author |

**Columns:**
- Book Title
- Author
- Assigned To
- Status (dropdown: Not Started / Research / Drafting / Revision / Complete)
- Word Count
- Last Updated
- Blocker (any issues)

**Sort by:** Status, then Last Updated

**Purpose:** Daily workflow management

---

## Sample Data Entry

### Example: In Patagonia by Bruce Chatwin

| Field | Value |
|-------|-------|
| ID | 1 |
| Status | Selected |
| Entry_Number | 23 |
| Title | In Patagonia |
| Subtitle | - |
| Author_Full_Name | Bruce Chatwin |
| Author_Last_Name | Chatwin |
| Author_Years | 1940-1989 |
| Publication_Year | 1977 |
| Journey_Year | 1974-1975 |
| Page_Count | 204 |
| ISBN | 978-0142437841 |
| Tier | 2 - Travel Canon |
| Primary_Genre | Literary Travelogue |
| Sub_Genres | Quest Narrative, Cultural History, Cubist Non-Fiction |
| Keywords | Nomadic, Elliptical, Mythic, Desolate, Fragments, Exile |
| Traveler_Profile | The Intellectual Explorer |
| Writing_Style | Literary, Poetic |
| Tone | Contemplative, Adventurous, Melancholic |
| Difficulty | Moderate |
| Primary_Region | South America |
| Countries | Argentina, Chile |
| Continents | South America |
| Urban_Rural | Rural, Remote |
| Specific_Places | Buenos Aires, Argentine Steppe, Welsh Valleys, Tierra del Fuego |
| Era_Category | Postwar (1946-1989) |
| Travel_Mode | On Foot |
| Duration_of_Journey | 6 months |
| Theme_1 | Solitude & Self-Discovery |
| Theme_2 | Historical Pilgrimage |
| Theme_3 | Cultural Immersion |
| Narrative_Type | Non-linear, Vignettes |
| Purpose_of_Journey | Search for "brontosaurus skin" from grandmother's cabinet |
| Key_Insight | Why humans wander; the internal landscape of those at world's edge |
| Author_Gender | M |
| Author_Nationality | British |
| Author_Ethnicity | White European |
| BIPOC | ☐ |
| Women_Writer | ☐ |
| LGBTQ | ☑ |
| Non_Western | ☐ |
| Opening_Quote | "Walking is a virtue, tourism is a deadly sin." |
| Signature_Quote | "Travel doesn't merely broaden the mind. It makes the mind." |
| Similar_Book_1 | The Songlines - Bruce Chatwin |
| Similar_Book_2 | The Old Ways - Robert Macfarlane |
| Drink_Pairing | Bitter maté or rugged Malbec |
| Soundtrack_Pairing | Low whistle of cold wind or lone cello |
| Setting_Pairing | Remote cabin with wood stove during storm |
| Read_Status | Read |
| Research_Status | Complete |
| Draft_Status | Completed |
| Word_Count | 487 |
| Fact_Checked | ☑ |
| Entry_File | in-patagonia-chatwin.md |
| Last_Updated | 2026-01-21 |
| Assigned_To | Ram |
| Notes | Definitive Chatwin work, genre-defining |

---

## Data Entry Workflow

### For Each Candidate Book:

1. **Initial Entry**
   - Add to MASTER LIST with ID
   - Fill in basic info (Title, Author, Year)
   - Set Status = "Maybe"

2. **Research Phase**
   - Complete all Core Information fields
   - Add Classification data
   - Fill Geographic and Temporal fields
   - Note Author Identity markers
   - Set Research_Status = "Complete"

3. **Selection Phase**
   - Change Status to "Selected" or "Cut"
   - If Selected, assign Entry_Number (1-100)
   - Verify all index tags are correct

4. **Content Creation Phase**
   - Set Draft_Status as you progress
   - Fill in Content Elements (quotes, pairings)
   - Update Word_Count
   - Enter Entry_File name
   - Check Fact_Checked when verified

5. **Completion**
   - Draft_Status = "Final"
   - All fields complete
   - Entry in FINAL 100 sheet

---

## Quality Checks Using Database

### Run These Reports:

**Diversity Check:**
```
=COUNTIF(Women_Writer, TRUE) / 100
Target: ≥ 30%
```

**Geographic Balance:**
```
=COUNTIF(Continents, "Africa")
Target: ≥ 8 books
```

**Era Distribution:**
```
=COUNTIF(Era_Category, "19th Century")
Avoid: Any single era > 40%
```

**Completion Status:**
```
=COUNTIF(Draft_Status, "Final")
Target: 100
```

**Word Count Compliance:**
```
=AVERAGE(Word_Count)
Target: 350-450 average
```

---

## Export & Sharing

### For Collaboration:
- **Google Sheets:** Share with collaborators, comment on cells
- **Weekly Snapshots:** Export CSV backups

### For Reference:
- **Print "cheat sheet"** of current selections
- **Export subsets** (e.g., "Books to Research")

### For Production:
- **Final 100 List:** Export as CSV for layout software
- **Index Data:** Generate index pages from pivot tables

---

## Maintenance

### Regular Updates:
- Mark books as completed immediately
- Update Last_Updated field when editing
- Add Notes for any issues or questions
- Review Status field weekly as selection evolves

### Data Validation:
- Use dropdowns to prevent typos
- Set numeric fields to number format only
- Require values for key fields
- Flag duplicates (same title/author)

---

**Last Updated:** 2026-01-21
**Next Steps:**
1. Create Google Sheet with this structure
2. Import candidate data from gemini100.md and chatgpt100.md
3. Begin filling in metadata for top candidates
