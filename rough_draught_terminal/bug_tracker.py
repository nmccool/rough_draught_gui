"""
-----------------------------------------------------------------------
ASSIGNMENT 11A REVISED: THE BUG TRACKING LOG
-----------------------------------------------------------------------
[X] 1. Program uses a while loop to keep asking for bugs.
[X] 2. Uses the datetime module to get a timestamp format.
[X] 3. Stores the timestamp, file name, description, and priority in a dictionary.
[X] 4. Uses `with open("bug_log.txt", "a")` to append to the file safely.
[X] 5. The bug_log.txt file is formatted neatly with newlines.
-----------------------------------------------------------------------
"""
import datetime
bug_id = 1

#1 --- While loop ---
while True:
    entry = input("Make a selection (log/quit): ").strip().lower()
    if entry == "quit":
        break
    elif entry == "log":
        file_name = input("File Name: ")
        bug_description = input("Bug Description: ")
        priority = input("Priority Level (High, Med, Low): ").strip().title()

#2 --- Datetime module ---        
        current_time = datetime.datetime.now()

#3 --- Store Datetime ---
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
    

        bug_entry = {
            timestamp: [file_name, bug_description, priority]
    }
        log_entry = "*" * 50 + "\n"
        log_entry += f"BUG SUBMISSION {bug_id}\n"
        log_entry += f"Timestamp: {timestamp}\n"
        log_entry += f"File: {file_name}\n"
        log_entry += f"Description: {bug_description}\n"
        log_entry += f"Priority: {priority}\n"
        log_entry += "*" * 50 + "\n"
        log_entry += "\n"

#4&5 --- With open and bug_log ---         
        with open("bug_log.txt", "a") as file:
            file.write(log_entry)

# ---  Added bug counter ---             
        bug_id += 1
            
        
        print("Bug recorded.")

    else:
        print("Invalid Entry.")
