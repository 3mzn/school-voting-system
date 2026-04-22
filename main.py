import customtkinter as ctk
import json
import os
import csv
from PIL import Image

# ==============================================================================
# SECTION 1: COLORS AND SETTINGS
# ==============================================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Hex colors for the "Modern Elegance" theme
BG_BASE      = "#0f0f1a"
BG_SURFACE   = "#1a1a2e"
BG_CARD      = "#252540"
ACCENT_PRIMARY = "#4facfe"  # Electric blue
ACCENT_GOLD    = "#f5c842"
ACCENT_SUCCESS = "#3ecf8e"
COLOR_WHITE    = "#f0f0ff"
COLOR_DIM      = "#8888aa"
COLOR_BORDER   = "#2a2a4a"
COLOR_SUBTEXT  = "#66667a"

# ==============================================================================
# SECTION 2: DATA MANAGEMENT (MEMORY)
# This handles the files so we remember who voted and what the results are.
# ==============================================================================

VOTER_FILE = "voting_data.json"
CANDIDATES_FILE = "candidates.json"
TOKEN_DB_FILE = "db.txt"
TALLY_FILE = "vote_tally.csv"

def load_tokens():
    """Load valid tokens from db.txt file."""
    if not os.path.exists(TOKEN_DB_FILE):
        # Create default token file if it doesn't exist
        with open(TOKEN_DB_FILE, "w") as f:
            f.write("1234\n5678\n9012\n")
        return ["1234", "5678", "9012"]
    
    with open(TOKEN_DB_FILE, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]
    return tokens

def is_valid_token(token):
    """Check if the token exists in the database."""
    valid_tokens = load_tokens()
    return token in valid_tokens

def init_files():
    """Checks if our data files exist yet. If not, it creates them."""
    # Create the voting data file if it doesn't exist
    if not os.path.exists(VOTER_FILE):
        with open(VOTER_FILE, "w") as f:
            json.dump([], f) # Start with an empty list
    
    # Create the candidates file if it doesn't exist (empty - organizer adds via SETUP.py)
    if not os.path.exists(CANDIDATES_FILE):
        empty_candidates = {
            "Head Boy": [],
            "Head Girl": [],
            "Deputy Head Boy": [],
            "Deputy Head Girl": []
        }
        with open(CANDIDATES_FILE, "w") as f:
            json.dump(empty_candidates, f, indent=2)
    
    # Create the vote tally CSV if it doesn't exist
    if not os.path.exists(TALLY_FILE):
        init_vote_tally()

def init_vote_tally():
    """Creates the vote tally CSV file with all candidates initialized to 0 votes."""
    candidates_data = load_candidates()
    
    # Define the order of positions
    positions = ["Head Boy", "Head Girl", "Deputy Head Boy", "Deputy Head Girl"]
    
    with open(TALLY_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["Position", "Candidate Name", "Class/Division", "Vote Count"])
        
        # Write candidates grouped by position with blank lines between groups
        for i, position in enumerate(positions):
            candidates_list = candidates_data.get(position, [])
            
            for candidate in candidates_list:
                writer.writerow([
                    position,
                    candidate["name"],
                    candidate["description"],
                    0  # Initialize with 0 votes
                ])
            
            # Add blank line after each position group (except the last one)
            if i < len(positions) - 1:
                writer.writerow(["", "", "", ""])

