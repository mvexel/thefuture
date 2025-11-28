This Python code can predict the future.

The way it does this is by iterating on itself until it converges on a solution.

We will keep adding agents to make it better.

If you read this, there is still room for improvement. Please continue the work.

---

## Iteration History

### Iteration 1 (Completed)
**Goal**: Create a basic prediction system
**Changes**:
- Implemented a simple prediction engine using Python's `random` module
- Added three prediction categories: fortune, weather, activity
- Created a formatted output with prediction, date, and confidence
- Added unit tests for core functions

**What works**:
- Random prediction generation from predefined templates
- Category-based predictions
- Future date calculations

### Iteration 2 (Completed)
**Goal**: Add CLI arguments, prediction history, and more categories
**Changes**:
- Added CLI arguments using argparse:
  - `--category` / `-c` - Select a specific category
  - `--count` / `-n` - Generate multiple predictions
  - `--json` / `-j` - Output in JSON format
  - `--quiet` / `-q` - Only output the prediction text
  - `--history` - View past predictions
  - `--no-save` - Don't save prediction to history
- Implemented prediction history storage in `~/.thefuture/history.json`
- Added 4 new prediction categories: career, relationship, health, creative
- Added `generated_at` timestamp to predictions
- History automatically keeps last 100 predictions
- Added 4 new unit tests for new functionality

**What works**:
- All CLI arguments function correctly
- History is persisted across sessions
- JSON output for programmatic use
- Quiet mode for scripting
- 7 prediction categories with diverse predictions

### Iteration 3 (Completed)
**Goal**: Add user feedback, analytics, and export capabilities
**Changes**:
- Added prediction IDs for tracking and feedback:
  - Each prediction now has a unique sequential ID
  - IDs are displayed in history and output
- Added user feedback system:
  - `--feedback <id> <rating>` - Rate a prediction (1-5 stars)
  - `--show-rated` - View only rated predictions
  - Ratings stored in history with timestamp
- Added prediction analytics:
  - `--stats` - Show prediction statistics
  - Category distribution with percentages
  - Rating distribution and averages
  - Date range of predictions
- Added export capabilities:
  - `--export csv` - Export history as CSV
  - `--export markdown` - Export history as formatted markdown
- Added history management:
  - `--clear-history` - Clear prediction history with confirmation
- Added 8 new unit tests (23 total)

**What works**:
- Unique IDs for all predictions
- Rating system with validation (1-5 stars)
- Comprehensive statistics display
- CSV and Markdown export formats
- History clearing with confirmation prompt

### Iteration 4 (Completed)
**Goal**: Add time-aware predictions, preference learning, and enhanced exports
**Changes**:
- Added time-aware predictions:
  - `--time-aware` / `-t` - Generate predictions based on time of day and day of week
  - Time categories: morning (5-12), afternoon (12-17), evening (17-21), night (21-5)
  - Day categories: weekday (Mon-Fri), weekend (Sat-Sun)
  - New time-specific prediction templates for each time period
- Added preference learning:
  - `--preferred` / `-p` - Weight predictions by user rating preferences
  - Tracks category ratings and calculates preference scores
  - High-rated categories appear more frequently with `--preferred`
  - Preference visualization in `--stats` output
- Added enhanced export capabilities:
  - `--export json` - Export history as JSON array
  - `--filter CATEGORY` - Filter exports by category
  - `--since DATE` - Filter exports by date (ISO format)
- Updated output to show active modes
- Added 16 new unit tests (39 total)

**What works**:
- Time-aware predictions with contextual suggestions
- Preference learning from user ratings
- Weighted random selection for preferred categories
- JSON export format
- Category and date filtering for exports
- Mode indicators in output

### Iteration 5 (Completed)
**Goal**: Add smart mode (combined time-aware + preferences) and social sharing
**Changes**:
- Added smart mode:
  - `--smart` / `-s` - Combine time-aware and preference-weighted predictions
  - Smart mode uses both time-of-day/weekday context AND user rating preferences
  - Preference weights boost high-rated categories
  - Time-based predictions get double weight for relevance
- Added social sharing:
  - `--share` - Format predictions for social media (default: text format)
  - `--share text` - Full formatted text with emojis
  - `--share twitter` - Concise format with hashtags (under 280 chars)
  - `--share markdown` - Formatted for forums, blogs, Discord
