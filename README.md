# MP3 Renumber Tool

A small, dependency-free command-line tool that **cleans and renumbers MP3 file names** in a folder. It strips any old numbering, sorts the files in natural order, and adds a fresh sequential prefix starting from any number you choose, with any padding width you choose.

```
03 - My Song.mp3   →   007 - My Song.mp3
My Song 12.mp3     →   008 - My Song.mp3
```

Ideal for lecture series, audiobooks, podcasts, and any collection where file order matters (for example, playing in the right order on a phone or car stereo).

---

## Features

- **Preview before renaming** – see every old → new name first, and nothing is touched until you confirm with `y`.
- **Natural sorting** – files are ordered the way a human expects (`2` comes before `10`), not alphabetically.
- **Cleans old numbering anywhere in the name** – not only at the start. Numbers such as `03`, `(3)`, `[3]`, `#3` are removed wherever they appear.
- **Safe with words containing digits** – `MP3`, `4K`, `2Pac` are left untouched, because the digits are attached to letters and are not standalone numbers.
- **Custom start number** – begin at `1`, `101`, or any non-negative number.
- **Custom zero-padding** – `01`, `001`, `0001`, and so on.
- **Collision-safe renaming** – files are moved to temporary names first, so overlapping names never overwrite each other.
- **Unicode friendly** – works with Arabic and other non-Latin file names.
- **Zero dependencies** – uses only the Python standard library.
- **Cross-platform** – Windows, macOS, Linux, and Android (Termux).

---

## Requirements

- Python **3.6** or newer

No other packages are needed.

**Termux (Android)**
```bash
pkg update
pkg install python
```

---

## Installation

```bash
git clone https://github.com/eldqyqy2007/mp3-renumber.git
cd mp3-renumber
```

Or simply download `mp3_renumber.py` and run it directly.

---

## Usage

```bash
python3 mp3_renumber.py
```

The tool asks three questions, shows a preview, and then asks for confirmation:

| Prompt | Meaning | Example |
|---|---|---|
| Folder path | Folder that contains the MP3 files | `/sdcard/Music/course` |
| Start number | First number to use | `1` |
| Number of digits | Padding width | `3` → `001` |

On Termux, the shared storage is available under `~/storage/shared/` after running `termux-setup-storage` once.

### Example session

```text
=== MP3 Renumber Tool ===

Enter the folder path containing the MP3 files: /sdcard/Music/course
Enter the number you want to start counting from: 1
How many digits should the numbers have? (e.g. 2 -> 01, 3 -> 001, 4 -> 0001): 3

Found 3 MP3 file(s). Starting from number 1.

Preview of the changes (nothing has been renamed yet):

  Lecture 1.mp3   ->  001 - Lecture.mp3
  Lecture 2.mp3   ->  002 - Lecture.mp3
  Lecture 10.mp3  ->  003 - Lecture.mp3

Rename these 3 file(s)? (y/n): y

  Lecture 1.mp3   ->  001 - Lecture.mp3
  Lecture 2.mp3   ->  002 - Lecture.mp3
  Lecture 10.mp3  ->  003 - Lecture.mp3

Done! Renamed 3 file(s) starting from 1.
```

Answer `n` at the confirmation prompt to cancel; no file is changed.

---

## How It Works

1. **Scan** – collects all files ending in `.mp3` (case-insensitive) in the chosen folder. Sub-folders are not searched.
2. **Sort** – orders them with a natural sort, splitting each name into text and number parts.
3. **Clean** – removes every standalone number (optionally wrapped in `()`, `[]`, or preceded by `#`) and tidies leftover separators (`-`, `_`, `.`, `:`, extra spaces).
4. **Number** – builds each new name as `<padded number> - <clean name>.mp3`.
5. **Preview & confirm** – prints the complete list of old and new names and waits for `y` or `n`. Nothing has been changed at this point.
6. **Rename safely** – after confirmation, renames every file to a temporary `.tmp_renaming` name first, then to its final name, so no file is ever overwritten.

### What counts as "old numbering"?

| Original name | Cleaned name | Why |
|---|---|---|
| `03 - My Song` | `My Song` | Leading number |
| `My Song 12` | `My Song` | Trailing number |
| `[7] Name #3` | `Name` | Bracketed and `#` numbers |
| `Song 2Pac` | `Song 2Pac` | Digit attached to letters – kept |
| `Intro MP3` | `Intro MP3` | Digit attached to letters – kept |
| `Track_05` | `Track_05` | Underscore joins the number to the word – kept |

---

## Important Notes

> **Always read the preview carefully.** The tool shows exactly what will change and only proceeds after you type `y`. Once confirmed, files are renamed in place and there is **no undo**, so consider working on a **copy** of your folder the first time you use it.

- **Every standalone number is removed**, not just the leading one. A name like `Lecture 5 - Part 2` becomes `Lecture Part`. This is by design, and the preview lets you spot it before anything changes. Cancel with `n` if your titles contain numbers you want to keep (years, episode numbers, etc.).
- **Separators inside a name may be merged.** Removing a number from the middle of a name can also drop the dash next to it (`Cool - Track 05` → `Cool Track`).
- **A name made only of numbers** (for example `2024.mp3`) becomes `001 - .mp3`, because nothing remains after cleaning.
- If the last number needs more digits than your chosen padding (for example 1000 files with padding 3), the tool prints a note and does not pad further.
- Only `.mp3` files are touched. All other files are left alone.
- If the tool is interrupted in the middle of renaming, some files may keep the `.tmp_renaming` suffix. Rename them back manually by removing that suffix.

---

## Troubleshooting

**"This path does not exist or is not a folder"**
Check the path for typos. On Termux, run `termux-setup-storage` first and use a path under `~/storage/shared/`.

**"No MP3 files were found in this folder"**
The tool only looks inside the folder you gave it, not its sub-folders, and only for files ending in `.mp3`.

**Some files end with `.tmp_renaming`**
The run was interrupted. Remove the `.tmp_renaming` suffix from those file names and run the tool again.

---

## Contributing

Issues and pull requests are welcome. Ideas for future improvements:

- Undo log (restore original names after a run)
- Support for more audio formats
- Optional recursive folder scanning

---

## License

This project is licensed under the [MIT License](LICENSE).
