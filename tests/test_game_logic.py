from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


# --- Starter tests ---
# FIX: check_guess returns (outcome, message), so the starter tests compared a
# tuple to a string and could never pass. They now unpack the outcome.

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1: hint messages were swapped ---

def test_too_high_hint_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- Bug 2: secret compared as a string ("9" > "50") ---

def test_single_digit_guess_against_two_digit_secret():
    # With string comparison, "9" > "50" was True and this said "Too High".
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


def test_two_digit_guess_against_single_digit_secret():
    # With string comparison, "10" < "9" was True and this said "Too Low".
    outcome, _ = check_guess(10, 9)
    assert outcome == "Too High"


# --- Difficulty ranges ---

def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    _, easy_high = get_range_for_difficulty("Easy")
    assert easy_high < normal_high < hard_high


# --- parse_guess edge cases ---

def test_parse_valid_number():
    assert parse_guess("42") == (True, 42, None)


def test_parse_empty_and_text_are_rejected():
    assert parse_guess("")[0] is False
    assert parse_guess("   ")[0] is False
    assert parse_guess("abc")[0] is False


def test_parse_decimal_is_rejected():
    ok, value, _ = parse_guess("4.9")
    assert ok is False and value is None


def test_parse_out_of_range_is_rejected():
    assert parse_guess("0", 1, 20)[0] is False
    assert parse_guess("21", 1, 20)[0] is False
    assert parse_guess("20", 1, 20) == (True, 20, None)


# --- Scoring ---

def test_wrong_guesses_never_add_points():
    for attempt in range(1, 9):
        assert update_score(50, "Too High", attempt) == 45
        assert update_score(50, "Too Low", attempt) == 45


def test_first_try_win_scores_90():
    assert update_score(0, "Win", 1) == 90


def test_win_score_has_a_floor_of_10():
    assert update_score(0, "Win", 20) == 10
