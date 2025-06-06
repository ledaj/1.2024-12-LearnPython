import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from PIL import Image, ImageTk
import threading
import time

class VisualNovel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Visual Novel Engine")
        self.root.geometry("1000x700")
        self.root.configure(bg='black')
        
        # Game state
        self.current_scene = 0
        self.character_states = {}
        self.inventory = []
        self.flags = {}
        
        # UI elements
        self.bg_label = None
        self.char_label = None
        self.text_frame = None
        self.name_label = None
        self.dialogue_text = None
        self.choice_frame = None
        self.menu_frame = None
        
        # Story data
        self.story = self.create_sample_story()
        
        self.setup_ui()
        self.load_scene(0)
        
    def setup_ui(self):
        """Set up the main UI elements"""
        # Background area
        self.bg_frame = tk.Frame(self.root, bg='black', width=1000, height=500)
        self.bg_frame.pack(fill=tk.BOTH, expand=True)
        self.bg_frame.pack_propagate(False)
        
        self.bg_label = tk.Label(self.bg_frame, bg='black')
        self.bg_label.pack(fill=tk.BOTH, expand=True)
        
        # Character sprite area (overlay on background)
        self.char_label = tk.Label(self.bg_frame, bg='black')
        self.char_label.place(relx=0.7, rely=0.3, anchor='center')
        
        # Text area
        self.text_frame = tk.Frame(self.root, bg='#2c2c2c', height=200)
        self.text_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.text_frame.pack_propagate(False)
        
        # Character name
        self.name_label = tk.Label(self.text_frame, text="", font=('Arial', 14, 'bold'),
                                  bg='#404040', fg='white', padx=10, pady=5)
        self.name_label.pack(anchor='w', padx=10, pady=(10, 0))
        
        # Dialogue text
        self.dialogue_text = tk.Text(self.text_frame, font=('Arial', 12), bg='#2c2c2c',
                                   fg='white', wrap=tk.WORD, height=6, state=tk.DISABLED,
                                   borderwidth=0, highlightthickness=0)
        self.dialogue_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Choice buttons frame
        self.choice_frame = tk.Frame(self.text_frame, bg='#2c2c2c')
        self.choice_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Menu frame
        self.setup_menu()
        
        # Bind click to advance dialogue
        self.root.bind('<Button-1>', self.advance_dialogue)
        self.root.bind('<Return>', self.advance_dialogue)
        
    def setup_menu(self):
        """Set up the game menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Save Game", command=self.save_game)
        game_menu.add_command(label="Load Game", command=self.load_game)
        game_menu.add_separator()
        game_menu.add_command(label="Quit", command=self.root.quit)
        
    def create_sample_story(self):
        """Create a sample story with multiple scenes and choices"""
        return [
            {
                "id": 0,
                "background": "#1a1a2e",  # Using color instead of image file
                "character": None,
                "name": "Narrator",
                "text": "Welcome to the Mysterious Academy. You are a new student arriving on a dark, stormy night...",
                "choices": [
                    {"text": "Enter the main building", "next": 1},
                    {"text": "Explore the gardens first", "next": 2}
                ]
            },
            {
                "id": 1,
                "background": "#2d1b69",
                "character": None,
                "name": "Narrator",
                "text": "You step into the grand hall. Ancient portraits line the walls, their eyes seeming to follow you. A figure approaches from the shadows.",
                "choices": [
                    {"text": "Greet the figure politely", "next": 3},
                    {"text": "Stay silent and wait", "next": 4}
                ]
            },
            {
                "id": 2,
                "background": "#0f3460",
                "character": None,
                "name": "Narrator",
                "text": "The gardens are overgrown and mysterious. Moonlight filters through the trees, creating eerie shadows. You hear footsteps behind you.",
                "choices": [
                    {"text": "Turn around quickly", "next": 5},
                    {"text": "Continue walking, pretending not to notice", "next": 6}
                ]
            },
            {
                "id": 3,
                "background": "#2d1b69",
                "character": None,
                "name": "Professor Blackwood",
                "text": "Ah, you must be our new student. I am Professor Blackwood. Welcome to Ravencrest Academy. You show promise already - politeness is a rare virtue here.",
                "choices": [
                    {"text": "Thank you, Professor. What should I know about this place?", "next": 7},
                    {"text": "Promise? What do you mean?", "next": 8}
                ]
            },
            {
                "id": 4,
                "background": "#2d1b69",
                "character": None,
                "name": "Professor Blackwood",
                "text": "Cautious, I see. That's wise in a place like this. I am Professor Blackwood, and you... you have an interesting aura about you.",
                "choices": [
                    {"text": "What kind of aura?", "next": 9},
                    {"text": "I should find my dormitory", "next": 10}
                ]
            },
            {
                "id": 5,
                "background": "#0f3460",
                "character": None,
                "name": "Luna",
                "text": "Oh! Sorry, I didn't mean to startle you. I'm Luna, another student here. I was just... collecting moonflowers. They only bloom at night.",
                "choices": [
                    {"text": "Moonflowers? That sounds magical", "next": 11},
                    {"text": "It's pretty late to be wandering around", "next": 12}
                ]
            },
            {
                "id": 6,
                "background": "#0f3460",
                "character": None,
                "name": "Narrator",
                "text": "The footsteps stop. You continue walking, but the feeling of being watched persists. Suddenly, a voice calls out softly.",
                "choices": [
                    {"text": "Stop and listen", "next": 13},
                    {"text": "Head back to the main building", "next": 1}
                ]
            },
            {
                "id": 7,
                "background": "#2d1b69",
                "character": None,
                "name": "Professor Blackwood",
                "text": "This academy teaches more than ordinary subjects. Here, we study the mysteries of the mind, the secrets of ancient knowledge, and the power that lies dormant in certain individuals.",
                "choices": [
                    {"text": "That sounds incredible", "next": 14},
                    {"text": "What kind of power?", "next": 15}
                ]
            },
            {
                "id": 8,
                "background": "#2d1b69",
                "character": None,
                "name": "Professor Blackwood",
                "text": "You have the Sight, child. The ability to perceive what others cannot. It's rare, and here at Ravencrest, we nurture such gifts.",
                "choices": [
                    {"text": "I've always seen things others couldn't...", "next": 16},
                    {"text": "I think you're mistaken", "next": 17}
                ]
            },
            # Add more scenes as needed...
            {
                "id": 14,
                "background": "#2d1b69",
                "character": None,
                "name": "Professor Blackwood",
                "text": "Indeed it is. Your journey begins tomorrow with your first classes. But for now, rest. The path ahead will test you in ways you cannot yet imagine.",
                "choices": [
                    {"text": "Thank you, Professor", "next": "end"}
                ]
            }
        ]
    
    def load_scene(self, scene_id):
        """Load and display a scene"""
        if scene_id == "end":
            self.show_ending()
            return
            
        scene = next((s for s in self.story if s["id"] == scene_id), None)
        if not scene:
            messagebox.showerror("Error", f"Scene {scene_id} not found!")
            return
            
        self.current_scene = scene_id
        
        # Set background
        if scene["background"].startswith("#"):
            # Color background
            self.bg_label.configure(bg=scene["background"])
        else:
            # Image background (if you have image files)
            try:
                img = Image.open(scene["background"])
                img = img.resize((1000, 500), Image.Resampling.LANCZOS)
                bg_photo = ImageTk.PhotoImage(img)
                self.bg_label.configure(image=bg_photo)
                self.bg_label.image = bg_photo  # Keep a reference
            except:
                self.bg_label.configure(bg='#1a1a2e')
        
        # Set character sprite
        if scene["character"]:
            try:
                char_img = Image.open(scene["character"])
                char_img = char_img.resize((200, 300), Image.Resampling.LANCZOS)
                char_photo = ImageTk.PhotoImage(char_img)
                self.char_label.configure(image=char_photo)
                self.char_label.image = char_photo
            except:
                self.char_label.configure(image="")
        else:
            self.char_label.configure(image="")
        
        # Set dialogue
        self.name_label.configure(text=scene["name"])
        self.display_text(scene["text"])
        
        # Clear existing choices
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # Add choice buttons
        if "choices" in scene and scene["choices"]:
            for i, choice in enumerate(scene["choices"]):
                btn = tk.Button(self.choice_frame, text=choice["text"],
                              command=lambda next_scene=choice["next"]: self.make_choice(next_scene),
                              bg='#404040', fg='white', font=('Arial', 10),
                              padx=10, pady=5, relief='raised')
                btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def display_text(self, text):
        """Display text with typewriter effect"""
        self.dialogue_text.configure(state=tk.NORMAL)
        self.dialogue_text.delete(1.0, tk.END)
        self.dialogue_text.configure(state=tk.DISABLED)
        
        # Simple typewriter effect
        def type_text():
            self.dialogue_text.configure(state=tk.NORMAL)
            for char in text:
                self.dialogue_text.insert(tk.END, char)
                self.dialogue_text.update()
                time.sleep(0.03)  # Adjust speed as needed
            self.dialogue_text.configure(state=tk.DISABLED)
        
        # Run in thread to prevent UI blocking
        threading.Thread(target=type_text, daemon=True).start()
    
    def make_choice(self, next_scene):
        """Handle player choice"""
        self.load_scene(next_scene)
    
    def advance_dialogue(self, event=None):
        """Advance dialogue on click (if no choices available)"""
        scene = next((s for s in self.story if s["id"] == self.current_scene), None)
        if scene and ("choices" not in scene or not scene["choices"]):
            # Auto-advance or handle single-choice scenarios
            pass
    
    def show_ending(self):
        """Show game ending"""
        self.name_label.configure(text="The End")
        self.dialogue_text.configure(state=tk.NORMAL)
        self.dialogue_text.delete(1.0, tk.END)
        self.dialogue_text.insert(tk.END, "Thank you for playing this visual novel demo!\n\nYour journey at Ravencrest Academy has just begun...")
        self.dialogue_text.configure(state=tk.DISABLED)
        
        # Clear choices
        for widget in self.choice_frame.winfo_children():
            widget.destroy()
        
        # Add restart button
        restart_btn = tk.Button(self.choice_frame, text="Restart Game",
                              command=lambda: self.load_scene(0),
                              bg='#404040', fg='white', font=('Arial', 12),
                              padx=20, pady=10)
        restart_btn.pack(pady=10)
    
    def save_game(self):
        """Save current game state"""
        save_data = {
            "current_scene": self.current_scene,
            "character_states": self.character_states,
            "inventory": self.inventory,
            "flags": self.flags
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(save_data, f, indent=2)
                messagebox.showinfo("Success", "Game saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save game: {str(e)}")
    
    def load_game(self):
        """Load saved game state"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    save_data = json.load(f)
                
                self.current_scene = save_data.get("current_scene", 0)
                self.character_states = save_data.get("character_states", {})
                self.inventory = save_data.get("inventory", [])
                self.flags = save_data.get("flags", {})
                
                self.load_scene(self.current_scene)
                messagebox.showinfo("Success", "Game loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load game: {str(e)}")
    
    def run(self):
        """Start the visual novel"""
        self.root.mainloop()

# Example of how to extend the story
def add_custom_scene(vn, scene_data):
    """Add a custom scene to the visual novel"""
    vn.story.append(scene_data)

if __name__ == "__main__":
    # Create and run the visual novel
    game = VisualNovel()
    
    # Example of adding a custom scene
    custom_scene = {
        "id": 99,
        "background": "#4a0e4e",
        "character": None,
        "name": "Mystery Voice",
        "text": "This is a custom scene added to demonstrate extensibility!",
        "choices": [
            {"text": "Return to main story", "next": 0}
        ]
    }
    add_custom_scene(game, custom_scene)
    
    print("Visual Novel Engine")
    print("==================")
    print("Features:")
    print("- Multiple scenes with branching dialogue")
    print("- Character names and dialogue")
    print("- Background colors (easily extendable to images)")
    print("- Character sprites support")
    print("- Choice-based progression")
    print("- Save/Load functionality")
    print("- Typewriter text effect")
    print("- Extensible story system")
    print("\nControls:")
    print("- Click on choices to progress")
    print("- Use Game menu to save/load")
    print("- Click anywhere to advance (when no choices)")
    print("\nStarting game...")
    
    game.run()