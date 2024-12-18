import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, Event, Attendee, Ticket

DATABASE_URL = "sqlite:///events.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
    print("Database Initialized")

def create_event():
    name = input("Enter event name: ")
    description = input("Enter event description: ")
    date_str = input("Enter event date (YYYY-MM-DD): ")
    date = datetime.strptime(date_str, '%Y-%m-%d')
    location = input("Enter event location: ")

    event = Event(name=name, description=description, date=date, location=location)
    session.add(event)
    session.commit()
    print(f"Event '{name}' created with ID {event.id}")

def update_event():
    event_id = int(input("Enter event ID to update: "))
    event = session.get(Event, event_id)
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        return

    event.name = input(f"Enter new name for event (current: {event.name}): ") or event.name
    event.description = input(f"Enter new description for event (current: {event.description}): ") or event.description
    event.location = input(f"Enter new location for event (current: {event.location}): ") or event.location
    date_str = input(f"Enter new date for event (current: {event.date.strftime('%Y-%m-%d')}): ") or event.date.strftime('%Y-%m-%d')
    event.date = datetime.strptime(date_str, '%Y-%m-%d')

    session.commit()
    print(f"Event with ID {event_id} updated successfully")

def delete_event():
    event_id = int(input("Enter event ID to delete: "))
    event = session.get(Event, event_id)
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        return

    session.delete(event)
    session.commit()
    print(f"Event with ID {event_id} deleted successfully.")

def create_ticket():
    event_id = int(input("Enter event ID to add ticket: "))
    event = session.get(Event, event_id)
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        return

    ticket_type = input("Enter ticket type (e.g., VIP, Regular): ")
    price = float(input("Enter ticket price: "))
    available_quantity = int(input("Enter number of available tickets: "))

    ticket = Ticket(type=ticket_type, price=price, available_quantity=available_quantity, event=event)
    session.add(ticket)
    session.commit()
    print(f"Ticket '{ticket_type}' added for event '{event.name}'!")

def view_attendees():
    event_id = int(input("Enter event ID to view attendees: "))
    event = session.get(Event, event_id)
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        return

    attendees = event.attendees
    if not attendees:
        print(f"No attendees found for event '{event.name}'.")
        return

    print(f"Attendees for event '{event.name}':")
    for attendee in attendees:
        print(f"- {attendee.name}")

def register_attendee():
    event_id = int(input("Enter event ID to register attendee: "))
    event = session.get(Event, event_id)
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        return

    name = input("Enter attendee name: ")
    email = input("Enter attendee email: ")
    phone = input("Enter attendee phone number: ")

    attendee = Attendee(name=name, email=email, phone=phone)
    session.add(attendee)
    session.commit()

    event.attendees.append(attendee)
    session.commit()

    print(f"Attendee '{name}' registered for event '{event.name}'!")

def delete_attendee():
    attendee_id = int(input("Enter attendee ID to delete: "))
    attendee = session.get(Attendee, attendee_id)
    if not attendee:
        print(f"Attendee with ID {attendee_id} does not exist.")
        return

    session.delete(attendee)
    session.commit()
    print(f"Attendee with ID {attendee_id} deleted successfully.")

def delete_ticket():
    event_id = int(input("Enter event ID to delete ticket: "))
    event = session.get(Event, event_id)
    if not event:
        print(f"Event with ID {event_id} does not exist.")
        return

    ticket_type = input("Enter ticket type to delete: ")
    ticket = session.query(Ticket).filter_by(event_id=event_id, type=ticket_type).first()

    if not ticket:
        print(f"Ticket '{ticket_type}' not found for event '{event.name}'.")
        return

    session.delete(ticket)
    session.commit()
    print(f"Ticket '{ticket_type}' deleted for event '{event.name}'.")

def main_menu():
    while True:
        print("\nEvent Management System - What would you like to do?")
        print("1. Create Event")
        print("2. Update Event")
        print("3. Delete Event")
        print("4. Create Ticket")
        print("5. View Attendees")
        print("6. Register Attendee")
        print("7. Delete Attendee")
        print("8. Delete Ticket")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_event()
        elif choice == "2":
            update_event()
        elif choice == "3":
            delete_event()
        elif choice == "4":
            create_ticket()
        elif choice == "5":
            view_attendees()
        elif choice == "6":
            register_attendee()
        elif choice == "7":
            delete_attendee()
        elif choice == "8":
            delete_ticket()
        elif choice == "9":
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    init_db()
    main_menu()
