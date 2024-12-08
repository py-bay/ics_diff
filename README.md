# ICS Diff Script

This script compares two ICS (iCalendar) files: a "base" ICS file and a "changed" ICS file. It identifies events that have been added, removed, or modified between the two files and then exports the results to a new ICS file. This can be helpful for tracking changes in calendar events, such as meetings, reminders, and other scheduled events.

## Overview

Given two ICS files:
- **Base ICS file**: The original calendar events.
- **Changed ICS file**: The updated calendar events after some modifications.

The script will:
1. Compare events in both ICS files.
2. Identify events that are added, removed, or updated.
3. Generate a new ICS file containing:
   - Events that are newly added.
   - Events that were removed (prefixed with "DELETED").
   - Events that were modified (prefixed with "UPDATED").

## Features

- **Identification of Added Events:** Any event present in the changed ICS that was not in the base ICS is marked as new.
- **Identification of Removed Events:** Any event present in the base ICS but not in the changed ICS is included with a "DELETED" tag.
- **Identification of Modified Events:** Any event present in both files but with differing details (name, start/end time, location) is included with an "UPDATED" tag.
- **Flexible Output Directory:** You can specify where the resulting ICS file should be stored.
- **Time-Stamped Output:** The output file name is time-stamped, ensuring no overwrites occur.

## Installation

1. Clone or download the script:
```bash
git clone https://github.com/py-bay/ics_diff.git
cd ics_diff
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python ics_diff_script.py [options] <path_to_base_ics> <path_to_changed_ics>
```

**Positional Arguments:**
- ```path_to_base_ics```: Path to the original/base ICS file.
- ```path_to_changed_ics```: Path to the ICS file containing changes.
- 
**Options:**
- ```-o, --output-dir```: Specify the directory for the output ICS file. Defaults to the current directory.
