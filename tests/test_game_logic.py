from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


def test_parse_guess_rejects_negative_numbers():
    ok, guess_int, err = parse_guess("-5")
    assert ok is False
    assert guess_int is None
    assert err == "Guess must be between 1 and 100."


def test_parse_guess_accepts_decimals_by_truncating():
    ok, guess_int, err = parse_guess("42.9")
    assert ok is True
    assert guess_int == 42
    assert err is None


def test_parse_guess_rejects_extremely_large_values():
    ok, guess_int, err = parse_guess("999999999999")
    assert ok is False
    assert guess_int is None
    assert err == "Guess must be between 1 and 100."
