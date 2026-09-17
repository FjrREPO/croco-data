# Oopsie Croco — Panduan Tier List & Lineup

Disusun dari tabel game itu sendiri (dump APK v1.8.6, data 2026-07-28), bukan dari meta komunitas.

**Cara membaca dokumen ini.** Ada dua jenis pernyataan di sini dan keduanya sengaja dipisah:

- **FAKTA** — terbaca langsung di tabel game. Bisa kamu cek sendiri, dan tidak akan berubah kecuali
  game-nya di-patch. Semua tabel di bagian 1–4, 6, dan 7 masuk kategori ini.
- **PENILAIAN** — urutan tier dan susunan lineup di bagian 5. Ini inferensi saya dari teks skill.
  **Tidak ada win rate, log tempur, atau data pemain di dump ini**, jadi anggap sebagai titik awal.

---

## 1. Struktur roster (FAKTA)

34 hero playable, tersusun sebagai **grid 8 profesi × 4 tier + 2 UR**:

| Profesi | UR | SP | SSR | SR | R |
|---|---|---|---|---|---|
| **Archer** | Goddess of the Hunt | Light Archer | Bounty Hunter | Turtle Shooter | Gunslinger |
| **Warrior** | Goddess of Wisdom | Dragon Warrior | Holy Knight | Radiant Warrior | Piggy Vanguard |
| **Mage** | — | Red Queen | Star Mage | Snow Witch | Ice Mage |
| **Assassin** | — | Catwoman | Phantom | Shadow Wolf | Silver Moon Assassin |
| **Summon** | — | Tidecaller | Fire Spirit Master | Necromancer Apprentice | Bear Caller |
| **Support** | — | Flower Spirit | Onmyoji | Little Healer | Priest Apprentice |
| **Control** | — | Succubus | Pharaoh | Pumpkin | Little Magic Fairy |
| **Calamity** | — | Sword Demon | Dark Knight | Pain Sorceress | Night Demon |

**Setiap profesi punya opsi di tiap tingkat harga.** Kamu tidak pernah terpaksa melewatkan bond
karena tidak punya hero mahal — selalu ada versi SSR, SR, atau R-nya.

### Apa yang benar-benar hilang kalau tanpa UR/SP

| Mekanik | Masih ada tanpa UR/SP? | Pengganti |
|---|---|---|
| Damage % Max HP | **TIDAK** — hanya 2 UR yang punya | tidak ada; ganti dengan DPS berkelanjutan |
| Defense penetration | ya | Star Mage [SSR], Snow Witch [SR] |
| True damage | ya | Phantom [SSR] |
| Hard CC | ya | Pharaoh [SSR], Pumpkin [SR], Priest Apprentice [R] |

Jadi F2P kehilangan **satu** mekanik saja, dan itu hanya terasa di Guild Boss (HP tetap). Sisanya
tersedia di SSR ke bawah.

---

## 2. Mekanik lineup (FAKTA)

### Ukuran lineup: 1 sampai 8, bukan selalu 5

`TableGrade` — Population naik dari **1 (grade 1) sampai 8 (grade 8)**, dan **setiap hero berbiaya
1** (`Population: 1` untuk keseluruhan 34 hero). Jadi jumlah slot adalah grade Hero Comp kamu, dan
naik dengan EXP.

Dokumen ini memakai **5 slot** sebagai dasar. Kalau slotmu berbeda:

| Slot | Susunan bond terbaik |
|---|---|
| 4 | 2 + 2 — dua bond |
| **5** | **2 + 2 + 1** — dua bond, satu slot bebas |
| 6 | 2 + 2 + 2 — tiga bond |
| 7 | 2 + 2 + 2 + 1 |
| 8 | 2 + 2 + 2 + 2 — empat bond |

Slot ganjil selalu menyisakan satu slot bebas. Isi slot itu dengan hero terkuat yang kelasnya tidak
di-counter musuh stage tersebut (lihat bagian 6).

### Bond — 2 unit sekelas

`TableBond`: kedelapan profesi punya bond dengan `RequiredCount: 2`.

> Lima kelas berbeda = nol bond. Ini kesalahan lineup paling mahal yang bisa dilakukan pemain baru.

*Batas yang jujur:* bond memberi **skill** (`AEIDs` → `SkillIDs`), bukan bonus stat (`AttrIDs`
kosong). Tapi skill-skill itu **tidak punya teks di lokalisasi**, jadi besarannya tidak bisa saya
sebut. Kalau ternyata efeknya kecil, seluruh saran 2+2+1 ikut melemah.

