import time

def get_current_time():
    return time.time()

def get_timer_duration():
    return int(input("Enter the timer duration in seconds: "))

def get_deadline(duration):
    return get_current_time() + duration

def time_remaining(deadline):
    return round(deadline - get_current_time(), 1)

def run_timer():
    while True:
        duration = get_timer_duration()
        print()
        input("Press Enter to start the timer.")
        deadline = get_deadline(duration)
        print()

        while get_current_time() < deadline:
            print(f"Time remaining: {time_remaining(deadline)} seconds", end='\r')
            time.sleep(1)

        print("\nTime's up!\n")

# Run the timer loop
run_timer()
"""
| Original                                                  | Simplified                                                                                   |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| ❌ **Global variables** (`timerDuration`, `timerDeadline`) | ✅ Replaced with local variables passed via functions (better encapsulation, no side effects) |
| ❌ `setTimerDuration()`, `isTimerSet()`                    | ✅ Inlined into a single function with a clear role: `get_timer_duration()`                   |
| ❌ `resetTimer()` function                                 | ✅ Unnecessary — variables are local and reset automatically on each loop                     |
| ❌ `clockTime()`                                           | ✅ Renamed to `get_current_time()` for clarity                                                |
| ❌ Mixing setting and checking logic                       | ✅ Clear separation: input > start > countdown                                                |
| ❌ Redundant `print()` lines and extra spacing             | ✅ Minimal clean output with clear separation                                                 |
"""