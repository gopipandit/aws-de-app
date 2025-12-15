# Recent Changes

## 1. Added Quit Button
- A "Quit Quiz" button is now available in the top-right corner of the quiz page
- When clicked, it shows your current progress before quitting
- Displays: number of questions answered and current score
- Confirms before exiting back to the question sets page

## 2. Smart Input Type Selection (Checkbox vs Radio Button)
- **Single Answer Questions**: Display as clickable buttons (radio-style behavior)
  - Only one option can be selected
  - Answer is submitted immediately when clicked

- **Multiple Answer Questions**: Display with checkboxes
  - Multiple options can be selected
  - Shows "Select all correct answers" hint
  - Requires clicking "Submit Answer" button

### Technical Implementation:
- Added `has_multiple_answers` field to MongoDB questions
- Field is automatically set based on number of correct answers
- `has_multiple_answers: true` when question has 2+ correct answers
- `has_multiple_answers: false` when question has 1 correct answer

### Migration:
- Re-ran data migration to add the flag to all existing questions
- All 329 questions now have this flag
- Flag is automatically set when adding/editing questions through admin panel

## How It Works:
1. When you open a question:
   - If `has_multiple_answers` is `true`: Shows checkboxes with "Submit Answer" button
   - If `has_multiple_answers` is `false`: Shows as clickable buttons (auto-submit)

2. Visual Indicators:
   - Multi-answer questions show: "Select all correct answers" in red text
   - Single-answer questions have no special indicator

3. Quit Button:
   - Located in top-right corner
   - Shows current progress before quitting
   - Safe to use at any time during the quiz
