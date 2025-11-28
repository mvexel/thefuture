# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 5)
The Future Predictor now has:
- Full CLI argument support (category, count, json, quiet, history, no-save)
- 7 prediction categories: fortune, weather, activity, career, relationship, health, creative
- Prediction history stored in `~/.thefuture/history.json`
- Unique IDs for each prediction
- User feedback system (1-5 star ratings)
- Prediction analytics with `--stats`
- Export to CSV, Markdown, and JSON formats
- History clearing functionality
- Time-aware predictions (`--time-aware` / `-t`)
  - Morning, afternoon, evening, night predictions
  - Weekday vs weekend predictions
- Preference learning (`--preferred` / `-p`)
  - Weighted predictions based on user ratings
  - Preference visualization in stats
- Enhanced filtering (`--filter`, `--since`)
  - Filter exports by category
  - Filter exports by date
- **NEW: Smart mode** (`--smart` / `-s`)
  - Combines time-aware and preference-weighted predictions
  - Best of both worlds for contextual, personalized predictions
- **NEW: Social sharing** (`--share`)
  - `--share text` - Full formatted text
  - `--share twitter` - Concise with hashtags
  - `--share markdown` - For forums/blogs
- 47 passing unit tests

## Suggested Tasks for Iteration 6

### Priority 1: Web Interface
Build a simple web interface:
- Flask or FastAPI backend
- Simple HTML/CSS frontend
- REST API endpoints for predictions
- Web-based history and stats viewing

### Priority 2: Prediction Reminders
- `--remind` flag to set a reminder for when the prediction applies
- Store reminders in a separate file or in history
- Simple notification system (print reminder on next run)

### Priority 3: Copy to Clipboard
- Add clipboard functionality to `--share` output
- Cross-platform support (pyperclip or similar)

### Priority 4: Prediction Themes
- Add themed prediction sets (Halloween, Holiday, Motivation, etc.)
- `--theme` flag to select prediction theme

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py --help` to see current options
3. Run `python -m unittest test_app -v` to verify tests pass (47 tests)
4. Implement changes incrementally
5. Update AGENTS.md with your iteration notes
6. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 7
