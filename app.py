#!/usr/bin/env python
"""
The Future Predictor - Iteration 10

A playful prediction system that generates fortunes and predictions.
This iteration adds a web frontend and enhanced API endpoints.
"""

import argparse
import csv
import json
import os
import random
import re
import sys
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path


# Time-of-day specific predictions
TIME_PREDICTIONS = {
    "morning": [
        "Your morning energy will set a positive tone for the day.",
        "An early start brings unexpected clarity.",
        "A morning routine change will boost your productivity.",
        "Breakfast with a twist will spark joy.",
        "The sunrise brings new possibilities.",
    ],
    "afternoon": [
        "The afternoon sun will bring clarity to a problem.",
        "A midday break will reveal a new perspective.",
        "Lunch will lead to an unexpected connection.",
        "Your afternoon focus will yield great results.",
        "An afternoon walk will inspire creativity.",
    ],
    "evening": [
        "The evening will bring relaxation and reflection.",
        "A cozy evening awaits with pleasant surprises.",
        "Evening conversations will deepen understanding.",
        "Sunset thoughts will guide tomorrow's decisions.",
        "The evening wind brings answers you seek.",
    ],
    "night": [
        "Night dreams will offer creative solutions.",
        "Late-night inspiration will strike unexpectedly.",
        "The quiet hours bring deep insights.",
        "Sleep will bring the clarity you need.",
        "Nighttime reflection reveals hidden truths.",
    ],
}

# Day-of-week specific predictions
DAY_PREDICTIONS = {
    "weekday": [
        "Your workweek productivity will reach new heights.",
        "A colleague will offer valuable help today.",
        "A weekday challenge will become a learning opportunity.",
        "Professional connections will strengthen this week.",
        "Your weekday efforts will be recognized.",
    ],
    "weekend": [
        "The weekend brings time for what matters most.",
        "Rest and recreation will recharge your spirit.",
        "Weekend adventures await around the corner.",
        "Quality time with loved ones brings joy.",
        "A leisurely pace reveals new perspectives.",
    ],
}

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

# Themed predictions - special prediction sets for different occasions
THEMES = {
    "motivational": {
        "fortune": [
            "Your potential is limitless—today is proof of that.",
            "Every step forward, no matter how small, is progress.",
            "You have the strength to overcome any challenge.",
            "Believe in yourself—others already do.",
            "Your persistence will lead to breakthrough success.",
        ],
        "career": [
            "Your dedication will open doors you never imagined.",
            "A mentor will recognize your unique talents soon.",
            "Your next big opportunity is just around the corner.",
            "Leadership qualities are emerging in you—embrace them.",
            "Your work ethic inspires those around you.",
        ],
        "health": [
            "Every healthy choice builds a stronger you.",
            "Your body is capable of amazing things—trust it.",
            "Small consistent habits create lasting transformation.",
            "You deserve to feel your best—make it happen.",
            "Energy follows intention—set yours high.",
        ],
        "creative": [
            "Your creativity knows no bounds—let it flow.",
            "The world needs your unique vision—share it.",
            "Every creation starts with a single inspired thought.",
            "Your artistic voice is valuable and worth hearing.",
            "Innovation comes naturally to those who dare to try.",
        ],
    },
    "holiday": {
        "fortune": [
            "The holiday season will bring unexpected joy and warmth.",
            "A gathering will create memories to last a lifetime.",
            "Generosity given will return to you tenfold.",
            "The spirit of the season will touch your heart.",
            "A meaningful gift will come from an unexpected source.",
        ],
        "relationship": [
            "Reconnecting with loved ones will bring deep happiness.",
            "A holiday tradition will gain new special meaning.",
            "Shared laughter will strengthen family bonds.",
            "Someone will express gratitude that warms your heart.",
            "New connections made this season will become lasting.",
        ],
        "activity": [
            "Volunteering will bring more joy than expected.",
            "A holiday recipe will become a new favorite.",
            "Decorating will spark childhood memories and smiles.",
            "A seasonal outing will create wonderful stories.",
            "Gift-giving will reveal your thoughtful nature.",
        ],
    },
    "spooky": {
        "fortune": [
            "A mysterious stranger will bring intriguing news.",
            "The shadows hold secrets waiting to be discovered.",
            "An eerie coincidence will lead to good fortune.",
            "Trust your instincts when things feel supernatural.",
            "What lurks in the unknown may surprise you pleasantly.",
        ],
        "creative": [
            "Dark inspiration will fuel your most creative work.",
            "A haunting melody will linger in your imagination.",
            "Embrace the strange—it leads to unique creations.",
            "Your spooky ideas will captivate others.",
            "The mysterious calls to your artistic soul.",
        ],
        "weather": [
            "Foggy mornings will bring moments of reflection.",
            "A stormy night will clear the air for fresh starts.",
            "The chill in the air awakens dormant ambitions.",
            "Moonlit evenings will inspire deep thoughts.",
            "Shadows dancing in candlelight will spark ideas.",
        ],
    },
    "adventure": {
        "fortune": [
            "An unexpected journey will change your perspective.",
            "Adventure awaits those who dare to step outside.",
            "A risk taken will lead to exciting discoveries.",
            "New horizons call to your adventurous spirit.",
            "The path less traveled will reward you greatly.",
        ],
        "activity": [
            "Try something you've never done before—today.",
            "Explore a new place, even if it's just nearby.",
            "Say yes to spontaneous opportunities.",
            "Break your routine and discover new favorites.",
            "Challenge yourself physically—you'll be amazed.",
        ],
        "health": [
            "An outdoor adventure will rejuvenate your spirit.",
            "Physical challenges will reveal hidden strength.",
            "Nature has healing powers waiting for you.",
            "Movement in new environments boosts mental clarity.",
            "Active exploration leads to lasting vitality.",
        ],
        "relationship": [
            "Shared adventures create the strongest bonds.",
            "A travel companion will become a lifelong friend.",
            "New experiences together deepen connections.",
            "Someone will join you on an unexpected journey.",
            "Adventures bring out the best in relationships.",
        ],
    },
    "spring": {
        "fortune": [
            "New beginnings are blooming all around you.",
            "Fresh energy will carry you to new heights.",
            "Growth is happening, even when you can't see it yet.",
            "Spring rain washes away what no longer serves you.",
            "A season of renewal awaits with open arms.",
        ],
        "health": [
            "Your energy levels will rise with the lengthening days.",
            "Outdoor activities will invigorate your spirit.",
            "Spring cleaning extends to mind, body, and soul.",
            "Fresh air and sunshine will boost your wellbeing.",
            "Seasonal fruits will nourish your body perfectly.",
        ],
        "relationship": [
            "New connections will blossom unexpectedly.",
            "Existing relationships will be refreshed and renewed.",
            "Love is in the air this season.",
            "A spring fling may lead to something lasting.",
            "Outdoor gatherings will strengthen social bonds.",
        ],
    },
    "summer": {
        "fortune": [
            "Warmth and abundance are heading your way.",
            "Long days will bring extended opportunities.",
            "Summer adventures will create lasting memories.",
            "The sun will shine on your endeavors.",
            "A carefree moment will bring unexpected insight.",
        ],
        "activity": [
            "Beach days will reset your perspective.",
            "A summer trip will exceed expectations.",
            "Outdoor concerts and events will bring joy.",
            "Water activities will be particularly refreshing.",
            "Late sunsets will inspire evening adventures.",
        ],
        "relationship": [
            "Summer gatherings will deepen friendships.",
            "Vacation time together will strengthen bonds.",
            "Warm weather invites warm conversations.",
            "A summer romance may blossom beautifully.",
            "Outdoor celebrations will create shared memories.",
        ],
    },
    "fall": {
        "fortune": [
            "A harvest of your efforts is approaching.",
            "Transformation is in the air—embrace change.",
            "Cozy moments will bring comfort and clarity.",
            "The changing leaves remind us of beautiful transitions.",
            "Preparation now leads to winter abundance.",
        ],
        "creative": [
            "Autumn colors will inspire your creative work.",
            "The crisp air will sharpen your focus.",
            "Reflection time will yield creative breakthroughs.",
            "Cozy indoor projects will flourish.",
            "Harvest themes will enhance your artistry.",
        ],
        "career": [
            "Fall momentum will accelerate your projects.",
            "New initiatives will take root beautifully.",
            "The busy season brings recognition opportunities.",
            "Strategic planning now pays off later.",
            "Professional harvest time is approaching.",
        ],
    },
    "winter": {
        "fortune": [
            "Warmth awaits in unexpected places.",
            "The quiet season brings inner wisdom.",
            "Winter's stillness reveals hidden truths.",
            "Rest now prepares you for spring's renewal.",
            "Even in darkness, light is always returning.",
        ],
        "health": [
            "Cozy self-care will restore your energy.",
            "Winter rest is essential for spring vitality.",
            "Warm foods will nourish body and soul.",
            "Indoor exercise will maintain your momentum.",
            "Hibernation mode brings necessary restoration.",
        ],
        "relationship": [
            "Cozy gatherings will strengthen bonds.",
            "Winter warmth is shared warmth.",
            "Holiday traditions will create lasting memories.",
            "Indoor time together deepens connections.",
            "Cold weather brings people closer together.",
        ],
    },
    "zodiac": {
        "aries": [
            "Your bold energy will open new doors.",
            "Leadership opportunities await your fiery spirit.",
            "Your courage will inspire those around you.",
            "Action taken today leads to victory tomorrow.",
            "Your pioneering spirit will blaze new trails.",
        ],
        "taurus": [
            "Patience will bring the rewards you seek.",
            "Your steady approach will lead to lasting success.",
            "Comfort and abundance are aligning for you.",
            "Trust your practical instincts—they are sound.",
            "Financial stability is within your reach.",
        ],
        "gemini": [
            "Communication will be your superpower.",
            "New ideas will flow effortlessly to you.",
            "Social connections will bring exciting opportunities.",
            "Your adaptability will serve you well.",
            "Curiosity will lead to wonderful discoveries.",
        ],
        "cancer": [
            "Home and family will bring deep fulfillment.",
            "Your intuition is especially strong right now.",
            "Nurturing others will nurture your soul.",
            "Emotional connections will deepen beautifully.",
            "Trust your feelings—they guide you wisely.",
        ],
        "leo": [
            "Your creativity will shine brightly for all to see.",
            "Recognition and appreciation are coming your way.",
            "Your generosity will return to you magnified.",
            "Leadership roles will suit you perfectly.",
            "Express yourself boldly—the world is watching.",
        ],
        "virgo": [
            "Attention to detail will bring major rewards.",
            "Your analytical skills will solve an important problem.",
            "Health improvements will boost your energy.",
            "Organization now leads to freedom later.",
            "Your helpful nature will be deeply appreciated.",
        ],
        "libra": [
            "Harmony and balance are aligning in your life.",
            "Partnership opportunities will prove beneficial.",
            "Your diplomacy will resolve a tricky situation.",
            "Beauty and art will inspire your path forward.",
            "Fairness you show will return to you.",
        ],
        "scorpio": [
            "Transformation and rebirth await you.",
            "Your intensity will achieve remarkable results.",
            "Hidden truths will be revealed in your favor.",
            "Passion will drive you to new heights.",
            "Trust your ability to navigate change.",
        ],
        "sagittarius": [
            "Adventure and exploration call to your spirit.",
            "Optimism will attract wonderful opportunities.",
            "Travel plans will exceed your expectations.",
            "Higher learning will open new doorways.",
            "Your philosophical insights will help others.",
        ],
        "capricorn": [
            "Your ambition will lead to significant achievement.",
            "Discipline and hard work will be rewarded.",
            "Long-term goals are closer than they appear.",
            "Authority and responsibility suit you well.",
            "Steady climbing leads to the summit.",
        ],
        "aquarius": [
            "Innovation and originality will set you apart.",
            "Humanitarian efforts will bring deep fulfillment.",
            "Your unique perspective will be valued.",
            "Technology will serve your goals beautifully.",
            "Independence brings you strength.",
        ],
        "pisces": [
            "Creativity and imagination will guide your way.",
            "Compassion shown to others will return tenfold.",
            "Dreams will bring important messages.",
            "Artistic expression will heal and inspire.",
            "Your sensitivity is a gift—honor it.",
        ],
    },
}

