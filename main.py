import os
from ics import Calendar, Event
from datetime import datetime

def main(path_base_ics: str, path_change_ics: str):
    # Ensure both file paths exist
    check_path(path_base_ics)
    check_path(path_change_ics)
    
    # Read ICS content from files
    base_ics_content = get_ics_content(path_base_ics)
    change_ics_content = get_ics_content(path_change_ics)

    # Parse calendars
    base_calendar = Calendar(base_ics_content)
    change_calendar = Calendar(change_ics_content)

    # Convert events to tuples for comparison
    base_events = {event_to_tuple(event) for event in base_calendar.events}
    change_events = {event_to_tuple(event) for event in change_calendar.events}

    # Calculate differences
    added_events = change_events - base_events  # Events in the new file only
    removed_events = base_events - change_events  # Events in the old file only
    modified_events = calculate_modifications(base_calendar.events, change_calendar.events)


    export_events = added_events + removed_events

    export_results_to_ics(export_events)


def event_to_tuple(event: Event) -> tuple:
    """Convert an Event object to a tuple of significant attributes for comparison."""
    return (event.name, event.begin, event.end, event.location)



def export_results_to_ics(events: set[Event]):
    c = Calendar()
    c.events.add(events)
    
    timestamp = datetime.now()
    with open(f"{timestamp}-export.ics", "w") as f:
        f.write(c.serialize())

def calculate_modifications(base_events, change_events):
    """Find events with the same identifier but different details."""
    modifications = []
    base_event_map = {event.uid: event for event in base_events}
    for event in change_events:
        if event.uid in base_event_map:
            base_event = base_event_map[event.uid]
            if not events_are_equal(base_event, event):
                modifications.append((base_event, event))
    return modifications


def events_are_equal(event1, event2):
    """Compare two events based on their significant attributes."""
    return (
        #event1.name == event2.name and
        event1.begin == event2.begin and
        event1.end == event2.end #and
        #event1.location == event2.location
    )


def get_ics_content(path_to_ics: str) -> str:
    """Read the content of an ICS file."""
    with open(path_to_ics, "r") as f:
        return f.read()


def check_path(path: str) -> bool:
    """Check if the given file path exists."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at path {path} does not exist.")
    return True


if __name__ == '__main__':
    # path_base_ics = sys.argv[1]
    # path_change_ics = sys.argv[2]
    path_base_ics = "base.ics"
    path_change_ics = "change.ics"

    main(path_base_ics, path_change_ics)
