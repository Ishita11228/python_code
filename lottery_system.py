import time
import random
import threading
import os
import sys

registration_duration = 60 * 60  # 1 hour in seconds
extension_duration = 30 * 60     # 30 minutes
save_interval = 5 * 60           # 5 minutes

participants = set()
start_time = time.time()
log_file = "lottery_log.txt"
lock = threading.Lock()

def save_progress():
    with lock:
        with open(log_file, "w") as f:
            f.write("Registration Timestamps:\n")
            for user, timestamp in registered_users:
                f.write(f"{user} - {time.ctime(timestamp)}\n")
            f.write("\nTotal Participants: " + str(len(participants)) + "\n")
        print("[Saved progress]")

def auto_save():
    while True:
        time.sleep(save_interval)
        save_progress()

def is_valid_username(username):
    return username.isalnum() and len(username) > 1

def register_user():
    while time.time() - start_time < registration_duration:
        remaining_time = int(registration_duration - (time.time() - start_time))
        print(f"\nTime left for registration: {remaining_time//60} minutes")
        print(f"Registered users: {len(participants)}")
        username = input("Enter a unique username to register: ").strip()
        
        if not is_valid_username(username):
            print("Invalid username. Must be alphanumeric and > 1 character.")
            continue
        if username in participants:
            print("Username already registered.")
            continue
        
        with lock:
            participants.add(username)
            registered_users.append((username, time.time()))

def extend_registration():
    global registration_duration
    registration_duration += extension_duration
    print("\nLess than 5 users registered. Extending registration by 30 minutes...")

def draw_winner():
    if len(participants) == 0:
        print("No participants registered. Exiting.")
        sys.exit()
    winner = random.choice(list(participants))
    with open(log_file, "a") as f:
        f.write("\nWinner: " + winner + "\n")
    print(f"\nWinner is: {winner}")
    print(f"Total participants: {len(participants)}")

# Main
registered_users = []

# Start auto-save thread
threading.Thread(target=auto_save, daemon=True).start()

try:
    register_user()
    if len(participants) < 5:
        extend_registration()
        register_user()

    if len(participants) == 0:
        print("No users registered even after extension. Exiting.")
        sys.exit()

    save_progress()
    draw_winner()

except KeyboardInterrupt:
    print("\n[Interrupted] Saving progress before exit...")
    save_progress()
    sys.exit()