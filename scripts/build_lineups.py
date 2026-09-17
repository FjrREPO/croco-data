"""Render each lineup as 5 slots with a per-slot substitution ladder.

The roster is a clean 8×4 grid, so a slot's fallback is simply the same
profession one tier down — minus whoever the lineup already uses, because two
slots cannot hold the same hero.
"""
import json
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

meta = json.load(open("out/meta.json"))
TIERS = ["UR", "SP", "SSR", "SR", "R"]

# epithet -> (rarity, profession)
INFO = {h["epithet"]: (h["rarity"], h["profession"]) for h in meta["heroes"]}
BY_PROF = {}
for h in meta["heroes"]:
    BY_PROF.setdefault(h["profession"], []).append(h["epithet"])
for p in BY_PROF:
    BY_PROF[p].sort(key=lambda e: TIERS.index(INFO[e][0]))

# mode -> [(hero, role note), ...] — always five
LINEUPS = {
    "Guild Boss": [
        ("Goddess of Wisdom", "damage %Max HP, tank"),
        ("Holy Knight", "bond Warrior, sustain"),
        ("Goddess of the Hunt", "damage %Max HP + DEF pen"),
        ("Bounty Hunter", "bond Archer, DPS single-target"),
        ("Flower Spirit", "heal"),
    ],
    "Rob Boss": [
        ("Goddess of Wisdom", "tank + damage"),
        ("Piggy Vanguard", "bond Warrior, shield terpadat"),
        ("Flower Spirit", "heal"),
        ("Onmyoji", "bond Support, heal kedua"),
        ("Goddess of the Hunt", "DPS berkelanjutan"),
    ],
    "Arena": [
        ("Pharaoh", "hard CC terpadat (7×)"),
        ("Succubus", "bond Control, soft CC"),
        ("Goddess of Wisdom", "tank + burst"),
        ("Dragon Warrior", "bond Warrior"),
        ("Flower Spirit", "heal"),
    ],
    "Co-op": [
        ("Goddess of Wisdom", "dapat buff kelas"),
        ("Dragon Warrior", "bond Warrior, dapat buff"),
        ("Goddess of the Hunt", "dapat buff"),
        ("Light Archer", "bond Archer, dapat buff"),
        ("Catwoman", "dapat buff"),
    ],
    "Dungeon": [
        ("Tidecaller", "summon menahan gelombang"),
        ("Bear Caller", "bond Summon"),
        ("Goddess of Wisdom", "tank"),
        ("Dragon Warrior", "bond Warrior"),
        ("Red Queen", "AoE"),
    ],
}


def fallbacks(hero, lineup):
    """Same profession, worse tier, not already used elsewhere in the lineup."""
    rar, prof = INFO[hero]
    used = {h for h, _ in lineup if h != hero}
    out = []
    for e in BY_PROF[prof]:
        if e == hero or e in used:
            continue
        if TIERS.index(INFO[e][0]) > TIERS.index(rar):
            out.append(f"{e} [{INFO[e][0]}]")
    return out


def main():
    for mode, lineup in LINEUPS.items():
        print(f"\n#### {mode}\n")
        print("| # | Utama | Alternatif (turun tier) | Kelas | Fungsi |")
        print("|---|---|---|---|---|")
        for i, (hero, note) in enumerate(lineup, 1):
            rar, prof = INFO[hero]
            alt = fallbacks(hero, lineup)
            print(f"| {i} | **{hero}** [{rar}] | {' → '.join(alt) or '—'} | {prof} | {note} |")


if __name__ == "__main__":
    main()
