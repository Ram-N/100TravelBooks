#!/bin/bash
# Project Status Dashboard
# Run this anytime to see current state of 100 Greatest Travel Books project
#
# Usage:
#   ./status.sh                    - Show summary dashboard (default)
#   ./status.sh --view candidates  - List all Candidate books
#   ./status.sh --view completed   - List all Completed books
#   ./status.sh --view honorable   - List all Honorable Mentions
#   ./status.sh --view cut         - List all Cut books
#   ./status.sh --view maybe       - List all Maybe books
#   ./status.sh --view duplicate   - List all Duplicate books
#   ./status.sh --view all         - List ALL books with status
#   ./status.sh --help             - Show this help

# View functions
view_candidates() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   📚 CANDIDATE BOOKS (Final 100)"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    grep '^[0-9]*,Candidate,' database/master-candidates.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-50s %s\n", $1, $3, $4}' | sort -n
    COUNT=$(grep -c '^[0-9]*,Candidate,' database/master-candidates.csv 2>/dev/null || echo "0")
    echo ""
    echo "  Total: $COUNT books"
    echo ""
}

view_completed() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   ✅ COMPLETED ENTRIES"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    grep '^[0-9]*,Completed,' database/master-candidates.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-50s %s\n", $1, $3, $4}' | sort -n
    COUNT=$(grep -c '^[0-9]*,Completed,' database/master-candidates.csv 2>/dev/null || echo "0")
    echo ""
    echo "  Total: $COUNT entries completed"
    echo ""
}

view_honorable() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   ⭐ HONORABLE MENTIONS"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    tail -n +2 database/honorable-mentions.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-50s %s\n", $1, $2, $3}' | sort -n
    COUNT=$(tail -n +2 database/honorable-mentions.csv 2>/dev/null | wc -l || echo "0")
    echo ""
    echo "  Total: $COUNT honorable mentions"
    echo ""
}

view_cut() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   ✗ CUT BOOKS"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    grep '^[0-9]*,Cut,' database/master-candidates.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-50s %s\n", $1, $3, $4}' | sort -n
    COUNT=$(grep -c '^[0-9]*,Cut,' database/master-candidates.csv 2>/dev/null || echo "0")
    echo ""
    echo "  Total: $COUNT books cut"
    echo ""
}

view_maybe() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   ❓ MAYBE BOOKS (Undecided)"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    grep '^[0-9]*,Maybe,' database/master-candidates.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-50s %s\n", $1, $3, $4}' | sort -n
    COUNT=$(grep -c '^[0-9]*,Maybe,' database/master-candidates.csv 2>/dev/null || echo "0")
    echo ""
    echo "  Total: $COUNT books pending decision"
    echo ""
}

view_duplicate() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   = DUPLICATE BOOKS"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    grep '^[0-9]*,Duplicate,' database/master-candidates.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-50s %s\n", $1, $3, $4}' | sort -n
    COUNT=$(grep -c '^[0-9]*,Duplicate,' database/master-candidates.csv 2>/dev/null || echo "0")
    echo ""
    echo "  Total: $COUNT duplicates identified"
    echo ""
}

view_all() {
    echo "═══════════════════════════════════════════════════════════"
    echo "   📋 ALL BOOKS WITH STATUS"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    tail -n +2 database/master-candidates.csv 2>/dev/null | \
        awk -F',' '{printf "  %3s. %-12s %-40s %s\n", $1, $2, $3, $4}' | sort -n
    COUNT=$(tail -n +2 database/master-candidates.csv 2>/dev/null | wc -l || echo "0")
    echo ""
    echo "  Total: $COUNT books in database"
    echo ""
}

show_help() {
    echo "Usage: ./status.sh [--view <category>] [--help]"
    echo ""
    echo "Options:"
    echo "  (no args)           Show summary dashboard (default)"
    echo "  --view candidates   List all Candidate books"
    echo "  --view completed    List all Completed books"
    echo "  --view honorable    List all Honorable Mentions"
    echo "  --view cut          List all Cut books"
    echo "  --view maybe        List all Maybe books"
    echo "  --view duplicate    List all Duplicate books"
    echo "  --view all          List ALL books with status"
    echo "  --help              Show this help"
    echo ""
}

# Parse command line arguments
if [ "$1" = "--help" ]; then
    show_help
    exit 0
elif [ "$1" = "--view" ]; then
    case "$2" in
        candidates)
            view_candidates
            exit 0
            ;;
        completed)
            view_completed
            exit 0
            ;;
        honorable)
            view_honorable
            exit 0
            ;;
        cut)
            view_cut
            exit 0
            ;;
        maybe)
            view_maybe
            exit 0
            ;;
        duplicate)
            view_duplicate
            exit 0
            ;;
        all)
            view_all
            exit 0
            ;;
        *)
            echo "Error: Unknown view category '$2'"
            echo ""
            show_help
            exit 1
            ;;
    esac
fi

# Default: Show dashboard
echo "═══════════════════════════════════════════════════════════"
echo "   📚 THE 100 GREATEST TRAVEL BOOKS - PROJECT STATUS"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Book Selection Status
echo "📖 BOOK SELECTION STATUS:"
echo "─────────────────────────────────────────────────────────"

