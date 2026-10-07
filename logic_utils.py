# FIX: Core game logic refactored out of app.py into this module with AI
# assistance (Claude), then reviewed and verified with pytest.

DIFFICULTY_RANGES = {
    "Easy": (1, 20),
    "Normal": (1, 50),
    "Hard": (1, 100),
}

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard used to be 1-50 (easier than Normal's 1-100). Ranges now grow
    # with difficulty.
    return DIFFICULTY_RANGES.get(difficulty, (1, 50))


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        # FIX: Decimals like "4.9" used to be silently truncated to 4.
        return False, None, "That is not a whole number."

    # FIX: Out-of-range guesses are rejected instead of counted.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: Hint messages were swapped ("Too High" said "Go HIGHER"), and the
    # TypeError fallback compared numbers as strings ("9" > "50"). Both ints
    # are now compared directly; app.py no longer passes a str secret.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    attempt_number is 1-based (1 = first guess).
    """
    if outcome == "Win":
        # FIX: Removed off-by-one (+1). A first-try win is worth 90.
        points = max(100 - 10 * attempt_number, 10)
        return current_score + points

    # FIX: Wrong guesses always cost 5 points. "Too High" used to give +5
    # on even attempts.
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
