#!/usr/bin/env python3
"""
Downloads Folder Organiser
Sorts files in your Downloads folder into subfolders by file extension.
"""

import os
import shutil
from pathlib import Path

# --- Configuration ---
# Map folder names to the extensions they should contain.
# Files with extensions not listed here go into 'Misc'.
FOLDER_MAP = {
    "Images":     {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico", ".heic", ".raw"},
    "Videos":     {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpeg", ".mpg"},
    "Audio":      {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".aiff", ".opus"},
    "Documents":  {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".txt", ".rtf", ".pages", ".numbers", ".key"},
    "Archives":   {".zip", ".tar", ".gz", ".bz2", ".rar", ".7z", ".xz", ".tgz", ".dmg", ".iso"},
    "Code":       {".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rb", ".php", ".sh", ".json", ".xml", ".yaml", ".yml", ".toml", ".sql", ".r", ".swift", ".kt"},
    "Executables":{".exe", ".msi", ".app", ".deb", ".rpm", ".pkg", ".apk"},
    "Fonts":      {".ttf", ".otf", ".woff", ".woff2", ".eot"},
    "Ebooks":     {".epub", ".mobi", ".azw", ".azw3"},
    "Torrents":   {".torrent"},
}

# Build a reverse lookup: extension -> folder name
EXT_TO_FOLDER = {}
for folder, exts in FOLDER_MAP.items():
    for ext in exts:
        EXT_TO_FOLDER[ext.lower()] = folder


def organise(downloads_path: Path, dry_run: bool = False) -> None:
    """
    Organise files in downloads_path into subfolders.

    Args:
        downloads_path: Path to the Downloads folder.
        dry_run:        If True, print what would happen without moving anything.
    """
    if not downloads_path.is_dir():
        print(f"Error: '{downloads_path}' is not a valid directory.")
        return

    mode = "[DRY RUN] " if dry_run else ""
    moved = 0
    skipped = 0

    print(f"\n{mode}Organising: {downloads_path}\n{'─' * 50}")

    for item in sorted(downloads_path.iterdir()):
        # Skip directories (including the ones we'll create)
        if item.is_dir():
            skipped += 1
            continue

        ext = item.suffix.lower()
        if not ext:
            folder_name = "Misc"          # no extension at all
        else:
            folder_name = EXT_TO_FOLDER.get(ext, "Misc")

        dest_dir = downloads_path / folder_name
        dest_file = dest_dir / item.name

        # Handle name collisions by appending a counter
        counter = 1
        while dest_file.exists():
            stem = item.stem
            dest_file = dest_dir / f"{stem} ({counter}){item.suffix}"
            counter += 1

        print(f"  {mode}{'→' if not dry_run else '↝'} {item.name:40s}  ➜  {folder_name}/")

        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_file))

        moved += 1

    print(f"\n{'─' * 50}")
    print(f"{mode}Done. {moved} file(s) {'moved' if not dry_run else 'would be moved'}, {skipped} folder(s) skipped.\n")


def main():
    import argparse

    default_downloads = Path.home() / "Downloads"

    parser = argparse.ArgumentParser(
        description="Organise your Downloads folder by file extension."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(default_downloads),
        help=f"Path to the folder to organise (default: {default_downloads})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without actually moving files.",
    )
    args = parser.parse_args()

    target = Path(args.path).expanduser().resolve()
    organise(target, dry_run=args.dry_run)


if __name__ == "__main__":
    main()