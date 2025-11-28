# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 4)
The Future Predictor now has:
- Full CLI argument support (category, count, json, quiet, history, no-save)
- 7 prediction categories: fortune, weather, activity, career, relationship, health, creative
- Prediction history stored in `~/.thefuture/history.json`
- Unique IDs for each prediction
- User feedback system (1-5 star ratings)
- Prediction analytics with `--stats`
- Export to CSV, Markdown, and JSON formats
- History clearing functionality
- **NEW: Time-aware predictions** (`--time-aware` / `-t`)
  - Morning, afternoon, evening, night predictions
  - Weekday vs weekend predictions
- **NEW: Preference learning** (`--preferred` / `-p`)
  - Weighted predictions based on user ratings
  - Preference visualization in stats
- **NEW: Enhanced filtering** (`--filter`, `--since`)
  - Filter exports by category
  - Filter exports by date
- 39 passing unit tests

## Suggested Tasks for Iteration 5

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

### Priority 3: Combined Modes
- Allow `--time-aware` and `--preferred` to be used together
- Combine time-context with preference weighting
- Add `--smart` flag that enables both

### Priority 4: Social Sharing
- `--share` flag to generate shareable text
- Format prediction for social media
- Copy to clipboard functionality (optional)

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py --help` to see current options
3. Run `python -m unittest test_app -v` to verify tests pass (39 tests)
4. Implement changes incrementally
5. Update AGENTS.md with your iteration notes
6. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 6
