"""Build knowledge/ — everything an on-site chatbot needs, and nothing it can invent from.

Three rules shape this, all aimed at the same failure: a bot that answers
confidently from something it half-remembers.

1. Every chunk is self-contained. A bot answers from what it retrieves, so a
   hero chunk that says "substitute one tier down" is useless if the ladder is
   in a chunk that did not come back.
2. Every chunk carries `confidence` — "fact" for values read out of the game's
   tables, "inference" for the tier and lineup opinions. The system prompt
   makes the bot say which it is using.
3. What the data does NOT answer is written down as loudly as what it does, in
   knowledge/UNKNOWNS.md, because the gaps are where a bot starts guessing.
"""
import json, re, collections, os
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

OUT = "knowledge"
os.makedirs(OUT, exist_ok=True)

loc = json.load(open("tables/_Localization_EN.json"))
UNITS = {u["UnitID"]: u for u in json.load(open("tables/TableUnitCard.json"))}
CARDS = {c["SkillID"]: c for c in json.load(open("tables/TableSkillCard.json"))}
HEROES = [h for h in json.load(open("out/heroes.json")) if h.get("blessings")]
META = json.load(open("out/meta.json"))

strip = lambda s: re.sub(r"<[^>]+>", "", s or "").replace(" ", " ").strip()
P = lambda n: strip(loc.get(f"Profession_{n}", f"#{n}"))
CODE = {0: "D", 1: "N", 2: "R", 3: "SR", 4: "SSR", 5: "SP", 6: "UR"}
TIERS = ["UR", "SP", "SSR", "SR", "R"]
DUMP = "Oopsie Croco v1.8.6, dump APK 2026-07-28"

INFO = {h["epithet"]: h for h in META["heroes"]}
BY_PROF = collections.defaultdict(list)
for h in META["heroes"]:
    BY_PROF[h["profession"]].append(h["epithet"])
for p in BY_PROF:
    BY_PROF[p].sort(key=lambda e: TIERS.index(INFO[e]["rarity"]))

chunks = []


def add(cid, kind, title, text, confidence="fact", **meta):
    chunks.append({"id": cid, "game": "croco", "type": kind, "title": title,
                   "text": " ".join(text.split()), "confidence": confidence,
                   "source": DUMP, **meta})


def prof_of(h):
    p = UNITS[h["id"]].get("Profession")
    p = p[0] if isinstance(p, list) and p else p
    return P(p) if p is not None else h["role"]


# ---------------- gacha rates, for the spender tiers ----------------
pool = collections.defaultdict(list)
for r in json.load(open("tables/TableLotteryPool.json")):
    pool[r["GropID"]].append(r)


def pool_rarity(gid):
    d = collections.Counter()
    for r in pool.get(gid, []):
        d[CODE.get(UNITS.get(r["RewardID"], {}).get("Quality"), "non-hero")] += r["Drop"]
    return d.most_common(1)[0][0] if d else "?"


banners = {}
cfg = collections.defaultdict(list)
for r in json.load(open("tables/TableLotteryPoolConfig.json")):
    cfg[r["CardLotteryID"]].append(r)
for cid, rows in cfg.items():
    tot = sum(r["Drop"] for r in rows)
    if not tot:
        continue
    d = collections.Counter()
    for r in rows:
        d[pool_rarity(r["GropID"])] += r["Drop"]
    banners[cid] = {"rates": {k: round(v / tot * 100, 2) for k, v in d.items()},
                    "pity": sorted({r["CumulativeMax"] for r in rows if r.get("CumulativeMax")})}

