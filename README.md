![Gescom Runner](gescom-runner-banner.png)

# Gescom-MiniDisc-Runner

Software to play back Gescom's 1998 album MiniDisc uniquely, every time.

Gescom Runner generates one 88-track M3U playlist at a time and moves through the possible track orders in exact lexicographic order. It does **not** try to create one enormous playlist containing every possible order; instead, it generates the current order, gives it to VLC, waits for playback to finish, records a checkpoint, and then moves to the next order.

## Full Backstory of the Gescom Runner Project

**Link to my original blog post:** [EI3LH - Gescom, MiniDisc and Mind-boggling Mathematics.](https://ei3lh.eu/2026/09/13/gescom-minidisc-and-mind-boggling-mathematics/)
>
> **Important:** This project is for use with audio files you have legally obtained. Do not add copyrighted audio recordings to this GitHub repository, branches or in your personal use of this software unless you have the necessary rights to redistribute them. Support the artists!
>
---

## Disclaimer & Credits

This project was written with the assistance of **AI (OpenAI's ChatGPT)**. AI was used to help develop, refine, and document the code, while the project itself is provided as an open-source experiment in exploring the absurd combinatorial possibilities of Gescom's *MiniDisc*.

The music is **not included** with this project. Please support the artists and obtain the music legally.

**Purchase Gescom – *MiniDisc*:** [Boomkat — MiniDisc](https://boomkat.com/products/mini-disc)

*Gescom – MiniDisc © Gescom. All rights reserved. This project is not affiliated with or endorsed by Gescom or the rights holders.*

---


## What you need

Before starting, install:

1. **Python 3**
2. **VLC media player**
3. Your 88 legally obtained Gescom 'MiniDisc' audio files representing the 88 pieces you want to play
4. This Python file:
   `gescom_exact_m3u_runner.py`

No third-party Python packages are required. The script uses Python's standard library.


## How the runner works

The program expects a text file containing exactly **88 track filenames or paths**, one per line.

The order in that file defines the starting order:

- permutation `0` = the exact order in `tracks.txt`
- permutation `1` = the next lexicographic order
- permutation `2` = the next one after that
- and so on

The program calculates the total as:

```text
88! = 1.8548264225739844 × 10^134
```

That number is unimaginably large, so the software only creates **one 88-entry M3U file at a time**.


# Step 1 — Put the project files in one folder

Create a folder for the project.

A simple layout is:

```text
Gescom-MiniDisc-Runner/
├── gescom_exact_m3u_runner.py
├── tracks.txt
├── assets/
│   └── gescom-runner-banner.png
├── gescom_current_permutation.m3u          # generated later
└── gescom_permutation_checkpoint.txt       # generated later
```

The last two files are created by the script and do not need to be committed to GitHub.


# Step 2 — Install Python

## Windows

Install Python 3 from the official Python website.

After installation, open **Command Prompt** or **PowerShell** and check:

```powershell
py --version
```

You should see a Python 3 version.

If `py` is not available, try:

```powershell
python --version
```


## macOS

Open **Terminal** and check:

```bash
python3 --version
```

You should see a Python 3 version.

If Python 3 is not installed, install it before continuing.


## Linux

Open a terminal and check:

```bash
python3 --version
```

Install Python 3 using your distribution's normal package manager if necessary.


# Step 3 — Install VLC

Install VLC from VideoLAN using the normal installer/package for your operating system.

After installing VLC, the easiest setup is to make the `vlc` command available from your terminal.

## Windows

Open a new Command Prompt or PowerShell window and run:

```powershell
vlc --version
```

If Windows says that `vlc` is not recognized, add the VLC installation directory to your system `PATH`, then open a new terminal window.

A typical VLC executable location is:

```text
C:\Program Files\VideoLAN\VLC
```

The goal is simply that this works:

```powershell
vlc --version
```


## macOS

The VLC application may not put a `vlc` command on your normal `PATH`.

You can test:

```bash
vlc --version
```

If that command is not found, use VLC's executable inside the application bundle:

```bash
/Applications/VLC.app/Contents/MacOS/VLC --version
```

The examples later in this README use that full path when necessary.


## Linux

Test:

```bash
vlc --version
```

If VLC was installed normally, this will usually work directly.


# Step 4 — Prepare your 88 audio files

Put your 88 audio files somewhere accessible.

For example:

```text
music/
├── track_01.flac
├── track_02.flac
├── track_03.flac
...
└── track_88.flac
```

The files can be WAV, FLAC, MP3, or another format supported by VLC.

**The order matters.**

Decide which file is track 1, which is track 2, and so on. That order becomes the starting point for the entire permutation sequence.


# Step 5 — Create `tracks.txt`

Create a plain text file called:

```text
tracks.txt
```

Put exactly **88 entries** in it, one per line.

For example:

```text
music/track_01.flac
music/track_02.flac
music/track_03.flac
music/track_04.flac
...
music/track_88.flac
```

You can also use absolute paths, for example:

```text
/home/you/Music/Gescom/track_01.flac
```

or:

```text
/Users/you/Music/Gescom/track_01.flac
```

or:

```text
D:\Music\Gescom\track_01.flac
```

Relative paths are often easier to maintain if the project is kept together in one directory.

The script ignores:

- blank lines
- lines beginning with `#`

It does **not** accept fewer or more than 88 track entries.


# Step 6 — Check that all 88 tracks were found

Open a terminal in the project directory.

### Windows

```powershell
py gescom_exact_m3u_runner.py tracks.txt --show-first
```

### macOS / Linux

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --show-first
```

The program should print 88 lines.

If you get:

```text
tracks.txt contains 87 track entries; exactly 88 are required.
```

or a similar message, fix `tracks.txt` before continuing.


# Step 7 — Generate the first playlist without playing it

This is the safest first test.

### Windows

```powershell
py gescom_exact_m3u_runner.py tracks.txt --once
```

### macOS / Linux

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --once
```

The script creates:

```text
gescom_current_permutation.m3u
```

That file contains exactly one 88-track permutation.

For the first run, permutation `0` is simply the order from `tracks.txt`.


# Step 8 — Open the generated M3U in VLC manually

Before starting the automated runner, test that VLC can play the generated playlist.

You can open:

```text
gescom_current_permutation.m3u
```

with VLC using your normal operating-system method.

Make sure:

- all 88 entries resolve to real files
- the tracks play
- VLC can move from one entry to the next
- there are no unexpected interruptions


# Step 9 — Test automated playback with VLC

Once the M3U works correctly, let Python launch VLC for one permutation.

## Windows

```powershell
py gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}" --once
```

## macOS

If `vlc` is available on your `PATH`:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}" --once
```

Otherwise:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "/Applications/VLC.app/Contents/MacOS/VLC --play-and-exit {m3u}" --once
```

## Linux

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}" --once
```

The important part is:

```text
{m3u}
```

The script replaces that placeholder with the path to the current generated playlist.


# Step 10 — Understand what `--once` does

The `--once` option means:

> Generate/play exactly one permutation, then stop.

This is useful for testing.

Once one permutation works correctly, you can remove `--once` to begin continuous operation.


# Step 11 — Start the full runner

## Windows

```powershell
py gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```

## macOS

With VLC on `PATH`:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```

Or with the standard VLC application path:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "/Applications/VLC.app/Contents/MacOS/VLC --play-and-exit {m3u}"
```

## Linux

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```

The runner will now repeat this cycle:

```text
Generate permutation
        ↓
Write M3U
        ↓
Launch VLC
        ↓
VLC plays all 88 tracks
        ↓
VLC exits
        ↓
Save checkpoint
        ↓
Generate next permutation
        ↓
Repeat
```


# Step 12 — Let VLC finish naturally

The script marks a permutation as complete **after VLC exits successfully**.

That means the intended workflow is:

```text
Start VLC
        ↓
Let all 88 tracks play
        ↓
VLC exits because --play-and-exit was reached
        ↓
Python advances to the next permutation
```

**Important:** the Python code only treats a non-zero VLC exit status as a playback failure. Manually closing VLC may therefore be interpreted as a successful exit by the operating system, causing the current permutation to be marked complete.

For the most reliable sequence, allow VLC to finish the playlist normally.


# Step 13 — Understand the checkpoint file

The runner creates:

```text
gescom_permutation_checkpoint.txt
```

The checkpoint contains the number of the **next** permutation to run.

For example, if the file contains:

```text
12345
```

the next run starts at permutation:

```text
12345
```

This means you can stop the computer and later run the same command again without starting from permutation `0`.

The script reads the checkpoint automatically unless you provide `--start`.


# Step 14 — Resume after restarting your computer

After a restart, simply run the same command again.

### Windows

```powershell
py gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```

### macOS / Linux

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```

The checkpoint tells the script where to continue.


# Step 15 — Start at a specific permutation

You can jump directly to a specific zero-based permutation with `--start`.

For example:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --start 1000000 --once
```

On Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --start 1000000 --once
```

This uses factorial-number-system unranking to calculate the requested permutation directly instead of generating all earlier permutations.


# Step 16 — Generate without launching VLC

To generate a playlist and print its contents without launching a player:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --dry-run
```

On Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --dry-run
```

This is useful when testing the permutation logic.


# Step 17 — Use a custom M3U filename

By default, the program creates:

```text
gescom_current_permutation.m3u
```

You can change that with `--m3u`.

Example:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --m3u current.m3u --once
```

Using a simple filename without spaces is recommended, particularly for cross-platform command-line use.


# Step 18 — Use a custom checkpoint filename

The default checkpoint is:

```text
gescom_permutation_checkpoint.txt
```

You can change it with `--checkpoint`.

Example:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt   --checkpoint my_progress.txt   --once
```

This can be useful if you want multiple independent runs or experiments.


# Step 19 — Reset everything and start again

To restart from permutation `0`, remove the checkpoint file:

```text
gescom_permutation_checkpoint.txt
```

Then run the normal command again.

You can also explicitly start from zero:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --start 0 --once
```

On Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --start 0 --once
```


# Step 20 — Do not change `tracks.txt` halfway through a run

The order in `tracks.txt` defines the permutation universe.

For example:

```text
A
B
C
...
```

creates a different universe from:

```text
B
A
C
...
```

Changing the file while keeping an old checkpoint means the checkpoint number will now refer to a different ordering.

For a clean run, keep `tracks.txt` unchanged for the entire sequence.


# Step 21 — Recommended Git configuration

The generated playlist and checkpoint are runtime files.

A useful `.gitignore` is:

```gitignore
gescom_current_permutation.m3u
gescom_permutation_checkpoint.txt
```

You may also choose not to commit `tracks.txt` if it contains personal absolute file paths.

Instead, commit a template such as:

```text
tracks.example.txt
```

with example paths.


# Step 22 — A portable repository layout

A convenient setup is:

```text
Gescom-MiniDisc-Runner/
├── gescom_exact_m3u_runner.py
├── README.md
├── tracks.example.txt
├── assets/
│   └── gescom-runner-banner.png
└── .gitignore
```

Your personal audio collection can live outside the Git repository.


# Step 23 — Command summary

## Test Python

Windows:

```powershell
py --version
```

macOS/Linux:

```bash
python3 --version
```

## Test VLC

```bash
vlc --version
```

or, on macOS when needed:

```bash
/Applications/VLC.app/Contents/MacOS/VLC --version
```

## Check the 88 tracks

Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --show-first
```

macOS/Linux:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --show-first
```

## Generate one playlist

Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --once
```

macOS/Linux:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --once
```

## Play one permutation through VLC

Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}" --once
```

macOS/Linux:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}" --once
```

## Run continuously

Windows:

```powershell
py gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```

macOS/Linux:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --player "vlc --play-and-exit {m3u}"
```


