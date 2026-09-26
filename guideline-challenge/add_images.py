"""Đăng ký ảnh ngoài (được giảng viên cho phép) vào data/ và data/catalog.csv.

Cách dùng (đứng trong thư mục guideline-challenge/):
    py add_images.py <thư mục chứa ảnh> [--prefix OVH] [--source overhang]

- Ảnh được sắp theo tên file, copy thành data/<source>/<PREFIX>01.jpg, <PREFIX>02.jpg, ...
- Mỗi ảnh thêm một dòng vào data/catalog.csv (original_name = tên file gốc).
- Chạy lại với cùng prefix sẽ bỏ qua các sample_id đã có trong catalog.
Chỉ dùng thư viện chuẩn của Python.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import struct
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
CATALOG = BASE / "data" / "catalog.csv"
COLUMNS = ["sample_id", "file", "source", "original_name", "sequence", "width", "height", "weather", "timeofday", "scene"]
EXTS = {".jpg", ".jpeg", ".png"}


def image_size(path: Path):
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            length = struct.unpack(">H", data[i + 2:i + 4])[0]
            i += 2 + length
    return "", ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--prefix", default="OVH")
    ap.add_argument("--source", default="overhang")
    args = ap.parse_args()

    src = Path(args.folder)
    files = sorted(p for p in src.iterdir() if p.suffix.lower() in EXTS)
    if not files:
        print(f"✗ Không thấy ảnh .jpg/.png trong {src}")
        return 1

    with CATALOG.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    existing = {r["sample_id"] for r in rows}
    originals = {(r["source"], r["original_name"]) for r in rows}

    out_dir = BASE / "data" / args.source
    out_dir.mkdir(parents=True, exist_ok=True)
    n = sum(1 for r in rows if r["sample_id"].startswith(args.prefix))
    added = []
    for p in files:
        if (args.source, p.name) in originals:
            continue
        n += 1
        sid = f"{args.prefix}{n:02d}"
        while sid in existing:
            n += 1
            sid = f"{args.prefix}{n:02d}"
        ext = ".jpg" if p.suffix.lower() in {".jpg", ".jpeg"} else ".png"
        dest = out_dir / f"{sid}{ext}"
        shutil.copy2(p, dest)
        w, h = image_size(dest)
        rows.append({"sample_id": sid, "file": f"data/{args.source}/{sid}{ext}", "source": args.source,
                     "original_name": p.name, "sequence": "", "width": w, "height": h,
                     "weather": "", "timeofday": "", "scene": ""})
        existing.add(sid)
        added.append(f"{sid} ← {p.name}")

    with CATALOG.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Đã thêm {len(added)} ảnh vào data/{args.source}/ và data/catalog.csv")
    for line in added:
        print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
