# Oopsie Croco — dump & data extraction

Package `com.oopsie.croco.challenge.leisure.battle.game`, versi 1.8.6 (versionCode 9).
Unity 2022.3.62f2, IL2CPP + HybridCLR, arm64-v8a, YooAsset 1.4.17.
Ditarik dari BlueStacks Air (Android 13) lewat adb.

## Struktur folder

```
croco/
├── README.md
├── gallery.html      # harus sefolder dengan icons/
├── scripts/          # semua tooling Python — jalankan dari mana saja, path relatif ke root
├── raw/              # sumber mentah (1.1 GB): apk/, builtin/, data/
├── tables/           # 212 tabel game hasil dump
├── icons/            # 3.646 PNG + index.json
├── out/              # hasil turunan: heroes/pets/monsters/summons/troops/units .json/.csv,
│                     #   meta.json, mode_scores.json, icon_map.json, portraits/, rarity/
└── knowledge/        # korpus chatbot (knowledge.jsonl, SYSTEM-PROMPT, TIERLIST, ENCOUNTERS, SUBSTITUSI)
```

## Hasil akhir

| file | isi |
|---|---|
| `out/heroes.json` / `.csv` | **53 hero playable** — stat, skill, passive, blessing, story |
| `out/pets.json` / `.csv` | **46 pet** — stat + `pet_quality`, `pet_max_level`, `piece_needed` |
| `out/monsters.json` / `.csv` | **141 monster & boss** |
| `out/summons.json` / `.csv` | **29 summon / totem** (klon, elemental, turret) |
| `out/troops.json` / `.csv` | **20 unit generik** (Apprentice Knight, Archer, dll) |
| `out/units.json` / `.csv` | gabungan 217 unit bernama, kalau butuh satu file |
| `tables/*.json` | 212 tabel game mentah (`TableUnitCard`, `TableSkillCard`, `TableUnitAttr`, …) |
| `tables/_Localization_EN.json` | 27.010 string lokalisasi Inggris |
| `icons/` (245 MB) | 3.646 gambar PNG: portrait, ikon skill, rarity, role, item, pet, UI |
| `icons/index.json` | nama aset → path file |
| `out/icon_map.json` | peta semantik: hero/skill/role/rarity/stat/item/pet → file ikon |
| `out/portraits/` | 42 portrait hero, dinamai `<rarity>_<nama>_<id>.png` |
| `gallery.html` | halaman Tailwind: 255 unit dengan tab kategori + portrait, ikon skill, role, stat. Buka langsung di browser — **harus satu folder dengan `icons/`** karena gambarnya dirujuk relatif |

Regenerasi: `cd scripts && python dump_tables.py && python build_heroes.py && python split_units.py && python extract_icons.py && python build_icon_map.py && python build_gallery.py`

Korpus chatbot: `python scripts/gather_meta.py && python scripts/build_encounters.py && python scripts/build_subs.py && python scripts/build_knowledge.py`

### Pembagian unit

Semua aktor tempur ada di satu `TableUnitCard` (289 baris), dipisah lewat `Race`:

| kategori | aturan | jumlah |
|---|---|---|
| hero | ada string `HeroName_<id>` | 53 |
| pet | `Race == 500000` (cocok dengan `TablePetNew.PetID`) | 46 |
| monster | `Race == 999` | 141 |
| summon | `Race == 998` | 29 |
| troop | sisa ras playable tanpa `HeroName` | 20 |

Skala rarity huruf (`QualityLiteName`) berhenti di SSS=6, padahal `Quality` sampai 9
(`QualityName_7..9` = Immortal Ⅰ/Ⅱ/Ⅲ) — tier di atas SSS ditulis `SSS+`, `SSS++`, `SSS+++`.

### Nama ikon penting

| konsep | pola nama | sumber |
|---|---|---|
| portrait hero | `Icon_Head_<artId>` | `TableUnitCard.HeadIcon`, fallback `TableUnitSkin.SkinHead/SkinIcon` |
| ikon **blessing** | `Icon_Skill_<blessId>` | `TableBless.BlessIcon` — **683 dari 686 aset `Icon_Skill_*` sebenarnya milik sini, bukan skill hero** |
| ikon skill hero | `Icon_Skill_<skillId+10>` | `TableSkillCard.SkillIcon`; hanya ~11% skill hero punya ikon sendiri |
| badge role | `Icon_Profession_1..8` | urutan sama dengan string `Position_*` |
| frame rarity | `FormationQualityBg_2..6` | indeks = `Quality` |
| ikon stat | `co_icon1_HP` / `_attack` / `_def` / `_speed` | — |
| item, pet, bless, gear | `Icon_Item_*`, `Icon_Pet_*`, `iconBless_*`, `Icon_Gear_*` | `TableItem.Icon`, `TablePetNew.PetIcon`, dst |

11 hero (Aeron, Borg, Zark, Lina, Cain, Ryan, Rain Steelfin, Karan, Edrick, Brook, Sol)
tidak punya art portrait di build ini — nama yang dirujuk tabel (`Icon_Head_1001`,
`Icon_Head_2008`, `heroIcon_002`, …) tidak ada di 1040 bundle maupun cache.

## Enkripsi bundle (yang perlu dibongkar)

