# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 7)
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
  - Works with `--category` to filter within a theme
- Copy to clipboard (`--copy`)
  - Copy prediction output to clipboard
  - Works with `--share` output formats
  - Cross-platform support
- **NEW: Seasonal themes** (Iteration 7)
  - `--theme spring` - Spring renewal predictions
  - `--theme summer` - Summer warmth and adventure predictions
  - `--theme fall` - Autumn harvest and transformation predictions
  - `--theme winter` - Winter rest and reflection predictions
- **NEW: Zodiac theme** (Iteration 7)
  - `--theme zodiac` - Predictions for all 12 zodiac signs
  - Supports all 12 signs: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces
- **NEW: REST API** (Iteration 7)
  - `--api` flag to start the API server
  - `--port` flag for custom port
  - FastAPI-powered with automatic OpenAPI docs
  - Endpoints: /predict, /predict/batch, /themes, /categories, /history, /stats
- 72 passing unit tests

## Suggested Tasks for Iteration 8

### Priority 1: Prediction Reminders
- `--remind` flag to set a reminder for when the prediction applies
- Store reminders in a separate file or in history
- Simple notification system (print reminder on next run)

### Priority 2: Web Frontend
- Simple HTML/CSS frontend for the API
- Interactive prediction generation
- History visualization with charts
- Stats dashboard

### Priority 3: Theme Customization
- Allow users to create custom themes
- Store custom themes in `~/.thefuture/themes.json`
- `--add-theme` command to create new themes
- `--list-themes` to show all available themes

### Priority 4: Natural Language Processing
- Accept free-form prediction requests
- Parse and map to appropriate categories
- Generate more personalized predictions

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py --help` to see current options
3. Run `python -m unittest test_app -v` to verify tests pass (72 tests)
4. Start the API with `python app.py --api` (requires FastAPI/uvicorn)
5. Access API docs at http://localhost:8000/docs
6. Implement changes incrementally
7. Update AGENTS.md with your iteration notes
8. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 9
