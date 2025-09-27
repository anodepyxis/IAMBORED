import customtkinter as ctk
import random
from data import activities_data  # Import the data from data.py

# ========== APP CONFIG ==========
ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # You can change to green, dark-blue, etc.

# Available themes
available_themes = ["blue", "green", "dark-blue", "purple", "red"]
current_theme_index = 0  # Default theme is the first one (blue)

# ========== APP WINDOW ==========
class BoredomBreakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Boredom Breaker")
        self.geometry("600x500")
        self.resizable(False, False)

        # Store current state
        self.current_category = None
        self.current_subcategory = None
        self.current_theme_index = 0  # Default theme index

        # Build UI
        self.create_main_menu()

    # ========== MAIN MENU ==========
    def create_main_menu(self):
        self.clear_widgets()
        
        title = ctk.CTkLabel(self, text="What do you feel like doing?", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(pady=30)

        buttons = [
            ("🧠 Productive", self.open_productive),
            ("💤 Lazy / Non-Productive", self.open_lazy),
            ("🎮 Entertainment", self.open_entertainment),
            ("🧘 Relaxation", self.open_relaxation),
            ("🎲 Random Activity", self.open_random_activity)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(self, text=text, command=command, width=220, height=50)
            btn.pack(pady=10)

        # Theme change button (Light/Dark Mode)
        self.mode_toggle_btn = ctk.CTkButton(self, text="Theme: Dark", command=self.toggle_mode, width=200)
        self.mode_toggle_btn.pack(pady=20)

        # Change theme button
        self.theme_toggle_btn = ctk.CTkButton(self, text="Theme: Blue", command=self.change_theme, width=200)
        self.theme_toggle_btn.pack(pady=20)

    # ========== CATEGORY NAVIGATION ==========
    def open_productive(self):
        self.current_category = "Productive"
        self.show_subcategories(["Learning & Skill-Building", "Personal Organization", "Creative Projects"])

    def open_lazy(self):
        self.current_category = "Lazy"
        self.show_subcategories(["Random & Time-Wasting", "Unfocused Tasks"])

    def open_entertainment(self):
        self.current_category = "Entertainment"
        self.show_subcategories(["Digital Entertainment", "Social Entertainment", "Creative Fun"])

    def open_relaxation(self):
        self.current_category = "Relaxation"
        self.show_subcategories(["Mind & Body", "Calm & Low-Energy"])

    def open_random_activity(self):
        self.clear_widgets()

        label = ctk.CTkLabel(self, text="Random Activity", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        # Get a random activity from any category and subcategory
        all_categories = list(activities_data.keys())
        random_category = random.choice(all_categories)
        random_subcategory = random.choice(list(activities_data[random_category].keys()))
        random_activity = random.choice(activities_data[random_category][random_subcategory])

        # Display the random activity
        random_label = ctk.CTkLabel(self, text=f"• {random_activity}", wraplength=500, justify="left")
        random_label.pack(pady=5, anchor="w", padx=40)

        # Button to try again (randomly pick another activity)
        try_again_btn = ctk.CTkButton(self, text="Try Again", command=self.open_random_activity, width=200)
        try_again_btn.pack(pady=20)

        # Button to go back to the home menu
        back_home_btn = ctk.CTkButton(self, text="Go Back Home", command=self.create_main_menu, width=200)
        back_home_btn.pack(pady=30)

    # ========== SHOW SUBCATEGORIES ==========
    def show_subcategories(self, subcategories):
        self.clear_widgets()

        label = ctk.CTkLabel(self, text=f"{self.current_category} Activities", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

        for sub in subcategories:
            btn = ctk.CTkButton(self, text=sub, width=250, command=lambda s=sub: self.show_activities(s))
            btn.pack(pady=8)

        back_btn = ctk.CTkButton(self, text="← Back", command=self.create_main_menu, width=120)
        back_btn.pack(pady=30)

    # ========== SHOW ACTIVITIES ==========
    def show_activities(self, subcategory):
        self.clear_widgets()
        self.current_subcategory = subcategory

        label = ctk.CTkLabel(self, text=f"{subcategory}", font=ctk.CTkFont(size=18, weight="bold"))
        label.pack(pady=20)

        # Get activities from the data
        suggestions = activities_data.get(self.current_category, {}).get(subcategory, ["No data found"])
        random.shuffle(suggestions)
        selected = suggestions[:3]

        for idea in selected:
            idea_label = ctk.CTkLabel(self, text=f"• {idea}", wraplength=500, justify="left")
            idea_label.pack(pady=5, anchor="w", padx=40)

        back_btn = ctk.CTkButton(self, text="← Back", command=lambda: self.show_subcategories(list(activities_data[self.current_category].keys())))
        back_btn.pack(pady=30)

    # ========== THEME TOGGLE ==========
    def toggle_mode(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.mode_toggle_btn.configure(text="Theme: Light")
        else:
            ctk.set_appearance_mode("Dark")
            self.mode_toggle_btn.configure(text="Theme: Dark")

    # ========== CHANGE COLOR THEME ==========
    def change_theme(self):
        # Get the next theme from the list
        self.current_theme_index = (self.current_theme_index + 1) % len(available_themes)
        new_theme = available_themes[self.current_theme_index]

        # Set the new theme
        ctk.set_default_color_theme(new_theme)

        # Update the theme button text to reflect the current theme
        self.theme_toggle_btn.configure(text=f"Theme: {new_theme.capitalize()}")

    # ========== HELPER ==========
    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

# ========== RUN APP ==========
if __name__ == "__main__":
    app = BoredomBreakerApp()
    app.mainloop()
