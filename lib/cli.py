from helpers import (
    exit_program,
    create_event_menu,
    book_ticket_menu,
    cancel_ticket_menu,
    view_events_menu,
    view_attendees_menu,
    view_all_attendees_menu,
    find_event_menu,
    find_attendee_menu
)

def main():
    print("\n" + "="*50)
    print("    WELCOME TO EVENT TICKETING SYSTEM")
    print("="*50)
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (0-8): ").strip()
        
        if choice == "0":
            exit_program()
        elif choice == "1":
            create_event_menu()
        elif choice == "2":
            book_ticket_menu()
        elif choice == "3":
            cancel_ticket_menu()
        elif choice == "4":
            view_events_menu()
        elif choice == "5":
            view_attendees_menu()
        elif choice == "6":
            view_all_attendees_menu()
        elif choice == "7":
            find_event_menu()
        elif choice == "8":
            find_attendee_menu()
        else:
            print("\n❌ Invalid choice! Please select a number between 0-8.")
            input("Press Enter to continue...")

def display_menu():
    print("\n" + "-"*50)
    print("              MAIN MENU")
    print("-"*50)
    print("1. Create New Event")
    print("2. Book Ticket")
    print("3. Cancel Ticket")
    print("4. View All Events")
    print("5. View Attendees for Event")
    print("6. View All Attendees")
    print("7. Find Event by ID")
    print("8. Find Attendee by ID")
    print("0. Exit")
    print("-"*50)

if __name__ == "__main__":
    main()