### Sistem counter (restrain)

Satu arah, dan **hanya berlaku pada monster biasa** — bukan bos, bukan PvP:

- 46 monster punya `RestrainPros` = kelas hero yang mengalahkannya
- 11 monster punya `Restrain` = kelas hero yang **mereka** kalahkan
- Semua unit ber-restrain ada di `monsters.json`; **tidak ada satu pun hero** yang punya

---

## 3. Aturan tiap mode (FAKTA)

| Mode | Draft blessing | Buff kelas | Sifat musuh |
|---|---|---|---|
| **Campaign** | **2 per level** (893 level) | — | monster, counter aktif |
| **Co-op** (TeamPVE) | **2 per level** (162 level) | **ya, 6 kelas** | monster, counter aktif |
| **Dungeon** (Instance) | **0 — tidak ada draft** (90 stage) | — | monster + bos |
| **Guild Boss** | — | — | HP tetap (150 → 1775+) |
| **Rob Boss** | — | — | **`unlimitedhp: -1`** — HP tak terbatas |
| **Arena** | — | — | tim pemain lain |

**Blessing hanya menumpuk di Campaign dan Co-op.** Hero yang kekuatannya di pohon blessing turun
kelas di Dungeon, Boss, dan Arena. Di Dungeon yang menang kit dasar.

**Buff kelas co-op melewatkan dua profesi.** `TableTeamPVEBuff` memberi buff ke Mage, Archer,
Warrior, Summon, Calamity, Assassin — **Support dan Control tidak dapat apa pun**.

**Rob Boss bukan soal membunuh.** HP tak terbatas, skornya berapa lama kamu bertahan sambil
memukul. Damage %Max HP tidak relevan di sini.

---

## 4. Kelangkaan mekanik (FAKTA)

| Mekanik | Jumlah hero | Siapa |
|---|---|---|
| Damage % Max HP | **2** | Goddess of the Hunt [UR], Goddess of Wisdom [UR] |
| Defense penetration | **4** | Goddess of the Hunt [UR], Red Queen [SP], **Star Mage [SSR]**, **Snow Witch [SR]** |
| True damage | **1** | **Phantom [SSR]** |
| Hard CC | **5** | **Pharaoh [SSR] — 7×**, Pumpkin [SR], Tidecaller [SP], Succubus [SP], Priest Apprentice [R] |

Pharaoh cuma SSR tapi pemegang hard CC terpadat di game. Snow Witch cuma SR tapi satu dari empat
pemilik DEF penetration. Piggy Vanguard cuma R tapi punya sinyal shield/damage-reduction terpadat.

---

## 5. Lineup per mode (PENILAIAN)

Setiap lineup **tepat 5 hero**. Kolom *Alternatif* adalah pengganti untuk slot itu kalau hero
utamanya belum kamu punya atau levelnya masih ketinggalan.

**Aturan mengganti:** ambil dari kiri, lewati siapa pun yang sudah dipakai di slot lain. Karena
roster-nya grid 8×4, penggantinya selalu **profesi yang sama satu tingkat di bawah** — jadi bond
tetap nyala berapa pun tier yang kamu pakai. Yang berubah kualitas isinya, bukan strukturnya.

Tanda `—` berarti hero itu sudah tingkat terendah di profesinya.

### 5.1 Guild Boss — HP tetap, lomba damage

**Tier:** S — Goddess of Wisdom, Goddess of the Hunt, Holy Knight · A — Dragon Warrior, Catwoman, Flower Spirit, Bounty Hunter · B — Red Queen, Star Mage, Onmyoji

Skill kedua UR saling menyebut: crit Goddess of the Hunt berlipat kalau Goddess of Wisdom ikut turun. Kalau keduanya tidak ada, ganti slot 3–4 jadi bond Mage (Red Queen + Star Mage) — dua DEF pen menggantikan damage %Max HP yang hilang.

