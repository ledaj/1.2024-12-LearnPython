class Letter:
    def __init__(self, sender, recipient, address, content="", priority="normal"):
        self.sender = sender
        self.recipient = recipient
        self.address = address
        self.content = content
        self.priority = priority
        self.delivered = False
    
    def __str__(self):
        return f"Letter from {self.sender} to {self.recipient} at {self.address}"

class Location:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.letters_to_pickup = []
        self.letters_delivered = []
    
    def add_outgoing_letter(self, letter):
        self.letters_to_pickup.append(letter)
    
    def receive_letter(self, letter):
        self.letters_delivered.append(letter)
        letter.delivered = True

class Player:
    def __init__(self, name):
        self.name = name
        self.current_location = None
        self.mail_bag = []
        self.max_capacity = 10
        self.score = 0
    
    def pickup_letters(self, location):
        available = location.letters_to_pickup[:]
        for letter in available:
            if len(self.mail_bag) < self.max_capacity:
                self.mail_bag.append(letter)
                location.letters_to_pickup.remove(letter)
                print(f"Picked up: {letter}")
            else:
                print("Mail bag is full!")
                break
    
    def deliver_letter(self, letter, location):
        if letter in self.mail_bag and letter.address == location.address:
            self.mail_bag.remove(letter)
            location.receive_letter(letter)
            self.score += 10
            print(f"Delivered: {letter}")
            return True
        return False

class DeliveryGame:
    def __init__(self):
        self.locations = {}
        self.player = None
        self.game_running = True
        self.setup_world()
    
    def setup_world(self):
        # Create locations
        self.locations = {
            "post_office": Location("Post Office", "123 Main St"),
            "house_1": Location("Johnson House", "456 Oak Ave"),
            "house_2": Location("Smith House", "789 Pine Rd"),
            "shop": Location("Corner Shop", "321 Elm St")
        }
        
        # Add some initial letters
        letter1 = Letter("Alice", "Bob Johnson", "456 Oak Ave", "Birthday invitation")
        letter2 = Letter("City Hall", "Mary Smith", "789 Pine Rd", "Tax notice")
        
        self.locations["post_office"].add_outgoing_letter(letter1)
        self.locations["post_office"].add_outgoing_letter(letter2)
    
    def display_status(self):
        print(f"\n--- {self.player.name}'s Status ---")
        print(f"Current Location: {self.player.current_location.name}")
        print(f"Mail Bag: {len(self.player.mail_bag)}/{self.player.max_capacity}")
        print(f"Score: {self.player.score}")
        
        if self.player.mail_bag:
            print("Letters in bag:")
            for i, letter in enumerate(self.player.mail_bag, 1):
                print(f"  {i}. {letter}")
    
    def display_location_info(self):
        loc = self.player.current_location
        print(f"\n--- At {loc.name} ({loc.address}) ---")
        
        if loc.letters_to_pickup:
            print("Letters available for pickup:")
            for i, letter in enumerate(loc.letters_to_pickup, 1):
                print(f"  {i}. {letter}")
        else:
            print("No letters to pick up here.")
    
    def move_player(self, location_key):
        if location_key in self.locations:
            self.player.current_location = self.locations[location_key]
            print(f"Moved to {self.player.current_location.name}")
            return True
        return False
    
    def start_game(self):
        print("Welcome to Letter Delivery Game!")
        player_name = input("Enter your name: ")
        self.player = Player(player_name)
        self.player.current_location = self.locations["post_office"]
        
        print(f"\nHello {player_name}! You're starting at the Post Office.")
        
        self.game_loop()
    
    def game_loop(self):
        while self.game_running:
            self.display_status()
            self.display_location_info()
            
            print("\nOptions:")
            print("1. Pick up letters")
            print("2. Deliver letter")
            print("3. Move to location")
            print("4. Quit")
            
            choice = input("\nWhat would you like to do? ")
            
            if choice == "1":
                self.player.pickup_letters(self.player.current_location)
            elif choice == "2":
                self.handle_delivery()
            elif choice == "3":
                self.handle_movement()
            elif choice == "4":
                self.game_running = False
                print(f"Game Over! Final Score: {self.player.score}")
    
    def handle_delivery(self):
        if not self.player.mail_bag:
            print("No letters to deliver!")
            return
        
        print("Which letter to deliver?")
        for i, letter in enumerate(self.player.mail_bag, 1):
            print(f"{i}. {letter}")
        
        try:
            choice = int(input("Enter number: ")) - 1
            letter = self.player.mail_bag[choice]
            
            if self.player.deliver_letter(letter, self.player.current_location):
                print("Letter delivered successfully!")
            else:
                print("Can't deliver this letter here!")
        except (ValueError, IndexError):
            print("Invalid choice!")
    
    def handle_movement(self):
        print("Available locations:")
        for key, location in self.locations.items():
            print(f"{key}: {location.name}")
        
        location_key = input("Where to go? ").lower()
        if not self.move_player(location_key):
            print("Invalid location!")

# Example usage
if __name__ == "__main__":
    game = DeliveryGame()
    game.start_game()