import calendar
import os
from datetime import datetime
from dateutil import parser
from typing import List

class CalendarManager:
    def __init__(self, filename: str = "events.txt"):
        """Initialize the CalendarManager with the events file."""
        self.filename = filename
        # Create the file if it doesn't exist
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                pass

    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n=== Personal Calendar Manager ===")
        print("1. Display Calendar")
        print("2. Add Event")
        print("3. View Events")
        print("4. Delete Event")
        print("5. Exit")
        print("================================")

    def validate_date(self, date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD). Returns True if valid, False otherwise."""
        try:
            parsed_date = parser.parse(date_str, fuzzy=False)
            # Ensure the input string exactly matches YYYY-MM-DD
            return parsed_date.strftime("%Y-%m-%d") == date_str
        except ValueError:
            return False

    def get_valid_date(self, prompt: str) -> str:
        """Prompt user for a valid date and return it."""
        while True:
            date_str = input(prompt).strip()
            if self.validate_date(date_str):
                return date_str
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2025-05-20)")

    def display_calendar(self) -> None:
        """Display calendar for a specified month and year."""
        try:
            year = int(input("Enter year (e.g., 2025): ").strip())
            month = int(input("Enter month (1-12): ").strip())
            
            if month < 1 or month > 12:
                print("Invalid month. Please enter a number between 1 and 12.")
                return
            
            # Generate and display the calendar
            print(f"\n{calendar.month_name[month]} {year}")
            print("Mo Tu We Th Fr Sa Su")
            cal = calendar.monthcalendar(year, month)
            
            for week in cal:
                for day in week:
                    if day == 0:
                        print("  ", end=" ")
                    else:
                        print(f"{day:2d}", end=" ")
                print()
        except ValueError:
            print("Invalid input. Please enter numeric values for year and month.")

    def add_event(self) -> None:
        """Add an event to the specified date in the format YYYY-MM-DD | Description."""
        date_str = self.get_valid_date("Enter event date (YYYY-MM-DD): ")
        description = input("Enter event description: ").strip()
        
        if not description:
            print("Event description cannot be empty.")
            return

        try:
            with open(self.filename, 'a') as f:
                f.write(f"{date_str} | {description}\n")
            print(f"Event added successfully for {date_str}!")
        except IOError as e:
            print(f"Error writing to file: {e}. Please try again.")

    def view_events(self) -> None:
        """View all events for a specified date by reading from the file."""
        date_str = self.get_valid_date("Enter date to view events (YYYY-MM-DD): ")
        events_found = False
        
        try:
            with open(self.filename, 'r') as f:
                print(f"\nEvents for {date_str}:")
                print("-" * 40)
                for line in f:
                    if line.startswith(date_str):
                        _, description = line.strip().split(" | ", 1)
                        print(f"- {description}")
                        events_found = True
                if not events_found:
                    print("No events found for this date.")
        except IOError as e:
            print(f"Error reading from file: {e}. Please try again.")

    def delete_event(self) -> None:
        """Delete a specific event based on date and exact description."""
        date_str = self.get_valid_date("Enter event date (YYYY-MM-DD): ")
        description = input("Enter event description to delete: ").strip()
        
        if not description:
            print("Event description cannot be empty.")
            return

        try:
            # Read all events
            events: List[str] = []
            event_found = False
            with open(self.filename, 'r') as f:
                events = f.readlines()

            # Rewrite file excluding the matching event
            with open(self.filename, 'w') as f:
                for line in events:
                    if not (line.startswith(date_str) and description in line):
                        f.write(line)
                    else:
                        event_found = True

            if event_found:
                print(f"Event deleted successfully for {date_str}!")
            else:
                print("No matching event found with the provided date and description.")
        except IOError as e:
            print(f"Error accessing file: {e}. Please try again.")

    def run(self) -> None:
        """Main loop to continuously interact with the user."""
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                self.display_calendar()
            elif choice == "2":
                self.add_event()
            elif choice == "3":
                self.view_events()
            elif choice == "4":
                self.delete_event()
            elif choice == "5":
                print("Thank you for using Personal Calendar Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")

def main():
    """Main function to start the calendar manager."""
    print("Welcome to Personal Calendar Manager!")
    manager = CalendarManager()
    manager.run()

if __name__ == "__main__":
    main()