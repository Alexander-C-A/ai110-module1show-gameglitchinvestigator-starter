# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A Streamlit number-guessing game. The app picks a secret number in a range set by difficulty (Easy 1–20, Normal 1–50, Hard 1–100). You guess until you get it or run out of attempts, and you get "Go HIGHER" / "Go LOWER" hints plus a score.
- [x] **Bugs found:**
  - Hint messages were reversed ("Too High" told you to go higher).
  - On every even attempt the secret was turned into a string, so numbers were compared alphabetically (`"9" > "50"`), which gave wrong hints.
  - New Game didn't reset `status`, so after a win or loss the game could never restart.
  - The attempt counter started at 1 on first load but 0 after New Game, and invalid input used up an attempt.
  - Hard (1–50) was easier than Normal (1–100), and the prompt always said "1 and 100."
  - Scoring gave +5 for some wrong guesses and had an off-by-one in the win bonus.
  - Starter tests compared a `(outcome, message)` tuple to a string, so they could never pass.
- [x] **Fixes applied:**
  - Moved all game logic from `app.py` into `logic_utils.py` so it can be tested without the UI.
  - Fixed the hint messages and removed the string-conversion of the secret.
  - Added a `start_new_game()` helper that resets all session state and uses the difficulty's range. Changing difficulty also starts a new game.
  - Attempts now start at 0 and only valid guesses count. `parse_guess` rejects decimals and out-of-range numbers.
  - Corrected difficulty ranges, prompt text, and scoring.
  - Fixed the starter tests, added 12 edge-case tests, and added a `pytest.ini` so plain `pytest` can import `logic_utils`.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py`. The game starts on Normal: "Guess a number between 1 and 50. Attempts left: 8." (Debug Info shows the secret is 30.)
2. User types `abc` and submits. The game shows "That is not a whole number." Attempts left stays at 8.
3. User enters a guess of 20. The game shows "Too Low" with the hint "📈 Go HIGHER!" Score goes to -5 and attempts left drops to 7.
4. User enters a guess of 40. The game shows "📉 Go LOWER!" Score goes to -10 and attempts left drops to 6.
5. User enters a guess of 30. The game shows "🎉 Correct!", balloons appear, and "You won! The secret was 30. Final score: 60" (70 points for winning on attempt 3, minus 10).
6. Submitting again shows "You already won. Start a new game to play again." The game has ended.
7. User clicks **New Game 🔁**. Score, attempts, and history reset, and a new secret is chosen in 1–50.
8. User switches difficulty to **Hard**. A new game starts with "Guess a number between 1 and 100. Attempts left: 5." After 5 wrong guesses, the game shows "Out of attempts! The secret was …" and ends.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest -v
============================= test session starts ==============================
platform linux -- Python 3.13.16, pytest-9.1.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: .../game-glitch-investigator
configfile: pytest.ini
testpaths: tests
collecting ... collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED        [ 26%]
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED        [ 33%]
tests/test_game_logic.py::test_single_digit_guess_against_two_digit_secret PASSED [ 40%]
tests/test_game_logic.py::test_two_digit_guess_against_single_digit_secret PASSED [ 46%]
tests/test_game_logic.py::test_hard_range_is_wider_than_normal PASSED    [ 53%]
tests/test_game_logic.py::test_parse_valid_number PASSED                 [ 60%]
tests/test_game_logic.py::test_parse_empty_and_text_are_rejected PASSED  [ 66%]
tests/test_game_logic.py::test_parse_decimal_is_rejected PASSED          [ 73%]
tests/test_game_logic.py::test_parse_out_of_range_is_rejected PASSED     [ 80%]
tests/test_game_logic.py::test_wrong_guesses_never_add_points PASSED     [ 86%]
tests/test_game_logic.py::test_first_try_win_scores_90 PASSED            [ 93%]
tests/test_game_logic.py::test_win_score_has_a_floor_of_10 PASSED        [100%]

============================== 15 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
