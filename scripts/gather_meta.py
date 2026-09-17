"""Collect everything the lineup guide needs into one JSON, from the tables."""
import json, re, collections
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

loc = json.load(open("tables/_Localization_EN.json"))
UNITS = {u["UnitID"]: u for u in json.load(open("tables/TableUnitCard.json"))}
HEROES = [h for h in json.load(open("out/heroes.json")) if h.get("blessings")]
strip = lambda s: re.sub(r"<[^>]+>", "", s or "").replace(" ", " ").strip()
P = lambda n: strip(loc.get(f"Profession_{n}", f"#{n}"))
NAME = lambda i: strip(loc.get(f"HeroName_{i}") or loc.get(f"UnitName_{i}") or str(i))
TIERS = ["UR", "SP", "SSR", "SR", "R", "N", "D"]
CODE = {0: "D", 1: "N", 2: "R", 3: "SR", 4: "SSR", 5: "SP", 6: "UR"}


def prof(h):
    p = UNITS[h["id"]].get("Profession")
    p = p[0] if isinstance(p, list) and p else p
    return P(p) if p is not None else h["role"]


def body(h):
    return " ".join(
        f"{s.get('name', '')} {s.get('desc', '')}"
        for s in h["skills"] + h["passives"]
    ) + " " + " ".join(f"{b['name']} {b['desc']}" for b in h.get("blessings", []))


MECHANICS = {
    "maxhp": r"\d+(\.\d+)?%\s*of\s*(the\s*)?(target'?s?\s*)?max(imum)?\s*HP",
    "defpen": r"defen[cs]e\s*penetration|ignore[sd]?\s*defen[cs]e",
    "truedmg": r"\btrue\s*(dmg|damage)\b",
    "hardcc": r"\bstun\b|\bparalysis\b|\bfreeze\b|\bsilence\b",
    "softcc": r"\bfear\b|\bcharm\b|\bnightmare\b|\btaunt",
    "heal": r"\bheal|restor\w*\s*(HP|health)|recovery",
    "shield": r"\bshield\b|dmg\s*red|damage\s*reduction",
    "aoe": r"\barea\b|all\s*enemies|nearby\s*enemies|random\s*enemies",
    "summon": r"\bsummon",
    "antictrl": r"immunity|cannot\s*fall\s*below|invincible",
}

out = {}

# ---- heroes, by profession and tier ----
heroes = []
for h in HEROES:
    t = body(h)
    heroes.append({
        "name": h["name"], "epithet": h["unit_name"], "rarity": CODE.get(h["quality"], h["rarity"]),
        "profession": prof(h), "cost": h["cost"], "blessings": len(h["blessings"]),
        "mech": {k: len(re.findall(p, t, re.I)) for k, p in MECHANICS.items() if re.search(p, t, re.I)},
    })
heroes.sort(key=lambda x: (x["profession"], TIERS.index(x["rarity"])))
out["heroes"] = heroes

ladder = collections.defaultdict(list)
for h in heroes:
    ladder[h["profession"]].append(f"{h['epithet']} [{h['rarity']}]")
out["ladder"] = dict(ladder)

# ---- monsters: who counters what ----
countered, counters = [], []
for u in UNITS.values():
    if u.get("RestrainPros"):
        countered.append({"name": NAME(u["UnitID"]), "beaten_by": [P(p) for p in u["RestrainPros"]]})
    if u.get("Restrain"):
        counters.append({"name": NAME(u["UnitID"]), "counters": P(u["Restrain"])})
# one row per name; the dump repeats a monster per stage variant
seen = {}
for c in countered:
    seen.setdefault(c["name"], set()).update(c["beaten_by"])
out["monsters_beaten_by"] = sorted(
    ({"name": n, "beaten_by": sorted(v)} for n, v in seen.items()), key=lambda x: x["name"]
)
out["monsters_that_counter"] = counters

# ---- bosses per mode ----
bosses = {}
for tbl, key, label in [
    ("TableGuildBoss", "BOSSId", "Guild Boss"),
    ("TableRobBoss", "BOSSId", "Rob Boss"),
    ("TableInstance", "BossID", "Dungeon"),
]:
    d = json.load(open(f"tables/{tbl}.json"))
    ids = sorted({r[key] for r in d if r.get(key)})
    bosses[label] = [
        {"name": NAME(i),
         "beaten_by": [P(p) for p in UNITS.get(i, {}).get("RestrainPros", [])],
         "counters": P(UNITS[i]["Restrain"]) if UNITS.get(i, {}).get("Restrain") else None}
        for i in ids
    ]
out["bosses"] = bosses

# ---- pets ----
try:
    pets = json.load(open("out/pets.json"))
    out["pets"] = sorted(
        ({"name": p.get("unit_name") or p["name"], "rarity": CODE.get(p.get("quality"), p.get("rarity")),
          "desc": strip((p.get("skills") or [{}])[0].get("desc", ""))[:150]}
         for p in pets if (p.get("skills") or p.get("passives"))),
        key=lambda x: TIERS.index(x["rarity"]) if x.get("rarity") in TIERS else 9,
    )[:16]
except Exception as e:
    out["pets"] = f"tidak terbaca: {e}"

# ---- mode rules ----
lvl = json.load(open("tables/TableLevel.json"))
pve = json.load(open("tables/TableTeamPVELevel.json"))
inst = json.load(open("tables/TableInstance.json"))
out["mode_rules"] = {
    "campaign_bless_draft": dict(collections.Counter(r["BlessCardCount"] for r in lvl)),
    "coop_bless_draft": dict(collections.Counter(r["BlessCardCount"] for r in pve)),
    "dungeon_bless_draft": dict(collections.Counter(r["BlessCardCount"] for r in inst)),
    "coop_class_buffs": [P(int(r["BuffIcon"].split("_")[-1]))
                         for r in json.load(open("tables/TableTeamPVEBuff.json"))
                         if r["BuffIcon"].startswith("Icon_Profession_")],
    "guild_boss_hp": [r["hpvalue"] for r in json.load(open("tables/TableGuildBoss.json"))[:8]],
    "rob_boss_hp": list({r["unlimitedhp"] for r in json.load(open("tables/TableRobBoss.json"))}),
    "bond_required_count": {P(r["BondProfession"]): r["RequiredCount"]
                            for r in json.load(open("tables/TableBond.json"))},
}

json.dump(out, open("out/meta.json", "w"), ensure_ascii=False, indent=1)
print("heroes:", len(out["heroes"]))
print("monsters beaten_by:", len(out["monsters_beaten_by"]), "| that counter:", len(out["monsters_that_counter"]))
print("bosses:", {k: len(v) for k, v in out["bosses"].items()})
print("pets:", len(out["pets"]) if isinstance(out["pets"], list) else out["pets"])
print("ladder:", {k: len(v) for k, v in out["ladder"].items()})
