# School Leadership Election Voting System

A modern, elegant desktop voting application built with Python and CustomTkinter for conducting school leadership elections.

## Features

- **Modern Dark UI** - Elegant dark theme with electric blue accents
- **Double-Voting Prevention** - Prevents voting with same name (case-insensitive)
- **Candidate Management** - Flexible JSON-based candidate configuration
- **Confirmation Screen** - Review selections before final submission
- **Progress Tracking** - 4-step guided voting process
- **Data Persistence** - Votes saved to JSON file with complete records

## Screens

1. **Voter Registration** - Enter name, class, division
2. **Candidate Selection** - 2-column grid layout with hover effects
3. **Review & Confirm** - Review selections with confirmation checkbox
4. **Thank You** - Success message with auto-redirect

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/school-voting-system.git
   cd school-voting-system
   ```

2. **Install dependencies:**
   ```bash
   pip install customtkinter==5.2.2
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Project Structure

```
school-voting-system/
├── main.py              # Main application
├── candidates.json      # Candidate data (editable)
├── voting_data.json    # Voting records (auto-generated)
├── requirements.txt    # Dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Configuration

### Candidates
Edit `candidates.json` to add/remove candidates:
```json
{
  "Head Boy": [
    {"name": "James Wilson", "description": "Grade 12A"},
    {"name": "David Smith", "description": "Grade 12C"}
  ],
  "Head Girl": [
    {"name": "Sarah Parker", "description": "Grade 12B"}
  ]
}
```

### Voting Data
Votes are saved to `voting_data.json`:
```json
[
  {
    "full_name": "John Doe",
    "class": "12",
    "division": "A",
    "votes": {
      "Head Boy": "James Wilson",
      "Head Girl": "Sarah Parker",
      "Deputy Head Boy": "Michael Brown",
      "Deputy Head Girl": "Jessica Alba"
    }
  }
]
```

## Features in Detail

### UI Design
- **2-Column Grid Layout** - Compact candidate display
- **Hover Effects** - Visual feedback on candidate cards
- **Checkmark Selection** - Clear visual confirmation
- **Progress Header** - Step-by-step guidance
- **Custom Scrollbar** - Blends with dark theme

### Data Management
- **JSON Storage** - Human-readable data files
- **Case-Insensitive Matching** - Prevents duplicate voting
- **Complete Records** - Stores voter info and selections
- **Auto-Initialization** - Creates files if missing

### Security Features
- **Name-Based Prevention** - Can't vote twice with same name
- **Input Validation** - All fields required
- **Confirmation Step** - Prevents accidental submissions
- **Data Integrity** - Proper error handling

## Development

### Dependencies
- Python 3.x
- customtkinter==5.2.2
- darkdetect==0.8.0

### Running Tests
```bash
# Test candidate loading
python -c "import json; print(json.load(open('candidates.json')))"

# Test voting logic
python -c "import main; main.init_files(); print('Files initialized')"
```

## License

This project is open source and available under the MIT License.