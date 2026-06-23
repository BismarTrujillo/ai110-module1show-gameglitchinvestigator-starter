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

I used Claude Code for this app as an in editor agent. I used it to analyze git diffs, identify bugs, generate targeted tests, and add inline documentation

**Correct AI suggestion:**
Claude Code spotted that the starter tests used `assert result == "Win"`, but `check_guess` returns a tuple — so they would always fail. The AI rewrote them to `outcome, _ = check_guess(...)`. I verified by running `pytest -v` and seeing all 14 tests pass.

**Incorrect/misleading AI suggestion:**
On the first pass, the AI only flagged two bugs (inverted labels, swapped difficulty ranges) and missed that the `update_score` win formula was also wrong. I had to ask it to look at the scoring diff specifically before it caught the `attempt_number + 1` error. I verified the fix by writing `test_first_attempt_win_scores_100` and confirming a first-attempt win awards 100 points, not 80.

---

## 3. Debugging and testing your fixes

A bug was only confirmed fixed when both a manual run and a targeted pytest test passed. Visual checks alone weren't enough, for example the direction labels looked correct in the UI, but a test asserting the message contains "LOWER" was the real proof.

The most revealing test was `test_too_high_always_deducts_score_on_even_attempt`: before the fix `update_score(50, "Too High", attempt_number=2)` returned `55`; after, `45`. One assertion caught the whole parity bug.

Claude generated all 14 tests grouped by bug, and explained why testing invariants is more durable than checking values.

---

## 4. What did you learn about Streamlit and state?

Every time user clicks a button or changes an input, streamlit reruns the entire page from top to bottom. Any variable defined normally gets reset on every rerun. `st.session_state` is a dictionary that survives those reruns, so it's the only way to remember things like the secret number. Most bugs in this project came from not initializing or updating session state correctly.

---

## 5. Looking ahead: your developer habits

I'll write a regression test right after every fix so bugs can't silently return. Next time I'll ask the AI for a full diff review in one prompt, that'd have caught all four bugs at once instead of finding the scoring bug only after a follow-up. This project taught me to treat AI code as a first draft: it looked right and had tests, but both had hidden errors that only appeared under real inputs.
