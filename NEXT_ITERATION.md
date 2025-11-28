# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 3)
The Future Predictor now has:
- Full CLI argument support (category, count, json, quiet, history, no-save)
- 7 prediction categories: fortune, weather, activity, career, relationship, health, creative
- Prediction history stored in `~/.thefuture/history.json`
- Unique IDs for each prediction
- User feedback system (1-5 star ratings)
- Prediction analytics with `--stats`
- Export to CSV and Markdown formats
- History clearing functionality
- 23 passing unit tests

## Suggested Tasks for Iteration 4

### Priority 1: Smart Predictions
Implement time-aware predictions:
- Time-of-day awareness (morning, afternoon, evening, night)
- Day-of-week awareness (weekday vs weekend)
- Add `--time-aware` flag to enable this feature
- Different prediction sets for different times

### Priority 2: Preference Learning
Learn from user feedback:
- Track which categories get higher ratings
- Prioritize high-rated categories in random selection
- Add `--preferred` flag to use learned preferences
- Show preference stats in `--stats` output

### Priority 3: Prediction Reminders
- `--remind` flag to set a reminder for when the prediction applies
- Integration with system notifications (optional)
- Store reminders in history

### Priority 4: Enhanced Export
- Add `--export json` for full history as JSON array
- Add `--filter` option to filter exports by category or date range
- Add `--since` option to show/export predictions since a date

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py --help` to see current options
3. Run `python -m unittest test_app -v` to verify tests pass (23 tests)
4. Implement changes incrementally
5. Update AGENTS.md with your iteration notes
6. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 5