# History file location
HISTORY_DIR = Path.home() / ".thefuture"
HISTORY_FILE = HISTORY_DIR / "history.json"
REMINDERS_FILE = HISTORY_DIR / "reminders.json"
CUSTOM_THEMES_FILE = HISTORY_DIR / "themes.json"


# Custom theme functions (Iteration 9)

def load_custom_themes() -> dict:
    """
    Load custom themes from file.
    
    Returns:
        Dictionary of custom themes.
    """
    if not CUSTOM_THEMES_FILE.exists():
        return {}
    
    try:
        with open(CUSTOM_THEMES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_custom_themes(themes: dict) -> None:
    """
    Save custom themes to file.
    
    Args:
        themes: Dictionary of themes to save.
    """
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(CUSTOM_THEMES_FILE, "w") as f:
        json.dump(themes, f, indent=2)


def get_all_themes() -> dict:
    """
    Get all themes (built-in and custom).
    
    Returns:
        Dictionary combining built-in and custom themes.
    """
    all_themes = dict(THEMES)
    custom = load_custom_themes()
    all_themes.update(custom)
    return all_themes


def add_custom_theme(name: str, categories: dict) -> bool:
    """
    Add a new custom theme.
    
    Args:
        name: The theme name.
        categories: Dictionary of categories with prediction lists.
    
    Returns:
        True if successful, False otherwise.
    """
    if not name:
        print("Error: Theme name cannot be empty.")
        return False
    
    # Validate name (alphanumeric, underscores, and hyphens only)
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        print("Error: Theme name can only contain letters, numbers, underscores, and hyphens.")
        return False
    
    name = name.lower()
    
    # Check if it's a built-in theme
    if name in THEMES:
        print(f"Error: Cannot overwrite built-in theme '{name}'.")
        return False
    
    # Validate categories
    if not categories:
        print("Error: Theme must have at least one category with predictions.")
        return False
    
    for cat_name, predictions in categories.items():
        if not cat_name:
            print("Error: Category name cannot be empty.")
            return False
        if not predictions:
            print(f"Error: Category '{cat_name}' must have at least one prediction.")
            return False
        if not isinstance(predictions, list):
            print(f"Error: Predictions for category '{cat_name}' must be a list.")
            return False
        for pred in predictions:
            if not isinstance(pred, str) or not pred.strip():
                print(f"Error: All predictions in category '{cat_name}' must be non-empty strings.")
                return False
    
    custom_themes = load_custom_themes()
    
    if name in custom_themes:
        print(f"Note: Updating existing custom theme '{name}'.")
    
    custom_themes[name] = categories
    save_custom_themes(custom_themes)
    
    print(f"✅ Theme '{name}' saved successfully!")
    print(f"   Categories: {', '.join(categories.keys())}")
    total_predictions = sum(len(preds) for preds in categories.values())
    print(f"   Total predictions: {total_predictions}")
    print(f"\n   Use with: python app.py --theme {name}")
    
    return True


def delete_custom_theme(name: str) -> bool:
    """
    Delete a custom theme.
    
    Args:
        name: The theme name to delete.
    
    Returns:
        True if successful, False otherwise.
    """
    name = name.lower()
    
    if name in THEMES:
        print(f"Error: Cannot delete built-in theme '{name}'.")
        return False
    
    custom_themes = load_custom_themes()
    
    if name not in custom_themes:
        print(f"Error: Custom theme '{name}' not found.")
        available = list(custom_themes.keys())
        if available:
            print(f"Available custom themes: {', '.join(available)}")
        else:
            print("No custom themes exist. Use --add-theme to create one.")
        return False
    
    del custom_themes[name]
    save_custom_themes(custom_themes)
    
    print(f"✅ Custom theme '{name}' deleted successfully!")
    return True


def list_themes() -> None:
    """Display all available themes (built-in and custom)."""
    print("\n🎭 Available Themes\n")
    
    # Built-in themes
    print("📦 Built-in Themes:")
    for name in sorted(THEMES.keys()):
        categories = list(THEMES[name].keys())
        total = sum(len(preds) for preds in THEMES[name].values())
        print(f"   {name}: {', '.join(categories)} ({total} predictions)")
    
    # Custom themes
    custom = load_custom_themes()
    if custom:
        print("\n🎨 Custom Themes:")
        for name in sorted(custom.keys()):
            categories = list(custom[name].keys())
            total = sum(len(preds) for preds in custom[name].values())
            print(f"   {name}: {', '.join(categories)} ({total} predictions)")
    else:
        print("\n🎨 Custom Themes:")
        print("   No custom themes. Use --add-theme to create one.")
    
    print()


def interactive_add_theme() -> bool:
    """
    Interactively create a new custom theme.
    
    Returns:
        True if a theme was created, False otherwise.
    """
    print("\n🎨 Create Custom Theme\n")
    print("Follow the prompts to create your own prediction theme.")
    print("Press Ctrl+C to cancel at any time.\n")
    
    try:
        # Get theme name
        name = input("Theme name (e.g., 'birthday', 'work_life'): ").strip().lower()
        if not name:
            print("Cancelled: Theme name is required.")
            return False
        
        if name in THEMES:
            print(f"Error: '{name}' is a built-in theme and cannot be overwritten.")
            return False
        
        categories = {}
        
        print("\nNow add categories and predictions.")
        print("Enter an empty category name when done.\n")
        
        while True:
            cat_name = input("Category name (or press Enter to finish): ").strip().lower()
            if not cat_name:
                break
            
            predictions = []
            print(f"  Enter predictions for '{cat_name}' (empty line to finish category):")
            
            pred_num = 1
            while True:
                pred = input(f"    {pred_num}. ").strip()
                if not pred:
                    break
                predictions.append(pred)
                pred_num += 1
            
            if predictions:
                categories[cat_name] = predictions
                print(f"  ✓ Added {len(predictions)} prediction(s) to '{cat_name}'")
            else:
                print(f"  ⚠ Category '{cat_name}' skipped (no predictions)")
        
        if not categories:
            print("\nCancelled: No categories were created.")
            return False
        
        return add_custom_theme(name, categories)
        
    except (KeyboardInterrupt, EOFError):
        print("\n\nTheme creation cancelled.")
        return False


def import_theme_from_file(filepath: str) -> bool:
    """
    Import a custom theme from a JSON file.
    
    The JSON file should have the format:
    {
        "name": "theme_name",
        "categories": {
            "category1": ["prediction1", "prediction2", ...],
            "category2": ["prediction1", "prediction2", ...]
        }
    }
    
    Args:
        filepath: Path to the JSON file.
    
    Returns:
        True if successful, False otherwise.
    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{filepath}': {e}")
        return False
    except IOError as e:
        print(f"Error reading file '{filepath}': {e}")
        return False
    
    # Validate structure
    if not isinstance(data, dict):
        print("Error: JSON must be an object with 'name' and 'categories' fields.")
        return False
    
    name = data.get("name")
    categories = data.get("categories")
    
    if not name:
        print("Error: Theme 'name' field is required.")
        return False
    
    if not categories:
        print("Error: Theme 'categories' field is required.")
        return False
    
    return add_custom_theme(name, categories)


def export_theme_to_json(theme_name: str) -> bool:
    """
    Export a theme to JSON format.
    
    Args:
        theme_name: Name of the theme to export.
    
    Returns:
        True if successful, False otherwise.
    """
    theme_name = theme_name.lower()
    all_themes = get_all_themes()
    
    if theme_name not in all_themes:
        print(f"Error: Theme '{theme_name}' not found.")
        available = ", ".join(sorted(all_themes.keys()))
        print(f"Available themes: {available}")
        return False
    
    export_data = {
        "name": theme_name,
        "categories": all_themes[theme_name]
    }
    
    print(json.dumps(export_data, indent=2))
    return True


def get_themed_prediction(theme: str, category: str = None) -> tuple[str, str]:
    """
    Generate a prediction from a specific theme (built-in or custom).
    
    Args:
        theme: The theme to use (built-in or custom theme name).
        category: Optional category within the theme.
    
    Returns:
        A tuple of (prediction string, category used).
    """
    all_themes = get_all_themes()
    
    if theme not in all_themes:
        available = ", ".join(sorted(all_themes.keys()))
        return f"Unknown theme '{theme}'. Available: {available}", theme
    
    theme_predictions = all_themes[theme]
    
    if category is not None:
        if category not in theme_predictions:
            available = ", ".join(theme_predictions.keys())
            return f"Category '{category}' not available in theme '{theme}'. Available: {available}", category
        return random.choice(theme_predictions[category]), category
    
    # Random category from the theme
    category = random.choice(list(theme_predictions.keys()))
    return random.choice(theme_predictions[category]), category


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to the system clipboard.
    
    Uses multiple methods to ensure cross-platform compatibility:
    1. pyperclip (if installed)
    2. pbcopy (macOS)
    3. xclip/xsel (Linux)
    4. clip.exe (Windows/WSL)
    
    Args:
        text: The text to copy to clipboard.
    
    Returns:
        True if successful, False otherwise.
    """
    import subprocess
    import platform
    
    # Try pyperclip first (cross-platform, if installed)
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        pass
    except Exception:
        pass
    
    system = platform.system().lower()
    
    # macOS
    if system == "darwin":
        try:
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    # Windows
    if system == "windows":
        try:
            subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    # Linux - try xclip first, then xsel
    if system == "linux":
        # Try xclip
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try xsel
        try:
            subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=text.encode("utf-8"),
                check=True,
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Try clip.exe (WSL)
        try:
            subprocess.run(["clip.exe"], input=text.encode("utf-8"), check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    return False


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


def get_time_of_day(dt: datetime = None) -> str:
    """
    Get the time of day as a string.
    
    Args:
        dt: Optional datetime. Defaults to now.
    
    Returns:
        One of: 'morning', 'afternoon', 'evening', 'night'
    """
    if dt is None:
        dt = datetime.now()
    
    hour = dt.hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def get_day_type(dt: datetime = None) -> str:
    """
    Get the type of day (weekday or weekend).
    
    Args:
        dt: Optional datetime. Defaults to now.
    
    Returns:
        'weekday' or 'weekend'
    """
    if dt is None:
        dt = datetime.now()
    
    # weekday() returns 0-4 for Monday-Friday, 5-6 for Saturday-Sunday
    return "weekend" if dt.weekday() >= 5 else "weekday"


def get_time_aware_prediction(category: str = None) -> tuple[str, str]:
    """
    Generate a time-aware prediction for the future.
    
    This function considers both the time of day and day of week
    to provide more contextually relevant predictions.
    
    Args:
        category: Optional category. If None, may include time-based predictions.
    
    Returns:
        A tuple of (prediction string, category used).
    """
    now = datetime.now()
    time_of_day = get_time_of_day(now)
    day_type = get_day_type(now)
    
    # If a specific category is requested, use it
    if category is not None:
        if category not in PREDICTIONS:
            available = ", ".join(PREDICTIONS.keys())
            return f"Unknown category '{category}'. Available: {available}", category
        return random.choice(PREDICTIONS[category]), category
    
    # Create a weighted pool of predictions
    # Include regular categories with some time-aware predictions mixed in
    pool = []
    
    # Add regular category predictions (70% chance overall)
    for cat, preds in PREDICTIONS.items():
        for pred in preds:
            pool.append((pred, cat))
    
    # Add time-of-day predictions (15% chance)
    for pred in TIME_PREDICTIONS.get(time_of_day, []):
        pool.append((pred, f"time:{time_of_day}"))
    
    # Add day-type predictions (15% chance)
    for pred in DAY_PREDICTIONS.get(day_type, []):
        pool.append((pred, f"day:{day_type}"))
    
    return random.choice(pool)


def get_preferred_categories() -> dict:
    """
    Calculate category preferences based on user ratings.
    
    Returns:
        Dictionary mapping categories to preference scores (0-1).
        Higher scores indicate more preferred categories.
    """
    history = load_history()
    
    if not history:
        return {}
    
    # Collect ratings by category
    category_ratings = {}
    for pred in history:
        if pred.get("rating") is not None:
            cat = pred.get("category", "unknown")
            if cat not in category_ratings:
                category_ratings[cat] = []
            category_ratings[cat].append(pred["rating"])
    
    if not category_ratings:
        return {}
    
    # Calculate average rating per category
    category_scores = {}
    for cat, ratings in category_ratings.items():
        avg = sum(ratings) / len(ratings)
        # Normalize to 0-1 range (1-5 rating -> 0-1 score)
        category_scores[cat] = (avg - 1) / 4
    
    return category_scores


def get_preferred_prediction(category: str = None) -> tuple[str, str]:
    """
    Generate a prediction weighted by user preferences.
    
    Higher-rated categories are more likely to be selected.
    
    Args:
        category: Optional category. If specified, preference weighting is skipped.
    
    Returns:
        A tuple of (prediction string, category used).
    """
    if category is not None:
        return get_prediction(category)
    
    preferences = get_preferred_categories()
    
    if not preferences:
        # No rated predictions, use regular random selection
        return get_prediction(None)
    
    # Build weighted list of categories
    weighted_categories = []
    for cat in PREDICTIONS.keys():
        # Default weight of 1, increased by preference score
        weight = 1.0 + preferences.get(cat, 0) * 4  # Boost up to 5x for highly rated
        weighted_categories.append((cat, weight))
    
    # Weighted random selection
    total_weight = sum(w for _, w in weighted_categories)
    rand = random.uniform(0, total_weight)
    cumulative = 0
    selected_category = list(PREDICTIONS.keys())[0]
    
    for cat, weight in weighted_categories:
        cumulative += weight
        if rand <= cumulative:
            selected_category = cat
            break
    
    return get_prediction(selected_category)


def get_smart_prediction(category: str = None) -> tuple[str, str]:
    """
    Generate a prediction combining time-awareness with preference learning.
    
    This function combines the best of both modes:
    - Time-aware predictions based on time of day and day of week
    - Preference weighting from user ratings
    
    Args:
        category: Optional category. If specified, uses that category with time context.
    
    Returns:
        A tuple of (prediction string, category used).
    """
    now = datetime.now()
    time_of_day = get_time_of_day(now)
    day_type = get_day_type(now)
    
    # If a specific category is requested, use it
    if category is not None:
        if category not in PREDICTIONS:
            available = ", ".join(PREDICTIONS.keys())
            return f"Unknown category '{category}'. Available: {available}", category
        return random.choice(PREDICTIONS[category]), category
    
    preferences = get_preferred_categories()
    
    # Build weighted list for efficient selection (without duplicating entries)
    weighted_items = []
    
    # Add regular category predictions with preference weighting
    for cat, preds in PREDICTIONS.items():
        # Apply preference weight (1.0 to 5.0 based on rating), capped at 5.0
        pref_weight = min(1.0 + preferences.get(cat, 0) * 4, 5.0)
        for pred in preds:
            weighted_items.append((pred, cat, pref_weight))
    
    # Add time-of-day predictions with moderate weight (2.0 for relevance)
    for pred in TIME_PREDICTIONS.get(time_of_day, []):
        weighted_items.append((pred, f"time:{time_of_day}", 2.0))
    
    # Add day-type predictions with moderate weight (2.0 for relevance)
    for pred in DAY_PREDICTIONS.get(day_type, []):
        weighted_items.append((pred, f"day:{day_type}", 2.0))
    
    # Weighted random selection using cumulative weights
    total_weight = sum(w for _, _, w in weighted_items)
    rand = random.uniform(0, total_weight)
    cumulative = 0
    
    for pred, cat, weight in weighted_items:
        cumulative += weight
        if rand <= cumulative:
            return pred, cat
    
    # Fallback (should not reach here)
    return weighted_items[-1][0], weighted_items[-1][1]


def predict_the_future(category: str = None, time_aware: bool = False, use_preferences: bool = False, smart: bool = False, theme: str = None) -> dict:
    """
    Generate a complete future prediction.
    
    Args:
        category: Optional prediction category.
        time_aware: If True, include time-of-day and day-of-week context.
        use_preferences: If True, weight categories by user ratings.
        smart: If True, combine time-aware and preference modes.
        theme: Optional theme for predictions (motivational, holiday, spooky, adventure).
    
    Returns:
        Dictionary with prediction details.
    """
    # Select prediction based on mode
    # Mode precedence: theme > smart > time_aware > use_preferences > default
    # Theme mode uses its own prediction sets and doesn't combine with other modes
    if theme:
        prediction, used_category = get_themed_prediction(theme, category)
    elif smart:
        prediction, used_category = get_smart_prediction(category)
    elif time_aware:
        prediction, used_category = get_time_aware_prediction(category)
    elif use_preferences:
        prediction, used_category = get_preferred_prediction(category)
    else:
        prediction, used_category = get_prediction(category)
    
    future_date = get_future_date(random.randint(1, 7))
    
    result = {
        "prediction": prediction,
        "applies_to": future_date,
        "category": used_category,
        "confidence": f"{random.randint(70, 99)}%",
        "generated_at": datetime.now().isoformat(),
    }
    
    # Add theme info if using a theme
    if theme:
        result["theme"] = theme
    
    # Add time context if time-aware or smart mode
    if time_aware or smart:
        now = datetime.now()
        result["time_of_day"] = get_time_of_day(now)
        result["day_type"] = get_day_type(now)
    
    return result


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
    
    # Assign an ID if not present
    if "id" not in prediction:
        # Find the next available ID
        max_id = 0
        for p in history:
            if "id" in p and isinstance(p["id"], int):
                max_id = max(max_id, p["id"])
        prediction["id"] = max_id + 1
    
    history.append(prediction)
    
    # Keep only the last 100 predictions
    history = history[-100:]
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def display_history(count: int = 10, show_rated_only: bool = False) -> None:
    """
    Display recent prediction history.
    
    Args:
        count: Number of recent predictions to display.
        show_rated_only: If True, only show predictions that have been rated.
    """
    history = load_history()
    
    if not history:
        print("No prediction history found.")
        return
    
    if show_rated_only:
        history = [p for p in history if p.get("rating") is not None]
        if not history:
            print("No rated predictions found. Use --feedback to rate predictions.")
            return
    
    recent = history[-count:]
    title = "rated prediction(s)" if show_rated_only else "prediction(s)"
    print(f"\n📜 Last {len(recent)} {title}:\n")
    
    for i, pred in enumerate(reversed(recent), 1):
        rating_str = ""
        if pred.get("rating") is not None:
            rating_str = f" ⭐{pred['rating']}/5"
        print(f"{i}. [ID:{pred.get('id', 'N/A')}] [{pred.get('category', 'unknown').title()}]{rating_str} {pred['prediction']}")
        if "generated_at" in pred:
            # Parse and format the timestamp
            try:
                dt = datetime.fromisoformat(pred["generated_at"])
                print(f"   Generated: {dt.strftime('%Y-%m-%d %H:%M')}")
            except (ValueError, TypeError):
                pass
        print()


def add_feedback(prediction_id: int, rating: int) -> bool:
    """
    Add a rating to a prediction in history.
    
    Args:
        prediction_id: The ID of the prediction to rate.
        rating: The rating (1-5).
    
    Returns:
        True if successful, False otherwise.
    """
    if rating < 1 or rating > 5:
        print(f"Error: Rating must be between 1 and 5, got {rating}")
        return False
    
    history = load_history()
    
    for pred in history:
        if pred.get("id") == prediction_id:
            pred["rating"] = rating
            pred["rated_at"] = datetime.now().isoformat()
            
            # Save updated history
            with open(HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)
            
            print(f"✅ Rated prediction {prediction_id} with {rating}/5 stars")
            print(f"   \"{pred['prediction']}\"")
            return True
    
    print(f"Error: Prediction with ID {prediction_id} not found.")
    print("Use --history to see available predictions and their IDs.")
    return False


def show_stats() -> None:
    """Display prediction statistics."""
    history = load_history()
    
    if not history:
        print("No prediction history found.")
        return
    
    print("\n📊 Prediction Statistics\n")
    print(f"Total predictions: {len(history)}")
    
    # Count by category
    category_counts = {}
    for pred in history:
        cat = pred.get("category", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\n📂 Predictions by category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        pct = (count / len(history)) * 100
        print(f"   {cat.title()}: {count} ({pct:.1f}%)")
    
    # Rated predictions
    rated = [p for p in history if p.get("rating") is not None]
    if rated:
        avg_rating = sum(p["rating"] for p in rated) / len(rated)
        print(f"\n⭐ Rated predictions: {len(rated)}")
        print(f"   Average rating: {avg_rating:.1f}/5")
        
        # Rating distribution
        rating_counts = {}
        for p in rated:
            r = p["rating"]
            rating_counts[r] = rating_counts.get(r, 0) + 1
        print("   Rating distribution:")
        for r in range(5, 0, -1):
            count = rating_counts.get(r, 0)
            bar = "★" * count
            print(f"      {r}: {bar} ({count})")
        
        # Preference stats (Iteration 4)
        preferences = get_preferred_categories()
        if preferences:
            print("\n🎯 Category Preferences (based on ratings):")
            sorted_prefs = sorted(preferences.items(), key=lambda x: -x[1])
            for cat, score in sorted_prefs:
                bar_length = int(score * 10)
                bar = "▓" * bar_length + "░" * (10 - bar_length)
                print(f"   {cat.title()}: [{bar}] {score:.0%}")
            print("   (Use --preferred to weight predictions by your preferences)")
    else:
        print("\n⭐ No rated predictions yet. Use --feedback to rate predictions.")
    
    # Time stats
    dates = []
    for pred in history:
        try:
            dt = datetime.fromisoformat(pred.get("generated_at", ""))
            dates.append(dt)
        except (ValueError, TypeError):
            pass
    
    if dates:
        oldest = min(dates)
        newest = max(dates)
        print(f"\n📅 Date range:")
        print(f"   First: {oldest.strftime('%Y-%m-%d %H:%M')}")
        print(f"   Last:  {newest.strftime('%Y-%m-%d %H:%M')}")
    
    print()


def filter_history(history: list, category: str = None, since: str = None) -> list:
    """
    Filter history by category and/or date.
    
    Args:
        history: The prediction history to filter.
        category: Optional category to filter by.
        since: Optional ISO date string to filter predictions after.
    
    Returns:
        Filtered list of predictions.
    """
    filtered = history
    
    if category:
        filtered = [p for p in filtered if p.get("category", "").lower() == category.lower()]
    
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
            filtered = [
                p for p in filtered
                if "generated_at" in p and datetime.fromisoformat(p["generated_at"]) >= since_dt
            ]
        except ValueError:
            print(f"Warning: Invalid date format '{since}'. Use ISO format (YYYY-MM-DD).")
    
    return filtered


def export_history(format_type: str, category: str = None, since: str = None) -> None:
    """
    Export prediction history to a file.
    
    Args:
        format_type: The export format ('csv', 'markdown', or 'json').
        category: Optional category to filter by.
        since: Optional ISO date string to filter predictions after.
    """
    history = load_history()
    
    if not history:
        print("No prediction history to export.")
        return
    
    # Apply filters
    history = filter_history(history, category, since)
    
    if not history:
        print("No predictions match the specified filters.")
        return
    
    if format_type == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "category", "prediction", "applies_to", "confidence", "generated_at", "rating"])
        for pred in history:
            writer.writerow([
                pred.get("id", ""),
                pred.get("category", ""),
                pred.get("prediction", ""),
                pred.get("applies_to", ""),
                pred.get("confidence", ""),
                pred.get("generated_at", ""),
                pred.get("rating", ""),
            ])
        print(output.getvalue())
    
    elif format_type == "json":
        print(json.dumps(history, indent=2))
    
    elif format_type == "markdown":
        print("# Prediction History\n")
        print(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
        if category:
            print(f"*Filtered by category: {category}*\n")
        if since:
            print(f"*Filtered since: {since}*\n")
        print(f"Total predictions: {len(history)}\n")
        print("---\n")
        
        for pred in reversed(history):
            rating_str = f" (⭐{pred['rating']}/5)" if pred.get("rating") else ""
            print(f"## {pred.get('category', 'unknown').title()}{rating_str}\n")
            print(f"> {pred['prediction']}\n")
            print(f"- **ID**: {pred.get('id', 'N/A')}")
            print(f"- **Applies to**: {pred.get('applies_to', 'N/A')}")
            print(f"- **Confidence**: {pred.get('confidence', 'N/A')}")
            if "generated_at" in pred:
                try:
                    dt = datetime.fromisoformat(pred["generated_at"])
                    print(f"- **Generated**: {dt.strftime('%Y-%m-%d %H:%M')}")
                except (ValueError, TypeError):
                    pass
            print()
    else:
        print(f"Unknown export format: {format_type}. Use 'csv', 'json', or 'markdown'.")


def clear_history() -> bool:
    """
    Clear prediction history after confirmation.
    
    Returns:
        True if history was cleared, False otherwise.
    """
    history = load_history()
    
    if not history:
        print("No prediction history to clear.")
        return False
    
    print(f"⚠️  This will delete {len(history)} prediction(s) from history.")
    print("This action cannot be undone.")
    
    try:
        response = input("Are you sure? (yes/no): ").strip().lower()
    except EOFError:
        print("\nOperation cancelled.")
        return False
    
    if response == "yes":
        HISTORY_FILE.unlink(missing_ok=True)
        print("✅ History cleared successfully.")
        return True
    else:
        print("Operation cancelled.")
        return False


# Reminder functions (Iteration 8)

def load_reminders() -> list:
    """
    Load reminders from file.
    
    Returns:
        List of reminders.
    """
    if not REMINDERS_FILE.exists():
        return []
    
    try:
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_reminder(prediction: dict, reminder_date: str = None) -> dict:
    """
    Save a prediction as a reminder.
    
    Args:
        prediction: The prediction dictionary to save as a reminder.
        reminder_date: Optional specific date for the reminder (ISO format).
                       If not provided, uses the prediction's "applies_to" date.
    
    Returns:
        The reminder dictionary that was saved.
    """
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    
    reminders = load_reminders()
    
    # Assign a reminder ID
    max_id = 0
    for r in reminders:
        if "reminder_id" in r and isinstance(r["reminder_id"], int):
            max_id = max(max_id, r["reminder_id"])
    
    # Parse the reminder date
    if reminder_date:
        try:
            # Try to parse as ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
            remind_dt = datetime.fromisoformat(reminder_date)
            remind_date_str = remind_dt.strftime("%Y-%m-%d")
        except ValueError:
            # Try to parse as date-only string (YYYY-MM-DD)
            try:
                remind_dt = datetime.strptime(reminder_date, "%Y-%m-%d")
                remind_date_str = remind_dt.strftime("%Y-%m-%d")
            except ValueError:
                # Invalid date format, default to tomorrow
                print(f"Warning: Invalid date format '{reminder_date}'. Using tomorrow's date.")
                remind_dt = datetime.now() + timedelta(days=1)
                remind_date_str = remind_dt.strftime("%Y-%m-%d")
    else:
        # Extract date from applies_to field
        applies_to = prediction.get("applies_to", "")
        try:
            remind_dt = datetime.strptime(applies_to, "%A, %B %d, %Y")
            remind_date_str = remind_dt.strftime("%Y-%m-%d")
        except ValueError:
            # Default to tomorrow if parsing fails
            remind_dt = datetime.now() + timedelta(days=1)
            remind_date_str = remind_dt.strftime("%Y-%m-%d")
    
    reminder = {
        "reminder_id": max_id + 1,
        "prediction_id": prediction.get("id"),
        "prediction": prediction.get("prediction"),
        "category": prediction.get("category"),
        "remind_date": remind_date_str,
        "created_at": datetime.now().isoformat(),
        "acknowledged": False,
    }
    
    reminders.append(reminder)
    
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)
    
    return reminder


def get_pending_reminders() -> list:
    """
    Get reminders that are due (today or past due).
    
    Returns:
        List of pending reminders.
    """
    reminders = load_reminders()
    today = datetime.now().strftime("%Y-%m-%d")
    
    pending = []
    for reminder in reminders:
        if not reminder.get("acknowledged", False):
            remind_date = reminder.get("remind_date", "")
            if remind_date and remind_date <= today:
                pending.append(reminder)
    
    return pending


def display_pending_reminders() -> bool:
    """
    Display any pending reminders.
    
    Returns:
        True if there were pending reminders, False otherwise.
    """
    pending = get_pending_reminders()
    
    if not pending:
        return False
    
    print()
    print("=" * 50)
    print("  ⏰ PREDICTION REMINDERS ⏰")
    print("=" * 50)
    print()
    
    for reminder in pending:
        remind_date = reminder.get("remind_date", "")
        category = reminder.get("category", "unknown").title()
        prediction = reminder.get("prediction", "")
        reminder_id = reminder.get("reminder_id", "N/A")
        
        # Check if overdue
        today = datetime.now().strftime("%Y-%m-%d")
        if remind_date < today:
            status = "⚠️  OVERDUE"
        else:
            status = "📅 TODAY"
        
        print(f"[{status}] Reminder #{reminder_id} ({category})")
        print(f"   🔮 {prediction}")
        print(f"   Due: {remind_date}")
        print()
    
    print(f"💡 Use --acknowledge <id> to dismiss a reminder.")
    print(f"💡 Use --list-reminders to see all reminders.")
    print("-" * 50)
    print()
    
    return True


def display_reminders(show_all: bool = False) -> None:
    """
    Display all reminders.
    
    Args:
        show_all: If True, show acknowledged reminders too.
    """
    reminders = load_reminders()
    
    if not reminders:
        print("No reminders found.")
        print("Use --remind when generating a prediction to create a reminder.")
        return
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    print()
    title = "all reminders" if show_all else "pending reminders"
    print(f"⏰ Showing {title}:")
    print()
    
    displayed = 0
    for reminder in reminders:
        if not show_all and reminder.get("acknowledged", False):
            continue
        
        displayed += 1
        remind_date = reminder.get("remind_date", "")
        category = reminder.get("category", "unknown").title()
        prediction = reminder.get("prediction", "")
        reminder_id = reminder.get("reminder_id", "N/A")
        acknowledged = reminder.get("acknowledged", False)
        
        # Determine status
        if acknowledged:
            status = "✅ DONE"
        elif remind_date < today:
            status = "⚠️  OVERDUE"
        elif remind_date == today:
            status = "📅 TODAY"
        else:
            status = f"🗓️  {remind_date}"
        
        print(f"[{status}] Reminder #{reminder_id}")
        print(f"   Category: {category}")
        print(f"   🔮 {prediction}")
        if not acknowledged:
            print(f"   Due: {remind_date}")
        print()
    
    if displayed == 0:
        print("No pending reminders. Great job!")
        print("Use --list-reminders --all to see acknowledged reminders.")
    else:
        print(f"Total: {displayed} reminder(s)")
        if not show_all:
            print("Use --list-reminders --all to include acknowledged reminders.")


def acknowledge_reminder(reminder_id: int) -> bool:
    """
    Acknowledge (dismiss) a reminder.
    
    Args:
        reminder_id: The ID of the reminder to acknowledge.
    
    Returns:
        True if successful, False otherwise.
    """
    reminders = load_reminders()
    
    for reminder in reminders:
        if reminder.get("reminder_id") == reminder_id:
            if reminder.get("acknowledged", False):
                print(f"Reminder #{reminder_id} was already acknowledged.")
                return False
            
            reminder["acknowledged"] = True
            reminder["acknowledged_at"] = datetime.now().isoformat()
            
            with open(REMINDERS_FILE, "w") as f:
                json.dump(reminders, f, indent=2)
            
            print(f"✅ Reminder #{reminder_id} acknowledged!")
            print(f"   \"{reminder.get('prediction', '')}\"")
            return True
    
    print(f"Error: Reminder #{reminder_id} not found.")
    print("Use --list-reminders to see available reminders.")
    return False


def clear_reminders(clear_all: bool = False) -> bool:
    """
    Clear reminders (acknowledged ones by default, or all if specified).
    
    Args:
        clear_all: If True, clear all reminders. Otherwise, only acknowledged ones.
    
    Returns:
        True if reminders were cleared, False otherwise.
    """
    reminders = load_reminders()
    
    if not reminders:
        print("No reminders to clear.")
        return False
    
    if clear_all:
        count = len(reminders)
        print(f"⚠️  This will delete ALL {count} reminder(s).")
    else:
        acknowledged = [r for r in reminders if r.get("acknowledged", False)]
        count = len(acknowledged)
        if count == 0:
            print("No acknowledged reminders to clear.")
            print("Use --clear-reminders --all to clear all reminders.")
            return False
        print(f"⚠️  This will delete {count} acknowledged reminder(s).")
    
    print("This action cannot be undone.")
    
    try:
        response = input("Are you sure? (yes/no): ").strip().lower()
    except EOFError:
        print("\nOperation cancelled.")
        return False
    
    if response == "yes":
        if clear_all:
            REMINDERS_FILE.unlink(missing_ok=True)
        else:
            remaining = [r for r in reminders if not r.get("acknowledged", False)]
            with open(REMINDERS_FILE, "w") as f:
                json.dump(remaining, f, indent=2)
        print(f"✅ Cleared {count} reminder(s).")
        return True
    else:
        print("Operation cancelled.")
        return False


def format_for_sharing(prediction: dict, format_type: str = "text") -> str:
    """
    Format a prediction for sharing on social media.
    
    Args:
        prediction: The prediction dictionary to format.
        format_type: The format type ('text', 'twitter', 'markdown').
    
    Returns:
        Formatted prediction string ready for sharing.
    """
    pred_text = prediction.get("prediction", "")
    category = prediction.get("category", "unknown").title()
    applies_to = prediction.get("applies_to", "")
    confidence = prediction.get("confidence", "")
    
    if format_type == "twitter":
        # Twitter/X format - concise with hashtags
        hashtag = f"#{category.replace(' ', '')}" if category else ""
        return f"🔮 {pred_text}\n\n{hashtag} #TheFuturePredictor"
    
    elif format_type == "markdown":
        # Markdown format for forums, blogs, Discord, etc.
        return f"## 🔮 My Fortune\n\n> {pred_text}\n\n**Category**: {category} | **Applies to**: {applies_to} | **Confidence**: {confidence}\n\n*Generated by The Future Predictor*"
    
    else:  # text format (default)
        # Plain text format for general sharing
        return f"🔮 {pred_text}\n\n📅 Applies to: {applies_to}\n🎯 Category: {category}\n💫 Confidence: {confidence}\n\n— The Future Predictor"


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
  python app.py --time-aware         # Time-aware prediction (morning/evening, weekday/weekend)
  python app.py --preferred          # Preference-weighted prediction (based on your ratings)
  python app.py --smart              # Smart mode (combines time-aware + preferences)
  python app.py --json               # JSON output
  python app.py --history            # View past predictions
  python app.py --feedback 5 4       # Rate prediction #5 with 4 stars
  python app.py --stats              # View prediction statistics
  python app.py --export csv         # Export history as CSV
  python app.py --export json --filter fortune   # Export fortune predictions as JSON
  python app.py --export csv --since 2025-01-01  # Export predictions since date
  python app.py --share              # Format for social sharing
  python app.py --share twitter      # Format for Twitter/X
  python app.py --theme motivational # Use motivational theme
  python app.py --theme holiday -c relationship  # Holiday relationship prediction
  python app.py --theme zodiac -c aries   # Zodiac prediction for Aries
  python app.py --theme spring       # Seasonal spring prediction
  python app.py --share --copy       # Share and copy to clipboard
  python app.py --api                # Start the REST API with web frontend
  python app.py --api --port 3000    # Start API on custom port
  python app.py --remind             # Set reminder for prediction's apply date
  python app.py --remind 2025-12-25  # Set reminder for specific date
  python app.py --list-reminders     # View pending reminders
  python app.py --acknowledge 1      # Dismiss reminder #1
  python app.py --list-themes        # Show all available themes
  python app.py --add-theme          # Create a custom theme interactively
  python app.py --theme my_theme     # Use a custom theme
  python app.py --delete-theme my_theme  # Delete a custom theme
  python app.py --export-theme zodiac    # Export theme to JSON
  python app.py --import-theme file.json # Import theme from JSON file

Web Frontend (NEW in Iteration 10):
  Start the API server with --api, then visit http://localhost:8000/app
        """,
    )
    
    parser.add_argument(
        "--category", "-c",
        metavar="NAME",
        help="Category of prediction (use with --theme for theme-specific categories)",
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
    # Iteration 3: New arguments
    parser.add_argument(
        "--feedback",
        nargs=2,
        metavar=("ID", "RATING"),
        type=int,
        help="Rate a prediction by ID (rating: 1-5)",
    )
    parser.add_argument(
        "--show-rated",
        action="store_true",
        help="Show only rated predictions from history",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show prediction statistics",
    )
    parser.add_argument(
        "--export",
        choices=["csv", "markdown", "json"],
        help="Export history (csv, markdown, or json)",
    )
    parser.add_argument(
        "--clear-history",
        action="store_true",
        help="Clear prediction history",
    )
    # Iteration 4: New arguments
    parser.add_argument(
        "--time-aware", "-t",
        action="store_true",
        help="Generate time-aware predictions based on time of day and day of week",
    )
    parser.add_argument(
        "--preferred", "-p",
        action="store_true",
        help="Weight predictions by your rating preferences",
    )
    parser.add_argument(
        "--filter",
        metavar="CATEGORY",
        help="Filter history/export by category",
    )
    parser.add_argument(
        "--since",
        metavar="DATE",
        help="Filter history/export by date (ISO format: YYYY-MM-DD)",
    )
    # Iteration 5: New arguments
    parser.add_argument(
        "--smart", "-s",
        action="store_true",
        help="Smart mode: combine time-aware and preference-weighted predictions",
    )
    parser.add_argument(
        "--share",
        nargs="?",
        const="text",
        choices=["text", "twitter", "markdown"],
        metavar="FORMAT",
        help="Format prediction for social sharing (text, twitter, markdown)",
    )
    # Iteration 6: Theme and clipboard arguments
    parser.add_argument(
        "--theme",
        metavar="NAME",
        help="Use a themed prediction set (built-in or custom theme name)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy prediction to clipboard (works with --share)",
    )
    # Iteration 7: API argument
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start the REST API server (requires FastAPI and uvicorn)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the API server (default: 8000)",
    )
    # Iteration 8: Reminder arguments
    parser.add_argument(
        "--remind",
        nargs="?",
        const="auto",
        metavar="DATE",
        help="Set a reminder for this prediction (optional date: YYYY-MM-DD)",
    )
    parser.add_argument(
        "--list-reminders",
        action="store_true",
        help="Show pending reminders",
    )
    parser.add_argument(
        "--acknowledge",
        type=int,
        metavar="ID",
        help="Acknowledge (dismiss) a reminder by ID",
    )
    parser.add_argument(
        "--clear-reminders",
        action="store_true",
        help="Clear acknowledged reminders (use --all for all reminders)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all items (with --list-reminders or --clear-reminders)",
    )
    # Iteration 9: Custom themes arguments
    parser.add_argument(
        "--add-theme",
        action="store_true",
        help="Interactively create a custom theme",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="Show all available themes (built-in and custom)",
    )
    parser.add_argument(
        "--delete-theme",
        metavar="NAME",
        help="Delete a custom theme by name",
    )
    parser.add_argument(
        "--import-theme",
        metavar="FILE",
        help="Import a custom theme from a JSON file",
    )
    parser.add_argument(
        "--export-theme",
        metavar="NAME",
        help="Export a theme to JSON format (prints to stdout)",
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the future predictor."""
    args = parse_args()
    
    # Handle API server startup (Iteration 7)
    if args.api:
        start_api(port=args.port)
        return
    
    # Handle clear history (must be first as it modifies history)
    if args.clear_history:
        clear_history()
        return
    
    # Handle reminder-related commands (Iteration 8)
    if args.acknowledge:
        acknowledge_reminder(args.acknowledge)
        return
    
    if args.list_reminders:
        display_reminders(show_all=args.all)
        return
    
    if args.clear_reminders:
        clear_reminders(clear_all=args.all)
        return
    
    # Handle feedback
    if args.feedback:
        pred_id, rating = args.feedback
        add_feedback(pred_id, rating)
        return
    
    # Handle stats display
    if args.stats:
        show_stats()
        return
    
    # Handle export (with optional filters)
    if args.export:
        export_history(args.export, category=args.filter, since=args.since)
        return
    
    # Handle history display
    if args.history or args.show_rated:
        display_history(show_rated_only=args.show_rated)
        return
    
    # Handle theme-related commands (Iteration 9)
    if args.list_themes:
        list_themes()
        return
    
    if args.add_theme:
        interactive_add_theme()
        return
    
    if args.delete_theme:
        delete_custom_theme(args.delete_theme)
        return
    
    if args.import_theme:
        import_theme_from_file(args.import_theme)
        return
    
    if args.export_theme:
        export_theme_to_json(args.export_theme)
        return
    
    # Check for pending reminders before generating predictions
    display_pending_reminders()
    
    predictions = []
    for _ in range(args.count):
        result = predict_the_future(
            category=args.category,
            time_aware=args.time_aware,
            use_preferences=args.preferred,
            smart=args.smart,
            theme=args.theme,
        )
        predictions.append(result)
        
        if not args.no_save:
            save_to_history(result)
    
    # Share output format
    if args.share:
        share_texts = []
        for pred in predictions:
            share_text = format_for_sharing(pred, args.share)
            share_texts.append(share_text)
            print(share_text)
            if len(predictions) > 1:
                print()
        
        # Copy to clipboard if requested
        if args.copy:
            full_text = "\n\n".join(share_texts)
            if copy_to_clipboard(full_text):
                print("📋 Copied to clipboard!")
            else:
                print("⚠️  Could not copy to clipboard. Install pyperclip or use xclip/pbcopy.")
        return
    
    # Copy to clipboard for non-share output
    if args.copy:
        # Use text format for clipboard
        share_texts = [format_for_sharing(pred, "text") for pred in predictions]
        full_text = "\n\n".join(share_texts)
        if copy_to_clipboard(full_text):
            print("📋 Copied to clipboard!")
        else:
            print("⚠️  Could not copy to clipboard. Install pyperclip or use xclip/pbcopy.")
    
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
    print("  🔮 THE FUTURE PREDICTOR - Iteration 10 🔮")
    print("=" * 50)
    
    # Show mode indicators
    # Note: Smart mode already includes both time-aware and preference features,
    # so we don't show those separately when smart mode is active
    modes = []
    if args.theme:
        modes.append(f"🎭 Theme: {args.theme.title()}")
    if args.smart:
        modes.append("🧠 Smart")
    elif args.time_aware:
        modes.append("⏰ Time-aware")
    if args.preferred and not args.smart:
        modes.append("⭐ Preference-weighted")
    if modes:
        print(f"  Mode: {', '.join(modes)}")
    
    for i, result in enumerate(predictions, 1):
        if len(predictions) > 1:
            print(f"\n--- Prediction {i} ---")
        print()
        print(f"ID: {result.get('id', 'N/A')}")
        print(f"Category: {result['category'].title()}")
        if result.get("theme"):
            print(f"Theme: {result['theme'].title()}")
        if result.get("time_of_day"):
            print(f"Time context: {result['time_of_day'].title()} ({result.get('day_type', '').title()})")
        print(f"Applies to: {result['applies_to']}")
        print(f"Confidence: {result['confidence']}")
        print()
        print(f"🌟 {result['prediction']}")
    
    # Handle reminder creation (Iteration 8)
    if args.remind:
        for pred in predictions:
            reminder_date = args.remind if args.remind != "auto" else None
            reminder = save_reminder(pred, reminder_date)
            print()
            print(f"⏰ Reminder #{reminder['reminder_id']} set for {reminder['remind_date']}")
    
    print()
    print("-" * 50)
    print("Use --help to see available options.")
    print("Use --history to view past predictions.")
    print("Use --feedback <id> <rating> to rate a prediction.")
    print("Use --api to start the web frontend.")


def create_api():
    """
    Create and return a FastAPI application for the prediction API.
    
    Returns:
        FastAPI application instance.
    """
    try:
        from fastapi import FastAPI, Query, HTTPException, Body
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        from pydantic import BaseModel
    except ImportError:
        raise ImportError("FastAPI is required for the API. Install with: pip install fastapi uvicorn")
    
    api = FastAPI(
        title="The Future Predictor API",
        description="🔮 A playful prediction system that generates fortunes and predictions.",
        version="Iteration 10",
    )
    
    class PredictionResponse(BaseModel):
        """Response model for predictions."""
        prediction: str
        applies_to: str
        category: str
        confidence: str
        generated_at: str
        id: int | None = None
        theme: str | None = None
        time_of_day: str | None = None
        day_type: str | None = None
    
    class HealthResponse(BaseModel):
        """Response model for health check."""
        status: str
        version: str
    
    class ReminderRequest(BaseModel):
        """Request model for creating reminders."""
        prediction_id: int | None = None
        prediction: str
        category: str
        remind_date: str
    
    class ReminderResponse(BaseModel):
        """Response model for reminders."""
        reminder_id: int
        prediction_id: int | None = None
        prediction: str
        category: str
        remind_date: str
        created_at: str
        acknowledged: bool
        acknowledged_at: str | None = None
    
    class FeedbackRequest(BaseModel):
        """Request model for prediction feedback."""
        prediction_id: int
        rating: int
    
    class FeedbackResponse(BaseModel):
        """Response model for feedback."""
        success: bool
        message: str
    
    @api.get("/", response_model=HealthResponse, tags=["Health"])
    def health_check():
        """Check if the API is running."""
        return {"status": "ok", "version": "Iteration 10"}
    
    @api.get("/predict", response_model=PredictionResponse, tags=["Predictions"])
    def get_prediction_endpoint(
        category: str = Query(None, description="Prediction category"),
        theme: str = Query(None, description="Prediction theme (e.g., zodiac, spring, motivational)"),
        time_aware: bool = Query(False, description="Use time-aware predictions"),
        smart: bool = Query(False, description="Use smart mode (time + preferences)"),
        save: bool = Query(True, description="Save prediction to history"),
    ):
        """
        Generate a new prediction.
        
        - **category**: Optional category (fortune, weather, activity, career, relationship, health, creative)
        - **theme**: Optional theme (motivational, holiday, spooky, adventure, spring, summer, fall, winter, zodiac)
        - **time_aware**: Generate time-aware predictions based on time of day
        - **smart**: Use smart mode combining time-awareness and preferences
        - **save**: Whether to save the prediction to history (default: True)
        """
        # Validate theme - check both built-in and custom themes
        all_themes = get_all_themes()
        if theme and theme not in all_themes:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown theme '{theme}'. Available: {', '.join(all_themes.keys())}"
            )
        
        # Validate category
        if category and category not in PREDICTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown category '{category}'. Available: {', '.join(PREDICTIONS.keys())}"
            )
        
        result = predict_the_future(
            category=category,
            time_aware=time_aware,
            smart=smart,
            theme=theme,
        )
        
        if save:
            save_to_history(result)
        
        return result
    
    @api.get("/predict/batch", response_model=list[PredictionResponse], tags=["Predictions"])
    def get_batch_predictions(
        count: int = Query(3, ge=1, le=100, description="Number of predictions to generate"),
        category: str = Query(None, description="Prediction category"),
        theme: str = Query(None, description="Prediction theme"),
        save: bool = Query(True, description="Save predictions to history"),
    ):
        """Generate multiple predictions at once."""
        predictions = []
        for _ in range(count):
            result = predict_the_future(category=category, theme=theme)
            if save:
                save_to_history(result)
            predictions.append(result)
        return predictions
    
    @api.get("/themes", tags=["Information"])
    def api_list_themes():
        """List all available prediction themes and their categories."""
        all_themes = get_all_themes()
        return {
            theme: list(categories.keys())
            for theme, categories in all_themes.items()
        }
    
    @api.get("/categories", tags=["Information"])
    def api_list_categories():
        """List all available prediction categories."""
        return list(PREDICTIONS.keys())
    
    @api.get("/history", tags=["History"])
    def get_history(
        count: int = Query(10, ge=1, le=100, description="Number of recent predictions"),
        category: str = Query(None, description="Filter by category"),
        rated_only: bool = Query(False, description="Show only rated predictions"),
    ):
        """Get prediction history."""
        history = load_history()
        
        if category:
            history = [p for p in history if p.get("category", "").lower() == category.lower()]
        
        if rated_only:
            history = [p for p in history if p.get("rating") is not None]
        
        return history[-count:]
    
    @api.get("/stats", tags=["History"])
    def get_stats():
        """Get prediction statistics."""
        history = load_history()
        
        if not history:
            return {"total_predictions": 0, "categories": {}, "ratings": {}}
        
        # Count by category
        category_counts = {}
        for pred in history:
            cat = pred.get("category", "unknown")
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Rating stats
        rated = [p for p in history if p.get("rating") is not None]
        rating_stats = {}
        if rated:
            rating_stats = {
                "count": len(rated),
                "average": round(sum(p["rating"] for p in rated) / len(rated), 2),
            }
        
        return {
            "total_predictions": len(history),
            "categories": category_counts,
            "ratings": rating_stats,
        }
    
    # Reminder endpoints (Iteration 10)
    @api.get("/reminders", response_model=list[ReminderResponse], tags=["Reminders"])
    def api_get_reminders(
        show_all: bool = Query(False, description="Include acknowledged reminders"),
    ):
        """Get all reminders."""
        reminders = load_reminders()
        
        if not show_all:
            reminders = [r for r in reminders if not r.get("acknowledged", False)]
        
        return reminders
    
    @api.post("/reminders", response_model=ReminderResponse, tags=["Reminders"])
    def api_create_reminder(request: ReminderRequest):
        """Create a new reminder for a prediction."""
        prediction = {
            "id": request.prediction_id,
            "prediction": request.prediction,
            "category": request.category,
            "applies_to": "",  # Not used when remind_date is provided
        }
        
        reminder = save_reminder(prediction, request.remind_date)
        return reminder
    
    @api.post("/reminders/{reminder_id}/acknowledge", tags=["Reminders"])
    def api_acknowledge_reminder(reminder_id: int):
        """Acknowledge (dismiss) a reminder."""
        reminders = load_reminders()
        
        for reminder in reminders:
            if reminder.get("reminder_id") == reminder_id:
                if reminder.get("acknowledged", False):
                    raise HTTPException(status_code=400, detail="Reminder already acknowledged")
                
                reminder["acknowledged"] = True
                reminder["acknowledged_at"] = datetime.now().isoformat()
                
                with open(REMINDERS_FILE, "w") as f:
                    json.dump(reminders, f, indent=2)
                
                return {"success": True, "message": f"Reminder {reminder_id} acknowledged"}
        
        raise HTTPException(status_code=404, detail=f"Reminder {reminder_id} not found")
    
    # Feedback endpoint (Iteration 10)
    @api.post("/feedback", response_model=FeedbackResponse, tags=["Feedback"])
    def api_add_feedback(request: FeedbackRequest):
        """Add a rating to a prediction."""
        if request.rating < 1 or request.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        history = load_history()
        
        for pred in history:
            if pred.get("id") == request.prediction_id:
                pred["rating"] = request.rating
                pred["rated_at"] = datetime.now().isoformat()
                
                with open(HISTORY_FILE, "w") as f:
                    json.dump(history, f, indent=2)
                
                return {"success": True, "message": f"Rated prediction {request.prediction_id} with {request.rating}/5 stars"}
        
        raise HTTPException(status_code=404, detail=f"Prediction {request.prediction_id} not found")
    
    # Static files and web frontend
    static_dir = Path(__file__).parent / "static"
    if static_dir.exists():
        api.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        
        @api.get("/app", include_in_schema=False)
        def serve_frontend():
            """Serve the web frontend."""
            return FileResponse(str(static_dir / "index.html"))
    
    return api


def start_api(port: int = 8000):
    """
    Start the FastAPI server.
    
    The server binds to localhost (127.0.0.1) for security. If you need to
    expose the API to external networks, implement proper authentication
    and authorization first.
    
    Args:
        port: Port to run the server on (default: 8000).
    """
    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is required to run the API server.")
        print("Install with: pip install uvicorn")
        return
    
    api = create_api()
    print(f"🔮 Starting The Future Predictor API on http://localhost:{port}")
    print(f"📱 Web Frontend: http://localhost:{port}/app")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print("Press Ctrl+C to stop the server.")
    uvicorn.run(api, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
