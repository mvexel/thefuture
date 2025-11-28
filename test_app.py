#!/usr/bin/env python
"""Tests for the Future Predictor app."""

import json
import os
import shutil
import sys
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch
from datetime import datetime, timedelta

from app import (
    get_prediction,
    get_future_date,
    predict_the_future,
    load_history,
    save_to_history,
    add_feedback,
    show_stats,
    export_history,
    filter_history,
    get_time_of_day,
    get_day_type,
    get_time_aware_prediction,
    get_preferred_categories,
    get_preferred_prediction,
    get_smart_prediction,
    format_for_sharing,
    get_themed_prediction,
    copy_to_clipboard,
    create_api,
    load_reminders,
    save_reminder,
    get_pending_reminders,
    acknowledge_reminder,
    PREDICTIONS,
    THEMES,
    HISTORY_DIR,
    HISTORY_FILE,
    REMINDERS_FILE,
)


class TestGetPrediction(unittest.TestCase):
    """Tests for the get_prediction function."""

    def test_returns_tuple(self):
        """Prediction should return a tuple of (prediction, category)."""
        result = get_prediction()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_valid_category(self):
        """Prediction from valid category should be in that category's list."""
        for category in PREDICTIONS.keys():
            prediction, returned_category = get_prediction(category)
            self.assertIn(prediction, PREDICTIONS[category])
            self.assertEqual(returned_category, category)

    def test_invalid_category(self):
        """Invalid category should return error message."""
        prediction, category = get_prediction("nonexistent")
        self.assertIn("Unknown category", prediction)
        self.assertEqual(category, "nonexistent")

    def test_none_category_returns_valid_prediction(self):
        """None category should return a valid prediction from any category."""
        prediction, category = get_prediction(None)
        self.assertIn(category, PREDICTIONS.keys())
        self.assertIn(prediction, PREDICTIONS[category])

    def test_new_categories_exist(self):
        """New categories from Iteration 2 should exist."""
        new_categories = ["career", "relationship", "health", "creative"]
        for category in new_categories:
            self.assertIn(category, PREDICTIONS)
            self.assertGreater(len(PREDICTIONS[category]), 0)


