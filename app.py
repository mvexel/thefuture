#!/usr/bin/env python
"""
The Future Predictor - Iteration 1

A playful prediction system that generates fortunes and predictions.
This is the first iteration of the self-improving prediction engine.
"""

import random
from datetime import datetime, timedelta


# Prediction templates by category
PREDICTIONS = {
    "fortune": [
        "You will find unexpected joy in a small moment today.",
        "A challenge you face will lead to personal growth.",
        "Someone will appreciate your kindness more than you know.",
        "An opportunity is closer than you think.",
        "Your patience will be rewarded soon.",
        "A creative idea will strike you at an unusual time.",
        "Trust your instincts on an important decision.",
        "A friendship will deepen in an unexpected way.",
    ],
    "weather": [
        "Expect sunshine in your mood, regardless of the clouds.",
        "A storm of ideas will clear the air for new thinking.",
        "Calm winds ahead will bring peace of mind.",
        "Rainbows of opportunity await after any brief troubles.",
    ],
    "activity": [
        "Today is a good day to start something new.",
        "Take a moment to appreciate what you have accomplished.",
        "Reach out to someone you haven't spoken to in a while.",
        "Learn something small but interesting today.",
        "Share your knowledge with someone who could benefit.",
    ],
}


def get_prediction(category: str = None) -> tuple[str, str]:
    """
    Generate a prediction for the future.
    
    Args:
        category: Optional category ('fortune', 'weather', 'activity').
                  If None, a random category is chosen.
    
    Returns:
        A tuple of (prediction string, category used).
    """
    if category is None:
        category = random.choice(list(PREDICTIONS.keys()))
    
    if category not in PREDICTIONS:
        available = ", ".join(PREDICTIONS.keys())
        return f"Unknown category '{category}'. Available: {available}", category
    
    return random.choice(PREDICTIONS[category]), category


def get_future_date(days_ahead: int = 1) -> str:
    """
    Get a formatted date in the future.
    
    Args:
        days_ahead: Number of days in the future.
    
    Returns:
        Formatted date string.
    """
    future = datetime.now() + timedelta(days=days_ahead)
    return future.strftime("%A, %B %d, %Y")


def predict_the_future(category: str = None) -> dict:
    """
    Generate a complete future prediction.
    
    Args:
        category: Optional prediction category.
    
    Returns:
        Dictionary with prediction details.
    """
    prediction, used_category = get_prediction(category)
    future_date = get_future_date(random.randint(1, 7))
    
    return {
        "prediction": prediction,
        "applies_to": future_date,
        "category": used_category,
        "confidence": f"{random.randint(70, 99)}%",
    }


def main():
    """Main entry point for the future predictor."""
    print("=" * 50)
    print("  🔮 THE FUTURE PREDICTOR - Iteration 1 🔮")
    print("=" * 50)
    print()
    
    result = predict_the_future()
    
    print(f"Category: {result['category'].title()}")
    print(f"Applies to: {result['applies_to']}")
    print(f"Confidence: {result['confidence']}")
    print()
    print(f"🌟 {result['prediction']}")
    print()
    print("-" * 50)
    print("Future iterations will add more features!")
    print("See AGENTS.md for improvement ideas.")


if __name__ == "__main__":
    main()
