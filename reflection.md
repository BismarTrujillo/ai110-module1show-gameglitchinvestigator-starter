# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|guess of 1 |go HIGHER |go LOWER | None |
|submit guess |secret within range|secret not within range | None |
|Change difficulty |new range, and new secret within selected range |random secret outside of range, and no UI reflecting difficulty change |None |
|Difficulty swap  |Hard range: 1 to 100, Normal range: 1 to 50|Normal range: 1 to 100, Hard range: 1 to 50 |None |
|New Game button pressed | Proper game restart | No changes at all. Couldn't start a new game |None |

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic's AI coding assistant) throughout this project as an in-editor agent. I used it to analyze git diffs, identify bugs, generate targeted tests, and add inline documentation.

**Correct AI suggestion:**
Claude Code analyzed the git history and correctly identified that the `check_guess` function was returning a tuple `(outcome, message)`, but the starter scaffold tests were written as `assert result == "Win"` — comparing the whole tuple to a bare string. This meant the tests always would have failed, even after the bug was fixed, giving a false picture of test coverage. The AI rewrote the assertions to `outcome, _ = check_guess(...)` and `assert outcome == "Win"`. I verified this by running `pytest -v` and confirming all 14 tests passed, including the previously broken ones.

**Incorrect/misleading AI suggestion:**
Early in the session, when I asked the AI to explain what bugs existed, it initially listed the inverted direction labels (`check_guess`) and the swapped difficulty ranges as separate issues — which was accurate — but it did not immediately flag that the `update_score` win formula was also wrong (using `attempt_number + 1` instead of `attempt_number - 1`). The scoring bug was subtler and the AI only surfaced it after I asked it to look specifically at the scoring logic in the diff. This was misleading because a quick first pass suggested only two bugs, when there were actually four. I verified the scoring formula by writing `test_first_attempt_win_scores_100` and confirming that a first-attempt win correctly awards 100 points, not 80.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only after two things were true: the game *looked* correct when I ran it manually, and a pytest test I wrote *specifically for that bug* passed. Relying on just one of those would not have been enough — the direction labels looked fixed visually, but without a test asserting that `guess > secret` returns a message containing "LOWER", the fix could have been broken again without warning.

The most revealing test was `test_too_high_always_deducts_score_on_even_attempt`. Before the fix, calling `update_score(50, "Too High", attempt_number=2)` returned `55` (adding points for a wrong guess). After the fix it returned `45`. That single assertion proved the parity branch bug was gone and that wrong guesses consistently deduct 5 points regardless of attempt number.

Claude Code helped design all the targeted regression tests. I described the bugs I had found from the git diff, and the AI generated 14 tests organized into four groups — one per bug. It also explained *why* each test was structured the way it was (e.g., why `test_hard_range_larger_than_normal` is more durable than just checking for the literal tuple `(1, 100)`). That explanation helped me understand the value of testing invariants (Hard must be harder than Normal) over hardcoded values.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