| # | Utama | Alternatif (turun tier) | Kelas | Fungsi |
|---|---|---|---|---|
| 1 | **Goddess of Wisdom** [UR] | Dragon Warrior [SP] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | damage %Max HP, tank |
| 2 | **Holy Knight** [SSR] | Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | bond Warrior, sustain |
| 3 | **Goddess of the Hunt** [UR] | Light Archer [SP] → Turtle Shooter [SR] → Gunslinger [R] | Archer | damage %Max HP + DEF pen |
| 4 | **Bounty Hunter** [SSR] | Turtle Shooter [SR] → Gunslinger [R] | Archer | bond Archer, DPS single-target |
| 5 | **Flower Spirit** [SP] | Onmyoji [SSR] → Little Healer [SR] → Priest Apprentice [R] | Support | heal |

### 5.2 Rob Boss — HP tak terbatas, bertahan selama mungkin

**HP tak terbatas**, jadi skornya berapa lama kamu bertahan sambil memukul. Damage %Max HP tidak berguna di sini, dan **Piggy Vanguard [R] justru naik kelas** — sinyal shield/damage-reduction terpadat di roster. Dia dipilih karena kemampuannya, bukan karena murah.

| # | Utama | Alternatif (turun tier) | Kelas | Fungsi |
|---|---|---|---|---|
| 1 | **Goddess of Wisdom** [UR] | Dragon Warrior [SP] → Holy Knight [SSR] → Radiant Warrior [SR] | Warrior | tank + damage |
| 2 | **Piggy Vanguard** [R] | — | Warrior | bond Warrior, shield terpadat |
| 3 | **Flower Spirit** [SP] | Little Healer [SR] → Priest Apprentice [R] | Support | heal |
| 4 | **Onmyoji** [SSR] | Little Healer [SR] → Priest Apprentice [R] | Support | bond Support, heal kedua |
| 5 | **Goddess of the Hunt** [UR] | Light Archer [SP] → Bounty Hunter [SSR] → Turtle Shooter [SR] → Gunslinger [R] | Archer | DPS berkelanjutan |

### 5.3 Arena — CC yang menentukan

**Tier:** S — Pharaoh, Goddess of Wisdom, Dragon Warrior · A — Sword Demon, Succubus, Dark Knight, Tidecaller · B — Holy Knight, Flower Spirit, Phantom

Inti arena ini **tidak butuh UR sama sekali** — Pharaoh, pemegang hard CC terpadat di game, cuma SSR.

| # | Utama | Alternatif (turun tier) | Kelas | Fungsi |
|---|---|---|---|---|
| 1 | **Pharaoh** [SSR] | Pumpkin [SR] → Little Magic Fairy [R] | Control | hard CC terpadat (7×) |
| 2 | **Succubus** [SP] | Pumpkin [SR] → Little Magic Fairy [R] | Control | bond Control, soft CC |
| 3 | **Goddess of Wisdom** [UR] | Holy Knight [SSR] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | tank + burst |
| 4 | **Dragon Warrior** [SP] | Holy Knight [SSR] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | bond Warrior |
| 5 | **Flower Spirit** [SP] | Onmyoji [SSR] → Little Healer [SR] → Priest Apprentice [R] | Support | heal |

### 5.4 Co-op — draft blessing + buff kelas

**Tier:** S — Goddess of Wisdom, Dragon Warrior, Goddess of the Hunt · A — Catwoman, Sword Demon, Tidecaller, Light Archer · B — Bear Caller, Fire Spirit Master

Kelima slot sengaja diisi kelas yang **dapat buff co-op**. Support dan Control tidak dapat apa pun, jadi Flower Spirit dan Pharaoh turun kelas di sini meski bagus di mode lain.

| # | Utama | Alternatif (turun tier) | Kelas | Fungsi |
|---|---|---|---|---|
| 1 | **Goddess of Wisdom** [UR] | Holy Knight [SSR] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | dapat buff kelas |
| 2 | **Dragon Warrior** [SP] | Holy Knight [SSR] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | bond Warrior, dapat buff |
| 3 | **Goddess of the Hunt** [UR] | Bounty Hunter [SSR] → Turtle Shooter [SR] → Gunslinger [R] | Archer | dapat buff |
| 4 | **Light Archer** [SP] | Bounty Hunter [SSR] → Turtle Shooter [SR] → Gunslinger [R] | Archer | bond Archer, dapat buff |
| 5 | **Catwoman** [SP] | Phantom [SSR] → Shadow Wolf [SR] → Silver Moon Assassin [R] | Assassin | dapat buff |

### 5.5 Dungeon — tanpa draft blessing, counter aktif

**Tier:** S — Dragon Warrior, Tidecaller · A — Bear Caller, Necromancer Apprentice, Red Queen, Goddess of Wisdom · B — Goddess of the Hunt *(kekuatannya di blessing yang tidak bisa di-draft di sini)*