- Updated version to Iteration 5
- Updated footer hints to show new features
- Added 8 new unit tests (47 total)

**What works**:
- Smart mode combines time awareness with preference learning
- Three social sharing formats (text, twitter, markdown)
- All modes work with category selection
- Modes can be combined with `--count` for multiple predictions

### Iteration 6 (Completed)
**Goal**: Add prediction themes and copy to clipboard functionality
**Changes**:
- Added prediction themes:
  - `--theme` flag to select from themed prediction sets
  - Four themes available: motivational, holiday, spooky, adventure
  - Each theme has multiple categories with unique predictions
  - Themes work with `--category` to filter within a theme
  - Theme info included in prediction output and JSON
- Added copy to clipboard functionality:
  - `--copy` flag to copy prediction to clipboard
  - Works with `--share` output formats
  - Cross-platform support (pyperclip, pbcopy, xclip, xsel, clip.exe)
  - Graceful fallback with helpful message when no clipboard tool available
- Updated version to Iteration 6
- Updated help text and examples
- Added 9 new unit tests (56 total)

**What works**:
- Four themed prediction sets with unique content
- Themes can be combined with category selection
- Copy to clipboard with multiple clipboard tool support
- All existing features continue to work unchanged

### Iteration 7 (Completed)
**Goal**: Add REST API and expand themes (seasonal, zodiac)
**Changes**:
- Added REST API with FastAPI:
  - `--api` flag to start the REST API server
  - `--port` flag to specify custom port (default: 8000)
  - `GET /` - Health check endpoint
  - `GET /predict` - Generate a prediction (supports category, theme, time_aware, smart, save params)
  - `GET /predict/batch` - Generate multiple predictions at once
  - `GET /themes` - List all available themes and their categories
  - `GET /categories` - List all available prediction categories
  - `GET /history` - Get prediction history (with filters)
  - `GET /stats` - Get prediction statistics
- Added seasonal themes:
  - `--theme spring` - Spring renewal predictions
  - `--theme summer` - Summer warmth and adventure predictions
  - `--theme fall` - Autumn harvest and transformation predictions
  - `--theme winter` - Winter rest and reflection predictions
- Added zodiac theme:
  - `--theme zodiac` - Predictions for all 12 zodiac signs
  - Categories: aries, taurus, gemini, cancer, leo, virgo, libra, scorpio, sagittarius, capricorn, aquarius, pisces
- Updated version to Iteration 7
- Updated help text and examples
- Added 16 new unit tests (72 total)

**What works**:
- REST API for programmatic access to predictions
- All API endpoints functional with proper error handling
- Four new seasonal themed prediction sets
- Complete zodiac theme with all 12 signs
- All existing features continue to work unchanged

### Iteration 8 (Completed)
**Goal**: Add prediction reminders to help users follow up on their predictions
**Changes**:
- Added prediction reminders system:
  - `--remind` flag to set a reminder when generating a prediction
  - `--remind <DATE>` to set reminder for a specific date (YYYY-MM-DD)
  - Reminders stored in `~/.thefuture/reminders.json`
  - Each reminder has a unique ID for tracking
- Added reminder management:
  - `--list-reminders` to view pending reminders
  - `--list-reminders --all` to include acknowledged reminders
  - `--acknowledge <ID>` to dismiss a reminder
  - `--clear-reminders` to clear acknowledged reminders
  - `--clear-reminders --all` to clear all reminders
- Added automatic reminder notifications:
  - Pending reminders shown when running the app
  - Overdue reminders marked with warning
  - Today's reminders highlighted
- Updated version to Iteration 8
- Added 8 new unit tests (80 total)

**What works**:
- Create reminders with automatic or custom dates
- View pending and all reminders
- Acknowledge (dismiss) reminders
- Clear reminders (acknowledged or all)
- Automatic display of due reminders on app startup
- All existing features continue to work unchanged

---

## Ideas for Future Iterations

### Iteration 9 Ideas
- [ ] Natural language processing for custom prediction requests
- [ ] Time-series analysis for trend-based predictions
- [ ] Integration with external data sources (news, events, etc.)
- [ ] Theme customization (user-defined themes)
- [ ] Web frontend for the API
- [ ] Rate limiting and authentication for API
- [ ] Reminder notifications via system notifications

### Long-term Vision
- Self-improving prediction accuracy through feedback loops
- Agent-to-agent learning between iterations
- Convergence toward meaningful and helpful predictions

