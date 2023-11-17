import os
import argparse
from pathlib import Path

def create_hard_link(src_path, dest_path, dry_run=False):
    """
    Create or replace a file with a hard link from src_path to dest_path.
    If dry_run is True, only print the actions without executing them.
    """
    if dry_run:
        print(f"Would create hard link from {src_path} to {dest_path}")
    else:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        if dest_path.exists():
            dest_path.unlink()
        os.link(src_path, dest_path)

def main(original_src, new_src, dry_run):
    for root, _, files in os.walk(new_src):
        for file in files:
            new_file_path = Path(root, file)
            relative_path = new_file_path.relative_to(new_src)
            original_file_path = Path(original_src, relative_path)

            create_hard_link(new_file_path, original_file_path, dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create hard links from new src to original src.")
    parser.add_argument("original_src", type=str, help="Path to the original src directory")
    parser.add_argument("new_src", type=str, help="Path to the new src directory")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without making any changes")

    args = parser.parse_args()
    main(args.original_src, args.new_src, args.dry_run)