File bundle bukan UnityFS biasa — **setiap byte ke-500 di-XOR** dengan keystream
15 byte, diindeks `(offset // 500) % 15`:

```
ED 35 C9 4D 50 DA 6B D0 08 63 E6 74 B8 8F B7
```

Offset 0 ikut terkena, itu sebabnya file diawali `0xB8` bukan `'U'` (`0x55 ^ 0xED`).
Setelah di-XOR balik, semuanya jadi UnityFS standar — 1040/1040 bundle terdekompresi
persis. Type tree aktif, jadi UnityPy bisa baca MonoBehaviour langsung.

Kunci ditemukan lewat `findkey.py`: cari blok LZ4 yang cuma memuat satu posisi
kelipatan-500, brute force nilainya sampai blok terdekompresi tepat sebesar ukuran
yang dideklarasikan, lalu bootstrap indeks keystream yang tersisa.

Catatan: `global-metadata.dat` juga terenkripsi (magic bukan `AF1BB1FA`), tapi tidak
diperlukan — data game ada di ScriptableObject, bukan di kode.

## Tooling

| script | fungsi |
|---|---|
| `scripts/bundle.py` | dekripsi + baca bundle → file di dalamnya |
| `scripts/manifest.py` | parser binary `PackageManifest` YooAsset (aset → bundle) |
| `scripts/extract_bundle.py` | CLI: `python scripts/extract_bundle.py <bundle> [outdir]` |
| `scripts/dump_tables.py` | dump 212 tabel ke JSON |
| `scripts/build_heroes.py` | join unit + stat + skill + lokalisasi → `out/units.*` |
| `scripts/extract_icons.py` | render semua Sprite/Texture2D jadi PNG → `icons/` |
| `scripts/build_icon_map.py` | peta konsep → file ikon → `out/icon_map.json` |
| `scripts/split_units.py` | pisah jadi `out/{heroes,pets,monsters,summons,troops}.json` + `.csv` |
| `scripts/build_gallery.py` | render `gallery.html` dari file terpisah + `icons/` |
| `scripts/findkey.py` |
| `scripts/gather_meta.py` | ringkas hero/pet/mode → `out/meta.json` |
| `scripts/analyze_modes.py` | skor hero per mode → `out/mode_scores.json` |
| `scripts/build_encounters.py` | `knowledge/ENCOUNTERS.md` |
| `scripts/build_subs.py` | `knowledge/SUBSTITUSI.md` |
| `scripts/build_lineups.py` | cetak tabel lineup (dipakai manual untuk `TIERLIST.md`) |
| `scripts/build_knowledge.py` | `knowledge/knowledge.jsonl` | rekonstruksi keystream (dokumentasi cara kunci didapat) |

Cari bundle berdasarkan path aset:

```python
from manifest import load
head, assets, bundles = load('raw/builtin/assets/BuildinFiles/PackageManifest_GameData_2026_07_28_17_44_19.bytes')
a = next(a for a in assets if a['path'].endswith('/TableUnitCard.asset'))
print(bundles[a['bundle']]['hash'])   # -> ddac25f022ec94586c4cded4572eacc3
```

## Sumber mentah

- `raw/apk/` (567 MB) — `base.apk`, `split_cb9f9f.apk` (bundle bawaan), `split_config.arm64_v8a.apk`.
  Install ulang: `adb install-multiple raw/apk/*.apk`
- `raw/builtin/` — 1043 file hasil unzip `assets/BuildinFiles/` dari split APK (1040 bundle + manifest)
- `raw/data/` (159 MB) — `persistentDataPath` dari `/sdcard/Android/data/<pkg>`:
  `SaveFile.es3` (Easy Save 3, terenkripsi AES), cache YooAsset, `il2cpp/`

`/data/data/<pkg>` belum diambil — butuh root, dan BlueStacks mematikannya
(`bst.feature.rooting="0"` di `/Users/Shared/Library/Application Support/BlueStacks/bluestacks.conf`).
Isinya kemungkinan hanya shared_prefs; tidak dibutuhkan untuk data game.

## Catatan data

`TableBless` (706 baris, 392 terkait hero playable) berisi pilihan blessing dalam run —
tiap entri punya nama, deskripsi, dan ikon, ditautkan lewat kolom `BlessHero`. Ini yang
memiliki hampir semua aset `Icon_Skill_*`. Skill hero sendiri jarang punya ikon.

Entri skill diberi label `kind`: `skill` (410, punya nama), `upgrade` (56, hanya ada
`SkillLvUpDesc` — catatan naik level, bukan skill), `effect` (9, ada deskripsi tanpa nama).

Tiga string di lokalisasi punya salah ketik dari pengembang — `ma1imum`, `e1ceeding`
(huruf x jadi 1) di `SkillDesc_410501110/120/130`. Bukan korupsi ekstraksi: 105 entri
lain mengeja `maximum` dengan benar.


Stat di `out/heroes.*` adalah nilai template level 1 dari `TableUnitAttr`. Skala
sebenarnya datang dari `TableUnitLevel` (301 baris), `TableUnitGrade` (1030) dan
`TableUnitStarUp` (62) — pakai itu kalau butuh angka end-game.
