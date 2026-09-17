"""Emit SUBSTITUSI.md — "kalau tidak punya X, pakai siapa?" for all 34 heroes.

Two answers per hero, because they are different questions. The drop-in keeps
the bond: same profession, one tier down, so the lineup's shape survives. The
mechanic column answers what you actually lose, and who else in the game has
it — which is often a different class, and therefore a different lineup.
"""
import json, collections
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

META = json.load(open("out/meta.json"))
TIERS = ["UR", "SP", "SSR", "SR", "R"]
H = {h["epithet"]: h for h in META["heroes"]}
BY_PROF = collections.defaultdict(list)
for h in META["heroes"]:
    BY_PROF[h["profession"]].append(h["epithet"])
for p in BY_PROF:
    BY_PROF[p].sort(key=lambda e: TIERS.index(H[e]["rarity"]))

# only the mechanics scarce enough that losing one changes how you play
SCARCE = {
    "maxhp": "damage %Max HP",
    "defpen": "defense penetration",
    "truedmg": "true damage",
    "hardcc": "hard CC",
}
OWNERS = {
    k: [e for e in H if H[e]["mech"].get(k)] for k in SCARCE
}


def main():
    md = ["""# Oopsie Croco — Tabel Substitusi Hero

Jawaban untuk satu pertanyaan: **"aku tidak punya X, pakai siapa?"**

Ada dua jawaban dan keduanya berbeda:

- **Pengganti langsung** — profesi sama, satu tingkat di bawah. Bond tetap nyala, bentuk lineup
  tidak berubah. Ini yang kamu pakai kalau cuma butuh mengisi slot.
- **Mekanik yang hilang** — kemampuan langka yang tidak dibawa penggantinya, dan siapa lagi di
  game yang punya. Sering beda profesi, jadi memilihnya berarti mengubah bond.

Hanya empat mekanik yang cukup langka untuk dicatat: damage %Max HP (2 hero), defense
penetration (4), true damage (1), dan hard CC (5). Selain itu penggantinya setara.
"""]
    for prof in sorted(BY_PROF):
        md.append(f"\n## {prof}\n")
        md.append("| Kalau tidak punya | Pakai (urut terbaik) | Mekanik yang hilang | Siapa lagi yang punya |")
        md.append("|---|---|---|---|")
        ladder = BY_PROF[prof]
        for i, e in enumerate(ladder):
            h = H[e]
            subs = [f"{x} [{H[x]['rarity']}]" for x in ladder[i + 1:]]
            lost, alt = [], []
            for k, label in SCARCE.items():
                if not h["mech"].get(k):
                    continue
                # kept by a same-class substitute? then nothing is lost
                if any(H[x]["mech"].get(k) for x in ladder[i + 1:]):
                    continue
                lost.append(label)
                others = [f"{x} [{H[x]['rarity']}] ({H[x]['profession']})"
                          for x in OWNERS[k] if x != e]
                alt.append(", ".join(others) if others else "**tidak ada pengganti**")
            md.append(
                f"| {e} [{h['rarity']}] | {' → '.join(subs) or '—'} "
                f"| {', '.join(lost) or '—'} | {' · '.join(alt) or '—'} |"
            )
    open("knowledge/SUBSTITUSI.md", "w").write("\n".join(md) + "\n")
    print("SUBSTITUSI.md ditulis —", len(META["heroes"]), "hero")


if __name__ == "__main__":
    main()
