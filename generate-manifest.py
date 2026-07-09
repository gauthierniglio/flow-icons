"""
Flow — Icon manifest generator

Génère un fichier manifest.json listant toutes les icônes présentes
dans le dossier /icons, à partir de la convention de nommage :
    nom.svg       → état "outline"
    nom-fill.svg  → état "fill"

Usage :
    python3 generate-manifest.py

Prérequis : lance ce script depuis la racine de ton repo, avec
le dossier "icons/" à côté.
"""

import os
import json
import re
from datetime import date

ICONS_DIR = "icons"
OUTPUT_FILE = "manifest.json"


def extract_inner_svg(svg_content):
    """Extrait le contenu interne d'un SVG (entre les balises <svg>...</svg>)."""
    match = re.search(r'<svg[^>]*>(.*)</svg>', svg_content, re.DOTALL)
    return match.group(1).strip() if match else ""


def main():
    if not os.path.isdir(ICONS_DIR):
        print(f"Erreur : le dossier '{ICONS_DIR}/' est introuvable.")
        print("Lance ce script depuis la racine de ton repo Flow.")
        return

    files = [f for f in os.listdir(ICONS_DIR) if f.endswith(".svg")]

    names = set()
    for f in files:
        if f.endswith("-fill.svg"):
            names.add(f[:-9])  # retire "-fill.svg"
        else:
            names.add(f[:-4])  # retire ".svg"

    manifest = {
        "icons": [],
        "count": 0,
        "updated": str(date.today()),
    }

    missing = []

    for name in sorted(names):
        outline_path = os.path.join(ICONS_DIR, f"{name}.svg")
        fill_path = os.path.join(ICONS_DIR, f"{name}-fill.svg")

        has_outline = os.path.isfile(outline_path)
        has_fill = os.path.isfile(fill_path)

        if not has_outline or not has_fill:
            missing.append((name, has_outline, has_fill))
            continue

        manifest["icons"].append(name)

    manifest["count"] = len(manifest["icons"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"✓ manifest.json généré avec {manifest['count']} icônes.")

    if missing:
        print("\n⚠ Icônes incomplètes (il manque un des deux états) :")
        for name, has_outline, has_fill in missing:
            state = []
            if not has_outline:
                state.append("outline manquant")
            if not has_fill:
                state.append("fill manquant")
            print(f"  - {name} : {', '.join(state)}")


if __name__ == "__main__":
    main()
