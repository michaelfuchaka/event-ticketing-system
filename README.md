# Event Ticketing System

A command-line interface (CLI) application for managing events, attendees, and ticket bookings built with Python, SQLAlchemy ORM, and SQLite database.

## Features

- **Event Management**: Create, view, and search events
- **Attendee Management**: Register attendees and view their information
- **Ticket Booking**: Book and cancel tickets for events
- **Data Persistence**: All data stored in SQLite database
- **Input Validation**: Comprehensive error handling and user input validation
- **Interactive CLI**: Menu-driven interface with clear navigation

## Project Structure

```
event-ticketing-system/
├── Pipfile                 # Project dependencies
├── Pipfile.lock           # Locked dependency versions
├── README.md              # Project documentation
└── lib/
    ├── models/            # Database models
    │   ├── __init__.py    # Database configuration
    │   ├── event.py       # Event model class
    │   ├── attendee.py    # Attendee model class
    │   └── ticket.py      # Ticket model class
    ├── migrations/        # Alembic database migrations
    ├── cli.py            # Main CLI application
    ├── helpers.py        # CLI helper functions
    ├── alembic.ini       # Alembic configuration
    └── event_ticketing.db # SQLite database file
```

## Installation and Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd event-ticketing-system
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   pipenv shell
   ```

3. **Set up the database**
   ```bash
   cd lib
   alembic upgrade head
   ```

4. **Run the application**
   ```bash
   python3 cli.py
   ```

## Database Models

### Event Model (`lib/models/event.py`)
Represents events with the following attributes:
- `id`: Primary key (auto-generated)
- `name`: Event name (string, required)
- `location`: Event location (string, required)
- `date`: Event date (date, required)
- `capacity`: Maximum attendees (integer, required)

**Methods:**
- `create(name, location, date, capacity)`: Create new event
- `get_all()`: Retrieve all events
- `find_by_id(event_id)`: Find event by ID
- `delete()`: Delete event and associated tickets
- `available_spots()`: Calculate available capacity
- `is_full()`: Check if event is at capacity

### Attendee Model (`lib/models/attendee.py`)
Represents event attendees with the following attributes:
- `id`: Primary key (auto-generated)
- `name`: Attendee full name (string, required)
- `contact`: Email or phone contact (string, required)

**Methods:**
- `create(name, contact)`: Create new attendee
- `get_all()`: Retrieve all attendees
- `find_by_id(attendee_id)`: Find attendee by ID
- `find_by_contact(contact)`: Find attendee by contact info
- `delete()`: Delete attendee and associated tickets
- `get_events()`: Get all events attendee is registered for

### Ticket Model (`lib/models/ticket.py`)
Junction table linking events and attendees with the following attributes:
- `id`: Primary key (auto-generated)
- `event_id`: Foreign key to events table
- `attendee_id`: Foreign key to attendees table
- `booked_at`: Timestamp of booking (auto-generated)

**Methods:**
- `create(event_id, attendee_id)`: Book new ticket
- `get_all()`: Retrieve all tickets
- `find_by_id(ticket_id)`: Find ticket by ID
- `get_tickets_for_event(event_id)`: Get all tickets for an event
- `get_tickets_for_attendee(attendee_id)`: Get all tickets for an attendee
- `delete()`: Cancel ticket booking

## CLI Application (`lib/cli.py`)

The main application file provides an interactive menu system with the following options:

1. **Create New Event**: Add events with validation for date, capacity, and required fields
2. **Book Ticket**: Select events and register attendees with duplicate booking prevention
3. **Cancel Ticket**: Remove existing bookings by ticket ID
4. **View All Events**: Display all events with capacity and booking information
5. **View Attendees for Event**: Show all attendees registered for a specific event
6. **View All Attendees**: List all attendees with their registration counts
7. **Find Event by ID**: Search and display detailed event information
8. **Find Attendee by ID**: Search and display detailed attendee information

## Helper Functions (`lib/helpers.py`)

Contains all CLI functionality organized into specific functions:

- `create_event_menu()`: Handle event creation with input validation
- `book_ticket_menu()`: Manage ticket booking process
- `cancel_ticket_menu()`: Handle ticket cancellation
- `view_events_menu()`: Display formatted event listings
- `view_attendees_menu()`: Show attendees for specific events
- `view_all_attendees_menu()`: Display all attendee information
- `find_event_menu()`: Search functionality for events
- `find_attendee_menu()`: Search functionality for attendees
- `exit_program()`: Clean application exit

## Input Validation and Error Handling

The application includes comprehensive validation:

- **Event Creation**: Validates name length, date format, future dates, positive capacity
- **Attendee Registration**: Validates name format, email/phone contact format
- **Ticket Booking**: Prevents double booking, checks event capacity, validates IDs
- **User Input**: Handles empty inputs, invalid data types, and out-of-range values

## Relationships

The database implements the following relationships:
- **One-to-Many**: Event → Tickets (one event can have many tickets)
- **One-to-Many**: Attendee → Tickets (one attendee can have many tickets)
- **Many-to-Many**: Events ↔ Attendees (through Tickets junction table)



## Dependencies

- **Python 3.8+**: Core programming language
- **SQLAlchemy**: Object-Relational Mapping (ORM)
- **Alembic**: Database migration management
- **SQLite**: Lightweight database engine
- **Faker**: Generate test data (development)
- **ipdb**: Interactive debugger (development)

## Usage Examples

### Creating an Event
```
Event name: Tech Conference 2025
Event location: Nairobi
Event date (YYYY-MM-DD): 2025-09-15
Event capacity: 100
```

### Booking a Ticket
```
Enter Event ID: 1
Attendee name: Michael Fuchaka
Attendee contact (email or phone): mike399@gmail.com
```

### Viewing Event Attendees
```
Enter Event ID: 1
```

## Error Messages

The application provides informative error messages for common issues:
- "Event is at full capacity" - when trying to book tickets for sold-out events
- "Attendee already has a ticket for this event" - prevents duplicate bookings
- "Event date cannot be in the past" - validates future event dates
- "Invalid email address or phone number" - validates contact information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the [MIT License](./LICENSE).

