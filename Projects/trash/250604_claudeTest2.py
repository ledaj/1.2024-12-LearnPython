import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Letter:
    recipient: str
    address: str
    location: str
    delivered: bool = False
    
    def __str__(self):
        return f"{self.recipient} - {self.address}"

class LetterDeliveryGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Letter Delivery Clicker")
        self.root.geometry("1000x700")
        
        # Game state
        self.current_day = 1
        self.score = 0
        self.letters_delivered = 0
        self.wrong_deliveries = 0
        self.game_running = False
        self.day_start_time = 0
        self.day_duration = 120  # 2 minutes per day
        
        # Letter management
        self.daily_letters = []
        self.sorted_letters = {}  # location -> [letters]
        
        # Locations and their address mappings
        self.locations = ["Downtown", "Suburbs", "Industrial", "Residential"]
        self.location_addresses = {
            "Downtown": ["Main St", "First St", "Second Ave", "Broadway", "Central Ave"],
            "Suburbs": ["Oak Ave", "Pine Rd", "Maple Ct", "Cedar Ln", "Willow Dr"],
            "Industrial": ["Factory Rd", "Warehouse Ave", "Industrial Blvd", "Commerce St", "Plant Dr"],
            "Residential": ["Elm Dr", "Birch Ln", "Sunset Dr", "Park Ave", "Garden St"]
        }
        
        # UI Components
        self.setup_ui()
        self.generate_daily_letters()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.columnconfigure(2, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Top info panel
        self.setup_info_panel(main_frame)
        
        # Main game area
        game_frame = ttk.Frame(main_frame)
        game_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        game_frame.columnconfigure(0, weight=1)
        game_frame.columnconfigure(1, weight=2)
        game_frame.rowconfigure(0, weight=1)
        
        # Letter sorting area (left side)
        self.setup_sorting_area(game_frame)
        
        # Delivery locations (center)
        self.setup_delivery_area(game_frame)
        
        # Address register/map (right side)
        self.setup_address_register(main_frame)
        
        # Control buttons
        self.setup_controls(main_frame)
        
    def setup_address_register(self, parent):
        """Setup the address register/map on the right side"""
        register_frame = ttk.LabelFrame(parent, text="Address Register", padding="10")
        register_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        register_frame.columnconfigure(0, weight=1)
        register_frame.rowconfigure(0, weight=1)
        
        # Create notebook for tabbed view
        notebook = ttk.Notebook(register_frame)
        notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create a tab for each location
        for location in self.locations:
            tab_frame = ttk.Frame(notebook, padding="5")
            notebook.add(tab_frame, text=location)
            
            # Title
            ttk.Label(tab_frame, text=f"{location} Streets:", 
                     font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
            
            # List of streets for this location
            streets_text = tk.Text(tab_frame, height=15, width=20, wrap=tk.WORD, 
                                 font=("Arial", 9), state=tk.DISABLED)
            streets_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            tab_frame.rowconfigure(1, weight=1)
            tab_frame.columnconfigure(0, weight=1)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=streets_text.yview)
            scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
            streets_text.configure(yscrollcommand=scrollbar.set)
            
            # Populate with street names
            streets_text.config(state=tk.NORMAL)
            for street in self.location_addresses[location]:
                streets_text.insert(tk.END, f"• {street}\n")
            streets_text.config(state=tk.DISABLED)
        
        # Add a "Quick Reference" tab
        quick_ref_frame = ttk.Frame(notebook, padding="5")
        notebook.add(quick_ref_frame, text="Quick Ref")
        
        quick_ref_text = tk.Text(quick_ref_frame, height=15, width=25, wrap=tk.WORD, 
                               font=("Arial", 8), state=tk.DISABLED)
        quick_ref_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        quick_ref_frame.rowconfigure(0, weight=1)
        quick_ref_frame.columnconfigure(0, weight=1)
        
        # Add quick reference content
        quick_ref_text.config(state=tk.NORMAL)
        for location in self.locations:
            quick_ref_text.insert(tk.END, f"{location.upper()}:\n", "header")
            for street in self.location_addresses[location]:
                quick_ref_text.insert(tk.END, f"  {street}\n")
            quick_ref_text.insert(tk.END, "\n")
        
        # Configure text tags for formatting
        quick_ref_text.tag_configure("header", font=("Arial", 9, "bold"))
        quick_ref_text.config(state=tk.DISABLED)
        
    def setup_info_panel(self, parent):
        info_frame = ttk.Frame(parent)
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Day and time info
        self.day_label = ttk.Label(info_frame, text=f"Day {self.current_day}", font=("Arial", 14, "bold"))
        self.day_label.grid(row=0, column=0, padx=(0, 20))
        
        self.time_label = ttk.Label(info_frame, text="Time: 00:00", font=("Arial", 12))
        self.time_label.grid(row=0, column=1, padx=(0, 20))
        
        # Score info
        self.score_label = ttk.Label(info_frame, text=f"Score: {self.score}", font=("Arial", 12))
        self.score_label.grid(row=0, column=2, padx=(0, 20))
        
        self.delivered_label = ttk.Label(info_frame, text=f"Delivered: {self.letters_delivered}", font=("Arial", 12))
        self.delivered_label.grid(row=0, column=3, padx=(0, 20))
        
        self.wrong_label = ttk.Label(info_frame, text=f"Wrong: {self.wrong_deliveries}", font=("Arial", 12))
        self.wrong_label.grid(row=0, column=4)
        
    def setup_sorting_area(self, parent):
        sorting_frame = ttk.LabelFrame(parent, text="Letter Sorting", padding="10")
        sorting_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        sorting_frame.columnconfigure(0, weight=1)
        sorting_frame.rowconfigure(1, weight=1)
        
        # Unsorted letters list
        ttk.Label(sorting_frame, text="Unsorted Letters:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        
        # Listbox for unsorted letters
        self.unsorted_listbox = tk.Listbox(sorting_frame, height=8)
        self.unsorted_listbox.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 10))
        
        # Sorting buttons
        sort_buttons_frame = ttk.Frame(sorting_frame)
        sort_buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        for i, location in enumerate(self.locations):
            btn = ttk.Button(sort_buttons_frame, text=f"Sort to {location}", 
                           command=lambda loc=location: self.sort_letter(loc))
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky=(tk.W, tk.E))
            sort_buttons_frame.columnconfigure(i%2, weight=1)
    
    def setup_delivery_area(self, parent):
        delivery_frame = ttk.LabelFrame(parent, text="Delivery Locations", padding="10")
        delivery_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        delivery_frame.columnconfigure(0, weight=1)
        delivery_frame.columnconfigure(1, weight=1)
        
        self.location_frames = {}
        self.location_listboxes = {}
        self.delivery_buttons = {}
        
        for i, location in enumerate(self.locations):
            # Create frame for each location
            loc_frame = ttk.LabelFrame(delivery_frame, text=location, padding="5")
            loc_frame.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
            loc_frame.columnconfigure(0, weight=1)
            loc_frame.rowconfigure(0, weight=1)
            
            # Listbox for sorted letters
            listbox = tk.Listbox(loc_frame, height=6)
            listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Delivery button
            btn = ttk.Button(loc_frame, text="Deliver Selected", 
                           command=lambda loc=location: self.deliver_letter(loc))
            btn.grid(row=1, column=0, pady=(5, 0), sticky=(tk.W, tk.E))
            
            self.location_frames[location] = loc_frame
            self.location_listboxes[location] = listbox
            self.delivery_buttons[location] = btn
        
        # Configure grid weights for location frames
        for i in range(2):
            delivery_frame.rowconfigure(i, weight=1)
    
    def setup_controls(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0))
        
        self.start_button = ttk.Button(control_frame, text="Start Day", command=self.start_day)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.next_day_button = ttk.Button(control_frame, text="Next Day", command=self.next_day, state="disabled")
        self.next_day_button.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="Reset Game", command=self.reset_game).grid(row=0, column=2)
    
    def generate_daily_letters(self):
        """Generate random letters for the day"""
        names = ["John Smith", "Mary Johnson", "Bob Wilson", "Alice Brown", "Tom Davis", 
                "Emma Miller", "James Garcia", "Linda Rodriguez", "David Martinez", "Sarah Lopez"]
        
        num_letters = min(8 + self.current_day * 2, 20)  # Increase difficulty
        self.daily_letters = []
        
        for i in range(num_letters):
            recipient = random.choice(names)
            
            # Choose a random location first, then pick a street from that location
            location = random.choice(self.locations)
            street = random.choice(self.location_addresses[location])
            house_num = random.randint(100, 999)
            address = f"{house_num} {street}"
            
            letter = Letter(recipient, address, location)
            self.daily_letters.append(letter)
        
        # Initialize sorted letters dict
        self.sorted_letters = {loc: [] for loc in self.locations}
        
        # Update unsorted letters display
        self.update_unsorted_display()
    
    def update_unsorted_display(self):
        """Update the unsorted letters listbox"""
        self.unsorted_listbox.delete(0, tk.END)
        for letter in self.daily_letters:
            if not letter.delivered:
                self.unsorted_listbox.insert(tk.END, str(letter))
    
    def update_sorted_displays(self):
        """Update all location listboxes"""
        for location in self.locations:
            listbox = self.location_listboxes[location]
            listbox.delete(0, tk.END)
            for letter in self.sorted_letters[location]:
                if not letter.delivered:
                    listbox.insert(tk.END, str(letter))
    
    def sort_letter(self, target_location):
        """Sort selected letter to target location"""
        selection = self.unsorted_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a letter to sort!")
            return
        
        # Find the letter in daily_letters
        selected_text = self.unsorted_listbox.get(selection[0])
        selected_letter = None
        
        for letter in self.daily_letters:
            if str(letter) == selected_text and not letter.delivered:
                selected_letter = letter
                break
        
        if selected_letter:
            self.sorted_letters[target_location].append(selected_letter)
            self.update_unsorted_display()
            self.update_sorted_displays()
    
    def deliver_letter(self, location):
        """Deliver selected letter from location"""
        if not self.game_running:
            messagebox.showwarning("Game Not Started", "Please start the day first!")
            return
            
        listbox = self.location_listboxes[location]
        selection = listbox.curselection()
        
        if not selection:
            messagebox.showwarning("No Selection", "Please select a letter to deliver!")
            return
        
        selected_text = listbox.get(selection[0])
        
        # Find the letter
        for letter in self.sorted_letters[location]:
            if str(letter) == selected_text and not letter.delivered:
                # Check if correct location
                if letter.location == location:
                    letter.delivered = True
                    self.letters_delivered += 1
                    self.score += 10
                    messagebox.showinfo("Success!", f"Letter delivered correctly! +10 points")
                else:
                    letter.delivered = True
                    self.wrong_deliveries += 1
                    self.score -= 5
                    messagebox.showwarning("Wrong Location!", f"This letter belongs to {letter.location}! -5 points")
                
                self.update_displays()
                break
    
    def start_day(self):
        """Start the current day timer"""
        self.game_running = True
        self.day_start_time = time.time()
        self.start_button.config(state="disabled")
        self.next_day_button.config(state="disabled")
        self.update_timer()
    
    def update_timer(self):
        """Update the timer display"""
        if not self.game_running:
            return
            
        elapsed = time.time() - self.day_start_time
        remaining = max(0, self.day_duration - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        self.time_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        
        if remaining <= 0:
            self.end_day()
        else:
            self.root.after(1000, self.update_timer)  # Update every second
    
    def end_day(self):
        """End the current day"""
        self.game_running = False
        
        # Calculate final score for the day
        undelivered = sum(1 for letter in self.daily_letters if not letter.delivered)
        time_bonus = max(0, (self.day_duration - (time.time() - self.day_start_time)) / 10)
        
        day_score = self.letters_delivered * 10 - self.wrong_deliveries * 5 + int(time_bonus)
        
        messagebox.showinfo("Day Complete!", 
                          f"Day {self.current_day} finished!\n"
                          f"Letters delivered: {self.letters_delivered}\n"
                          f"Wrong deliveries: {self.wrong_deliveries}\n"
                          f"Undelivered: {undelivered}\n"
                          f"Time bonus: {int(time_bonus)}\n"
                          f"Day score: {day_score}")
        
        self.next_day_button.config(state="normal")
    
    def next_day(self):
        """Advance to next day"""
        self.current_day += 1
        self.letters_delivered = 0
        self.wrong_deliveries = 0
        
        # Clear sorted letters
        for location in self.locations:
            self.sorted_letters[location] = []
        
        self.generate_daily_letters()
        self.update_displays()
        
        self.start_button.config(state="normal")
        self.next_day_button.config(state="disabled")
    
    def reset_game(self):
        """Reset the entire game"""
        self.current_day = 1
        self.score = 0
        self.letters_delivered = 0
        self.wrong_deliveries = 0
        self.game_running = False
        
        for location in self.locations:
            self.sorted_letters[location] = []
        
        self.generate_daily_letters()
        self.update_displays()
        
        self.start_button.config(state="normal")
        self.next_day_button.config(state="disabled")
    
    def update_displays(self):
        """Update all UI displays"""
        self.day_label.config(text=f"Day {self.current_day}")
        self.score_label.config(text=f"Score: {self.score}")
        self.delivered_label.config(text=f"Delivered: {self.letters_delivered}")
        self.wrong_label.config(text=f"Wrong: {self.wrong_deliveries}")
        
        self.update_unsorted_display()
        self.update_sorted_displays()
    
    def run(self):
        """Start the game"""
        self.root.mainloop()

# Run the game
if __name__ == "__main__":
    game = LetterDeliveryGame()
    game.run()