class TestGetFutureDate(unittest.TestCase):
    """Tests for the get_future_date function."""

    def test_returns_string(self):
        """Future date should be a string."""
        result = get_future_date()
        self.assertIsInstance(result, str)

    @patch('app.datetime')
    def test_default_one_day_ahead(self, mock_datetime):
        """Default should be one day ahead."""
        fixed_time = datetime(2025, 1, 15, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        # Need to re-import to get the patched version
        from app import get_future_date
        expected = (fixed_time + timedelta(days=1)).strftime("%A, %B %d, %Y")
        result = get_future_date()
        self.assertEqual(result, expected)

    @patch('app.datetime')
    def test_custom_days_ahead(self, mock_datetime):
        """Custom days should work correctly."""
        fixed_time = datetime(2025, 1, 15, 12, 0, 0)
        mock_datetime.now.return_value = fixed_time
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        from app import get_future_date
        expected = (fixed_time + timedelta(days=7)).strftime("%A, %B %d, %Y")
        result = get_future_date(7)
        self.assertEqual(result, expected)


class TestPredictTheFuture(unittest.TestCase):
    """Tests for the predict_the_future function."""

    def test_returns_dict(self):
        """Should return a dictionary."""
        result = predict_the_future()
        self.assertIsInstance(result, dict)

    def test_has_required_keys(self):
        """Result should have all required keys."""
        result = predict_the_future()
        required_keys = ["prediction", "applies_to", "category", "confidence"]
        for key in required_keys:
            self.assertIn(key, result)

    def test_confidence_format(self):
        """Confidence should be a percentage string."""
        result = predict_the_future()
        self.assertTrue(result["confidence"].endswith("%"))

    def test_category_matches_prediction(self):
        """Category should match where prediction came from."""
        result = predict_the_future()
        category = result["category"]
        prediction = result["prediction"]
        # If it's a valid category, prediction should be in that category's list
        if category in PREDICTIONS:
            self.assertIn(prediction, PREDICTIONS[category])

    def test_has_generated_at_key(self):
        """Result should have generated_at timestamp."""
        result = predict_the_future()
        self.assertIn("generated_at", result)
        # Should be a valid ISO format datetime
        datetime.fromisoformat(result["generated_at"])


class TestHistory(unittest.TestCase):
    """Tests for prediction history functions."""

    def setUp(self):
        """Set up a temporary directory for history tests."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_history_dir = HISTORY_DIR
        self.original_history_file = HISTORY_FILE

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_load_empty_history(self, mock_dir, mock_file):
        """Loading history from non-existent file returns empty list."""
        mock_file.exists.return_value = False
        result = load_history()
        self.assertEqual(result, [])

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_save_and_load_history(self, mock_dir, mock_file):
        """Saving and loading history should work."""
        # Use a real temp file for this test
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            prediction = {
                "prediction": "Test prediction",
                "category": "test",
                "generated_at": datetime.now().isoformat(),
            }
            save_to_history(prediction)
            
            history = load_history()
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["prediction"], "Test prediction")

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_save_adds_id(self, mock_dir, mock_file):
        """Saving prediction should add an ID."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            prediction = {
                "prediction": "Test prediction",
                "category": "test",
            }
            save_to_history(prediction)
            
            history = load_history()
            self.assertEqual(len(history), 1)
            self.assertIn("id", history[0])
            self.assertEqual(history[0]["id"], 1)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_sequential_ids(self, mock_dir, mock_file):
        """Multiple predictions should have sequential IDs."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            for i in range(3):
                save_to_history({"prediction": f"Test {i}", "category": "test"})
            
            history = load_history()
            self.assertEqual(len(history), 3)
            self.assertEqual(history[0]["id"], 1)
            self.assertEqual(history[1]["id"], 2)
            self.assertEqual(history[2]["id"], 3)


class TestFeedback(unittest.TestCase):
    """Tests for the feedback system."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_add_feedback_valid(self, mock_dir, mock_file):
        """Adding feedback with valid rating should succeed."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            save_to_history({"prediction": "Test prediction", "category": "test"})
            
            result = add_feedback(1, 5)
            self.assertTrue(result)
            
            history = load_history()
            self.assertEqual(history[0]["rating"], 5)
            self.assertIn("rated_at", history[0])

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_add_feedback_invalid_id(self, mock_dir, mock_file):
        """Adding feedback for non-existent prediction should fail."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            save_to_history({"prediction": "Test prediction", "category": "test"})
            
            result = add_feedback(999, 5)
            self.assertFalse(result)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_add_feedback_invalid_rating(self, mock_dir, mock_file):
        """Adding feedback with invalid rating should fail."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            save_to_history({"prediction": "Test prediction", "category": "test"})
            
            result_low = add_feedback(1, 0)
            self.assertFalse(result_low)
            
            result_high = add_feedback(1, 6)
            self.assertFalse(result_high)


class TestStats(unittest.TestCase):
    """Tests for the statistics functionality."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_stats_with_data(self, mock_dir, mock_file):
        """Stats should display without error when data exists."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            # Add some predictions
            save_to_history({"prediction": "Test 1", "category": "fortune", "generated_at": datetime.now().isoformat()})
            save_to_history({"prediction": "Test 2", "category": "fortune", "generated_at": datetime.now().isoformat()})
            save_to_history({"prediction": "Test 3", "category": "career", "generated_at": datetime.now().isoformat()})
            
            show_stats()
            output = mock_stdout.getvalue()
            
            self.assertIn("Total predictions: 3", output)
            self.assertIn("Fortune:", output)
            self.assertIn("Career:", output)


class TestExport(unittest.TestCase):
    """Tests for the export functionality."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_export_csv(self, mock_dir, mock_file):
        """CSV export should produce valid CSV output."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            save_to_history({"prediction": "Test prediction", "category": "fortune"})
            
            export_history("csv")
            output = mock_stdout.getvalue()
            
            self.assertIn("id,category,prediction", output)
            self.assertIn("fortune", output)
            self.assertIn("Test prediction", output)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_export_markdown(self, mock_dir, mock_file):
        """Markdown export should produce valid markdown output."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            save_to_history({"prediction": "Test prediction", "category": "fortune"})
            
            export_history("markdown")
            output = mock_stdout.getvalue()
            
            self.assertIn("# Prediction History", output)
            self.assertIn("## Fortune", output)
            self.assertIn("Test prediction", output)


