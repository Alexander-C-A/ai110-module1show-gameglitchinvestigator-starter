# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

I was short on time, so I had my AI assistant (Claude) read through `app.py` and find the bugs instead of finding them by playing first. The code looked like a normal guessing game, but it had a lot of hidden problems. The two clearest were that the hints were backwards ("Too High" told you to "Go HIGHER") and that on every even attempt the secret was turned into a string, so the game compared numbers alphabetically (`"9" > "50"`). New Game was also broken: after you won or lost, it never actually restarted the game. The rows below describe how to reproduce each bug. They came from reading the code and were confirmed by tests after the fix.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Secret 50 (from Debug Info), guess 60 | "Too High" outcome with a "Go LOWER" hint | Outcome is "Too High" but hint says "📈 Go HIGHER!" | none | `app.py`, `check_guess` (messages swapped, lines 37–40) |
| Secret 50, first guess 9 (attempt counter is even) | "Too Low" | "Too High" — the secret was turned into the string `"50"`, so `"9" > "50"` compares alphabetically | none (TypeError is caught silently) | `app.py` lines 158–161 (`str(secret)` on even attempts) + `check_guess` `except TypeError` branch |
| Win or lose a game, then click "New Game 🔁" | A fresh game starts | Still shows "Game over" / "You already won"; can't play again | none | `app.py` New Game handler (lines 134–138) never resets `status`, `score`, or `history` |
| Load page on Normal (8 attempts) | "Attempts left: 8" | "Attempts left: 7" — first load starts `attempts` at 1, New Game resets it to 0 | none | `app.py` line 96 vs line 135 |
| Select "Hard" difficulty | Harder than Normal | Range is 1–50 (easier than Normal's 1–100); prompt still says "between 1 and 100" | none | `app.py`, `get_range_for_difficulty` and hardcoded `st.info` text (line 110) |
| Type `abc` and submit | Error message, attempt not used | Error shown, but an attempt is still used up | "That is not a number." | `app.py` line 148 (`attempts += 1` before parsing) |

**Other issues noticed in the code:**
- `update_score` gives +5 points for a wrong "Too High" guess on even attempts, and the win bonus is off by one (`attempt_number + 1`).
- New Game always picks the secret from 1–100, regardless of difficulty.
- The starter tests compare `check_guess(...)` to a string, but the function returns a `(outcome, message)` tuple, so the tests could never pass as written.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

I used Claude for most of this project. I gave it the assignment and repo link, and it found the bugs, refactored the logic into `logic_utils.py`, wrote the tests, and made the commits. I directed the work and decided how much to hand off.

**Correct suggestion:** Claude pointed out that `app.py` was turning the secret into a string on even-numbered attempts. That forced `check_guess` into its `except TypeError` branch, which compares text alphabetically, so a guess of 9 against a secret of 50 said "Too High." This was correct. It's verified by `test_single_digit_guess_against_two_digit_secret` and `test_two_digit_guess_against_single_digit_secret`, which both pass after the fix.

**Suggestion not accepted as written:** The starter README is written as if by the AI that built the game. It says the main bug is that "the secret number changes every time you click Submit" and suggests asking how to stop a variable from resetting. We didn't follow that: the code already stores the secret in `st.session_state`, so its *value* never changed, only its *type*. Chasing the README's hint would have meant fixing a bug that wasn't there. The Debug Info panel shows the same secret across guesses, and the string-comparison tests above show where the real problem was.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

A bug counted as fixed only when a pytest test targeting it passed and the game behaved correctly when played. One example: `check_guess(9, 50)` must return "Too Low." That test would have failed under the old string-comparison behavior, so it proves that exact bug is gone. Claude also found that the three starter tests could never pass, because they compared `check_guess`'s `(outcome, message)` tuple to a plain string; we changed them to unpack the outcome. It added `pytest.ini` too, because plain `pytest` couldn't import `logic_utils`. AI designed the tests: 15 in total, all passing (output is in the README). Claude also simulated a full game with Streamlit's `AppTest`: an invalid input that doesn't cost an attempt, a wrong guess with the right hint, a win, New Game, and a loss on Hard.


---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type something, Streamlit runs your whole Python script again from top to bottom. That's a "rerun." Normal variables get wiped out each time, so anything that needs to survive between clicks (the secret number, attempts, score) has to live in `st.session_state`, which acts like a dictionary that sticks around for that browser session. The pattern `if "secret" not in st.session_state:` means "only set this up the first time." This game's New Game bug happened because the reset only updated some of the session state values and forgot `status`, so the old "game over" state survived every rerun.


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

- **Habit to keep:** Writing a small test for each specific bug, like "guess 9 vs secret 50 must be Too Low," so it's clear the bug is really gone and doesn't come back.
- **Do differently:** I relied on AI for almost everything because I was behind and studying for an exam. Next time I'd run the buggy app myself first and try to find at least one bug on my own before handing it off, so I'm checking the AI's work instead of just trusting it.
- **How it changed my thinking:** AI-generated code can look clean and "production-ready" while hiding bugs that only show up in specific cases, like silent type mixing. Its own explanations (like the README hint) can be wrong too, so the code and the tests are what you should trust.

