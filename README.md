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

- [ ] Describe the game's purpose.
- App provides a random number within a preselected range, (Difficulty selection). The objective is to *guess* this number using a finite number of guesses 
- [ ] Detail which bugs you found.
  - Settings changes aren't reflected on game
  - Banner bellow *Make a guess* does not reflect actual Difficulty or range of numbers. 
  -  Difficulty swap (Normal and Hard)
  	-  Difficulty: Normal shows *Range: 1 to 100* 
  	-  Difficulty: Hard shows *Range: 1 to 50*
  -  The Hint does not follow the range
  	- If secret is higher number, hint shows LOWER
  	- If secret is lower numbers, hint shows HIGHER
  - The Secret doesn't follow range
  - When one game ends, *New Game* button does not work
- [ ] Explain what fixes you applied.
- Session state fix; stored the secret in st.session_state.secret so it only generates once and persists across button clicks.
- Hints fix: swapped the branches in check_guess so guess > secret returns "Go LOWER!" and guess < secret returns "Go HIGHER!".
- Difficulty ranges fix; corrected get_range_for_difficulty so Normal returns (1, 50) and Hard returns (1, 100).
- Score formula fix: changed 100 - 10 * (attempt_number + 1) to 100 - 10 * (attempt_number - 1) so a first-attempt win correctly scores 100 points.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Open the app and choose a difficulty from sidebar
2. Type a number into the guess field and click **Submit Guess**.
3. Read the hint "Go LOWER!" or "Go HIGHER!" adjust next guess.
4. Keep guessing until you hit the secret number
5. Click **New Game** to reset and play again.

## 🧪 Test Results

```
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\bisma\OneDrive\Escritorio\AI110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 14 items                                                                                                                  

tests\test_game_logic.py ..............
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
