"""Join the unit/skill/stat tables into one dataset of every named unit.

See split_units.py for the per-category files (heroes/pets/monsters/...).
"""
import json, csv, os
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

T = "tables"


def tbl(name):
    return json.load(open(os.path.join(T, name + ".json")))


loc = json.load(open(os.path.join(T, "_Localization_EN.json")))


def s(key, default=""):
    return loc.get(key, default)


import re

TAG = re.compile(r"</?(?:color|link|u|b|i)[^>]*>")


def clean(t):
    return TAG.sub("", t).replace("&", " / ").strip()


def skill_info(sid):
    """Active skills are keyed at level 1 (id+10); passives are keyed directly.

    `kind` records where the text came from, because the three cases are not
    the same thing: a named skill, an unnamed effect the game describes but
    never titles, and a per-level upgrade note (SkillLvUpDesc).
    """
    name = s(f"SkillName_{sid + 10}") or s(f"SkillName_{sid}")
    desc = (s(f"SkillDesc_{sid + 10}") or s(f"SkillDesc_{sid}")
            or s(f"SkillUIShow_{sid + 10}") or s(f"SkillUIShow_{sid}"))
    kind = "skill" if name else ("effect" if desc else "")
    if not desc:
        desc = s(f"SkillLvUpDesc_{sid + 10}") or s(f"SkillLvUpDesc_{sid + 20}")
        if desc:
            kind = "upgrade"
    return {"id": sid, "name": clean(name), "desc": clean(desc), "kind": kind}


def named(ids, uid):
    """Skills for a unit. Some units carry no SkillName/SkillDesc at all — their
    signature ability is described by the Bless entry keyed on the unit id."""
    out = [k for k in map(skill_info, ids) if k["name"] or k["desc"]]
    if not any(k["name"] for k in out) and s(f"BlessName_{uid}"):
        out.insert(0, {"id": uid, "kind": "skill",
                       "name": clean(s(f"BlessName_{uid}")),
                       "desc": clean(s(f"BlessDesc_{uid}") or s(f"BlessShortDesc_{uid}"))})
    return out


def blessings(uid, bless):
    """In-run blessing choices tied to this hero — these are what the
    Icon_Skill_* art actually belongs to (TableBless.BlessIcon)."""
    out = []
    for b in bless:
        if b["BlessHero"] != uid:
            continue
        bid = b["BlessID"]
        out.append({"id": bid, "icon": b["BlessIcon"],
                    "quality": b["BlessQuality"],
                    "name": clean(s(f"BlessName_{bid}")),
                    "desc": clean(s(f"BlessDesc_{bid}") or s(f"BlessShortDesc_{bid}"))})
    return out


def main():
    units = tbl("TableUnitCard")
    attrs = {a["UnitID"]: a for a in tbl("TableUnitAttr")}
    bless = tbl("TableBless")
    heroes = []
    for u in units:
        uid = u["UnitID"]
        name = s(f"HeroName_{uid}") or s(f"UnitName_{uid}")
        if not name:
            continue
        a = attrs.get(uid, {})
        heroes.append({
            "id": uid,
            "name": name,
            # the game carries two labels: HeroName is the character's proper
            # name, UnitName is their class/epithet ("Lia" vs "Flower Spirit")
            "unit_name": s(f"UnitName_{uid}").strip(),
            "playable": bool(s(f"HeroName_{uid}")),
            "rarity": s(f"QualityLiteName_{u['Quality']}", str(u["Quality"])).strip("[]"),
            "rarity_name": s(f"QualityName_{u['Quality']}"),
            "quality": u["Quality"],
            "race": s(f"Race_{u['Race']}") or "-",
            "role": s(f"Position_{u['Position']}") or "-",
            "cost": u["Population"],
            "max_level": u["MaxLevel"],
            "hp": a.get("MaxHP"), "atk": a.get("PhysicalAttack"),
            "defense": a.get("PhysicalDefense"), "atk_speed": a.get("AtkSpeed"),
            "move_speed": a.get("MoveSpeed"), "atk_range": a.get("AtkRange"),
            "crit": a.get("CriticalChance"), "crit_dmg": a.get("CriticalDmgAddition"),
            "accuracy": a.get("Accuracy"), "dodge": a.get("Dodge"),
            "mp": a.get("MaxMP"), "mp_regen": a.get("AtkMpRecover"),
            "skills": named(u["SkillIDs"], uid),
            "passives": [k for k in map(skill_info, u["InitPassiveIDs"] + u["TopPassiveIDs"])
                         if k["name"] or k["desc"]],
            "blessings": blessings(uid, bless),
            "story": s(f"UnitStory_{uid}_0") or s(f"UnitStory_{uid}_1"),
        })
    heroes.sort(key=lambda h: (-h["quality"], h["name"]))
    json.dump(heroes, open("out/units.json", "w"), ensure_ascii=False, indent=1)

    cols = ["id", "name", "unit_name", "playable", "rarity", "rarity_name", "race", "role", "cost",
            "hp", "atk", "defense", "atk_speed", "atk_range", "move_speed",
            "crit", "crit_dmg", "mp", "mp_regen", "max_level"]
    with open("out/units.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols + ["skills", "passives"])
        for h in heroes:
            w.writerow([h[c] for c in cols]
                       + ["; ".join(x["name"] for x in h["skills"] if x["name"]),
                          "; ".join(x["name"] for x in h["passives"] if x["name"])])
    print(f"units.json / units.csv: {len(heroes)} named units "
          f"({sum(1 for h in heroes if h['playable'])} playable)")
    return heroes


if __name__ == "__main__":
    hs = main()
    for h in [x for x in hs if x["playable"]][:5]:
        print(f"\n{h['name']} [{h['rarity']}] {h['race']} / {h['role']} "
              f"HP{h['hp']} ATK{h['atk']} DEF{h['defense']}")
        for sk in h["skills"] + h["passives"]:
            if sk["name"]:
                print(f"   - {sk['name']}: {sk['desc'][:110]}")
