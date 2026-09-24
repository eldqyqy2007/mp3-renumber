#!/usr/bin/env python3
"""
MP3 Renumber Tool
------------------
Scans a folder for .mp3 files, removes any existing numbering found
ANYWHERE in each file name (not just at the start), then adds a new
sequential number prefix starting from a number you choose, with a
padding width you choose (e.g. 001, 0001, ...).

Example:
    "03 - My Song.mp3"        -> "007 - My Song.mp3"
    "My Song 12.mp3"          -> "008 - My Song.mp3"
    "(1) Cool - Track 05.mp3" -> "009 - Cool - Track.mp3"

Any standalone number found in the name is treated as old numbering
and removed, wherever it appears. Only isolated digit groups are
removed (a number that is glued to letters, like "MP3" or "4K", is
left alone since it isn't a standalone number).

Before anything is renamed, the tool shows a full preview of the old and
new names and asks for confirmation. Nothing is changed until you
answer "y".
"""

import os
import re
import sys

# Matches a standalone number anywhere in the name, optionally wrapped
# in brackets/parentheses/hash, e.g.: "03", "(03)", "[7]", "#12"
NUMBER_TOKEN_PATTERN = re.compile(r'[\(\[]?#?\b\d+\b[\)\]]?')

# Matches leftover separator clutter after numbers are removed
# (extra spaces, dashes, underscores, dots, colons)
SEPARATOR_CLUTTER_PATTERN = re.compile(r'[\s\-_.:]{2,}')
EDGE_SEPARATOR_PATTERN = re.compile(r'^[\s\-_.:]+|[\s\-_.:]+$')


def natural_sort_key(filename):
    """Sort files in a human-friendly way (so '2' comes before '10')."""
    return [
        int(chunk) if chunk.isdigit() else chunk.lower()
        for chunk in re.split(r'(\d+)', filename)
    ]


def strip_old_numbering(name_without_ext):
    """Remove any standalone old numbering found anywhere in the name."""
    without_numbers = NUMBER_TOKEN_PATTERN.sub(' ', name_without_ext)
    collapsed = SEPARATOR_CLUTTER_PATTERN.sub(' ', without_numbers)
    return EDGE_SEPARATOR_PATTERN.sub('', collapsed).strip(' -_.:')


def get_folder_path():
    while True:
        folder = input("Enter the folder path containing the MP3 files: ").strip().strip('"')
        if os.path.isdir(folder):
            return folder
        print("This path does not exist or is not a folder. Please try again.\n")


def get_start_number():
    while True:
        raw = input("Enter the number you want to start counting from: ").strip()
        if raw.isdigit() and int(raw) >= 0:
            return int(raw)
        print("Please enter a valid non-negative number.\n")


def get_padding_width():
    while True:
        raw = input(
            "How many digits should the numbers have? "
            "(e.g. 2 -> 01, 3 -> 001, 4 -> 0001): "
        ).strip()
        if raw.isdigit() and int(raw) >= 1:
            return int(raw)
        print("Please enter a valid positive number.\n")


def confirm(prompt):
    """Ask a yes/no question. Returns True only for an explicit yes."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please answer with y or n.\n")


def main():
    print("=== MP3 Renumber Tool ===\n")

    folder = get_folder_path()
    start_number = get_start_number()
    pad_width = get_padding_width()

    mp3_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp3')]

    if not mp3_files:
        print("\nNo MP3 files were found in this folder.")
        return

    mp3_files.sort(key=natural_sort_key)

    total_files = len(mp3_files)
    largest_number = start_number + total_files - 1
    if len(str(largest_number)) > pad_width:
        print(
            f"\nNote: the last file number ({largest_number}) has more digits "
            f"than your chosen padding ({pad_width}), so it won't be padded further."
        )

    print(f"\nFound {total_files} MP3 file(s). Starting from number {start_number}.\n")

    # First pass: build the list of (old_path, new_path) to avoid
    # collisions/overwrites while renaming.
    rename_plan = []
    current_number = start_number
    for filename in mp3_files:
        name_only, ext = os.path.splitext(filename)
        clean_name = strip_old_numbering(name_only)

        number_str = str(current_number).zfill(pad_width)
        new_filename = f"{number_str} - {clean_name}{ext}"

        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_filename)

        rename_plan.append((old_path, new_path, filename, new_filename))
        current_number += 1

    # Preview: show the full plan and ask for confirmation. Nothing has
    # been changed on disk up to this point.
    print("Preview of the changes (nothing has been renamed yet):\n")
    for _, _, old_name, new_name in rename_plan:
        print(f"  {old_name}  ->  {new_name}")

    print()
    if not confirm(f"Rename these {total_files} file(s)? (y/n): "):
        print("\nCancelled. No files were changed.")
        return
    print()

    # Use temporary names first to safely handle any name overlaps
    temp_paths = []
    for old_path, new_path, _, _ in rename_plan:
        temp_path = old_path + ".tmp_renaming"
        os.rename(old_path, temp_path)
        temp_paths.append(temp_path)

    for temp_path, (_, new_path, old_name, new_name) in zip(temp_paths, rename_plan):
        os.rename(temp_path, new_path)
        print(f"  {old_name}  ->  {new_name}")

    print(f"\nDone! Renamed {total_files} file(s) starting from {start_number}.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