main = banners.get(10000, {})
add("gacha:rates", "gacha", "Peluang gacha dan pity",
    f"""Peluang tarikan dibaca dari TableLotteryPoolConfig (bobot pemilihan pool) digabung dengan
    TableLotteryPool (isi tiap pool). Banner utama 10000: {', '.join(f'{k} {v}%' for k, v in sorted(main.get('rates', {}).items(), key=lambda x: -x[1]))},
    dengan pity di {main.get('pity')}. Banner 30000 (pool berisi hero bagus saja):
    {', '.join(f'{k} {v}%' for k, v in sorted(banners.get(30000, {}).get('rates', {}).items(), key=lambda x: -x[1]))},
    pity {banners.get(30000, {}).get('pity')}.
    Angka ini yang mendasari segmentasi spender: SP dan UR sangat jarang di banner utama,
    jadi roster pemain sangat ditentukan oleh berapa banyak dia menarik.""")

# ---------------- spender segments ----------------
SEG = {
    "f2p": ("F2P (tanpa belanja)",
        "R dan SR lengkap, 1–3 SSR dari pity dan event, biasanya tanpa SP dan tanpa UR",
        """Rakit dua bond dari SSR/SR/R — semuanya tersedia di tiap profesi. Prioritas:
        Holy Knight + Radiant Warrior (bond Warrior, kelas yang tidak pernah di-counter), lalu
        Pharaoh + Pumpkin (bond Control) kalau main Arena, atau Star Mage + Snow Witch (bond Mage,
        dua-duanya DEF penetration) kalau main Boss. Yang benar-benar hilang tanpa SP/UR hanya
        damage %Max HP. True damage, DEF penetration, dan hard CC semuanya masih tersedia di SSR
        ke bawah. Jangan sebar sumber daya: naikkan 5 hero inti ke Lv15 dulu sebelum menyentuh
        hero keenam."""),
    "low": ("Low spender",
        "SSR lengkap, 1–2 SP, belum ada UR",
        """SP pertama sebaiknya Dragon Warrior (Warrior) karena mengunci bond teraman, atau
        Flower Spirit (Support) kalau belum punya healer kuat. Pasangkan SP dengan SSR sekelas
        supaya bond tetap nyala tanpa SP kedua. Target level: Lv12 untuk Campaign/Co-op
        (Additional Blessing), Lv15 untuk Arena/Boss (Exclusive Passive)."""),
    "mid": ("Mid spender",
        "3–5 SP, mungkin 1 UR",
        """Kejar dua bond penuh berisi SP+SSR, lalu dorong ke Lv20 (skill bernama) pada dua hero
        utama saja. Kalau sudah punya satu UR, bangun lineup di sekitar kelasnya: UR Archer berarti
        bond Archer, UR Warrior berarti bond Warrior. Hindari menumpuk Support/Control di Co-op
        karena kedua kelas itu tidak dapat buff mode."""),
    "sultan": ("Sultan",
        "hampir semua SP, 1–2 UR",
        """Kedua UR (Goddess of the Hunt dan Goddess of Wisdom) saling menguatkan — skill mereka
        menyebut satu sama lain, dan keduanya pemegang tunggal damage %Max HP. Turunkan berdua di
        Guild Boss. Sisa slot dipakai untuk bond kedua sesuai mode. Level: Lv20 pada lima hero inti,
        lalu Lv25."""),
    "whale": ("Whale spender",
        "roster lengkap, level tinggi, semua bond tersedia",
        """Batasnya bukan roster lagi tapi jumlah slot: Population naik 1→8 mengikuti grade Hero Comp,
        jadi naikkan grade untuk membuka bond ketiga dan keempat (2+2+2+2 di 8 slot). Ganti lineup
        per encounter mengikuti tabel resist — itu satu-satunya optimasi yang tersisa setelah roster
        penuh. Di Endless jangan repot menyusun counter: 41 monsternya tidak punya resist kelas
        sama sekali, jadi bawa lineup terkuat."""),
}
for k, (title, roster, plan) in SEG.items():
    add(f"segment:{k}", "segment", f"Rencana untuk {title}",
        f"""Segmen {title}. Roster yang biasanya dimiliki: {roster}. Rencana: {plan}""",
        confidence="inference", segment=k)

