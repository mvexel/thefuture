#!/usr/bin/env python
"""Tests for the Future Predictor app."""

import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

from app import get_prediction, get_future_date, predict_the_future, PREDICTIONS


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


if __name__ == "__main__":
    unittest.main()
