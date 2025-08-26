from models.event import Event
from models.attendee import Attendee
from models.ticket import Ticket
from datetime import datetime

def exit_program():
    print("\nThank you for using Event Ticketing System!")
    print("Goodbye!")
    exit()

def create_event_menu():
    print("\n" + "="*40)
    print("         CREATE NEW EVENT")
    print("="*40)
    
    try:
        # Get event details from user
        name = input("Event name: ").strip()
        if not name:
            raise ValueError("Event name cannot be empty")
        
        location = input("Event location: ").strip()
        if not location:
            raise ValueError("Event location cannot be empty")
        
        date_str = input("Event date (YYYY-MM-DD): ").strip()
        if not date_str:
            raise ValueError("Event date cannot be empty")
        
        # Validate date format
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if date_obj < datetime.now().date():
                raise ValueError("Event date cannot be in the past")
        except ValueError as e:
            if "does not match format" in str(e):
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
            raise e
        
        capacity_str = input("Event capacity: ").strip()
        if not capacity_str:
            raise ValueError("Event capacity cannot be empty")
        
        try:
            capacity = int(capacity_str)
            if capacity <= 0:
                raise ValueError("Capacity must be a positive number")
        except ValueError:
            raise ValueError("Capacity must be a valid number")
        
        # Create the event
        event = Event.create(name, location, date_str, capacity)
        print(f"\nEvent created successfully!")
        print(f"Event ID: {event.id}")
        print(f"Name: {event.name}")
        print(f"Location: {event.location}")
        print(f"Date: {event.date}")
        print(f"Capacity: {event.capacity}")
        
    except Exception as e:
        print(f"\nError creating event: {str(e)}")
    
    input("\nPress Enter to continue...")

def book_ticket_menu():
    print("\n" + "="*40)
    print("           BOOK TICKET")
    print("="*40)
    
    try:
        # Show available events first
        events = Event.get_all()
        if not events:
            print("No events available!")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable Events:")
        print("-" * 80)
        for event in events:
            # Get ticket count for this event
            event_tickets = Ticket.get_tickets_for_event(event.id)
            available_spots = event.capacity - len(event_tickets)
            status = "AVAILABLE" if available_spots > 0 else "FULL"
            print(f"ID: {event.id} | {event.name} | {event.location} | {event.date} | Spots: {available_spots}/{event.capacity} | {status}")
        print("-" * 80)
        
        # Get event ID
        event_id_str = input("\nEnter Event ID: ").strip()
        if not event_id_str:
            raise ValueError("Event ID cannot be empty")
        
        try:
            event_id = int(event_id_str)
        except ValueError:
            raise ValueError("Event ID must be a valid number")
        
        # Check if event exists
        event = Event.find_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        
        # Get attendee details
        print(f"\nBooking ticket for: {event.name}")
        attendee_name = input("Attendee name: ").strip()
        if not attendee_name:
            raise ValueError("Attendee name cannot be empty")
        
        attendee_contact = input("Attendee contact (email or phone): ").strip()
        if not attendee_contact:
            raise ValueError("Attendee contact cannot be empty")
        
        # Create or find attendee
        attendee = Attendee.find_by_contact(attendee_contact)
        if not attendee:
            attendee = Attendee.create(attendee_name, attendee_contact)
            print(f"New attendee created: {attendee.name}")
        else:
            print(f"Found existing attendee: {attendee.name}")
        
        # Create ticket
        ticket = Ticket.create(event_id, attendee.id)
        
        print(f"\nTicket booked successfully!")
        print(f"Ticket ID: {ticket.id}")
        print(f"Event: {event.name}")
        print(f"Attendee: {attendee.name}")
        print(f"Contact: {attendee.contact}")
        print(f"Booked at: {ticket.booked_at}")
        
    except Exception as e:
        print(f"\nError booking ticket: {str(e)}")
    
    input("\nPress Enter to continue...")