add("segment:how", "segment", "Cara menentukan segmen pemain",
    """Kalau pemain tidak menyebut segmennya, tanyakan dua hal saja: berapa hero SP/UR yang dia
    punya, dan berapa slot lineup-nya (grade Hero Comp). Dari situ: 0 SP tanpa UR = F2P;
    1–2 SP = low; 3–5 SP = mid; hampir semua SP dengan 1–2 UR = sultan; roster penuh = whale.
    Jangan menebak segmen dari nama hero yang disebut saja — pemain F2P bisa punya satu SP dari
    event.""", confidence="inference")

# ---------------- heroes ----------------
for h in HEROES:
    prof, rar = prof_of(h), CODE.get(h["quality"], h["rarity"])
    ladder = BY_PROF[prof]
    i = ladder.index(h["unit_name"]) if h["unit_name"] in ladder else -1
    subs = [f"{x} [{INFO[x]['rarity']}]" for x in ladder[i + 1:]] if i >= 0 else []
    unlocks = sorted({(u, s["name"] or "efek tanpa nama")
                      for s in h["skills"] + h["passives"]
                      for u in (CARDS.get(s["id"], {}).get("UnlockLevels") or []) if u})
    skills = "; ".join(f"{s['name'] or 'tanpa nama'}: {strip(s['desc'])[:170]}"
                       for s in h["skills"] + h["passives"] if s.get("desc"))
    bless = "; ".join(f"{b['name']} ({strip(b['desc'])[:80]})" for b in h["blessings"][:12])
    add(f"hero:{h['id']}", "hero", f"{h['name']} — {h['unit_name']}",
        f"""{h['name']}, dikenal juga sebagai "{h['unit_name']}", hero {rar} kelas {prof}.
        Ras {h['race']}, deploy cost {h['cost']}, level maksimum {h['max_level']}.
        Stat dasar level 1: HP {h['hp']}, ATK {h['atk']}, DEF {h['defense']},
        ATK Speed {h['atk_speed']}, Range {h['atk_range']}.
        Skill dan passive: {skills}.
        Level unlock: {', '.join(f'Lv{u} {n}' for u, n in unlocks) or 'tidak tercatat'}.
        Blessing ({len(h['blessings'])}): {bless}.
        Kalau pemain tidak punya hero ini, pengganti sekelas agar bond tetap nyala:
        {' lalu ' .join(subs) or 'tidak ada, dia tingkat terendah di kelasnya'}.""",
        hero=h["name"], epithet=h["unit_name"], profession=prof, rarity=rar,
        aliases=[h["name"], h["unit_name"]])

# ---------------- classes ----------------
for prof, members in sorted(BY_PROF.items()):
    weak = [m["name"] for m in META["monsters_beaten_by"] if prof in m["beaten_by"]]
    hard = [m["name"] for m in META["monsters_that_counter"] if m["counters"] == prof]
    add(f"class:{prof}", "class", f"Kelas {prof}",
        f"""Kelas {prof} punya {len(members)} hero, terkuat ke termurah:
        {', '.join(f'{m} [{INFO[m]["rarity"]}]' for m in members)}.
        Bond {prof} aktif dengan 2 hero kelas ini di lineup.
        Musuh yang lemah terhadap {prof} (menerima +20% damage): {', '.join(weak[:16]) or 'tidak ada'}.
        Musuh yang meng-counter {prof}: {', '.join(hard) or 'tidak ada — kelas ini aman dibawa ke stage mana pun'}.""",
        profession=prof)

