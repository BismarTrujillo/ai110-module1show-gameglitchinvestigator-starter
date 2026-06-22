from logic_utils import check_guess, get_range_for_difficulty, update_score


# --- existing tests (fixed: check_guess returns a tuple) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1: direction labels were inverted in check_guess (commit f3ea6af) ---
# Before fix: guess > secret returned "Go HIGHER!" (wrong); guess < secret returned "Go LOWER!" (wrong)

def test_too_high_message_says_go_lower():
    # Guess is above secret — player must go LOWER, not higher
    _, message = check_guess(75, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: {message}"

def test_too_low_message_says_go_higher():
    # Guess is below secret — player must go HIGHER, not lower
    _, message = check_guess(25, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: {message}"


# --- Bug 2: Hard/Normal difficulty ranges were swapped (commit ab8c73b) ---
# Before fix: Normal → (1,100), Hard → (1,50) — Hard was easier than Normal

def test_normal_difficulty_range():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50), f"Normal should be (1,50), got ({low},{high})"

def test_hard_difficulty_range():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100), f"Hard should be (1,100), got ({low},{high})"

def test_hard_range_larger_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard difficulty must have a larger range than Normal"


# --- Bug 3: update_score rewarded +5 on even-attempt "Too High" guesses (commit add3585) ---
# Before fix: if attempt_number % 2 == 0 and outcome == "Too High", score += 5 (wrong)

def test_too_high_always_deducts_score_on_even_attempt():
    score = update_score(50, "Too High", attempt_number=2)
    assert score < 50, f"Too High on even attempt should deduct points, got {score}"

def test_too_high_always_deducts_score_on_odd_attempt():
    score = update_score(50, "Too High", attempt_number=1)
    assert score < 50, f"Too High on odd attempt should deduct points, got {score}"

def test_too_high_and_too_low_deduct_equally():
    score_high = update_score(50, "Too High", attempt_number=2)
    score_low = update_score(50, "Too Low", attempt_number=2)
    assert score_high == score_low, "Too High and Too Low should deduct the same amount"


# --- Bug 4: Win score formula used attempt_number+1 instead of attempt_number-1 (commit add3585) ---
# Before fix: points = 100 - 10 * (attempt_number + 1), so attempt 1 win gave only 80 pts

def test_first_attempt_win_scores_100():
    score = update_score(0, "Win", attempt_number=1)
    assert score == 100, f"First-attempt win should score 100, got {score}"

def test_win_score_decreases_with_more_attempts():
    score_attempt1 = update_score(0, "Win", attempt_number=1)
    score_attempt3 = update_score(0, "Win", attempt_number=3)
    assert score_attempt1 > score_attempt3, "Earlier wins should score more than later wins"

def test_win_score_never_below_10():
    # Win on a very late attempt should still award minimum 10 points
    score = update_score(0, "Win", attempt_number=100)
    assert score >= 10, f"Win score floor should be 10, got {score}"