def cancel_ticket_menu():
    print("\n" + "="*40)
    print("         CANCEL TICKET")
    print("="*40)
    
    try:
        # Get ticket ID
        ticket_id_str = input("Enter Ticket ID to cancel: ").strip()
        if not ticket_id_str:
            raise ValueError("Ticket ID cannot be empty")
        
        try:
            ticket_id = int(ticket_id_str)
        except ValueError:
            raise ValueError("Ticket ID must be a valid number")
        
        # Find ticket
        ticket = Ticket.find_by_id(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        
        # Show ticket details
        print(f"\nTicket Details:")
        print(f"Ticket ID: {ticket.id}")
        print(f"Event: {ticket.event.name}")
        print(f"Attendee: {ticket.attendee.name}")
        print(f"Contact: {ticket.attendee.contact}")
        
        # Confirm cancellation
        confirm = input("\nAre you sure you want to cancel this ticket? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            ticket.delete()
            print("\nTicket cancelled successfully!")
        else:
            print("\nTicket cancellation aborted.")
        
    except Exception as e:
        print(f"\nError cancelling ticket: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_events_menu():
    print("\n" + "="*40)
    print("         ALL EVENTS")
    print("="*40)
    
    try:
        events = Event.get_all()
        if not events:
            print("No events found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nTotal Events: {len(events)}")
        print("-" * 100)
        print(f"{'ID':<4} {'Name':<25} {'Location':<20} {'Date':<12} {'Capacity':<10} {'Booked':<8} {'Available':<10}")
        print("-" * 100)
        
        for event in events:
            # Get ticket count for this event
            event_tickets = Ticket.get_tickets_for_event(event.id)
            booked_tickets = len(event_tickets)
            available_spots = event.capacity - booked_tickets
            print(f"{event.id:<4} {event.name[:24]:<25} {event.location[:19]:<20} {event.date:<12} {event.capacity:<10} {booked_tickets:<8} {available_spots:<10}")
        
        print("-" * 100)
        
    except Exception as e:
        print(f"Error retrieving events: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_attendees_menu():
    print("\n" + "="*40)
    print("      VIEW EVENT ATTENDEES")
    print("="*40)
    
    try:
        # Show available events first
        events = Event.get_all()
        if not events:
            print("No events available!")
            input("Press Enter to continue...")
            return
        
        print("\nAvailable Events:")
        print("-" * 60)
        for event in events:
            attendee_count = len(event.tickets)
            print(f"ID: {event.id} | {event.name} | Attendees: {attendee_count}")
        print("-" * 60)
        
        # Get event ID
        event_id_str = input("\nEnter Event ID: ").strip()
        if not event_id_str:
            raise ValueError("Event ID cannot be empty")
        
        try:
            event_id = int(event_id_str)
        except ValueError:
            raise ValueError("Event ID must be a valid number")
        
        # Find event
        event = Event.find_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        
        # Get attendees
        tickets = Ticket.get_tickets_for_event(event_id)
        if not tickets:
            print(f"\nNo attendees registered for '{event.name}'")
            input("Press Enter to continue...")
            return
        
        print(f"\nAttendees for '{event.name}':")
        print(f"Total Attendees: {len(tickets)}")
        print("-" * 80)
        print(f"{'Ticket ID':<10} {'Name':<25} {'Contact':<25} {'Booked At':<20}")
        print("-" * 80)
        
        for ticket in tickets:
            booked_at_str = ticket.booked_at.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{ticket.id:<10} {ticket.attendee.name[:24]:<25} {ticket.attendee.contact[:24]:<25} {booked_at_str:<20}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error retrieving attendees: {str(e)}")
    
    input("\nPress Enter to continue...")

def view_all_attendees_menu():
    print("\n" + "="*40)
    print("        ALL ATTENDEES")
    print("="*40)
    
    try:
        attendees = Attendee.get_all()
        if not attendees:
            print("No attendees found!")
            input("Press Enter to continue...")
            return
        
        print(f"\nTotal Attendees: {len(attendees)}")
        print("-" * 80)
        print(f"{'ID':<4} {'Name':<25} {'Contact':<25} {'Events Registered':<20}")
        print("-" * 80)
        
        for attendee in attendees:
            # Get ticket count for this attendee
            attendee_tickets = Ticket.get_tickets_for_attendee(attendee.id)
            events_count = len(attendee_tickets)
            print(f"{attendee.id:<4} {attendee.name[:24]:<25} {attendee.contact[:24]:<25} {events_count:<20}")
        
        print("-" * 80)
        
    except Exception as e:
        print(f"Error retrieving attendees: {str(e)}")
    
    input("\nPress Enter to continue...")

def find_event_menu():
    print("\n" + "="*40)
    print("         FIND EVENT BY ID")
    print("="*40)
    
    try:
        event_id_str = input("Enter Event ID: ").strip()
        if not event_id_str:
            raise ValueError("Event ID cannot be empty")
        
        try:
            event_id = int(event_id_str)
        except ValueError:
            raise ValueError("Event ID must be a valid number")
        
        event = Event.find_by_id(event_id)
        if not event:
            print("Event not found!")
            input("Press Enter to continue...")
            return
        
        # Get ticket count for this event
        event_tickets = Ticket.get_tickets_for_event(event.id)
        
        # Display event details
        print(f"\nEvent Found:")
        print("-" * 50)
        print(f"ID: {event.id}")
        print(f"Name: {event.name}")
        print(f"Location: {event.location}")
        print(f"Date: {event.date}")
        print(f"Capacity: {event.capacity}")
        print(f"Tickets Sold: {len(event_tickets)}")
        print(f"Available Spots: {event.capacity - len(event_tickets)}")
        print(f"Status: {'FULL' if len(event_tickets) >= event.capacity else 'AVAILABLE'}")
        print("-" * 50)
        
    except Exception as e:
        print(f"Error finding event: {str(e)}")
    
    input("\nPress Enter to continue...")

def find_attendee_menu():
    print("\n" + "="*40)
    print("       FIND ATTENDEE BY ID")
    print("="*40)
    
    try:
        attendee_id_str = input("Enter Attendee ID: ").strip()
        if not attendee_id_str:
            raise ValueError("Attendee ID cannot be empty")
        
        try:
            attendee_id = int(attendee_id_str)
        except ValueError:
            raise ValueError("Attendee ID must be a valid number")
        
        attendee = Attendee.find_by_id(attendee_id)
        if not attendee:
            print("Attendee not found!")
            input("Press Enter to continue...")
            return
        
        # Get tickets for this attendee
        attendee_tickets = Ticket.get_tickets_for_attendee(attendee.id)
        
        # Display attendee details
        print(f"\nAttendee Found:")
        print("-" * 60)
        print(f"ID: {attendee.id}")
        print(f"Name: {attendee.name}")
        print(f"Contact: {attendee.contact}")
        print(f"Total Events Registered: {len(attendee_tickets)}")
        
        if attendee_tickets:
            print(f"\nRegistered Events:")
            print("-" * 60)
            for ticket in attendee_tickets:
                print(f"- {ticket.event.name} (Ticket ID: {ticket.id}) - {ticket.event.date}")
        
        print("-" * 60)
        
    except Exception as e:
        print(f"Error finding attendee: {str(e)}")
    
    input("\nPress Enter to continue...")