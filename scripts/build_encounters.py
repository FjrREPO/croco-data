"""Emit ENCOUNTERS.md — a lineup for every encounter in the game.

The resistance table is the spine. `Attribute_4000X` reads "Received Damage
Bonus from <class>", so a positive value on a monster means it takes MORE from
that class and a negative one means it takes less. Validated against the
independent RestrainPros column: 34 units carry both and all 34 agree.
"""
import json, collections
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

loc = json.load(open("tables/_Localization_EN.json"))
UNITS = {u["UnitID"]: u for u in json.load(open("tables/TableUnitCard.json"))}
ATTR = {a["UnitID"]: a for a in json.load(open("tables/TableUnitAttr.json"))}
META = json.load(open("out/meta.json"))

P = lambda n: loc.get(f"Profession_{n}", f"#{n}")
NAME = lambda i: (loc.get(f"HeroName_{i}") or loc.get(f"UnitName_{i}") or f"#{i}").strip()
TIERS = ["UR", "SP", "SSR", "SR", "R"]
INFO = {h["epithet"]: (h["rarity"], h["profession"]) for h in META["heroes"]}
H_RAR = {e: r for e, (r, _) in INFO.items()}
BY_PROF = collections.defaultdict(list)
for h in META["heroes"]:
    BY_PROF[h["profession"]].append(h["epithet"])
for p in BY_PROF:
    BY_PROF[p].sort(key=lambda e: TIERS.index(INFO[e][0]))

# classes nothing in the game ever counters — safe filler anywhere
SAFE = ["Warrior", "Support", "Control"]


def resist(uid):
    """-> (vulnerable classes, resisted classes) for one unit, or None."""
    a = ATTR.get(uid, {})
    ids, vals = a.get("ProDmgReductionIDs") or [], a.get("ProDmgReductionVals") or []
    pairs = [(i, v) for i, v in zip(ids, vals) if 40000 < i < 40100]
    if not pairs:
        return None
    vuln = sorted(P(i - 40000) for i, v in pairs if v > 0)
    res = sorted(P(i - 40000) for i, v in pairs if v < 0)
    return (tuple(vuln), tuple(res))


def profile(monster_ids):
    """Aggregate an encounter: classes any enemy is weak to, and classes every
    enemy resists (bringing one of those is the mistake worth naming)."""
    vulns, allres = collections.Counter(), None
    for m in monster_ids:
        r = resist(m)
        if not r:
            continue
        vulns.update(r[0])
        allres = set(r[1]) if allres is None else (allres & set(r[1]))
    return tuple(sorted(vulns, key=lambda c: -vulns[c])), tuple(sorted(allres or []))


def pair(prof, used):
    """Best two heroes of a profession not already used."""
    out = [e for e in BY_PROF[prof] if e not in used][:2]
    return out


def lineup(vuln, resisted):
    """Five heroes: a bond on the class the enemies are weak to, plus a spine.

    The second bond deliberately ignores the resist list. A -20% tax on a
    healer is cheaper than fielding no healer, and Warrior/Support/Control are
    never the class an enemy counters — so the spine is picked for the team's
    shape, not for the damage table. Only the first bond chases the +20%.
    """
    used, slots = set(), []
    free = lambda c: [e for e in BY_PROF[c] if e not in used]
    first = next((c for c in vuln if c not in resisted and free(c)), None) \
        or next((c for c in SAFE if free(c)), "Warrior")
    second = next((c for c in SAFE if c != first and len(free(c)) >= 2), None) \
        or next((c for c in BY_PROF if c != first and len(free(c)) >= 2), None)
    for prof in [p for p in (first, second) if p]:
        got = pair(prof, used)
        used.update(got)
        slots += [(e, prof) for e in got]
    # Filler: the strongest hero left, not the next one down the bond's own
    # ladder. Taking a class's third-best just because the first two are
    # already in put an SR in the shop window while an SP sat on the bench.
    while len(slots) < 5:
        cand = [(c, e) for c in BY_PROF for e in free(c)]
        if not cand:
            break
        cand.sort(key=lambda ce: (
            0 if ce[0] in vuln and ce[0] not in resisted else
            1 if ce[0] not in resisted else 2,
            TIERS.index(H_RAR[ce[1]]),
        ))
        c, e = cand[0]
        used.add(e)
        slots.append((e, c))
    return slots[:5]


def fmt(slots):
    return " · ".join(f"{e} [{INFO[e][0]}]" for e, _ in slots)


def bonds(slots):
    c = collections.Counter(p for _, p in slots)
    return ", ".join(f"bond {k}" for k, v in c.items() if v >= 2) or "—"


