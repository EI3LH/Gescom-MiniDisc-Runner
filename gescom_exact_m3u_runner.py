#!/usr/bin/env python3
"""
Gescom MiniDisc exact-order permutation runner.

Purpose
-------
Enumerate all 88! permutations of the 88 ripped tracks in exact
lexicographic order, without ever materializing the impossible full
playlist.

The script writes ONE 88-entry M3U at a time and optionally launches
your media player with it. When the player exits, the script advances to
the next permutation.

Track order
-----------
The initial order is exactly the order of filenames in TRACKS.TXT.
Therefore, put your 88 files in the intended canonical track order
(one filename per line) and do not alphabetize them unless that is what
you want.

Example with mpv:
    python gescom_exact_m3u_runner.py tracks.txt --player "mpv --playlist={m3u}"

Example with VLC:
    python gescom_exact_m3u_runner.py tracks.txt --player "vlc --playlist={m3u}"

The {m3u} placeholder is replaced with the temporary playlist path.

Checkpointing
-------------
A checkpoint file stores the permutation number that has been completed.
If the machine stops, rerun the same command and the script resumes from
the next permutation.

The permutation counter is zero-based:
    0 = the original order
    1 = the next lexicographic ordering
    ...
    88! - 1 = the final ordering

The script is deliberately designed not to create an astronomical M3U.
Only one 88-entry M3U exists at a time.
"""

from __future__ import annotations

import argparse
import math
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path


TOTAL_PERMUTATIONS = math.factorial(88)


def load_tracks(path: Path) -> list[str]:
    """Load exactly 88 track paths in the user's specified base order."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise RuntimeError(f"Could not read {path}: {exc}") from exc

    tracks = [
        line.strip()
        for line in lines
        if line.strip() and not line.lstrip().startswith("#")
    ]

    if len(tracks) != 88:
        raise RuntimeError(
            f"{path} contains {len(tracks)} track entries; exactly 88 are required."
        )

    return tracks


def next_permutation(values: list[int]) -> bool:
    """
    Transform `values` into the next lexicographic permutation in place.
    Return False after the final permutation has been reached.
    """
    i = len(values) - 2
    while i >= 0 and values[i] >= values[i + 1]:
        i -= 1

    if i < 0:
        return False

    j = len(values) - 1
    while values[j] <= values[i]:
        j -= 1

    values[i], values[j] = values[j], values[i]
    values[i + 1 :] = reversed(values[i + 1 :])
    return True


def permutation_from_rank(n: int, rank: int) -> list[int]:
    """
    Return the exact zero-based lexicographic permutation for `rank`
    using factorial-number-system unranking.
    """
    if rank < 0 or rank >= math.factorial(n):
        raise ValueError("Permutation rank is outside the valid range.")

    remaining = list(range(n))
    result: list[int] = []

    for k in range(n, 0, -1):
        block = math.factorial(k - 1)
        index, rank = divmod(rank, block)
        result.append(remaining.pop(index))

    return result


def write_m3u(tracks: list[str], permutation: list[int], output: Path, number: int) -> None:
    """Write a single exact 88-entry M3U playlist."""
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("#EXTM3U\n")
        handle.write(f"# Gescom MiniDisc exact permutation {number}\n")
        for index in permutation:
            handle.write(tracks[index] + "\n")


def read_checkpoint(path: Path) -> int:
    """Return the next permutation number to play."""
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return 0
    value = int(text)
    if value < 0:
        raise RuntimeError("Checkpoint cannot be negative.")
    return value


def write_checkpoint(path: Path, next_number: int) -> None:
    """Atomically replace the checkpoint file."""
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(str(next_number), encoding="utf-8")
    temp.replace(path)


def launch_player(player_template: str, m3u_path: Path) -> int:
    """
    Launch the user's media player.

    `{m3u}` inside player_template is replaced by a safely shell-quoted
    absolute path. The template is executed through the user's shell so
    normal player command lines and flags work.
    """
    quoted = shlex.quote(str(m3u_path.resolve()))
    command = player_template.replace("{m3u}", quoted)
    completed = subprocess.run(command, shell=True, check=False)
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Play every Gescom MiniDisc track permutation in exact lexicographic order."
    )
    parser.add_argument(
        "tracks",
        type=Path,
        help="Text file containing exactly 88 track filenames/paths, in canonical order.",
    )
    parser.add_argument(
        "--player",
        help="Player command containing {m3u}, e.g. 'mpv --playlist={m3u}'.",
    )
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=Path("gescom_permutation_checkpoint.txt"),
        help="Checkpoint file used to resume after interruption.",
    )
    parser.add_argument(
        "--m3u",
        type=Path,
        default=Path("gescom_current_permutation.m3u"),
        help="Temporary/current one-permutation M3U file.",
    )
    parser.add_argument(
        "--start",
        type=int,
        help="Start at this zero-based permutation number instead of using the checkpoint.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Generate/play exactly one permutation, then exit.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print permutation numbers and filenames without launching the player.",
    )
    parser.add_argument(
        "--show-first",
        action="store_true",
        help="Show the first 88-entry permutation and exit.",
    )

    args = parser.parse_args()

    try:
        tracks = load_tracks(args.tracks)
        number = args.start if args.start is not None else read_checkpoint(args.checkpoint)

        if number >= TOTAL_PERMUTATIONS:
            print("Checkpoint is already at the end: all permutations are complete.")
            return 0

        permutation = permutation_from_rank(88, number)

        if args.show_first:
            for position, track_index in enumerate(permutation, start=1):
                print(f"{position:02d}: {tracks[track_index]}")
            return 0

        while number < TOTAL_PERMUTATIONS:
            write_m3u(tracks, permutation, args.m3u, number)

            print(f"Permutation {number + 1} / {TOTAL_PERMUTATIONS:,}")
            print(f"Scientific form: {number + 1:.6e} / 1.8548264225739844e134")

            if args.dry_run:
                for track_index in permutation:
                    print(tracks[track_index])
            elif args.player:
                return_code = launch_player(args.player, args.m3u)
                if return_code != 0:
                    print(
                        f"Player exited with status {return_code}. "
                        "The current permutation is NOT marked complete.",
                        file=sys.stderr,
                    )
                    return return_code
            else:
                print(f"Generated: {args.m3u.resolve()}")
                print("No --player supplied, so playback was not started.")

            # Only mark this permutation complete after successful generation/
            # playback handling. Then advance to the next exact permutation.
            number += 1
            write_checkpoint(args.checkpoint, number)

            if args.once or not args.player:
                return 0

            if number >= TOTAL_PERMUTATIONS:
                print("All permutations have been completed.")
                return 0

            if not next_permutation(permutation):
                # Defensive consistency check; this should happen only after
                # the final permutation, which is handled above.
                raise RuntimeError("Could not advance to the next permutation.")

        return 0

    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
