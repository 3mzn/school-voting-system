"""
TESTING ONLY - Fresh Start
This script completely resets the voting system to a clean state.
WARNING: This will erase ALL data including candidates, votes, and tally.
"""

import json
import os

VOTER_FILE = "voting_data.json"
CANDIDATES_FILE = "candidates.json"
TALLY_FILE = "vote_tally.csv"

def fresh_start():
    """Completely resets the voting system to initial state."""
    
    print("=" * 60)
    print("FRESH START - TESTING ONLY")
    print("=" * 60)
    print()
    print("This will completely reset the voting system:")
    print("  • Clear all voting records (voting_data.json)")
    print("  • Clear all candidates (candidates.json)")
    print("  • Clear vote tally (vote_tally.csv)")
    print()
    print("WARNING: ALL DATA WILL BE PERMANENTLY DELETED!")
    print("This action cannot be undone!")
    print()
    
    # Ask for confirmation
    confirm = input("Type 'DELETE ALL' to confirm fresh start: ").strip().upper()
    
    if confirm != "DELETE ALL":
        print("\nFresh start cancelled.")
        return
    
    print("\nResetting system...")
    
    # 1. Clear voting_data.json
    with open(VOTER_FILE, "w") as f:
        json.dump([], f, indent=2)
    print("✓ Voting records cleared")
    
    # 2. Clear candidates.json
    empty_candidates = {
        "Head Boy": [],
        "Head Girl": [],
        "Deputy Head Boy": [],
        "Deputy Head Girl": []
    }
    with open(CANDIDATES_FILE, "w") as f:
        json.dump(empty_candidates, f, indent=2)
    print("✓ Candidates cleared")
    
    # 3. Clear vote_tally.csv
    with open(TALLY_FILE, "w", newline='', encoding='utf-8') as f:
        f.write("Position,Candidate Name,Class/Division,Vote Count\n")
    print("✓ Vote tally cleared")
    
    print("\n" + "=" * 60)
    print("FRESH START COMPLETE!")
    print("=" * 60)
    print()
    print("The voting system has been reset to a clean state.")
    print("You can now:")
    print("  1. Run SETUP.py to add new candidates")
    print("  2. Run main.py to start fresh voting")
    print()
    print("Note: Token database (db.txt) was NOT modified.")

if __name__ == "__main__":
    # Check if files exist
    missing_files = []
    for file in [VOTER_FILE, CANDIDATES_FILE, TALLY_FILE]:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Error: The following files were not found:")
        for file in missing_files:
            print(f"  • {file}")
        print("\nMake sure you're running this script in the correct directory.")
    else:
        fresh_start()
