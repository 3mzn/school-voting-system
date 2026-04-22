import customtkinter as ctk
import json
import os

# Setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Use the directory where SETUP.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATES_FILE = os.path.join(SCRIPT_DIR, "candidates.json")

# Colors
BG_COLOR = "#1a1a2e"
FG_COLOR = "#252540"
TEXT_COLOR = "white"
BUTTON_COLOR = "#4facfe"

def load_candidates():
    if not os.path.exists(CANDIDATES_FILE):
        data = {"Head Boy": [], "Head Girl": [], "Deputy Head Boy": [], "Deputy Head Girl": []}
        save_candidates(data)
        return data
    with open(CANDIDATES_FILE, "r") as f:
        return json.load(f)

def save_candidates(data):
    with open(CANDIDATES_FILE, "w") as f:
        json.dump(data, f, indent=2)

class SetupApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Candidate Setup")
        self.geometry("600x500")
        self.configure(fg_color=BG_COLOR)
        
        self.candidates = load_candidates()
        self.current_role = "Head Boy"
        
        self._build_ui()

    def _build_ui(self):
        # Role buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        roles = ["Head Boy", "Head Girl", "Deputy Head Boy", "Deputy Head Girl"]
        for role in roles:
            ctk.CTkButton(
                btn_frame, text=role, width=120, height=35,
                fg_color=FG_COLOR, command=lambda r=role: self._switch_role(r)
            ).pack(side="left", padx=5)

        # Title
        self.title_label = ctk.CTkLabel(self, text=f"{self.current_role} Candidates", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        # List frame
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Input frame
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=10)
        
        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="Name", width=180)
        self.name_entry.pack(side="left", padx=5)
        
        self.desc_entry = ctk.CTkEntry(input_frame, placeholder_text="Class/Division", width=180)
        self.desc_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(input_frame, text="Add", width=80, command=self._add_candidate).pack(side="left", padx=5)
        
        # Save button
        ctk.CTkButton(self, text="Save to File", command=self._save).pack(pady=10)
        
        self._refresh_list()

    def _switch_role(self, role):
        self.current_role = role
        self.title_label.configure(text=f"{self.current_role} Candidates")
        self._refresh_list()

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        candidates = self.candidates.get(self.current_role, [])
        
        if not candidates:
            ctk.CTkLabel(self.list_frame, text="(empty)").pack()
            return
        
        for i, c in enumerate(candidates):
            row = ctk.CTkFrame(self.list_frame, fg_color=FG_COLOR)
            row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(row, text=f"{c['name']} - {c['description']}", width=350, anchor="w").pack(side="left", padx=10)
            ctk.CTkButton(row, text="X", width=40, fg_color="red", command=lambda idx=i: self._delete(idx)).pack(side="right", padx=5, pady=5)

    def _add_candidate(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip() or "N/A"
        
        if name:
            if self.current_role not in self.candidates:
                self.candidates[self.current_role] = []
            self.candidates[self.current_role].append({"name": name, "description": desc})
            self.name_entry.delete(0, "end")
            self.desc_entry.delete(0, "end")
            self._refresh_list()

    def _delete(self, index):
        del self.candidates[self.current_role][index]
        self._refresh_list()

    def _save(self):
        save_candidates(self.candidates)
        print("Saved!")

if __name__ == "__main__":
    app = SetupApp()
    app.mainloop()