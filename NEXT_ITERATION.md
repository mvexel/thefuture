# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 8)
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
- Smart mode (`--smart` / `-s`)
  - Combines time-aware and preference-weighted predictions
  - Best of both worlds for contextual, personalized predictions
- Social sharing (`--share`)
  - `--share text` - Full formatted text
  - `--share twitter` - Concise with hashtags
  - `--share markdown` - For forums/blogs
- Prediction themes (`--theme`)
  - `--theme motivational` - Uplifting, empowering predictions
  - `--theme holiday` - Seasonal, festive predictions
  - `--theme spooky` - Mysterious, eerie predictions
  - `--theme adventure` - Exciting, exploration-focused predictions
  - Seasonal themes: spring, summer, fall, winter
  - Zodiac theme with all 12 signs
  - Works with `--category` to filter within a theme
- Copy to clipboard (`--copy`)
  - Copy prediction output to clipboard
  - Works with `--share` output formats
  - Cross-platform support
- REST API (Iteration 7)
  - `--api` flag to start the API server
  - `--port` flag for custom port
  - FastAPI-powered with automatic OpenAPI docs
  - Endpoints: /predict, /predict/batch, /themes, /categories, /history, /stats
- **NEW: Prediction Reminders** (Iteration 8)
  - `--remind` flag to set a reminder when generating a prediction
  - `--remind <DATE>` to set reminder for a specific date (YYYY-MM-DD)
  - `--list-reminders` to view pending reminders
  - `--list-reminders --all` to include acknowledged reminders
  - `--acknowledge <ID>` to dismiss a reminder
  - `--clear-reminders` to clear acknowledged reminders
  - `--clear-reminders --all` to clear all reminders
  - Reminders stored in `~/.thefuture/reminders.json`
  - Automatic display of due reminders on app startup
- 80 passing unit tests

## Suggested Tasks for Iteration 9

### Priority 1: Web Frontend
- Simple HTML/CSS frontend for the API
- Interactive prediction generation
- History visualization with charts
- Stats dashboard

### Priority 2: Theme Customization
- Allow users to create custom themes
- Store custom themes in `~/.thefuture/themes.json`
- `--add-theme` command to create new themes
- `--list-themes` to show all available themes

### Priority 3: Natural Language Processing
- Accept free-form prediction requests
- Parse and map to appropriate categories
- Generate more personalized predictions

### Priority 4: API Enhancements
- Add reminder endpoints to the API
- Rate limiting and authentication for API
- System notifications for reminders

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py --help` to see current options
3. Run `python -m unittest test_app -v` to verify tests pass (80 tests)
4. Start the API with `python app.py --api` (requires FastAPI/uvicorn)
5. Access API docs at http://localhost:8000/docs
6. Implement changes incrementally
7. Update AGENTS.md with your iteration notes
8. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 10