# How this implementation works

The attached Python program uses two permutation techniques.

### 1. Direct permutation lookup

`permutation_from_rank()` uses factorial-number-system unranking.

That allows the program to take a number such as:

```text
1000000
```

and calculate exactly which 88-track permutation that number represents without storing all earlier permutations.

### 2. Sequential advancement

`next_permutation()` changes the current ordering into the next lexicographic ordering.

That lets the runner move from:

```text
permutation N
```

to:

```text
permutation N + 1
```

without generating a giant collection of future playlists.

### 3. One playlist at a time

`write_m3u()` writes only the current 88-entry playlist.

The software therefore scales with the size of a single playlist, not with the total number of permutations.

The Python source explicitly describes this design as generating one 88-entry M3U at a time and avoiding materialization of the full permutation set. fileciteturn0file0L5-L12

### 4. Checkpointed progress

The runner reads a checkpoint when it starts and writes the next permutation number after successful playback handling. The source also defines the permutation counter as zero-based. fileciteturn0file0L30-L40


# Troubleshooting

## "Exactly 88 are required"

Your `tracks.txt` does not contain exactly 88 usable entries.

Count the lines and make sure you have exactly 88 filenames/paths.


## VLC command is not found

Try:

```bash
vlc --version
```

If that fails, either:

- add VLC to your `PATH`
- or use VLC's full executable path in `--player`

On macOS, the standard application-bundle executable is:

```text
/Applications/VLC.app/Contents/MacOS/VLC
```


## VLC opens but does not play the files

First generate a playlist manually:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --once
```

Then open:

```text
gescom_current_permutation.m3u
```

directly in VLC.

If the M3U does not work when opened manually, fix the paths in `tracks.txt` before troubleshooting the Python runner.


## The runner stops after VLC closes

This is expected if VLC returns a non-zero exit status.

The script reports the exit status and does **not** advance the checkpoint in that situation. That behavior is implemented directly in `launch_player()` and the playback loop. fileciteturn0file0L150-L160 fileciteturn0file0L227-L255


## I restarted the computer and it began in the wrong place

Check:

```text
gescom_permutation_checkpoint.txt
```

Also make sure `tracks.txt` has not been changed since the checkpoint was created.


## I want to see a particular permutation

Use:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --start NUMBER --once
```

For example:

```bash
python3 gescom_exact_m3u_runner.py tracks.txt --start 1000000 --once
```


# A note about Windows and command-line paths

The attached script builds the media-player command through a shell and uses Python's `shlex.quote()` when inserting the generated M3U path. fileciteturn0file0L150-L160

For the easiest cross-platform setup:

- keep the generated M3U filename simple, such as `gescom_current_permutation.m3u`
- avoid spaces in the project directory path where practical
- use `vlc` from `PATH` on Windows rather than passing a VLC executable path containing spaces

This avoids unnecessary command-line quoting problems.


# What this project does not do

This runner does **not**:

- randomly shuffle tracks
- create a gigantic all-permutations M3U
- permanently store all permutations
- include the copyrighted audio recordings
- magically make `88!` permutations finish in a human lifetime

It does provide a deterministic, repeatable and resumable way to enumerate the permutation space one playlist at a time.


# Final note

The entire point of Gescom Runner is that the sequence is mathematically enormous while the software needed to traverse it is small.

One playlist is created.

VLC plays it.

The checkpoint advances.

The next playlist is created.

And the process continues.

**Gescom MiniDisc: same tracks, different order, every time.**
