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

---

## Ideas for Future Iterations

### Iteration 5 Ideas
- [ ] Web interface or API endpoint
- [ ] Prediction reminders (`--remind` flag)
- [ ] Share predictions via social media or email
- [ ] Combine time-aware and preferred modes
- [ ] Natural language processing for custom prediction requests
- [ ] Time-series analysis for trend-based predictions
- [ ] Integration with external data sources (news, events, etc.)
- [ ] Share predictions via social media or email
- [ ] Prediction reminders and follow-ups

### Long-term Vision
- Self-improving prediction accuracy through feedback loops
- Agent-to-agent learning between iterations
- Convergence toward meaningful and helpful predictions

