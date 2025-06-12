import time

# Sample delivery jobs
jobs = [
    {"id": 1, "name": "Midtown Urgent", "pay": 350, "deadline": "11:00 AM", "fragile": True, "accepted": False},
    {"id": 2, "name": "Westside Standard", "pay": 120, "deadline": "EOD", "fragile": False, "accepted": False},
    {"id": 3, "name": "East Hills VIP", "pay": 260, "deadline": "1:30 PM", "fragile": False, "accepted": False},
]

status = {
    "time": "9:12 AM",
    "money": 1420,
    "reputation": 3,
    "truck_health": "Low",
    "notifications": ["Package Delay", "Truck Needs Maintenance"]
}


def show_dashboard():
    print("\n==== MAIL MASTER 2075 ====\n")
    print(f"Time: {status['time']} | 💵 ${status['money']} | ⭐ Reputation: {'★' * status['reputation']}{'☆' * (5 - status['reputation'])}")
    print("Notifications:", " | ".join(status["notifications"]))
    print("\n[1] View Delivery Inbox")
    print("[2] View Map")
    print("[3] View Schedule")
    print("[4] End Day\n")


def show_inbox():
    print("\n📬 DELIVERY INBOX")
    for job in jobs:
        if not job["accepted"]:
            print(f"({job['id']}) {job['name']} | ${job['pay']} | Deadline: {job['deadline']} | Fragile: {'Yes' if job['fragile'] else 'No'}")
    print("\nChoose job ID to accept, or [0] to go back.")
    choice = input("> ")
    if choice.isdigit():
        choice = int(choice)
        if choice == 0:
            return
        for job in jobs:
            if job["id"] == choice:
                job["accepted"] = True
                print(f"> You accepted: {job['name']}")
                return


def show_map():
    print("\n🗺️ MAP VIEW (Simulation)")
    print("- Truck A → Midtown (ETA 10:45 AM) | Low Fuel")
    print("- Drone 1 → East Hills (ETA 1:00 PM) | Wind Risk")
    print("\nOptions:")
    print("[1] Reroute Truck A")
    print("[2] Ignore")
    print("[0] Go back")
    choice = input("> ")
    if choice == "1":
        print("You rerouted Truck A. ETA updated to 11:05 AM.")
    elif choice == "2":
        print("You chose to ignore the warning.")


def show_schedule():
    print("\n📅 TODAY'S SCHEDULE")
    for job in jobs:
        if job["accepted"]:
            print(f"- {job['name']} | Deadline: {job['deadline']} | Status: Scheduled")
    input("\nPress Enter to return.")


def end_day():
    print("\n🌙 END OF DAY SUMMARY")
    completed = sum(1 for job in jobs if job["accepted"])
    earned = sum(job["pay"] for job in jobs if job["accepted"])
    print(f"Deliveries completed: {completed}")
    print(f"Money earned: ${earned}")
    print("Customer Satisfaction: 87%")
    print("New Perk: Express Lane License 🆕")
    print("\nThanks for playing!")
    exit()


# Main loop
while True:
    show_dashboard()
    option = input("> ")
    if option == "1":
        show_inbox()
    elif option == "2":
        show_map()
    elif option == "3":
        show_schedule()
    elif option == "4":
        end_day()
    else:
        print("Invalid option.")