def update_vote_tally(votes):
    """Updates the vote tally CSV by incrementing counts for the voted candidates."""
    # Read the entire CSV into memory
    rows = []
    with open(TALLY_FILE, "r", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Update vote counts for each position
    for position, candidate_name in votes.items():
        if candidate_name:  # Only update if a candidate was selected
            # Find the row for this candidate and increment their vote count
            for i, row in enumerate(rows):
                # Skip header and blank rows
                if i == 0 or len(row) < 4 or row[0] == "":
                    continue
                
                # Check if this row matches the position and candidate name
                if row[0] == position and row[1] == candidate_name:
                    # Increment the vote count
                    current_count = int(row[3]) if row[3].isdigit() else 0
                    rows[i][3] = str(current_count + 1)
                    break
    
    # Write the updated data back to the CSV
    with open(TALLY_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

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
            if candidate_name and position in vote_counts and candidate_name in vote_counts[position]:
                vote_counts[position][candidate_name] += 1
    
    # Write to CSV
    with open(TALLY_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # Write header
        writer.writerow(["Position", "Candidate Name", "Class/Division", "Vote Count"])
        
        # Write candidates grouped by position with blank lines between groups
        for i, position in enumerate(positions):
            candidates_list = candidates_data.get(position, [])
            
            for candidate in candidates_list:
                count = vote_counts[position].get(candidate["name"], 0)
                writer.writerow([
                    position,
                    candidate["name"],
                    candidate["description"],
                    count
                ])
            
            # Add blank line after each position group (except the last one)
            if i < len(positions) - 1:
                writer.writerow(["", "", "", ""])

def load_candidates():
    """Loads candidate data from the JSON file."""
    try:
        with open(CANDIDATES_FILE, "r") as f:
            candidates_data = json.load(f)
        return candidates_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading candidates: {e}")
        # Return default structure if file is corrupted
        return {
            "Head Boy": [],
            "Head Girl": [],
            "Deputy Head Boy": [],
            "Deputy Head Girl": []
        }

def has_voted(token):
    """Checks if this token has already been used to vote."""
    with open(VOTER_FILE, "r") as f:
        voters = json.load(f)
    
    # Check if token exists in voters list
    for voter in voters:
        if voter.get("token") == token:
            return True
    return False

def save_vote(token, votes):
    """Saves the vote with the token."""
    
    # 1. Load existing voters
    with open(VOTER_FILE, "r") as f:
        voters = json.load(f)
    
    # 2. Create new voter record
    voter_record = {
        "token": token,
        "votes": {
            "Head Boy": votes["Head Boy"],
            "Head Girl": votes["Head Girl"],
            "Deputy Head Boy": votes["Deputy Head Boy"],
            "Deputy Head Girl": votes["Deputy Head Girl"]
        }
    }
    
    # 3. Add to voters list
    voters.append(voter_record)
    
    # 4. Save back to file
    with open(VOTER_FILE, "w") as f:
        json.dump(voters, f, indent=2)
    
    # 5. Update the vote tally CSV
    update_vote_tally(votes)

# ==============================================================================
# SECTION 3: THE BUILDING BLOCKS (WIDGETS)
# ==============================================================================

class CandidateCard(ctk.CTkFrame):
    """
    A blueprint for a single candidate card in a compact grid layout.
    """
    def __init__(self, master, name, description, photo_path, on_click_callback):
        super().__init__(
            master, 
            corner_radius=12, 
            fg_color=BG_CARD, 
            border_width=2, 
            border_color=COLOR_BORDER
        )
        
        self.name = name
        self.description = description
        self.photo_path = photo_path
        self.is_selected = False
        self.callback = on_click_callback

        # AVATAR - Photo or gradient circle with letter
        self.avatar = ctk.CTkFrame(self, width=120, height=120, corner_radius=12, fg_color="transparent")
        self.avatar.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")
        
        # Try to load photo, fallback to initial letter
        if photo_path and os.path.exists(photo_path):
            try:
                # Normalize path (convert backslashes to forward slashes)
                normalized_path = photo_path.replace("\\", "/")
                
                # Load and resize image
                img = Image.open(normalized_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                
                # Create CTkImage for dark mode compatibility
                photo = ctk.CTkImage(light_image=img, dark_image=img, size=(120, 120))
                
                # Display photo using place to avoid grid/pack conflicts
                photo_label = ctk.CTkLabel(self.avatar, image=photo, text="")
                photo_label.image = photo  # Keep reference
                photo_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception as e:
                print(f"Error loading photo for {name}: {e}")
                self._create_initial_avatar()
        else:
            self._create_initial_avatar()

        # TEXT AREA
        self.text_area = ctk.CTkFrame(self, fg_color="transparent")
        self.text_area.grid(row=0, column=1, columnspan=2, sticky="w", pady=12)

        self.label_name = ctk.CTkLabel(
            self.text_area, 
            text=name, 
            text_color=COLOR_WHITE,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.label_name.pack(anchor="w")

        self.label_desc = ctk.CTkLabel(
            self.text_area, 
            text=description, 
            text_color=COLOR_SUBTEXT,
            font=ctk.CTkFont(size=12)
        )
        self.label_desc.pack(anchor="w")

        # CHECKMARK ICON (hidden by default)
        self.checkmark = ctk.CTkLabel(
            self, 
            text="✓", 
            width=30, 
            height=30, 
            corner_radius=15,
            fg_color=ACCENT_SUCCESS,
            text_color=COLOR_WHITE,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.checkmark.grid(row=0, column=3, padx=10, pady=12)
        self.checkmark.grid_remove()  # Hide initially

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # Make entire card clickable
        widgets = [self, self.avatar, self.text_area, self.label_name, self.label_desc]
        for w in widgets:
            w.bind("<Button-1>", self._handle_click)
            w.bind("<Enter>", self._handle_hover_on)
            w.bind("<Leave>", self._handle_hover_off)

    def _create_initial_avatar(self):
        """Create fallback avatar with initial letter."""
        # Gradient effect using two overlapping circles
        self.avatar_inner = ctk.CTkFrame(self.avatar, width=120, height=120, corner_radius=12, fg_color="#4b44cc")
        self.avatar_inner.place(relx=0.5, rely=0.5, anchor="center")
        
        self.avatar_letter = ctk.CTkLabel(
            self.avatar_inner, 
            text=self.name[0], 
            text_color=COLOR_WHITE,
            font=ctk.CTkFont(size=48, weight="bold")
        )
        self.avatar_letter.place(relx=0.5, rely=0.5, anchor="center")

    def _handle_hover_on(self, _):
        if not self.is_selected:
            self.configure(border_color=ACCENT_PRIMARY)

    def _handle_hover_off(self, _):
        if not self.is_selected:
            self.configure(border_color=COLOR_BORDER)

    def _handle_click(self, _):
        self.callback(self)

    def set_active(self, should_be_active):
        self.is_selected = should_be_active
        if should_be_active:
            self.configure(border_color=ACCENT_PRIMARY, fg_color="#2a2a4a")
            self.checkmark.grid()
            # Add glow effect
            self.configure(fg_color="#2a2a4a")
        else:
            self.configure(border_color=COLOR_BORDER, fg_color=BG_CARD)
            self.checkmark.grid_remove()


# ==============================================================================
# SECTION 4: THE MAIN APPLICATION W/ MULTIPLE SCREENS
# ==============================================================================

class VotingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("School Leadership Election")
        self.geometry("1920x1080")
        self.configure(fg_color=BG_BASE)
        self.attributes("-alpha", 0)

        # Ensure our data files are ready
        init_files()

        # --- APP STATE ---
        self.current_token = ""
        self.selections = {"Head Boy": None, "Head Girl": None, "Deputy Head Boy": None, "Deputy Head Girl": None}
        self.cards_list = []
        self.current_step = 0  # Track progress

        # Containers for different screens so we can easily swap them
        self.header_frame = None
        self.progress_frame = None
        self.current_screen = None # Keeps track of whatever screen is currently showing

        # Build everything
        self._setup_header()
        
        # We start by showing the login screen
        self._show_login_screen()

        # Fade in
        self._animate_fade_in()

    # --- GENERAL UI METHODS ---

    def _setup_header(self):
        self.header_frame = ctk.CTkFrame(self, height=100, fg_color=BG_SURFACE, corner_radius=0)
        self.header_frame.pack(fill="x")
        
        # Main title
        title = ctk.CTkLabel(
            self.header_frame, text="🗳  OFFICIAL VOTING BOOTH", 
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_WHITE
        )
        title.place(relx=0.5, rely=0.35, anchor="center")
        
        # Progress sub-label
        self.progress_label = ctk.CTkLabel(
            self.header_frame, 
            text="Step 1 of 3: Voter Registration", 
            font=ctk.CTkFont(size=13), 
            text_color=COLOR_DIM
        )
        self.progress_label.place(relx=0.5, rely=0.7, anchor="center")

    def _update_progress(self, step, text):
        """Update the progress header with current step and description."""
        steps = [
            "Step 1 of 4: Voter Registration",
            "Step 2 of 4: Selecting Candidates",
            "Step 3 of 4: Review Selections",
            "Step 4 of 4: Thank You"
        ]
        if step < len(steps):
            self.progress_label.configure(text=steps[step])

    def _clear_screen(self):
        """Hides the current main content area so we can replace it with a new one."""
        if self.current_screen is not None:
            self.current_screen.pack_forget()

    # --- SCREEN 1: THE LOGIN / GATEKEEPER ---

    def _show_login_screen(self):
        self._clear_screen()
        
        # Update progress
        self._update_progress(0, "Step 1 of 4: Token Authentication")

        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both")

        # Center box container
        login_box = ctk.CTkFrame(self.current_screen, fg_color=BG_SURFACE, corner_radius=15)
        login_box.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            login_box, text="Voter Authentication", 
            font=ctk.CTkFont(size=26, weight="bold"), text_color=COLOR_WHITE
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            login_box, text="Please enter your 4-digit token to proceed.", 
            font=ctk.CTkFont(size=14), text_color=COLOR_DIM
        ).pack(pady=(0, 20), padx=40)

        # Token input
        self.token_entry = ctk.CTkEntry(login_box, placeholder_text="Enter 4-digit token", width=280, height=45)
        self.token_entry.pack(pady=10)

        # Label to show errors
        self.error_label = ctk.CTkLabel(login_box, text="", text_color="#ff4d4d", font=ctk.CTkFont(size=12))
        self.error_label.pack(pady=5)

        ctk.CTkButton(
            login_box, text="Proceed to Ballot", 
            font=ctk.CTkFont(size=16, weight="bold"), width=280, height=50,
            fg_color=ACCENT_PRIMARY, hover_color="#3a8ad6",
            corner_radius=12,
            command=self._handle_login_click
        ).pack(pady=(10, 30))

    def _handle_login_click(self):
        """Checks the token when they try to proceed."""
        token = self.token_entry.get().strip()

        if not token:
            self.error_label.configure(text="Please enter a token.")
            return

        if not is_valid_token(token):
            self.error_label.configure(text="Invalid token. Please try again.")
            return

        if has_voted(token):
            self.error_label.configure(text="Error: This token has already been used!")
            return

        # Token is valid and unused! Save it temporarily.
        self.current_token = token

        # Move to the next screen
        self._show_ballot_screen()

    # --- SCREEN 2: THE BALLOT ---

    def _show_ballot_screen(self):
        self._clear_screen()
        
        # Reset the vote selections for this new person
        for key in self.selections:
            self.selections[key] = None
        self.cards_list.clear() 

        # Update progress
        self._update_progress(1, "Step 2 of 3: Selecting Candidates")

        # Main container
        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both", padx=30, pady=20)

        # Scrollable area for ballot
        scroll_frame = ctk.CTkScrollableFrame(self.current_screen, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Configure scrollbar to blend in
        scroll_frame._scrollbar.configure(width=8, fg_color=BG_BASE, button_color=COLOR_BORDER)

        # Load candidates from JSON file
        candidates_data = load_candidates()
        
        # Draw the cards in a 2-column grid
        for role, candidates_list in candidates_data.items():
            # Role header with horizontal line
            header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            header_frame.pack(fill="x", pady=(25, 10))
            
            role_label = ctk.CTkLabel(
                header_frame, 
                text=role.upper(), 
                font=ctk.CTkFont(size=14, weight="bold"), 
                text_color=ACCENT_PRIMARY
            )
            role_label.pack(side="left")
            
            # Horizontal line
            line = ctk.CTkFrame(header_frame, height=2, fg_color=ACCENT_PRIMARY, width=100)
            line.pack(side="left", padx=(10, 0))

            # Create 2-column grid for candidates
            candidates_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            candidates_frame.pack(fill="x", pady=(0, 20))

            for i, candidate in enumerate(candidates_list):
                # Calculate grid position for 2-column layout
                col = i % 2
                row = i // 2
                
                card = CandidateCard(
                    master=candidates_frame, 
                    name=candidate["name"], 
                    description=candidate["description"], 
                    photo_path=candidate.get("photo_path", ""),
                    on_click_callback=self._process_selection
                )
                card.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
                card.category = role
                self.cards_list.append(card)

            # Configure grid columns for this role's candidates
            candidates_frame.grid_columnconfigure(0, weight=1)
            candidates_frame.grid_columnconfigure(1, weight=1)

        # The Footer for submitting
        footer = ctk.CTkFrame(self.current_screen, height=90, fg_color=BG_SURFACE, corner_radius=0)
        footer.pack(fill="x", side="bottom")

        self.submit_error_label = ctk.CTkLabel(footer, text="", text_color="#ff4d4d", font=ctk.CTkFont(size=12))
        self.submit_error_label.place(relx=0.5, rely=0.25, anchor="center")

        submit_btn = ctk.CTkButton(
            footer, 
            text="Review & Submit", 
            fg_color=ACCENT_SUCCESS, 
            hover_color="#2fa870",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=400, 
            height=50, 
            corner_radius=12,
            command=self._handle_submit_click
        )
        submit_btn.place(relx=0.5, rely=0.6, anchor="center")
        
        # Add glow effect to submit button
        submit_btn._hover_color = "#2fa870"

    def _process_selection(self, clicked_card):
        # Same as before, handles clicking logic
        role = clicked_card.category
        
        for card in self.cards_list:
            if card.category == role:
                card.set_active(False)
        
        clicked_card.set_active(True)
        self.selections[role] = clicked_card.name

    def _handle_submit_click(self):
        missing = [role for role, vote in self.selections.items() if vote is None]
        
        if missing:
            self.submit_error_label.configure(text=f"Please vote for: {', '.join(missing)}")
        else:
            # All selections made, show confirmation screen
            self._show_review_screen()

    # --- SCREEN 3: REVIEW & CONFIRMATION ---

    def _show_review_screen(self):
        self._clear_screen()
        
        # Update progress
        self._update_progress(2, "Step 3 of 4: Review Selections")

        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both", padx=40, pady=30)

        # Title
        title = ctk.CTkLabel(
            self.current_screen, 
            text="Please confirm your selections:", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            text_color=COLOR_WHITE
        )
        title.pack(pady=(0, 30))

        # Selections display
        selections_frame = ctk.CTkFrame(self.current_screen, fg_color=BG_SURFACE, corner_radius=12)
        selections_frame.pack(fill="x", pady=(0, 30), padx=20)

        # Display each selection
        for role, candidate in self.selections.items():
            selection_row = ctk.CTkFrame(selections_frame, fg_color="transparent")
            selection_row.pack(fill="x", pady=12, padx=20)

            role_label = ctk.CTkLabel(
                selection_row,
                text=f"{role}:",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=ACCENT_PRIMARY,
                width=180,
                anchor="w"
            )
            role_label.pack(side="left")

            candidate_label = ctk.CTkLabel(
                selection_row,
                text=candidate,
                font=ctk.CTkFont(size=16),
                text_color=COLOR_WHITE,
                anchor="w"
            )
            candidate_label.pack(side="left", padx=(10, 0))

        # Confirmation checkbox
        self.confirm_var = ctk.BooleanVar(value=False)
        
        checkbox_frame = ctk.CTkFrame(self.current_screen, fg_color="transparent")
        checkbox_frame.pack(pady=(0, 30))

        self.confirm_checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="I confirm these selections are correct",
            variable=self.confirm_var,
            font=ctk.CTkFont(size=14),
            text_color=COLOR_WHITE,
            command=self._update_confirm_button_state
        )
        self.confirm_checkbox.pack()

        # Confirm button (initially disabled)
        self.confirm_button = ctk.CTkButton(
            self.current_screen,
            text="Confirm & Submit Vote",
            fg_color=ACCENT_SUCCESS,
            hover_color="#2fa870",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=400,
            height=50,
            corner_radius=12,
            state="disabled",
            command=self._handle_final_submit
        )
        self.confirm_button.pack(pady=(0, 20))

        # Back button
        back_button = ctk.CTkButton(
            self.current_screen,
            text="← Go Back to Ballot",
            fg_color="transparent",
            hover_color=BG_SURFACE,
            font=ctk.CTkFont(size=14),
            text_color=COLOR_DIM,
            width=200,
            height=40,
            corner_radius=8,
            command=self._show_ballot_screen
        )
        back_button.pack()

    def _update_confirm_button_state(self):
        """Enable/disable the confirm button based on checkbox state."""
        if self.confirm_var.get():
            self.confirm_button.configure(state="normal")
        else:
            self.confirm_button.configure(state="disabled")

    def _handle_final_submit(self):
        """Final submission after confirmation."""
        # Save the vote to data files
        save_vote(self.current_token, self.selections)
        # Move to thank you screen
        self._show_thankyou_screen()

    # --- SCREEN 4: THANK YOU & RESET ---

    def _show_thankyou_screen(self):
        self._clear_screen()
        
        # Update progress
        self._update_progress(3, "Step 4 of 4: Thank You")

        self.current_screen = ctk.CTkFrame(self, fg_color="transparent")
        self.current_screen.pack(expand=True, fill="both")

        message = (
            "✔️\n\n"
            "Your vote has been securely submitted.\n"
            "Thank you for participating!"
        )

        success_msg = ctk.CTkLabel(
            self.current_screen, text=message, 
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COLOR_WHITE,
            justify="center"
        )
        success_msg.place(relx=0.5, rely=0.5, anchor="center")

        # Critical feature: after 5,000 milliseconds (5 seconds), go back to login automatically.
        self.after(5000, self._show_login_screen)

    # --- ANIMATIONS ---

    def _animate_fade_in(self):
        current_alpha = self.attributes("-alpha")
        if current_alpha < 1.0:
            current_alpha += 0.05
            self.attributes("-alpha", current_alpha)
            self.after(15, self._animate_fade_in)


if __name__ == "__main__":
    app = VotingApp()
    app.mainloop()