Satu-satunya mode yang lineup-nya **harus diganti per stage** — lihat bagian 6.3.

| # | Utama | Alternatif (turun tier) | Kelas | Fungsi |
|---|---|---|---|---|
| 1 | **Tidecaller** [SP] | Fire Spirit Master [SSR] → Necromancer Apprentice [SR] | Summon | summon menahan gelombang |
| 2 | **Bear Caller** [R] | — | Summon | bond Summon |
| 3 | **Goddess of Wisdom** [UR] | Holy Knight [SSR] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | tank |
| 4 | **Dragon Warrior** [SP] | Holy Knight [SSR] → Radiant Warrior [SR] → Piggy Vanguard [R] | Warrior | bond Warrior |
| 5 | **Red Queen** [SP] | Star Mage [SSR] → Snow Witch [SR] → Ice Mage [R] | Mage | AoE |


## 6. Lineup per musuh (FAKTA + PENILAIAN)

### 6.1 Bawa kelas ini

| Kelas | Musuh yang dikalahkannya |
|---|---|
| **Archer** | Stone Giant, Shield-Breaking Stone Giant, Rocksolid Giant, Mountain Titan, Hard-Shell Crab Emperor, Hermit Crab, Land Shark King |
| **Mage** | Slime King, Crab Emperor, Ironclad Crab King, Sea-Splitting Crab Emperor, Shapeshifting Queen, Deep Sea Touch |
| **Support** | Abyssal Shadow, Deepsea Shadow, Dread of the Dark Sea, Venomous Catfish King |
| **Assassin** | Octopus King, Tentacle, Deep Sea Fiend-Arm, Giant-Armed Fiend, Two-Headed Dog, Venom-Stinger Bee Queen |
| **Calamity** | Hellhound, Eye Monster, Corrupted Fungal Lord, Toxic Spore Mushroom King, Venom Mushroom King |
| **Summon** | Bomb King, The Split Slime King, Slime Queen, Corrosive Empress |
| **Control** | Eye of the Void, Eye of the Rift, Demonic Eye of the End, Phantom Eye Monster |
| **Warrior** | Pig Overlord, Hive Tyrant, Venom Bee Queen |

Pola tematiknya: **batu dan cangkang → Archer**, **laut dan slime → Mage**, **bayangan → Support**,
**tentakel dan serangga → Assassin**, **jamur dan iblis → Calamity**, **raja yang membelah diri →
Summon**, **mata → Control**, **babi dan lebah → Warrior**.

### 6.2 JANGAN bawa kelas ini

| Musuh | Meng-counter |
|---|---|
| Mutated Slime, Shrinkshell Seaweed | **Archer** |
| Seed Flower, Spellbreaking Lantern Tree, Catfish King | **Mage** |
| Bigmouth Man-eating Flower, Desert Worm | **Summon** |
| Nightshade Charm Fox, Mist Octopus | **Assassin** |
| Illusion Seahorse, Hardshell Rhinoceros Beetle | **Calamity** |

Tidak ada musuh yang meng-counter **Warrior, Support, atau Control**. Tiga kelas itu aman dibawa ke
stage mana pun — alasan bagus menaruh **bond Warrior sebagai fondasi tetap** dan mengganti bond
kedua sesuai musuh.

### 6.3 Cara mengganti bond kedua

Bond Warrior (slot 3–4) tetap. Tukar slot 1–2 sesuai isi stage:

| Isi stage | Bond kedua | Pasangan |
|---|---|---|
| Slime King, Crab | Mage | Red Queen + Star Mage · Star Mage + Snow Witch · Snow Witch + Ice Mage |
| Stone Giant, Titan | Archer | Goddess of the Hunt + Light Archer · Bounty Hunter + Turtle Shooter · Turtle Shooter + Gunslinger |
| Bomb King, Split Slime | Summon | Tidecaller + Fire Spirit Master · Fire Spirit Master + Necromancer Apprentice · Necromancer Apprentice + Bear Caller |
| Mata (Eye) | Control | Succubus + Pharaoh · Pharaoh + Pumpkin · Pumpkin + Little Magic Fairy |
| Jamur, Hellhound | Calamity | Sword Demon + Dark Knight · Dark Knight + Pain Sorceress · Pain Sorceress + Night Demon |
| Tentakel, lebah | Assassin | Catwoman + Phantom · Phantom + Shadow Wolf · Shadow Wolf + Silver Moon Assassin |
| Bayangan | Support | Flower Spirit + Onmyoji · Onmyoji + Little Healer · Little Healer + Priest Apprentice |
| Pig Overlord, Hive | Warrior ×2 | pakai 4 Warrior sekaligus, atau tetap 2 + isi bebas |

