"""Split TableUnitCard into heroes / pets / monsters / summons / troops.

The game keeps every battle actor in one table and separates them by Race:
  500000  pets (mirrored in TablePet / TablePetNew)
  999     monsters and bosses
  998     summons and totems
  1..8/-1 playable races — heroes if a HeroName string exists, otherwise the
          generic troops used for low-rank units
"""
import json, csv, os
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project
from build_heroes import s, clean, skill_info, named, blessings, tbl

IDX = json.load(open("icons/index.json"))
PET_RACE, MONSTER_RACE, SUMMON_RACE = 500000, 999, 998


def icon(*names):
    for n in names:
        if n and n in IDX:
            return "icons/" + IDX[n]
    return None


def rarity(q):
    """The letter scale (QualityLiteName) stops at SSS=6, but quality runs to 9
    (QualityName_7..9 = Immortal Ⅰ/Ⅱ/Ⅲ), so extend it with plus signs."""
    lite = s(f"QualityLiteName_{q}").strip("[]")
    return lite or ("SSS" + "+" * (q - 6) if q > 6 else str(q))


def category(u):
    if s(f"HeroName_{u['UnitID']}"):
        return "heroes"
    return {PET_RACE: "pets", MONSTER_RACE: "monsters",
            SUMMON_RACE: "summons"}.get(u["Race"], "troops")


def main():
    units = tbl("TableUnitCard")
    attrs = {a["UnitID"]: a for a in tbl("TableUnitAttr")}
    bless = tbl("TableBless")
    skins = tbl("TableUnitSkin")
    pet_rows = {p["PetID"]: p for p in tbl("TablePetNew")}
    pet_old = {p["PetID"]: p for p in tbl("TablePet")}

    per_unit = {}
    for sk in skins:
        per_unit.setdefault(sk["UnitID"], []).extend([sk["SkinHead"], sk["SkinIcon"]])

    out = {k: [] for k in ("heroes", "pets", "monsters", "summons", "troops")}
    for u in units:
        uid, cat = u["UnitID"], category(u)
        a = attrs.get(uid, {})
        name = (s(f"PetName_{uid}") if cat == "pets" else "") \
            or s(f"HeroName_{uid}") or s(f"UnitName_{uid}")
        if name == "None":
            name = ""
        rec = {
            "id": uid, "name": name.strip(),
            "unit_name": s(f"UnitName_{uid}").strip(),
            "rarity": rarity(u["Quality"]),
            "rarity_name": s(f"QualityName_{u['Quality']}"),
            "quality": u["Quality"],
            "race": s(f"Race_{u['Race']}") or "-",
            "role": s(f"Position_{u['Position']}") or "-",
            "cost": u["Population"], "max_level": u["MaxLevel"],
            "hp": a.get("MaxHP"), "atk": a.get("PhysicalAttack"),
            "defense": a.get("PhysicalDefense"), "atk_speed": a.get("AtkSpeed"),
            "atk_range": a.get("AtkRange"), "move_speed": a.get("MoveSpeed"),
            "crit_dmg": a.get("CriticalDmgAddition"), "mp_regen": a.get("AtkMpRecover"),
            "skills": named(u["SkillIDs"], uid),
            "passives": [k for k in map(skill_info, u["InitPassiveIDs"] + u["TopPassiveIDs"])
                         if k["name"] or k["desc"]],
            "icon": icon(u["HeadIcon"], *per_unit.get(uid, []),
                         f"Icon_Head_{uid}", f"Icon_Pet_{uid}"),
        }
        if cat == "heroes":
            rec["blessings"] = blessings(uid, bless)
            rec["story"] = s(f"UnitStory_{uid}_0") or s(f"UnitStory_{uid}_1")
        if cat == "pets":
            p, o = pet_rows.get(uid, {}), pet_old.get(uid, {})
            rec["pet_quality"] = p.get("PetQuality")
            rec["pet_max_level"] = o.get("MaxLevel")
            rec["piece_needed"] = o.get("PieceNeeded")
            rec["attr_ids"] = o.get("AttrIDs", [])
            rec["attr_vals"] = o.get("AttrVals", [])
        out[cat].append(rec)

    for cat, rows in out.items():
        rows.sort(key=lambda r: (-r["quality"], r["name"] or "zzz"))
        json.dump(rows, open(f"out/{cat}.json", "w"), ensure_ascii=False, indent=1)
        cols = ["id", "name", "unit_name", "rarity", "race", "role", "cost",
                "hp", "atk", "defense", "atk_speed", "atk_range", "max_level"]
        with open(f"out/{cat}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols + ["skills", "icon"])
            for r in rows:
                w.writerow([r.get(c) for c in cols]
                           + ["; ".join(x["name"] for x in r["skills"] + r["passives"]
                                        if x["name"]), r["icon"] or ""])
        named_n = sum(1 for r in rows if r["name"])
        art = sum(1 for r in rows if r["icon"])
        print(f"{cat + '.json':<14} {len(rows):>4} rows  "
              f"({named_n} named, {art} with art)")
    return out


if __name__ == "__main__":
    main()