# Iteration 4 Tests
class TestTimeAwareness(unittest.TestCase):
    """Tests for time-aware prediction functionality."""

    def test_get_time_of_day_morning(self):
        """Morning hours should return 'morning'."""
        from app import get_time_of_day
        morning = datetime(2025, 1, 15, 8, 0, 0)
        self.assertEqual(get_time_of_day(morning), "morning")

    def test_get_time_of_day_afternoon(self):
        """Afternoon hours should return 'afternoon'."""
        from app import get_time_of_day
        afternoon = datetime(2025, 1, 15, 14, 0, 0)
        self.assertEqual(get_time_of_day(afternoon), "afternoon")

    def test_get_time_of_day_evening(self):
        """Evening hours should return 'evening'."""
        from app import get_time_of_day
        evening = datetime(2025, 1, 15, 19, 0, 0)
        self.assertEqual(get_time_of_day(evening), "evening")

    def test_get_time_of_day_night(self):
        """Night hours should return 'night'."""
        from app import get_time_of_day
        night = datetime(2025, 1, 15, 23, 0, 0)
        self.assertEqual(get_time_of_day(night), "night")
        early_night = datetime(2025, 1, 15, 3, 0, 0)
        self.assertEqual(get_time_of_day(early_night), "night")

    def test_get_day_type_weekday(self):
        """Monday-Friday should return 'weekday'."""
        from app import get_day_type
        monday = datetime(2025, 1, 13, 12, 0, 0)  # Monday
        self.assertEqual(get_day_type(monday), "weekday")
        friday = datetime(2025, 1, 17, 12, 0, 0)  # Friday
        self.assertEqual(get_day_type(friday), "weekday")

    def test_get_day_type_weekend(self):
        """Saturday and Sunday should return 'weekend'."""
        from app import get_day_type
        saturday = datetime(2025, 1, 18, 12, 0, 0)  # Saturday
        self.assertEqual(get_day_type(saturday), "weekend")
        sunday = datetime(2025, 1, 19, 12, 0, 0)  # Sunday
        self.assertEqual(get_day_type(sunday), "weekend")

    def test_time_aware_prediction_returns_tuple(self):
        """Time-aware prediction should return a tuple."""
        from app import get_time_aware_prediction
        result = get_time_aware_prediction()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_time_aware_prediction_with_category(self):
        """Time-aware prediction with category should return that category."""
        from app import get_time_aware_prediction
        prediction, category = get_time_aware_prediction("fortune")
        self.assertEqual(category, "fortune")


class TestPreferenceLearning(unittest.TestCase):
    """Tests for preference learning functionality."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_get_preferred_categories_empty(self, mock_dir, mock_file):
        """No rated predictions should return empty preferences."""
        from app import get_preferred_categories
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            prefs = get_preferred_categories()
            self.assertEqual(prefs, {})

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_get_preferred_categories_with_ratings(self, mock_dir, mock_file):
        """Rated predictions should generate preference scores."""
        from app import get_preferred_categories
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            # Create history with ratings
            history = [
                {"prediction": "Test 1", "category": "fortune", "rating": 5},
                {"prediction": "Test 2", "category": "fortune", "rating": 5},
                {"prediction": "Test 3", "category": "career", "rating": 3},
            ]
            with open(temp_file, "w") as f:
                json.dump(history, f)
            
            prefs = get_preferred_categories()
            
            # Fortune should have higher score than career
            self.assertIn("fortune", prefs)
            self.assertIn("career", prefs)
            self.assertGreater(prefs["fortune"], prefs["career"])

    def test_preferred_prediction_returns_tuple(self):
        """Preferred prediction should return a tuple."""
        from app import get_preferred_prediction
        result = get_preferred_prediction()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


class TestEnhancedExport(unittest.TestCase):
    """Tests for enhanced export functionality."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_export_json(self, mock_dir, mock_file):
        """JSON export should produce valid JSON output."""
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)), \
             patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            save_to_history({"prediction": "Test prediction", "category": "fortune"})
            
            export_history("json")
            output = mock_stdout.getvalue()
            
            # Should be valid JSON
            parsed = json.loads(output)
            self.assertIsInstance(parsed, list)
            self.assertEqual(len(parsed), 1)
            self.assertEqual(parsed[0]["category"], "fortune")

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_filter_by_category(self, mock_dir, mock_file):
        """Export should filter by category."""
        from app import filter_history
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            history = [
                {"prediction": "Test 1", "category": "fortune"},
                {"prediction": "Test 2", "category": "career"},
                {"prediction": "Test 3", "category": "fortune"},
            ]
            
            filtered = filter_history(history, category="fortune")
            
            self.assertEqual(len(filtered), 2)
            self.assertTrue(all(p["category"] == "fortune" for p in filtered))

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_filter_by_date(self, mock_dir, mock_file):
        """Export should filter by since date."""
        from app import filter_history
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            history = [
                {"prediction": "Old", "category": "fortune", "generated_at": "2024-01-01T12:00:00"},
                {"prediction": "New", "category": "career", "generated_at": "2025-06-01T12:00:00"},
            ]
            
            filtered = filter_history(history, since="2025-01-01")
            
            self.assertEqual(len(filtered), 1)
            self.assertEqual(filtered[0]["prediction"], "New")


