#!/usr/bin/env python
"""Tests for the Future Predictor app."""

import unittest
from datetime import datetime, timedelta

from app import get_prediction, get_future_date, predict_the_future, PREDICTIONS


class TestGetPrediction(unittest.TestCase):
    """Tests for the get_prediction function."""

    def test_returns_string(self):
        """Prediction should be a string."""
        result = get_prediction()
        self.assertIsInstance(result, str)

    def test_valid_category(self):
        """Prediction from valid category should be in that category's list."""
        for category in PREDICTIONS.keys():
            result = get_prediction(category)
            self.assertIn(result, PREDICTIONS[category])

    def test_invalid_category(self):
        """Invalid category should return error message."""
        result = get_prediction("nonexistent")
        self.assertIn("Unknown category", result)

    def test_none_category_returns_valid_prediction(self):
        """None category should return a valid prediction from any category."""
        result = get_prediction(None)
        all_predictions = []
        for predictions in PREDICTIONS.values():
            all_predictions.extend(predictions)
        self.assertIn(result, all_predictions)


class TestGetFutureDate(unittest.TestCase):
    """Tests for the get_future_date function."""

    def test_returns_string(self):
        """Future date should be a string."""
        result = get_future_date()
        self.assertIsInstance(result, str)

    def test_default_one_day_ahead(self):
        """Default should be one day ahead."""
        expected = (datetime.now() + timedelta(days=1)).strftime("%A, %B %d, %Y")
        result = get_future_date()
        self.assertEqual(result, expected)

    def test_custom_days_ahead(self):
        """Custom days should work correctly."""
        expected = (datetime.now() + timedelta(days=7)).strftime("%A, %B %d, %Y")
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


if __name__ == "__main__":
    unittest.main()