# ---------------- mechanics & modes ----------------
FACTS = {
    "mech:bond": ("Bond profesi", """Bond aktif kalau lineup berisi 2 hero dari profesi sama
        (TableBond, RequiredCount 2 untuk kedelapan profesi). Di 5 slot susunan terbaik 2+2+1.
        Lima kelas berbeda berarti nol bond. Bond memberi skill (AEIDs → SkillIDs), bukan bonus
        stat — dan skill itu tidak punya teks di lokalisasi, jadi BESARAN EFEKNYA TIDAK DIKETAHUI."""),
    "mech:slots": ("Jumlah slot lineup", """Bukan tetap 5. TableGrade: Population naik 1 (grade 1)
        sampai 8 (grade 8) seiring EXP Hero Comp, dan setiap hero berbiaya 1. Susunan bond:
        4 slot → 2+2, 5 → 2+2+1, 6 → 2+2+2, 7 → 2+2+2+1, 8 → 2+2+2+2."""),
    "mech:resist": ("Resistensi kelas", """Musuh punya Attribute_4000X = "Received Damage Bonus from
        <kelas>". Positif (+2000 = +20%) berarti menerima LEBIH BANYAK damage dari kelas itu — itu
        kelemahannya. Negatif (−2000 = −20%) berarti menahan. Pola umum: lemah terhadap 1 kelas,
        menahan 7. Divalidasi dengan kolom RestrainPros: 34 unit membawa keduanya dan semuanya
        sepakat. Hanya monster biasa yang punya — tidak ada hero yang punya, dan keempat bos bernama
        netral."""),
    "mech:blessing": ("Sistem blessing", """Draft blessing HANYA ada di Campaign (2 per level, 893
        level) dan Co-op (2 per level, 162 level). Dungeon punya BlessCardCount 0 di seluruh 90
        stage. Guild Boss, Rob Boss, dan Arena tidak punya blessing sama sekali."""),
    "mech:levels": ("Level unlock skill", """Unlock seragam di Lv12, Lv15, Lv20, Lv25. Lv12 memberi
        "Additional Blessing" yang HANYA berguna di Campaign dan Co-op. Lv15 memberi Exclusive
        Passive. Lv20 memberi skill bernama. Level maksimum 200."""),
    "mech:coopbuff": ("Buff kelas Co-op", """TableTeamPVEBuff memberi buff hanya ke 6 profesi: Mage,
        Archer, Warrior, Summon, Calamity, Assassin. Support dan Control TIDAK dapat apa pun."""),
    "mech:roster": ("Struktur roster", """34 hero playable: grid 8 profesi × 4 tier (SP/SSR/SR/R)
        ditambah 2 UR — Goddess of the Hunt (Archer) dan Goddess of Wisdom (Warrior). Tangga rarity
        yang dilihat pemain: UR > SP > SSR > SR > R > N > D."""),
    "mech:scarcity": ("Mekanik langka", """Damage %Max HP: hanya Goddess of the Hunt [UR] dan
        Goddess of Wisdom [UR]. DEF penetration: Goddess of the Hunt [UR], Red Queen [SP],
        Star Mage [SSR], Snow Witch [SR]. True damage: hanya Phantom [SSR]. Hard CC: Pharaoh [SSR]
        (terpadat), Pumpkin [SR], Tidecaller [SP], Succubus [SP], Priest Apprentice [R]."""),
    "mode:guildboss": ("Mode Guild Boss", """Bos Igris, HP tetap (150 sampai 1775+) — lomba damage.
        Tanpa blessing. Bos netral tanpa resist kelas."""),
    "mode:robboss": ("Mode Rob Boss", """Bos Darkflame Dragonlord Serre, unlimitedhp -1 alias HP TAK
        TERBATAS. Skornya berapa lama bertahan, bukan membunuh. Damage %Max HP tidak relevan."""),
    "mode:arena": ("Mode Arena", """PvP lawan tim pemain. Tanpa blessing, tanpa sistem resist.
        Hard CC paling menentukan."""),
    "mode:coop": ("Mode Co-op", """16 chapter. Draft 2 blessing per level. Buff kelas untuk 6 profesi
        (bukan Support/Control). Sistem resist aktif."""),
    "mode:dungeon": ("Mode Dungeon", """90 stage di dua dungeon: Yggdrasil dan Beastmen Altar. TANPA
        draft blessing — kit dasar yang menentukan. Sistem resist aktif."""),
    "mode:campaign": ("Mode Story", """Tutorial plus Chapter 1–71. TableLevel berhenti di ChapterID
        9071 meski TableChapter punya 1000 baris; 928 sisanya tanpa level. Draft 2 blessing per
        level."""),
    "mode:endless": ("Mode Endless", """2000 stage — ini yang angkanya menembus ribuan, bukan story.
        Memakai 41 monster unik dan TIDAK SATU PUN punya resist kelas, jadi pilihan kelas tidak
        berpengaruh; murni adu kekuatan."""),
}
for cid, (title, body) in FACTS.items():
    add(cid, cid.split(":")[0], title, body)