class TestPredictTheFutureIteration4(unittest.TestCase):
    """Tests for predict_the_future with Iteration 4 features."""

    def test_time_aware_adds_time_context(self):
        """Time-aware prediction should include time_of_day and day_type."""
        result = predict_the_future(time_aware=True)
        
        self.assertIn("time_of_day", result)
        self.assertIn("day_type", result)
        self.assertIn(result["time_of_day"], ["morning", "afternoon", "evening", "night"])
        self.assertIn(result["day_type"], ["weekday", "weekend"])

    def test_regular_prediction_no_time_context(self):
        """Regular prediction should not include time context."""
        result = predict_the_future(time_aware=False)
        
        self.assertNotIn("time_of_day", result)
        self.assertNotIn("day_type", result)


# Iteration 5 Tests
class TestSmartMode(unittest.TestCase):
    """Tests for smart mode functionality."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        # shutil already imported at top
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_smart_prediction_returns_tuple(self):
        """Smart prediction should return a tuple."""
        from app import get_smart_prediction
        result = get_smart_prediction()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_smart_prediction_with_category(self):
        """Smart prediction with category should return that category."""
        from app import get_smart_prediction
        prediction, category = get_smart_prediction("fortune")
        self.assertEqual(category, "fortune")

    def test_smart_mode_adds_time_context(self):
        """Smart mode should include time_of_day and day_type."""
        result = predict_the_future(smart=True)
        
        self.assertIn("time_of_day", result)
        self.assertIn("day_type", result)
        self.assertIn(result["time_of_day"], ["morning", "afternoon", "evening", "night"])
        self.assertIn(result["day_type"], ["weekday", "weekend"])

    @patch("app.HISTORY_FILE")
    @patch("app.HISTORY_DIR")
    def test_smart_mode_with_preferences(self, mock_dir, mock_file):
        """Smart mode should work with user preferences."""
        from app import get_smart_prediction
        temp_file = Path(self.temp_dir) / "history.json"
        
        with patch("app.HISTORY_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            # Create history with ratings
            history = [
                {"prediction": "Test 1", "category": "fortune", "rating": 5},
            ]
            with open(temp_file, "w") as f:
                json.dump(history, f)
            
            # Should still work without errors
            result = get_smart_prediction()
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)


class TestSocialSharing(unittest.TestCase):
    """Tests for social sharing functionality."""

    def test_format_for_sharing_text(self):
        """Text format should include prediction and metadata."""
        from app import format_for_sharing
        prediction = {
            "prediction": "Test prediction",
            "category": "fortune",
            "applies_to": "Monday, January 1, 2025",
            "confidence": "85%",
        }
        result = format_for_sharing(prediction, "text")
        
        self.assertIn("Test prediction", result)
        self.assertIn("Fortune", result)
        self.assertIn("85%", result)
        self.assertIn("The Future Predictor", result)

    def test_format_for_sharing_twitter(self):
        """Twitter format should be concise with hashtags."""
        from app import format_for_sharing
        prediction = {
            "prediction": "Test prediction",
            "category": "fortune",
            "applies_to": "Monday, January 1, 2025",
            "confidence": "85%",
        }
        result = format_for_sharing(prediction, "twitter")
        
        self.assertIn("Test prediction", result)
        self.assertIn("#Fortune", result)
        self.assertIn("#TheFuturePredictor", result)
        # Twitter format should be shorter
        self.assertLess(len(result), 280)  # Twitter character limit

    def test_format_for_sharing_markdown(self):
        """Markdown format should include proper markdown syntax."""
        from app import format_for_sharing
        prediction = {
            "prediction": "Test prediction",
            "category": "fortune",
            "applies_to": "Monday, January 1, 2025",
            "confidence": "85%",
        }
        result = format_for_sharing(prediction, "markdown")
        
        self.assertIn("##", result)  # Header
        self.assertIn(">", result)   # Blockquote
        self.assertIn("**", result)  # Bold
        self.assertIn("Test prediction", result)

    def test_format_for_sharing_default(self):
        """Default format should be text."""
        from app import format_for_sharing
        prediction = {
            "prediction": "Test prediction",
            "category": "fortune",
            "applies_to": "Monday, January 1, 2025",
            "confidence": "85%",
        }
        result_default = format_for_sharing(prediction)
        result_text = format_for_sharing(prediction, "text")
        
        self.assertEqual(result_default, result_text)


# Iteration 6 Tests
class TestThemes(unittest.TestCase):
    """Tests for prediction themes functionality."""

    def test_themes_exist(self):
        """All expected themes should exist."""
        from app import THEMES
        expected_themes = ["motivational", "holiday", "spooky", "adventure"]
        for theme in expected_themes:
            self.assertIn(theme, THEMES)
            self.assertGreater(len(THEMES[theme]), 0)

    def test_themed_prediction_returns_tuple(self):
        """Themed prediction should return a tuple."""
        from app import get_themed_prediction
        result = get_themed_prediction("motivational")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    def test_themed_prediction_with_category(self):
        """Themed prediction with category should return that category."""
        from app import get_themed_prediction, THEMES
        # Test with a category that exists in the theme
        prediction, category = get_themed_prediction("motivational", "fortune")
        self.assertEqual(category, "fortune")
        self.assertIn(prediction, THEMES["motivational"]["fortune"])

    def test_themed_prediction_invalid_theme(self):
        """Invalid theme should return error message."""
        from app import get_themed_prediction
        prediction, category = get_themed_prediction("nonexistent")
        self.assertIn("Unknown theme", prediction)
        self.assertEqual(category, "nonexistent")

    def test_themed_prediction_invalid_category_for_theme(self):
        """Invalid category for theme should return error message."""
        from app import get_themed_prediction
        # "weather" exists in spooky but not in motivational
        prediction, category = get_themed_prediction("motivational", "weather")
        self.assertIn("not available", prediction)

    def test_predict_the_future_with_theme(self):
        """predict_the_future should work with theme parameter."""
        from app import predict_the_future
        result = predict_the_future(theme="adventure")
        
        self.assertIn("theme", result)
        self.assertEqual(result["theme"], "adventure")
        self.assertIn("prediction", result)
        self.assertIn("category", result)

    def test_predict_the_future_theme_with_category(self):
        """predict_the_future should work with theme and category."""
        from app import predict_the_future, THEMES
        result = predict_the_future(theme="holiday", category="relationship")
        
        self.assertEqual(result["theme"], "holiday")
        self.assertEqual(result["category"], "relationship")
        self.assertIn(result["prediction"], THEMES["holiday"]["relationship"])


class TestCopyToClipboard(unittest.TestCase):
    """Tests for copy to clipboard functionality."""

    def test_copy_to_clipboard_returns_bool(self):
        """copy_to_clipboard should return a boolean."""
        from app import copy_to_clipboard
        result = copy_to_clipboard("test text")
        self.assertIsInstance(result, bool)

    def test_copy_to_clipboard_handles_unicode(self):
        """copy_to_clipboard should handle unicode text."""
        from app import copy_to_clipboard
        # Should not raise an exception
        result = copy_to_clipboard("🔮 Test prediction with emojis 🌟")
        self.assertIsInstance(result, bool)


# Iteration 7 Tests
class TestSeasonalThemes(unittest.TestCase):
    """Tests for seasonal prediction themes (Iteration 7)."""

    def test_seasonal_themes_exist(self):
        """Seasonal themes should exist in THEMES."""
        from app import THEMES
        seasonal_themes = ["spring", "summer", "fall", "winter"]
        for theme in seasonal_themes:
            self.assertIn(theme, THEMES)
            self.assertGreater(len(THEMES[theme]), 0)

    def test_spring_theme_categories(self):
        """Spring theme should have expected categories."""
        from app import THEMES
        expected_categories = ["fortune", "health", "relationship"]
        for category in expected_categories:
            self.assertIn(category, THEMES["spring"])
            self.assertGreater(len(THEMES["spring"][category]), 0)

    def test_summer_theme_categories(self):
        """Summer theme should have expected categories."""
        from app import THEMES
        expected_categories = ["fortune", "activity", "relationship"]
        for category in expected_categories:
            self.assertIn(category, THEMES["summer"])
            self.assertGreater(len(THEMES["summer"][category]), 0)

    def test_fall_theme_categories(self):
        """Fall theme should have expected categories."""
        from app import THEMES
        expected_categories = ["fortune", "creative", "career"]
        for category in expected_categories:
            self.assertIn(category, THEMES["fall"])
            self.assertGreater(len(THEMES["fall"][category]), 0)

    def test_winter_theme_categories(self):
        """Winter theme should have expected categories."""
        from app import THEMES
        expected_categories = ["fortune", "health", "relationship"]
        for category in expected_categories:
            self.assertIn(category, THEMES["winter"])
            self.assertGreater(len(THEMES["winter"][category]), 0)

    def test_predict_with_seasonal_theme(self):
        """predict_the_future should work with seasonal themes."""
        from app import predict_the_future
        for theme in ["spring", "summer", "fall", "winter"]:
            result = predict_the_future(theme=theme)
            self.assertEqual(result["theme"], theme)
            self.assertIn("prediction", result)
            self.assertIn("category", result)


class TestZodiacTheme(unittest.TestCase):
    """Tests for zodiac prediction theme (Iteration 7)."""

    def test_zodiac_theme_exists(self):
        """Zodiac theme should exist in THEMES."""
        from app import THEMES
        self.assertIn("zodiac", THEMES)

    def test_zodiac_signs_exist(self):
        """All 12 zodiac signs should be in zodiac theme."""
        from app import THEMES
        zodiac_signs = [
            "aries", "taurus", "gemini", "cancer",
            "leo", "virgo", "libra", "scorpio",
            "sagittarius", "capricorn", "aquarius", "pisces"
        ]
        for sign in zodiac_signs:
            self.assertIn(sign, THEMES["zodiac"])
            self.assertGreater(len(THEMES["zodiac"][sign]), 0)

    def test_predict_with_zodiac_theme(self):
        """predict_the_future should work with zodiac theme."""
        from app import predict_the_future
        result = predict_the_future(theme="zodiac")
        self.assertEqual(result["theme"], "zodiac")
        self.assertIn("prediction", result)
        self.assertIn("category", result)

    def test_zodiac_with_specific_sign(self):
        """Zodiac theme should work with specific zodiac sign."""
        from app import get_themed_prediction, THEMES
        prediction, category = get_themed_prediction("zodiac", "leo")
        self.assertEqual(category, "leo")
        self.assertIn(prediction, THEMES["zodiac"]["leo"])


class TestAPI(unittest.TestCase):
    """Tests for REST API functionality (Iteration 7)."""

    def test_create_api_returns_fastapi_app(self):
        """create_api should return a FastAPI application."""
        from app import create_api
        try:
            from fastapi import FastAPI
            api = create_api()
            self.assertIsInstance(api, FastAPI)
        except ImportError:
            self.skipTest("FastAPI not installed")

    def test_api_has_predict_endpoint(self):
        """API should have /predict endpoint."""
        from app import create_api
        try:
            api = create_api()
            routes = [route.path for route in api.routes]
            self.assertIn("/predict", routes)
        except ImportError:
            self.skipTest("FastAPI not installed")

    def test_api_has_themes_endpoint(self):
        """API should have /themes endpoint."""
        from app import create_api
        try:
            api = create_api()
            routes = [route.path for route in api.routes]
            self.assertIn("/themes", routes)
        except ImportError:
            self.skipTest("FastAPI not installed")

    def test_api_has_categories_endpoint(self):
        """API should have /categories endpoint."""
        from app import create_api
        try:
            api = create_api()
            routes = [route.path for route in api.routes]
            self.assertIn("/categories", routes)
        except ImportError:
            self.skipTest("FastAPI not installed")

    def test_api_has_history_endpoint(self):
        """API should have /history endpoint."""
        from app import create_api
        try:
            api = create_api()
            routes = [route.path for route in api.routes]
            self.assertIn("/history", routes)
        except ImportError:
            self.skipTest("FastAPI not installed")

    def test_api_has_stats_endpoint(self):
        """API should have /stats endpoint."""
        from app import create_api
        try:
            api = create_api()
            routes = [route.path for route in api.routes]
            self.assertIn("/stats", routes)
        except ImportError:
            self.skipTest("FastAPI not installed")


# Iteration 8 Tests
class TestReminders(unittest.TestCase):
    """Tests for prediction reminders functionality (Iteration 8)."""

    def setUp(self):
        """Set up a temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary files."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_load_empty_reminders(self, mock_dir, mock_file):
        """Loading reminders from non-existent file returns empty list."""
        mock_file.exists.return_value = False
        result = load_reminders()
        self.assertEqual(result, [])

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_save_and_load_reminder(self, mock_dir, mock_file):
        """Saving and loading reminders should work."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            prediction = {
                "id": 1,
                "prediction": "Test prediction",
                "category": "fortune",
                "applies_to": "Monday, January 20, 2025",
            }
            reminder = save_reminder(prediction)
            
            self.assertIn("reminder_id", reminder)
            self.assertEqual(reminder["reminder_id"], 1)
            self.assertEqual(reminder["prediction"], "Test prediction")
            self.assertIn("remind_date", reminder)
            
            reminders = load_reminders()
            self.assertEqual(len(reminders), 1)

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_save_reminder_with_custom_date(self, mock_dir, mock_file):
        """Saving reminder with custom date should work."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            prediction = {
                "id": 1,
                "prediction": "Test prediction",
                "category": "fortune",
                "applies_to": "Monday, January 20, 2025",
            }
            reminder = save_reminder(prediction, "2025-12-25")
            
            self.assertEqual(reminder["remind_date"], "2025-12-25")

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_sequential_reminder_ids(self, mock_dir, mock_file):
        """Multiple reminders should have sequential IDs."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            for i in range(3):
                prediction = {
                    "id": i + 1,
                    "prediction": f"Test {i}",
                    "category": "test",
                    "applies_to": "Monday, January 20, 2025",
                }
                save_reminder(prediction)
            
            reminders = load_reminders()
            self.assertEqual(len(reminders), 3)
            self.assertEqual(reminders[0]["reminder_id"], 1)
            self.assertEqual(reminders[1]["reminder_id"], 2)
            self.assertEqual(reminders[2]["reminder_id"], 3)

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_get_pending_reminders(self, mock_dir, mock_file):
        """Getting pending reminders should work."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            # Create reminders: one past, one future
            reminders = [
                {
                    "reminder_id": 1,
                    "prediction": "Past reminder",
                    "category": "test",
                    "remind_date": "2020-01-01",
                    "acknowledged": False,
                },
                {
                    "reminder_id": 2,
                    "prediction": "Future reminder",
                    "category": "test",
                    "remind_date": "2099-01-01",
                    "acknowledged": False,
                },
            ]
            with open(temp_file, "w") as f:
                json.dump(reminders, f)
            
            pending = get_pending_reminders()
            
            # Only the past reminder should be pending
            self.assertEqual(len(pending), 1)
            self.assertEqual(pending[0]["reminder_id"], 1)

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_acknowledge_reminder(self, mock_dir, mock_file):
        """Acknowledging a reminder should work."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            prediction = {
                "id": 1,
                "prediction": "Test prediction",
                "category": "fortune",
                "applies_to": "Monday, January 20, 2025",
            }
            save_reminder(prediction)
            
            result = acknowledge_reminder(1)
            self.assertTrue(result)
            
            reminders = load_reminders()
            self.assertTrue(reminders[0]["acknowledged"])
            self.assertIn("acknowledged_at", reminders[0])

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_acknowledge_nonexistent_reminder(self, mock_dir, mock_file):
        """Acknowledging non-existent reminder should fail."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            result = acknowledge_reminder(999)
            self.assertFalse(result)

    @patch("app.REMINDERS_FILE")
    @patch("app.HISTORY_DIR")
    def test_acknowledged_reminders_not_pending(self, mock_dir, mock_file):
        """Acknowledged reminders should not appear in pending."""
        temp_file = Path(self.temp_dir) / "reminders.json"
        
        with patch("app.REMINDERS_FILE", temp_file), \
             patch("app.HISTORY_DIR", Path(self.temp_dir)):
            reminders = [
                {
                    "reminder_id": 1,
                    "prediction": "Acknowledged reminder",
                    "category": "test",
                    "remind_date": "2020-01-01",
                    "acknowledged": True,
                },
            ]
            with open(temp_file, "w") as f:
                json.dump(reminders, f)
            
            pending = get_pending_reminders()
            self.assertEqual(len(pending), 0)


if __name__ == "__main__":
    unittest.main()