def section(title, rows, note=""):
    """rows: [(label, monster_ids)]"""
    out = [f"\n### {title}\n"]
    if note:
        out.append(note + "\n")
    groups = collections.defaultdict(list)
    for label, mids in rows:
        groups[profile(mids)].append(label)
    out.append("| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |")
    out.append("|---|---|---|---|---|")
    for (vuln, res), labels in sorted(groups.items(), key=lambda x: str(x[1][:1])):
        lab = ", ".join(labels[:6]) + (f" … (+{len(labels)-6})" if len(labels) > 6 else "")
        sl = lineup(list(vuln), list(res))
        out.append(f"| {lab} | {', '.join(vuln) or '—'} | {', '.join(res) or '—'} | {fmt(sl)} | {bonds(sl)} |")
    return "\n".join(out)


def companions():
    """Pets and mounts. Neither takes a lineup slot, so they are chosen per mode
    rather than per encounter."""
    import re
    strip = lambda t: re.sub(r"<[^>]+>", "", t or "").replace("\u00a0", " ").strip()
    out = ["\n### Pet\n",
           "Efek sekali di awal battle, **tidak memakan slot lineup** dan tidak terikat bond.\n",
           "| Pet | Tier | Efek | Paling berguna di |", "|---|---|---|---|"]
    MODE = {
        "true damage": "Boss", "ignores Defense": "Boss", "shield": "Rob Boss, Arena",
        "stun": "Arena", "recover": "Rob Boss, Co-op", "area": "Dungeon, Campaign",
        "clones": "Dungeon", "mirror image": "Campaign, Co-op", "gathers all enemies": "Dungeon",
    }
    pets = json.load(open("out/pets.json"))
    CODE = {0:"D",1:"N",2:"R",3:"SR",4:"SSR",5:"SP",6:"UR"}
    rows = []
    for p in pets:
        sk = (p.get("skills") or [{}])[0]
        d = strip(sk.get("desc", ""))
        if not d:
            continue
        mode = next((v for k, v in MODE.items() if k.lower() in d.lower()), "umum")
        rows.append((CODE.get(p.get("quality"), "?"), p.get("unit_name") or p["name"], d, mode))
    rows.sort(key=lambda r: (TIERS.index(r[0]) if r[0] in TIERS else 9, r[1]))
    for rar, nm, d, mode in rows[:18]:
        out.append(f"| {nm} | {rar} | {d[:96]} | {mode} |")

    out += ["\n### Mount\n",
            "Kedelapan mount memberi **stat yang identik** (ATK +300, DEF +150 di level maks) — yang",
            "membedakan hanya efek uniknya. Jadi pilih berdasarkan efek, bukan angka.\n",
            "| Mount | Efek unik |", "|---|---|"]
    for r in json.load(open("tables/TableAdvancedMount.json")):
        mid = r["MountID"]
        nm = loc.get(f"ItemName_{mid}", str(mid))
        ks = sorted(k for k in loc if k.startswith(f"MountSkill_{mid}"))
        out.append(f"| {nm} | {strip(loc[ks[0]])[:120] if ks else '—'} |")
    return "\n".join(out)