COMPLETED=$(grep -c '^[0-9]*,Completed,' database/master-candidates.csv 2>/dev/null)
COMPLETED=${COMPLETED:-0}
CANDIDATES=$(grep -c '^[0-9]*,Candidate,' database/master-candidates.csv 2>/dev/null)
CANDIDATES=${CANDIDATES:-0}
FINAL_100=$((COMPLETED + CANDIDATES))
MAYBE=$(grep -c '^[0-9]*,Maybe,' database/master-candidates.csv 2>/dev/null)
MAYBE=${MAYBE:-0}
HM=$(tail -n +2 database/honorable-mentions.csv 2>/dev/null | wc -l)
HM=${HM:-0}
CUT=$(grep -c '^[0-9]*,Cut,' database/master-candidates.csv 2>/dev/null)
CUT=${CUT:-0}
DUPLICATE=$(grep -c '^[0-9]*,Duplicate,' database/master-candidates.csv 2>/dev/null)
DUPLICATE=${DUPLICATE:-0}

echo "  ✓ Final 100 (Selected):     $FINAL_100"
echo "    - Entries completed:      $COMPLETED"
echo "    - Still to write:         $CANDIDATES"
echo "  ? Maybe (undecided):        $MAYBE"
echo "  ⭐ Honorable Mentions:       $HM"
echo "  ✗ Hard Cuts:                $CUT"
echo "  = Duplicates:               $DUPLICATE"

TOTAL=$((FINAL_100 + MAYBE + HM + CUT))
echo ""
echo "  Total books reviewed:       $TOTAL"
echo ""

# Writing Progress
echo "✍️  WRITING PROGRESS:"
echo "─────────────────────────────────────────────────────────"

ENTRIES_DONE=$COMPLETED
ENTRIES_REMAINING=$CANDIDATES

echo "  ✓ Entries completed:        $ENTRIES_DONE"
echo "  ⏳ Entries remaining:        $ENTRIES_REMAINING"

if [ "$FINAL_100" -gt 0 ]; then
    PERCENT=$((ENTRIES_DONE * 100 / FINAL_100))
    echo "  📊 Progress:                 $PERCENT%"
fi

echo ""

# Progress Bar
echo "  Progress Bar:"
BARS=$((ENTRIES_DONE / 5))
SPACES=$((ENTRIES_REMAINING / 5))
printf "  ["
for i in $(seq 1 $BARS); do printf "█"; done
for i in $(seq 1 $SPACES); do printf "░"; done
printf "] $ENTRIES_DONE/$FINAL_100\n"

echo ""

# Recent Entries
echo "📝 RECENTLY COMPLETED ENTRIES:"
echo "─────────────────────────────────────────────────────────"
if [ -d "book-writeups" ]; then
    ls -t book-writeups/*.md 2>/dev/null | head -5 | while read file; do
        basename "$file" .md | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++){$i=toupper(substr($i,1,1)) substr($i,2)}}1' | sed 's/^/  • /'
    done
    [ $(ls book-writeups/*.md 2>/dev/null | wc -l) -eq 0 ] && echo "  (none yet)"
else
    echo "  (no book-writeups directory found)"
fi

echo ""

# Decision Items
echo "⚠️  PENDING DECISIONS:"
echo "─────────────────────────────────────────────────────────"

if [ "$MAYBE" -gt 0 ]; then
    echo "  • $MAYBE book(s) in 'Maybe' status need decision"
    grep '^[0-9]*,Maybe,' database/master-candidates.csv 2>/dev/null | cut -d',' -f3,4 | sed 's/^/    - /' | sed 's/,/ by /'
fi

# TBD items from notes
echo "  • Borneo: Hansen vs O'Hanlon - keep both or choose one?"

echo ""

# Target Metrics
echo "🎯 DIVERSITY TARGETS:"
echo "─────────────────────────────────────────────────────────"

# Count women authors in candidates (approximate - would need better data)
echo "  Women authors:              TBD (target: 30%+)"
echo "  BIPOC authors:              TBD (target: 20%+)"
echo "  (Run detailed analysis to calculate)"

echo ""

# Timeline
echo "⏰ TIMELINE:"
echo "─────────────────────────────────────────────────────────"

START_DATE="2026-01-21"
TARGET_DATE="2026-02-21"
TODAY=$(date +%Y-%m-%d)

DAYS_ELAPSED=$(( ( $(date -d "$TODAY" +%s) - $(date -d "$START_DATE" +%s) ) / 86400 ))
DAYS_TOTAL=$(( ( $(date -d "$TARGET_DATE" +%s) - $(date -d "$START_DATE" +%s) ) / 86400 ))
DAYS_REMAINING=$((DAYS_TOTAL - DAYS_ELAPSED))

echo "  Start date:                 $START_DATE"
echo "  Target date:                $TARGET_DATE"
echo "  Days elapsed:               $DAYS_ELAPSED"
echo "  Days remaining:             $DAYS_REMAINING"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "💡 Tip: Use './status.sh --view <category>' to see filtered lists"
echo "   Examples: --view completed, --view honorable, --view all"
echo "   Run './status.sh --help' for all options"
echo ""