Tiga pasangan per baris: mahal → menengah → murah.

---

## 7. Bos (FAKTA)

| Mode | Bos | Counter |
|---|---|---|
| Guild Boss | Igris | **netral** |
| Rob Boss | Darkflame Dragonlord·Serre | **netral** |
| Dungeon | Demonic Ancient Tree Urosa, Rift King·Magthosen | **netral** |

**Keempat bos bernama tidak punya data restrain sama sekali.** Untuk fight bos, lupakan sistem
counter dan optimalkan bond + mekanik. Counter hanya berlaku di gelombang monster sebelum bos.

---

## 8. Pet (FAKTA)

Pet memberi efek sekali di awal battle dan **tidak terikat bond**, jadi bebas dipilih per mode dan
tidak memakan slot lineup.

| Pet | Tier | Efek | Cocok untuk |
|---|---|---|---|
| **Magneto** | UR | menarik semua musuh ke satu titik | Dungeon, Campaign |
| **Zog・Everdark** | UR | 5× true damage | Boss — satu-satunya sumber true damage selain Phantom |
| **Iron Rabbit** | UR | 15 pukulan, makin sakit ke target sama | Boss single-target |
| **Godoff** | UR | shield untuk semua hero | Rob Boss, Arena |
| **Celebi** | UR | damage area 5×5 per detik | Dungeon |
| **Aizen / Panda** | UR / SP | menggandakan hero dengan Blessing terbanyak | **Campaign & Co-op saja** |
| **Bone Eagle** | SP | stun sampai 5 musuh | Arena |
| **Joyboy** | SP | heal + buff seluruh tim | Rob Boss, Co-op |

Aizen dan Panda hanya masuk akal di Campaign dan Co-op — di Dungeon/Boss/Arena tidak ada blessing
yang ditumpuk, jadi "hero dengan Blessing terbanyak" tidak berarti apa-apa.

---

## 9. Ringkasan keputusan

1. **Isi semua slot, dan susun 2+2+1** (di 5 slot). Lima kelas berbeda = nol bond.
2. **Bond Warrior sebagai fondasi** — tidak ada musuh yang meng-counter Warrior, dan tangganya
   lengkap dari UR sampai R.
3. **Ganti bond kedua sesuai musuh** (bagian 6.3), tapi hanya di Campaign dan Dungeon.
4. **Di Co-op hindari menumpuk Support/Control** — dua kelas itu tidak dapat buff mode.
5. **Di Dungeon jangan andalkan hero berbasis blessing** — tidak ada draft di sana.
6. **Lawan bos, abaikan counter** — keempatnya netral.
7. **Tanpa UR/SP kamu hanya kehilangan damage %Max HP.** Inti arena bahkan tidak butuh UR.

---

## 10. Batas dokumen ini

- Urutan tier adalah **penilaian saya dari teks skill**, bukan hasil ukur. Tidak ada win rate di dump.
- **Nilai bond tidak diketahui** — efeknya berupa skill tanpa teks lokalisasi. Kalau ternyata lemah,
  saran 2+2+1 melemah.
- Skor mekanik dihitung dari frekuensi kata, jadi hero yang kuat lewat satu angka besar bisa kalah
  peringkat dari hero yang menyebut "shield" belasan kali.
- **Bounty Hunter kemungkinan saya kecilkan.** Panduan komunitas menempatkannya di core team;
  kekuatannya di DPS single-target berkelanjutan lewat tumpukan Ammunition, dan metode saya tidak
  menangkap itu. Kalau saya dan panduan berbeda, ikuti panduan.
- Angka HP Guild Boss (150 → 1775) satuannya tidak jelas — kemungkinan pengali, bukan HP mentah.
- Susunan bond untuk 6–8 slot belum saya uji terhadap apa pun; itu perpanjangan logis dari aturan
  `RequiredCount: 2`, bukan temuan.

Dihasilkan dari `analyze_modes.py` dan `gather_meta.py`; data mentahnya di `meta.json` dan
`mode_scores.json`.
