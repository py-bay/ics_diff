import argparse
import os
from ics import Calendar, Event
from datetime import datetime

def main(path_base_ics: str, path_change_ics: str, output_dir: str):
    # Read ICS content from files
    base_ics_content = get_ics_content(path_base_ics)
    change_ics_content = get_ics_content(path_change_ics)

    # Parse calendars
    base_calendar = Calendar(base_ics_content)
    change_calendar = Calendar(change_ics_content)

    # Convert events to comparable tuples
    base_events = {event_to_tuple(event): event for event in base_calendar.events}
    change_events = {event_to_tuple(event): event for event in change_calendar.events}

    # Calculate differences
    added_events = set(change_events.keys()) - set(base_events.keys())
    removed_events = set(base_events.keys()) - set(change_events.keys())
    modified_events = calculate_modifications(base_events, change_events)

    # Prepare results for export
    export_events = []

    # Add removed events
    for key in removed_events:
        event = base_events[key]
        event.name = f"DELETED ({event.name})"
        export_events.append(event)
    
    # Add added events
    for key in added_events:
        event = change_events[key]
        export_events.append(event)

    # Add modified events
    for _, updated_event in modified_events:
        updated_event.name = f"UPDATED ({updated_event.name})"
        export_events.append(updated_event)

    # Export results to a new ICS file
    export_results_to_ics(export_events, output_dir)


def event_to_tuple(event: Event) -> tuple:
    """Convert an Event object to a tuple of significant attributes for comparison."""
    return (event.name, event.begin, event.end, event.location)


def export_results_to_ics(events: list[Event], output_dir: str):
    """Export a list of Event objects to an ICS file."""
    c = Calendar()
    for event in events:
        c.events.add(event)
    
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_path = os.path.join(output_dir, f"{timestamp}-export.ics")
    
    with open(output_path, "w", newline='') as f:
        for line in c.serialize_iter():
            f.write(line.rstrip('\r\n') + '\r\n')

    print(f"Exported results to {output_path}")


def calculate_modifications(base_events, change_events):
    """Find events with the same identifier but different details."""
    modifications = []
    for key in set(base_events.keys()) & set(change_events.keys()):
        base_event = base_events[key]
        change_event = change_events[key]
        if not events_are_equal(base_event, change_event):
            modifications.append((base_event, change_event))
    return modifications


def events_are_equal(event1: Event, event2: Event) -> bool:
    """Compare two events based on their significant attributes."""
    return (
        event1.name == event2.name and
        event1.begin == event2.begin and
        event1.end == event2.end and
        event1.location == event2.location
    )


def get_ics_content(path_to_ics: str) -> str:
    """Read the content of an ICS file."""
    with open(path_to_ics, "r") as f:
        return f.read()


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Compare a base ICS calendar file with a changed ICS file.\n"
            "Identify differences and export updated events to a new ICS file."
        )
    )

    parser.add_argument(
        "path_to_base_ics",
        type=str,
        help="Path to the base ICS file"
    )
    parser.add_argument(
        "path_to_changed_ics",
        type=str,
        help="Path to the changed ICS file"
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Directory to store the exported ICS file (default: current directory)"
    )

    args = parser.parse_args()

    # Validate that the paths exist
    if not os.path.exists(args.path_to_base_ics):
        parser.error(f"The base ICS file does not exist: {args.path_to_base_ics}")

    if not os.path.exists(args.path_to_changed_ics):
        parser.error(f"The changed ICS file does not exist: {args.path_to_changed_ics}")

    return args


if __name__ == '__main__':
    args = parse_args()
    main(args.path_to_base_ics, args.path_to_changed_ics, args.output_dir)
