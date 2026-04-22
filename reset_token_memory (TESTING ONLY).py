"""
TESTING ONLY - Reset Token Memory
This script clears the voting_data.json file so tokens can be reused for testing.
WARNING: This will erase all voting records but keep candidates and tally data.
"""

import json
import os

VOTER_FILE = "voting_data.json"

def reset_token_memory():
    """Clears all voting records so tokens can be reused."""
    
    print("=" * 60)
    print("RESET TOKEN MEMORY - TESTING ONLY")
    print("=" * 60)
    print()
    print("This will clear all voting records from voting_data.json")
    print("Tokens will be able to vote again.")
    print()
    print("WARNING: This action cannot be undone!")
    print()
    
    # Ask for confirmation
    confirm = input("Type 'YES' to confirm reset: ").strip().upper()
    
    if confirm != "YES":
        print("\nReset cancelled.")
        return
    
    # Clear voting_data.json
    with open(VOTER_FILE, "w") as f:
        json.dump([], f, indent=2)
    
    print("\n✓ Token memory reset successfully!")
    print("✓ All tokens can now be reused for voting.")
    print("\nNote: Candidates and tally data were NOT affected.")
    print("Run 'rebuild_tally.py' to reset the vote counts in the CSV.")

if __name__ == "__main__":
    if os.path.exists(VOTER_FILE):
        reset_token_memory()
    else:
        print(f"Error: {VOTER_FILE} not found!")
        print("Make sure you're running this script in the correct directory.")
