"""Score each hero per game mode from what their text actually says.

No rarity in the score. Every point comes from a mechanic named in a skill,
passive or blessing, because that is the only evidence in the dump — there is
no combat log, no win rate and no player data here.
"""
import json, re, collections
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

HEROES = [h for h in json.load(open("out/heroes.json")) if h.get("blessings")]

# Mechanic → what it is worth in each mode, and why.
# boss: one huge target, long fight, high DEF and a health pool percentages eat.
# arena: five-on-five burst, where a landed stun decides more than damage.
# dungeon: waves of weak enemies, so area damage and not dying are what scale.
SIGNALS: list[tuple[str, str, dict[str, int]]] = [
    # name,                 regex,                                          boss arena dungeon
    ("%max HP dmg",  r"\b\d+(\.\d+)?%\s*of\s*(the\s*)?(target'?s?\s*)?max(imum)?\s*HP", {"boss": 3, "arena": 1, "dungeon": 0}),
    ("true dmg",     r"\btrue\s*(dmg|damage)\b",                            {"boss": 2, "arena": 1, "dungeon": 0}),
    ("DEF pen",      r"defen[cs]e\s*penetration|ignore[sd]?\s*defen[cs]e",  {"boss": 3, "arena": 1, "dungeon": 0}),
    ("execute",      r"low\s*health|below\s*\d+%\s*HP|finishing\s*strike",  {"boss": 1, "arena": 2, "dungeon": 1}),
    ("stacking",     r"\bstacks?\b|entire\s*adventure|each\s*cast",         {"boss": 2, "arena": 0, "dungeon": 1}),
    ("atk speed",    r"attack\s*speed|ATK\s*Speed",                         {"boss": 2, "arena": 1, "dungeon": 1}),
    ("crit",         r"crit\s*(rate|dmg|damage)",                           {"boss": 2, "arena": 1, "dungeon": 1}),

    ("hard CC",      r"\bstun\b|\bparalysis\b|\bfreeze\b|\bsilence\b",      {"boss": 0, "arena": 3, "dungeon": 1}),
    ("soft CC",      r"\bfear\b|\bcharm\b|\bnightmare\b|\btaunt",           {"boss": 1, "arena": 3, "dungeon": 1}),
    ("burst",        r"instantly|immediately\s*cast|upon\s*entering\s*battle", {"boss": 0, "arena": 2, "dungeon": 0}),
    ("anti-control", r"immunity|cannot\s*fall\s*below|invincible|unyielding", {"boss": 1, "arena": 3, "dungeon": 1}),

    ("AoE",          r"\barea\b|all\s*enemies|nearby\s*enemies|random\s*enemies|rectangular", {"boss": 0, "arena": 2, "dungeon": 3}),
    ("summon",       r"\bsummon", {"boss": 1, "arena": 1, "dungeon": 3}),
    ("heal",         r"\bheal|restor\w*\s*(HP|health)|recovery", {"boss": 2, "arena": 2, "dungeon": 3}),
    ("shield/red.",  r"\bshield\b|dmg\s*red|damage\s*reduction|damage\s*taken\s*.*reduced", {"boss": 2, "arena": 3, "dungeon": 2}),
]

MODES = ("boss", "arena", "dungeon")


def text_of(h) -> str:
    parts = []
    for s in h["skills"] + h["passives"]:
        parts.append(f"{s.get('name', '')} {s.get('desc', '')}")
    for b in h.get("blessings", []):
        parts.append(f"{b.get('name', '')} {b.get('desc', '')}")
    return " ".join(parts)


def score(h):
    body = text_of(h)
    hits, per = {}, dict.fromkeys(MODES, 0)
    for label, pattern, weights in SIGNALS:
        n = len(re.findall(pattern, body, re.I))
        if not n:
            continue
        # Diminishing returns: a hero repeating one word twenty times is not
        # twenty times better at it, and the blessing lists are repetitive.
        strength = min(n, 4)
        hits[label] = n
        for mode, w in weights.items():
            per[mode] += w * strength
    return per, hits


def main():
    rows = []
    for h in HEROES:
        per, hits = score(h)
        rows.append((h, per, hits))

    for mode in MODES:
        rows.sort(key=lambda r: -r[1][mode])
        print(f"\n{'=' * 72}\n{mode.upper()}\n{'=' * 72}")
        for h, per, hits in rows[:12]:
            top = sorted(
                ((l, n) for l, n in hits.items()
                 if dict(SIGNALS_BY[l])[mode] > 0),
                key=lambda x: -x[1],
            )[:4]
            why = ", ".join(f"{l}×{n}" for l, n in top)
            print(f"  {per[mode]:>3}  {h['rarity']:<4} {h['unit_name'][:22]:<24} {h['role'][:10]:<11} {why}")

    json.dump(
        [{"name": h["name"], "unit_name": h["unit_name"], "rarity": h["rarity"],
          "role": h["role"], "scores": per, "hits": hits} for h, per, hits in rows],
        open("out/mode_scores.json", "w"), ensure_ascii=False, indent=1)


SIGNALS_BY = {label: list(weights.items()) for label, _, weights in SIGNALS}

if __name__ == "__main__":
    main()