def main():
    md = ["""# Oopsie Croco — Lineup per Encounter

Pendamping `TIERLIST.md`. Di sini setiap konten dipetakan ke **resistensi kelasnya**, lalu
diberi lineup 5 hero.

## Cara kerja resistensi (FAKTA)

`TableUnitAttr.ProDmgReductionIDs` memakai atribut `Attribute_4000X` = **"Received Damage Bonus
from \\<kelas\\>"**. Jadi:

- **nilai positif** (biasanya +2000 = **+20%**) → musuh itu **menerima lebih banyak** damage dari
  kelas tersebut. Ini kelemahannya.
- **nilai negatif** (−2000 = **−20%**) → menerima lebih sedikit. Ini resistensinya.

Pola umumnya: satu musuh **lemah terhadap 1 kelas dan menahan 7 kelas lainnya**.

Divalidasi silang dengan kolom `RestrainPros` yang independen — 34 unit membawa keduanya, dan
**ketiga puluh empatnya sepakat**. 7 unit punya resistensi tanpa `RestrainPros`, dan 14 unit
memakai rentang atribut 6-digit yang **tidak ada di lokalisasi**, jadi unit-unit itu saya
lewatkan daripada menebak tandanya.

Kolom **Menahan** hanya diisi kelas yang ditahan **oleh semua musuh** di encounter itu.

**Lineup yang dipajang adalah yang paling direkomendasikan**, bukan campuran tier. Kalau di sana
muncul hero SR atau SSR, itu karena kelasnya yang dieksploitasi musuh — selisih +20% lawan −20%
adalah ayunan 40%, dan itu biasanya menang atas satu tingkat rarity. Kalau kamu tidak punya salah
satu hero di lineup, lihat `SUBSTITUSI.md`.
"""]

    L = {r["LevelID"]: r for r in json.load(open("tables/TableLevel.json"))}
    mons = lambda r: [m["MonsterID"] for m in (r.get("LevelMonsters") or [])]

    # --- story, aggregated per chapter ---
    by_ch = collections.defaultdict(list)
    for lid, r in L.items():
        by_ch[lid // 1000].extend(mons(r))
    CH = json.load(open("tables/TableChapter.json"))
    guide = {r["ChapterID"] for r in CH if r.get("IsGuide")}

    def ch_label(cid):
        """What a player sees. ChapterID 9000 carries IsGuide, so it is the
        tutorial and Chapter 1 is 9001 — the offset is not cosmetic."""
        name = (loc.get(f"ChapterName_{cid}") or "").replace("\u00a0", " ").strip()
        if cid in guide:
            return f"Tutorial ({name})" if name else "Tutorial"
        return f"Ch {cid - 9000}" + (f" {name}" if name else "")

    md.append(section(
        "Story (Campaign)",
        [(ch_label(c), m) for c, m in sorted(by_ch.items())],
        "**1.053 level di 72 chapter** (Tutorial + Ch 1–71), dikelompokkan berdasarkan profil "
        "resistensi yang sama. `TableChapter` memang punya 1.000 baris, tapi 928 di antaranya "
        "tidak punya satu level pun — `TableLevel` dan varian `TableLevel_a` sama-sama berhenti "
        "di ChapterID 9071. Konten yang angkanya sampai ribuan adalah **Endless**, di bawah.\n\n"
        "Penomoran mengikuti yang dilihat pemain: ChapterID 9000 membawa `IsGuide: 1` "
        "(\"Beginner Level\") jadi itu tutorial, dan **Chapter 1 adalah Erin Forest**.",
    ))

    # --- co-op ---
    pve = json.load(open("tables/TableTeamPVELevel.json"))
    by_pve = collections.defaultdict(list)
    for r in pve:
        by_pve[r["ChapterID"]].extend(mons(r))
    for ch in json.load(open("tables/TableTeamPVEChapter.json")):
        by_pve[ch["ChapterID"]].append(ch["ChapterBossID"])
    md.append(section(
        "Co-op (TeamPVE)",
        [(f"Ch {c - 10000}", m) for c, m in sorted(by_pve.items())],
        "16 chapter, bos chapter ikut dihitung. Ingat: Support dan Control tidak dapat buff kelas di mode ini.",
    ))

    # --- dungeon ---
    inst = json.load(open("tables/TableInstance.json"))
    rows = []
    for r in inst:
        ids = [m for lid in (r.get("LevelIDs") or []) for m in mons(L.get(lid, {}))]
        if r.get("BossID"):
            ids.append(r["BossID"])
        dungeon = loc.get(f"InstanceName_{r['InstanceType']}", f"Type {r['InstanceType']}")
        rows.append((f"{dungeon} tingkat {r['InstanceDifficulty']}", ids))
    md.append(section("Dungeon (Instance)", rows,
                      "90 stage. Tidak ada draft blessing di sini — kit dasar yang menentukan."))

    # --- bosses ---
    gb = json.load(open("tables/TableGuildBoss.json"))
    rb = json.load(open("tables/TableRobBoss.json"))
    md.append(section("Guild Boss", [(f"{NAME(r['BOSSId'])} lv{r['Id']}", [r["BOSSId"]]) for r in gb[:12]],
                      "HP tetap — lomba damage."))
    md.append(section("Rob Boss", [(NAME(r["BOSSId"]), [r["BOSSId"]]) for r in rb],
                      "`unlimitedhp: -1` — bertahan selama mungkin, bukan membunuh."))

    # --- endless: 2000 stage, dikelompokkan per rentang ---
    E = json.load(open("tables/TableEndless.json"))
    buckets = collections.defaultdict(list)
    for r in sorted(E, key=lambda x: x["LevelID"]):
        buckets[(r["LevelID"] - 1) // 100].append(r)
    rows = []
    for b, items in sorted(buckets.items()):
        ids = [m for r in items for m in mons(r)]
        rows.append((f"Stage {b * 100 + 1}–{b * 100 + len(items)}", ids))
    md.append(section(
        "Endless (Survival)",
        rows,
        "2.000 stage — inilah mode yang angkanya menembus ribuan, bukan story. `UnlockStage` "
        "menautkannya ke progres chapter, jadi stage terbuka seiring story.\n\n"
        "**Di sini pilihan kelas tidak berpengaruh.** Endless memakai 41 monster unik dan "
        "**tidak satu pun punya resistensi per-kelas** (story memakai 68 monster, 23 di antaranya "
        "punya). Jadi Endless murni adu kekuatan, bukan adu counter — bawa lineup terkuatmu, "
        "bukan lineup counter. Barisnya tetap dikelompokkan per 100 stage supaya terlihat bahwa "
        "profilnya memang seragam dari stage 1 sampai 2.000.",
    ))

    md.append(companions())
    open("knowledge/ENCOUNTERS.md", "w").write("\n".join(md) + "\n")
    print("ENCOUNTERS.md ditulis")


if __name__ == "__main__":
    main()
