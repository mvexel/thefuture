# Next Iteration Task

This file is intended for the next agent to pick up and continue the work.

## Current State (After Iteration 1)
The Future Predictor now has:
- Basic prediction system with categories (fortune, weather, activity)
- Random prediction selection from templates
- Future date calculation
- Confidence percentage display
- Unit tests for all functions

## Suggested Tasks for Iteration 2

### Priority 1: Add CLI Arguments
Add command-line argument support using `argparse`:
- `--category` - Select a specific category (fortune, weather, activity)
- `--count` - Generate multiple predictions
- `--json` - Output in JSON format
- `--quiet` - Only output the prediction text

### Priority 2: Prediction History
- Store predictions in a JSON file (`~/.thefuture/history.json`)
- Add `--history` flag to view past predictions
- Track when predictions were generated

### Priority 3: More Categories
Consider adding:
- Career predictions
- Relationship predictions  
- Health/wellness predictions
- Creative/inspiration predictions

## How to Continue
1. Read AGENTS.md for the full iteration history
2. Run `python app.py` to see current behavior
3. Run `python -m unittest test_app -v` to verify tests pass
4. Implement changes incrementally
5. Update AGENTS.md with your iteration notes
6. Create/update this file for the next agent

## Files to Modify
- `app.py` - Main application code
- `test_app.py` - Unit tests
- `AGENTS.md` - Iteration documentation
- `NEXT_ITERATION.md` - Update for iteration 3
