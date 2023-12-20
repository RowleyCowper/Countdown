import sys
import time
import os
import subprocess

def clear_screen():
    os.system('clear')

def print_progress_bar(percentage, bar_length=50):
    progress = int(bar_length * percentage)
    bar = '[' + '=' * progress + ' ' * (bar_length - progress) + ']'
    sys.stdout.write('\r' + bar)
    sys.stdout.flush()

def post_notification(title, message):
    script = f'display notification "{message}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])

def bring_terminal_to_front():
    script = """
    tell application "Terminal"
        activate
    end tell
    """
    subprocess.run(["osascript", "-e", script])

def countdown_timer(total_seconds):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = total_seconds - elapsed_time
        if remaining_time <= 0:
            break

        percentage = 1 - (remaining_time / total_seconds)
        print_progress_bar(percentage)
        time.sleep(0.1)
    
    # Notify and bring terminal to front
    post_notification("Countdown Timer", "Time's up!")
    bring_terminal_to_front()

    # Flash red when the timer is up
    for _ in range(5):
        sys.stdout.write('\033[41m\033[2J\033[H')  # Set background to red and clear screen
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write('\033[49m\033[2J\033[H')  # Reset background color and clear screen
        sys.stdout.flush()
        time.sleep(0.5)

def main():
    while True:
        clear_screen()
        duration = input("Enter countdown time in minutes (or 'q' to quit): ")

        if duration.lower() == 'q':
            break

        try:
            total_minutes = int(duration)
            total_seconds = total_minutes * 60
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        countdown_timer(total_seconds)

        while True:
            choice = input("Timer done! Choose (R) Restart, (N) New timer, or (q) Quit: ").lower()
            sys.stdout.write('\033[49m\033[2J\033[H')  # Reset background color and clear screen
            sys.stdout.flush()
            if choice == 'r':
                countdown_timer(total_seconds)
            elif choice == 'n':
                break
            elif choice == 'q':
                return
            else:
                print("Invalid choice. Please choose R, N, or q.")

if __name__ == "__main__":
    main()
