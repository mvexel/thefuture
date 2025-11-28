# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 2)
The Future Predictor now has:
- Full CLI argument support (category, count, json, quiet, history, no-save)
- 7 prediction categories: fortune, weather, activity, career, relationship, health, creative
- Prediction history stored in `~/.thefuture/history.json`
- JSON output mode for programmatic use
- Quiet mode for scripting
- 15 passing unit tests

## Suggested Tasks for Iteration 3

### Priority 1: User Feedback System
Add the ability for users to rate predictions:
- `--feedback <id> <rating>` - Rate a prediction (1-5 stars or thumbs up/down)
- Store feedback alongside predictions in history
- Add `--show-rated` flag to view predictions with their ratings

### Priority 2: Prediction Analytics
- `--stats` flag to show prediction statistics
- Count predictions by category
- Show average confidence levels
- Display most/least frequent categories

### Priority 3: Smart Predictions
Consider implementing:
- Time-of-day aware predictions (morning vs evening)
- Day-of-week aware predictions (weekday vs weekend)
- Learn from user preferences based on feedback

### Priority 4: Export Capabilities
- `--export csv` - Export history to CSV
- `--export markdown` - Export history as markdown
- `--clear-history` - Clear prediction history

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py --help` to see current options
3. Run `python -m unittest test_app -v` to verify tests pass (15 tests)
4. Implement changes incrementally
5. Update AGENTS.md with your iteration notes
6. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 4
