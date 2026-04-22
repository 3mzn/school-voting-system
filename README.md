# School Leadership Election Voting System

A modern, elegant desktop voting application built with Python and CustomTkinter for conducting school leadership elections.

## Features

- **Modern Dark UI** - Elegant dark theme with electric blue accents (1920x1080 resolution)
- **Token-Based Authentication** - 4-digit token login system with database support (db.txt or db.csv)
- **Double-Voting Prevention** - Prevents voting with same token
- **Candidate Photos** - Display profile photos on candidate cards (falls back to initial if no photo)
- **Flexible Candidate Management** - Use SETUP.py to add/edit/remove candidates with photos
- **Confirmation Screen** - Review selections before final submission
- **Progress Tracking** - 4-step guided voting process
- **Data Persistence** - Votes saved to JSON file with complete records
- **Empty by Default** - No hardcoded candidates, organizer sets them up

## Quick Start

### 1. Install Dependencies
```bash
pip install customtkinter==5.2.2
```

### 2. Setup Candidates (First Time Only)
```bash
python SETUP.py
```
- Click role buttons to switch between positions
- Enter candidate name and class/division
- Click "Add" to add candidates
- Click "Save to File" when done

### 3. Run the Voting App
```bash
python main.py
```

## Project Structure

```
school-voting-system/
├── main.py              # Main voting application
├── SETUP.py             # Candidate setup tool
├── candidates.json      # Candidate data (auto-generated, empty by default)
├── voting_data.json     # Voting records (auto-generated)
├── requirements.txt     # Dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## How It Works

### Setup Phase (SETUP.py)
1. **Run SETUP.py** - Opens candidate management interface
2. **Add Candidates** - Enter name and class/division for each position
3. **Save** - Saves to candidates.json
4. **candidates.json** - Now populated with your candidates

### Voting Phase (main.py)
1. **Token Login** - Enter 4-digit token to authenticate
2. **Candidate Selection** - 2-column grid layout with candidate photos and names
3. **Review Selections** - Confirm all choices before submitting
4. **Submit Vote** - Vote saved to voting_data.json
5. **Thank You** - Auto-redirect to login after 5 seconds

## File Formats

### candidates.json (Empty by Default)
```json
{
  "Head Boy": [],
  "Head Girl": [],
  "Deputy Head Boy": [],
  "Deputy Head Girl": []
}
```

### candidates.json (After Setup)
```json
{
  "Head Boy": [
    {"name": "James Wilson", "description": "Grade 12A", "photo_path": "/path/to/photo1.jpg"},
    {"name": "David Smith", "description": "Grade 12C", "photo_path": "/path/to/photo2.jpg"}
  ],
  "Head Girl": [
    {"name": "Sarah Parker", "description": "Grade 12B", "photo_path": "/path/to/photo3.jpg"}
  ]
}
```

### voting_data.json (Voting Records)
```json
[
  {
    "token": "1234",
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
- **2-Column Grid Layout** - Compact candidate display with larger cards
- **Candidate Photos** - Profile images displayed on cards (120x120px)
- **Hover Effects** - Visual feedback on candidate cards
- **Checkmark Selection** - Clear visual confirmation
- **Progress Header** - Step-by-step guidance (4 steps)
- **Custom Scrollbar** - Blends with dark theme
- **Confirmation Step** - Prevents accidental submissions
- **1920x1080 Resolution** - Full HD display for better visibility

### Data Management
- **JSON Storage** - Human-readable data files
- **Token-Based Authentication** - 4-digit tokens from db.txt or db.csv
- **Token Validation** - Checks token database before allowing vote
- **Complete Records** - Stores token and selections
- **Auto-Initialization** - Creates files if missing
- **Empty by Default** - No hardcoded data
- **Photo Support** - Stores photo paths in candidate records

### Security Features
- **Token-Based Authentication** - 4-digit token login system
- **Token Database** - Supports db.txt or db.csv formats
- **Double-Voting Prevention** - Can't vote twice with same token
- **Input Validation** - All fields required
- **Confirmation Step** - Prevents accidental submissions
- **Data Integrity** - Proper error handling

## SETUP.py Features

- **Add Candidates** - Enter name, class/division, and select a profile photo
- **Edit Candidates** - Modify existing candidates
- **Delete Candidates** - Remove candidates from positions
- **Switch Roles** - Easy navigation between positions
- **Photo Selection** - File explorer to choose candidate photos (JPG, PNG, BMP)
- **Save to File** - Persists all changes to candidates.json
- **Minimal UI** - Simple, non-technical interface

## Workflow

### First Time Setup
```
1. Run: python SETUP.py
2. Add all candidates for each position
3. Click "Save to File"
4. Run: python main.py
5. Students vote
```

### Subsequent Elections
```
1. Run: python SETUP.py
2. Delete old candidates (optional)
3. Add new candidates
4. Click "Save to File"
5. Delete voting_data.json (to reset votes)
6. Run: python main.py
7. Students vote
```

## Dependencies

- Python 3.x
- customtkinter==5.2.2
- darkdetect==0.8.0
- packaging==26.1

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/3mzn/school-voting-system.git
   cd school-voting-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run setup (first time):**
   ```bash
   python SETUP.py
   ```

4. **Run the voting app:**
   ```bash
   python main.py
   ```

## Important Notes

- **Candidates must be set up first** - Use SETUP.py before running main.py
- **No default candidates** - Start with empty candidates.json
- **One-time setup per election** - Set candidates once, don't change during voting
- **Voting records are permanent** - Delete voting_data.json to reset votes
- **Token-based voting** - Each token can only vote once
- **Photo formats** - Supports JPG, JPEG, PNG, BMP images
- **Photo display** - Photos are automatically resized to 120x120px on cards

## License

This project is open source and available under the MIT License.