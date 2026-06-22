def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Hard and Normal ranges were swapped (Normal gave 1-100, Hard gave 1-50).
    # AI identified the inversion by diffing commits; verified by checking sidebar range display in the game.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Hard":
        return 1, 100
    if difficulty == "Normal":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: Labels were inverted — "Too High" previously showed "Go HIGHER!" and vice versa.
        # AI spotted it in the git diff; verified via pytest test_too_high_message_says_go_lower.
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: Formula used (attempt_number + 1), cutting first-attempt wins to 80 pts instead of 100.
        # Changed to (attempt_number - 1); verified by pytest test_first_attempt_win_scores_100.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: "Too High" on even attempts previously awarded +5 (rewarding a wrong guess).
    # AI identified the parity branch in the diff; verified by pytest test_too_high_always_deducts_score_on_even_attempt.
    if outcome == "Too High":
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score

