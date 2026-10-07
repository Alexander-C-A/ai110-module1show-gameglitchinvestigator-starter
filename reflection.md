# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

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

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
