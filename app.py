#!/usr/bin/env python
"""
The Future Predictor - Iteration 2

A playful prediction system that generates fortunes and predictions.
This iteration adds CLI arguments, prediction history, and more categories.
"""

import argparse
import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path


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
    "career": [
        "A professional breakthrough is on the horizon.",
        "Your hard work will soon be recognized by others.",
        "A new skill you learn will open unexpected doors.",
        "Collaboration will bring better results than going alone.",
        "Trust your professional instincts on an upcoming decision.",
    ],
    "relationship": [
        "A meaningful conversation will strengthen a bond.",
        "Someone new will bring positive energy into your life.",
        "Patience with a loved one will pay off beautifully.",
        "An old connection may resurface with good news.",
        "Your empathy will make a real difference to someone.",
    ],
    "health": [
        "A small change in routine will boost your energy.",
        "Listen to your body's needs today.",
        "Rest will bring more clarity than pushing harder.",
        "A mindful moment will improve your whole day.",
        "Movement, however small, will lift your spirits.",
    ],
    "creative": [
        "Inspiration will strike when you least expect it.",
        "A project you've been pondering will finally click.",
        "Embrace imperfection—it leads to discovery.",
        "Collaboration will spark new creative ideas.",
        "Your unique perspective is exactly what's needed.",
    ],
}

# History file location
HISTORY_DIR = Path.home() / ".thefuture"
HISTORY_FILE = HISTORY_DIR / "history.json"


def get_prediction(category: str = None) -> tuple[str, str]:
    """
    Generate a prediction for the future.
    
    Args:
        category: Optional category. Available categories are:
                  fortune, weather, activity, career, relationship, health, creative.
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
        "generated_at": datetime.now().isoformat(),
    }


def load_history() -> list:
    """
    Load prediction history from file.
    
    Returns:
        List of past predictions.
    """
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_to_history(prediction: dict) -> None:
    """
    Save a prediction to history file.
    
    Args:
        prediction: The prediction dictionary to save.
    """
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    
    history = load_history()
    history.append(prediction)
    
    # Keep only the last 100 predictions
    history = history[-100:]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def display_history(count: int = 10) -> None:
    """
    Display recent prediction history.
    
    Args:
        count: Number of recent predictions to display.
    """
    history = load_history()
    
    if not history:
        print("No prediction history found.")
        return
    
    recent = history[-count:]
    print(f"\n📜 Last {len(recent)} prediction(s):\n")
    
    for i, pred in enumerate(reversed(recent), 1):
        print(f"{i}. [{pred.get('category', 'unknown').title()}] {pred['prediction']}")
        if "generated_at" in pred:
            # Parse and format the timestamp
            try:
                dt = datetime.fromisoformat(pred["generated_at"])
                print(f"   Generated: {dt.strftime('%Y-%m-%d %H:%M')}")
            except (ValueError, TypeError):
                pass
        print()


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="🔮 The Future Predictor - Generate predictions for your future!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py                      # Random prediction
  python app.py --category fortune   # Fortune prediction
  python app.py --count 3            # Three predictions
  python app.py --json               # JSON output
  python app.py --history            # View past predictions
        """,
    )
    
    parser.add_argument(
        "--category", "-c",
        choices=list(PREDICTIONS.keys()),
        help="Category of prediction",
    )

    def positive_int(value):
        """Validate that count is a positive integer."""
        ivalue = int(value)
        if ivalue < 1:
            raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
        if ivalue > 100:
            raise argparse.ArgumentTypeError(f"{value} exceeds maximum of 100")
        return ivalue

    parser.add_argument(
        "--count", "-n",
        type=positive_int,
        default=1,
        help="Number of predictions to generate (default: 1, max: 100)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Only output the prediction text",
    )
    parser.add_argument(
        "--history",
        action="store_true",
        help="Show recent prediction history",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save prediction to history",
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the future predictor."""
    args = parse_args()
    
    # Handle history display
    if args.history:
        display_history()
        return
    
    predictions = []
    for _ in range(args.count):
        result = predict_the_future(args.category)
        predictions.append(result)
        
        if not args.no_save:
            save_to_history(result)
    
    # JSON output
    if args.json:
        output = predictions if len(predictions) > 1 else predictions[0]
        print(json.dumps(output, indent=2))
        return
    
    # Quiet output
    if args.quiet:
        for pred in predictions:
            print(pred["prediction"])
        return
    
    # Standard formatted output
    print("=" * 50)
    print("  🔮 THE FUTURE PREDICTOR - Iteration 2 🔮")
    print("=" * 50)
    
    for i, result in enumerate(predictions, 1):
        if len(predictions) > 1:
            print(f"\n--- Prediction {i} ---")
        print()
        print(f"Category: {result['category'].title()}")
        print(f"Applies to: {result['applies_to']}")
        print(f"Confidence: {result['confidence']}")
        print()
        print(f"🌟 {result['prediction']}")
    
    print()
    print("-" * 50)
    print("Use --help to see available options.")
    print("Use --history to view past predictions.")


if __name__ == "__main__":
    main()
