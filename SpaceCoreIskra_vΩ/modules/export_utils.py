import csv
import os
import zipfile
from typing import Iterable


def export_md(entries: Iterable[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(f"## {entry.get('facet', 'Unknown')}\n")
            fh.write(entry.get("answer", "") + "\n\n")


def export_csv(entries: Iterable[dict], path: str) -> None:
    fieldnames = ["facet", "snapshot", "answer", "∆", "D", "Ω", "Λ", "timestamp"]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            row = {key: entry.get(key) for key in fieldnames}
            writer.writerow(row)


def zip_files(files: Iterable[str], zipname: str) -> None:
    with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as archive:
        for file_path in files:
            if os.path.exists(file_path):
                archive.write(file_path, arcname=os.path.basename(file_path))
