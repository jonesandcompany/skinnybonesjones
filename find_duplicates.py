"""
Find duplicate photos between the homepage folder and another project folder.

Usage:
    python find_duplicates.py <project_folder_name>

Example:
    python find_duplicates.py weddings
    python find_duplicates.py pardonme
"""

import os
import sys
import numpy as np
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
HOMEPAGE_DIR = os.path.join(BASE, 'homepage')


def thumb_arr(path, size=32):
    return np.array(
        Image.open(path).convert('L').resize((size, size), Image.LANCZOS),
        dtype=float
    )


def find_duplicates(project_folder):
    pm_dir = os.path.join(BASE, project_folder)

    if not os.path.isdir(pm_dir):
        print(f"Error: folder '{project_folder}' not found at {pm_dir}")
        sys.exit(1)

    print(f"Loading homepage thumbnails...")
    hp_thumbs = {
        f: thumb_arr(os.path.join(HOMEPAGE_DIR, f))
        for f in os.listdir(HOMEPAGE_DIR) if f.endswith('.jpg')
    }

    print(f"Comparing against '{project_folder}'...\n")
    matches = []
    for pf in sorted(os.listdir(pm_dir)):
        if not pf.endswith('.jpg'):
            continue
        pt = thumb_arr(os.path.join(pm_dir, pf))
        best_score, best_hf = min(
            (np.mean(np.abs(pt - ht)), hf)
            for hf, ht in hp_thumbs.items()
        )
        if best_score < 1.0:
            matches.append((best_hf, pf, best_score))

    matches.sort(key=lambda x: x[1])
    print(f"Found {len(matches)} duplicate(s):\n")
    for hf, pf, score in matches:
        print(f"  ({hf}, {pf})")

    return matches


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    find_duplicates(sys.argv[1])