# ---------------- pets & mounts ----------------
for p in json.load(open("out/pets.json")):
    d = strip((p.get("skills") or [{}])[0].get("desc", ""))
    if d:
        add(f"pet:{p['id']}", "pet", f"Pet {p.get('unit_name') or p['name']}",
            f"""{p.get('unit_name') or p['name']}, pet {CODE.get(p.get('quality'), '?')}.
            Efek: {d[:200]}. Pet beraksi sekali di awal battle, tidak memakan slot lineup,
            tidak terikat bond.""")
for r in json.load(open("tables/TableAdvancedMount.json")):
    mid = r["MountID"]
    ks = sorted(k for k in loc if k.startswith(f"MountSkill_{mid}"))
    add(f"mount:{mid}", "mount", f"Mount {loc.get(f'ItemName_{mid}', mid)}",
        f"""{loc.get(f'ItemName_{mid}', mid)}. Efek unik:
        {strip(loc[ks[0]])[:200] if ks else 'tidak tercatat'}. Kedelapan mount memberi stat identik
        (ATK +300, DEF +150 di level maks), jadi pilih berdasarkan efek, bukan angka.""")

# ---------------- inference ----------------
add("op:tiers", "opinion", "Tier list per mode (PENILAIAN)",
    """PENILAIAN, bukan fakta — dibaca dari teks skill, tanpa win rate atau log tempur.
    Guild Boss: Goddess of Wisdom, Goddess of the Hunt, Holy Knight. Arena: Pharaoh,
    Goddess of Wisdom, Dragon Warrior. Co-op: Goddess of Wisdom, Dragon Warrior,
    Goddess of the Hunt. Dungeon: Dragon Warrior, Tidecaller. Panduan komunitas menempatkan
    Bounty Hunter di core team sementara metode ini tidak menangkapnya — kalau berbeda, ikuti
    panduan komunitas.""", confidence="inference")
add("op:lineup", "opinion", "Aturan menyusun lineup (PENILAIAN)",
    """Susun 2+2+1 supaya dua bond aktif. Jadikan bond Warrior fondasi karena tidak ada musuh yang
    meng-counter Warrior, Support, atau Control. Ganti bond kedua sesuai kelemahan musuh. Di Co-op
    hindari menumpuk Support/Control. Di Dungeon jangan andalkan hero berbasis blessing. Lawan bos
    abaikan counter. Catatan: saran ini bersandar pada asumsi efek bond signifikan, dan besarannya
    tidak diketahui.""", confidence="inference")

with open(f"{OUT}/knowledge.jsonl", "w") as f:
    for c in chunks:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")

by = collections.Counter(c["type"] for c in chunks)
conf = collections.Counter(c["confidence"] for c in chunks)
print(f"{len(chunks)} chunk -> {OUT}/knowledge.jsonl")
print("  per tipe:", dict(by))
print("  per confidence:", dict(conf))
print("  panjang teks rata-rata:", sum(len(c["text"]) for c in chunks) // len(chunks))
