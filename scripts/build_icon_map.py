"""Map game concepts (hero, skill, role, rarity, stat) to extracted icon files."""
import json, os
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

IDX = json.load(open("icons/index.json"))


def find(*names):
    for n in names:
        if n and n in IDX:
            return IDX[n]
    return None


def main():
    units = {u["UnitID"]: u for u in json.load(open("tables/TableUnitCard.json"))}
    skins = json.load(open("tables/TableUnitSkin.json"))
    cards = json.load(open("tables/TableSkillCard.json"))
    heroes = json.load(open("out/heroes.json"))

    per_unit = {}
    for s in skins:
        per_unit.setdefault(s["UnitID"], []).extend([s["SkinHead"], s["SkinIcon"]])

    hero_icons = {}
    for h in heroes:
        u = units[h["id"]]
        hero_icons[h["id"]] = find(u["HeadIcon"], *per_unit.get(h["id"], []),
                                   f"Icon_Head_{h['id']}")

    skill_icons = {}
    for c in cards:
        p = find(c["SkillIcon"], f"Icon_Skill_{c['SkillID']}",
                 f"Icon_Skill_{c['SkillID'] + 10}")
        if p:
            skill_icons[c["SkillID"]] = p

    out = {
        "heroes": hero_icons,
        "skills": skill_icons,
        # role badge per Position/Profession id (1..8, see Position_* strings)
        "roles": {n: IDX[f"Icon_Profession_{n}"] for n in range(1, 10)
                  if f"Icon_Profession_{n}" in IDX},
        # rarity frame per Quality value (0..7)
        "rarity": {n: IDX[f"FormationQualityBg_{n}"] for n in range(0, 8)
                   if f"FormationQualityBg_{n}" in IDX},
        "stats": {k: v for k, v in {
            "hp": find("co_icon1_HP", "Icon1_HP"),
            "atk": find("co_icon1_attack"),
            "def": find("co_icon1_def"),
            "speed": find("co_icon1_speed"),
        }.items() if v},
        "items": {i["Id"]: IDX[i["Icon"]]
                  for i in json.load(open("tables/TableItem.json"))
                  if i.get("Icon") in IDX},
        "pets": {p["PetID"] if "PetID" in p else p.get("Id"): IDX[p["PetIcon"]]
                 for p in json.load(open("tables/TablePetNew.json"))
                 if p.get("PetIcon") in IDX},
    }
    json.dump(out, open("out/icon_map.json", "w"), indent=1)
    for k, v in out.items():
        print(f"{k}: {len(v)}")
    missing = [h["name"] for h in heroes if not hero_icons[h["id"]]]
    print(f"heroes without portrait art in this build ({len(missing)}): {missing}")
    return out


if __name__ == "__main__":
    main()
