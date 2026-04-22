import json
import csv
import os

VOTER_FILE = "voting_data.json"
CANDIDATES_FILE = "candidates.json"
TALLY_FILE = "vote_tally.csv"

def load_candidates():
    """Loads candidate data from the JSON file."""
    try:
        with open(CANDIDATES_FILE, "r") as f:
            candidates_data = json.load(f)
        return candidates_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading candidates: {e}")
        return {
            "Head Boy": [],
            "Head Girl": [],
            "Deputy Head Boy": [],
            "Deputy Head Girl": []
        }

def rebuild_vote_tally():
    """Rebuilds the vote tally CSV from scratch by counting all votes in voting_data.json."""
    # Load all votes
    with open(VOTER_FILE, "r") as f:
        voters = json.load(f)
    
    # Load candidates
    candidates_data = load_candidates()
    
    # Initialize vote counts dictionary
    vote_counts = {}
    positions = ["Head Boy", "Head Girl", "Deputy Head Boy", "Deputy Head Girl"]
    
    for position in positions:
        vote_counts[position] = {}
        for candidate in candidates_data.get(position, []):
            vote_counts[position][candidate["name"]] = 0
    
    # Count all votes
    for voter in voters:
        for position, candidate_name in voter.get("votes", {}).items():
            if candidate_name:
                # Add candidate to vote_counts if not already there
                if position not in vote_counts:
                    vote_counts[position] = {}
                if candidate_name not in vote_counts[position]:
                    vote_counts[position][candidate_name] = 0
                vote_counts[position][candidate_name] += 1
    
    # Write to CSV
    with open(TALLY_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["Position", "Candidate Name", "Class/Division", "Vote Count"])
        
        # Write candidates grouped by position with blank lines between groups
        for i, position in enumerate(positions):
            candidates_list = candidates_data.get(position, [])
            
            # First write candidates from candidates.json
            for candidate in candidates_list:
                count = vote_counts[position].get(candidate["name"], 0)
                writer.writerow([
                    position,
                    candidate["name"],
                    candidate["description"],
                    count
                ])
            
            # Then write any candidates that received votes but aren't in candidates.json
            for candidate_name, count in vote_counts[position].items():
                # Check if this candidate is already in candidates.json
                is_in_json = any(c["name"] == candidate_name for c in candidates_list)
                if not is_in_json and count > 0:
                    writer.writerow([
                        position,
                        candidate_name,
                        "(removed candidate)",
                        count
                    ])
            
            # Add blank line after each position group (except the last one)
            if i < len(positions) - 1:
                writer.writerow(["", "", "", ""])
    
    print(f"Vote tally rebuilt successfully!")
    print(f"Total votes counted: {len(voters)}")

if __name__ == "__main__":
    rebuild_vote_tally()
