# Oopsie Croco — Lineup per Encounter

Pendamping `TIERLIST.md`. Di sini setiap konten dipetakan ke **resistensi kelasnya**, lalu
diberi lineup 5 hero.

## Cara kerja resistensi (FAKTA)

`TableUnitAttr.ProDmgReductionIDs` memakai atribut `Attribute_4000X` = **"Received Damage Bonus
from \<kelas\>"**. Jadi:

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


### Story (Campaign)

**1.053 level di 72 chapter** (Tutorial + Ch 1–71), dikelompokkan berdasarkan profil resistensi yang sama. `TableChapter` memang punya 1.000 baris, tapi 928 di antaranya tidak punya satu level pun — `TableLevel` dan varian `TableLevel_a` sama-sama berhenti di ChapterID 9071. Konten yang angkanya sampai ribuan adalah **Endless**, di bawah.

Penomoran mengikuti yang dilihat pemain: ChapterID 9000 membawa `IsGuide: 1` ("Beginner Level") jadi itu tutorial, dan **Chapter 1 adalah Erin Forest**.

| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |
|---|---|---|---|---|
| Ch 1 Erin Forest, Ch 24 Moonshade, Ch 54 Shadow | Summon | Archer, Assassin, Calamity, Control, Mage, Support, Warrior | Tidecaller [SP] · Fire Spirit Master [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Necromancer Apprentice [SR] | bond Summon, bond Warrior |
| Ch 12 Bone Desert, Ch 13 Dragon Bay, Ch 14 Ebon Song, Ch 15 Shadow, Ch 42 Red Desert, Ch 43 Silver Beach … (+2) | Archer | Assassin, Calamity, Control, Mage, Summon, Support, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Bounty Hunter [SSR] | bond Archer, bond Warrior |
| Ch 16 Misty Bay, Ch 46 Oath Island | Calamity, Archer | Assassin, Control, Mage, Summon, Support, Warrior | Sword Demon [SP] · Dark Knight [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Goddess of the Hunt [UR] | bond Calamity, bond Warrior |
| Ch 17 Windleaf, Ch 47 Emerald | Archer, Calamity | Assassin, Control, Mage, Summon, Support, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Sword Demon [SP] | bond Archer, bond Warrior |
| Ch 18 Red Desert, Ch 20 Mistwhisper, Ch 48 White Dream, Ch 50 Leafwhisper | Warrior, Calamity | Archer, Assassin, Control, Mage, Summon, Support | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Sword Demon [SP] | bond Warrior, bond Support |
| Ch 19 Bone Coast, Ch 49 Wind Beach | Support, Calamity | Archer, Assassin, Control, Mage, Summon, Warrior | Flower Spirit [SP] · Onmyoji [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Sword Demon [SP] | bond Support, bond Warrior |
| Ch 21 Erin Forest, Ch 51 Bone Desert | Summon, Calamity | Archer, Assassin, Control, Mage, Support, Warrior | Tidecaller [SP] · Fire Spirit Master [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Sword Demon [SP] | bond Summon, bond Warrior |
| Ch 22 Red Desert, Ch 52 Dragon Bay | Archer, Summon | Assassin, Calamity, Control, Mage, Support, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Tidecaller [SP] | bond Archer, bond Warrior |
| Ch 23 Silver Beach, Ch 53 Ebon Song | Support, Summon | Archer, Assassin, Calamity, Control, Mage, Warrior | Flower Spirit [SP] · Onmyoji [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Tidecaller [SP] | bond Support, bond Warrior |
| Ch 25 Waste Gorge, Ch 55 Misty Bay | Archer, Support | Assassin, Calamity, Control, Mage, Summon, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] | bond Archer, bond Warrior |
| Ch 26 Oath Island, Ch 56 Windleaf | Warrior, Support | Archer, Assassin, Calamity, Control, Mage, Summon | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Holy Knight [SSR] | bond Warrior, bond Support |
| Ch 27 Emerald, Ch 28 White Dream, Ch 57 Red Desert, Ch 58 Bone Coast | Summon, Assassin | Archer, Calamity, Control, Mage, Support, Warrior | Tidecaller [SP] · Fire Spirit Master [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Catwoman [SP] | bond Summon, bond Warrior |
| Ch 29 Wind Beach, Ch 59 Mistwhisper | Archer, Assassin | Calamity, Control, Mage, Summon, Support, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Catwoman [SP] | bond Archer, bond Warrior |
| Ch 30 Leafwhisper, Ch 60 Redmane | Mage, Assassin | Archer, Calamity, Control, Summon, Support, Warrior | Red Queen [SP] · Star Mage [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Catwoman [SP] | bond Mage, bond Warrior |
| Ch 31 Bone Desert, Ch 61 Erin Forest | Control, Assassin | Archer, Calamity, Mage, Summon, Support, Warrior | Succubus [SP] · Pharaoh [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Catwoman [SP] | bond Control, bond Warrior |
| Ch 32 Dragon Bay, Ch 62 Red Desert | Mage, Control | Archer, Assassin, Calamity, Summon, Support, Warrior | Red Queen [SP] · Star Mage [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Succubus [SP] | bond Mage, bond Warrior |
| Ch 33 Ebon Song, Ch 63 Silver Beach | Archer, Control | Assassin, Calamity, Mage, Summon, Support, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Succubus [SP] | bond Archer, bond Warrior |
| Ch 34 Shadow, Ch 64 Moonshade | Warrior, Control | Archer, Assassin, Calamity, Mage, Summon, Support | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Succubus [SP] | bond Warrior, bond Support |
| Ch 35 Misty Bay, Ch 65 Waste Gorge | Calamity, Warrior | Archer, Assassin, Control, Mage, Summon, Support | Sword Demon [SP] · Dark Knight [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Holy Knight [SSR] | bond Calamity, bond Warrior |
| Ch 36 Windleaf, Ch 66 Oath Island | Mage, Warrior | Archer, Assassin, Calamity, Control, Summon, Support | Red Queen [SP] · Star Mage [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Holy Knight [SSR] | bond Mage, bond Warrior |
| Ch 37 Red Desert, Ch 41 Erin Forest, Ch 67 Emerald, Ch 71 Bone Desert | Control, Mage | Archer, Assassin, Calamity, Summon, Support, Warrior | Succubus [SP] · Pharaoh [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Red Queen [SP] | bond Control, bond Warrior |
| Ch 38 Bone Coast, Ch 68 White Dream | Calamity, Mage | Archer, Assassin, Control, Summon, Support, Warrior | Sword Demon [SP] · Dark Knight [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Red Queen [SP] | bond Calamity, bond Warrior |
| Ch 39 Mistwhisper, Ch 69 Wind Beach | Support, Mage | Archer, Assassin, Calamity, Control, Summon, Warrior | Flower Spirit [SP] · Onmyoji [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Red Queen [SP] | bond Support, bond Warrior |
| Ch 40 Redmane, Ch 70 Leafwhisper | Summon, Mage | Archer, Assassin, Calamity, Control, Support, Warrior | Tidecaller [SP] · Fire Spirit Master [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Red Queen [SP] | bond Summon, bond Warrior |
| Tutorial (Beginner Level), Ch 2 Erin Forest, Ch 3 Red Desert, Ch 4 Silver Beach, Ch 5 Moonshade, Ch 6 Waste Gorge … (+5) | — | — | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |

### Co-op (TeamPVE)

16 chapter, bos chapter ikut dihitung. Ingat: Support dan Control tidak dapat buff kelas di mode ini.

| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |
|---|---|---|---|---|
| Ch 1 | Mage, Control | Archer, Assassin, Calamity, Summon, Support, Warrior | Red Queen [SP] · Star Mage [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Succubus [SP] | bond Mage, bond Warrior |
| Ch 17, Ch 18 | — | — | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |
| Ch 2, Ch 10 | Calamity | Archer, Assassin, Control, Mage, Summon, Support, Warrior | Sword Demon [SP] · Dark Knight [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Pain Sorceress [SR] | bond Calamity, bond Warrior |
| Ch 3, Ch 11 | Assassin, Mage | Archer, Calamity, Control, Summon, Support, Warrior | Catwoman [SP] · Phantom [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Red Queen [SP] | bond Assassin, bond Warrior |
| Ch 4, Ch 12 | Mage | Archer, Assassin, Calamity, Control, Summon, Support, Warrior | Red Queen [SP] · Star Mage [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Snow Witch [SR] | bond Mage, bond Warrior |
| Ch 5, Ch 13 | Archer | Assassin, Calamity, Control, Mage, Summon, Support, Warrior | Goddess of the Hunt [UR] · Light Archer [SP] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Bounty Hunter [SSR] | bond Archer, bond Warrior |
| Ch 6, Ch 14 | Summon | Archer, Assassin, Calamity, Control, Mage, Support, Warrior | Tidecaller [SP] · Fire Spirit Master [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Necromancer Apprentice [SR] | bond Summon, bond Warrior |
| Ch 7, Ch 15 | Warrior, Archer | Assassin, Calamity, Control, Mage, Summon, Support | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |
| Ch 8, Ch 16 | Control | Archer, Assassin, Calamity, Mage, Summon, Support, Warrior | Succubus [SP] · Pharaoh [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Pumpkin [SR] | bond Control, bond Warrior |
| Ch 9 | Assassin, Summon | Archer, Calamity, Control, Mage, Support, Warrior | Catwoman [SP] · Phantom [SSR] · Goddess of Wisdom [UR] · Dragon Warrior [SP] · Tidecaller [SP] | bond Assassin, bond Warrior |

### Dungeon (Instance)

90 stage. Tidak ada draft blessing di sini — kit dasar yang menentukan.

| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |
|---|---|---|---|---|
| Yggdrasil tingkat 1, Yggdrasil tingkat 2, Yggdrasil tingkat 3, Yggdrasil tingkat 4, Yggdrasil tingkat 5, Yggdrasil tingkat 6 … (+84) | — | — | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |

### Guild Boss

HP tetap — lomba damage.

| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |
|---|---|---|---|---|
| Igris lv1, Igris lv2, Igris lv3, Igris lv4, Igris lv5, Igris lv6 … (+6) | — | — | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |

### Rob Boss

`unlimitedhp: -1` — bertahan selama mungkin, bukan membunuh.

| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |
|---|---|---|---|---|
| Darkflame Dragonlord·Serregos, Darkflame Dragonlord·Serregos, Darkflame Dragonlord·Serregos, Darkflame Dragonlord·Serregos, Darkflame Dragonlord·Serregos, Darkflame Dragonlord·Serregos … (+1) | — | — | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |

### Endless (Survival)

2.000 stage — inilah mode yang angkanya menembus ribuan, bukan story. `UnlockStage` menautkannya ke progres chapter, jadi stage terbuka seiring story.

**Di sini pilihan kelas tidak berpengaruh.** Endless memakai 41 monster unik dan **tidak satu pun punya resistensi per-kelas** (story memakai 68 monster, 23 di antaranya punya). Jadi Endless murni adu kekuatan, bukan adu counter — bawa lineup terkuatmu, bukan lineup counter. Barisnya tetap dikelompokkan per 100 stage supaya terlihat bahwa profilnya memang seragam dari stage 1 sampai 2.000.

| Encounter | Lemah terhadap | Menahan | Lineup (5) | Bond |
|---|---|---|---|---|
| Stage 1–100, Stage 101–200, Stage 201–300, Stage 301–400, Stage 401–500, Stage 501–600 … (+14) | — | — | Goddess of Wisdom [UR] · Dragon Warrior [SP] · Flower Spirit [SP] · Onmyoji [SSR] · Goddess of the Hunt [UR] | bond Warrior, bond Support |

### Pet

Efek sekali di awal battle, **tidak memakan slot lineup** dan tidak terikat bond.

| Pet | Tier | Efek | Paling berguna di |
|---|---|---|---|
| Abo | UR | At the start of battle, summons 3 clones of yourself to join the fight for 25 seconds. Each clon | Dungeon |
| Aizen | UR | At the start of battle, summons 2 mirror images of the hero with the most Blessings, the mirror  | Campaign, Co-op |
| Celebi | UR | At the start of battle, deals {0}% ATK damage every second to the 5x5 area containing the target | Dungeon, Campaign |
| Creed | UR | At battle start, deals 3 hits of {0}% ATK damage and marks the target for 3s, increasing damage  | umum |
| Godoff | UR | At battle start, all allied heroes immediately gain a shield equal to {0}% ATK and recover {1}%  | Rob Boss, Arena |
| Harry | UR | At battle start, deals {0} ATK damage separately to the target's 3x3 area and the 5x5 cross area | Dungeon, Campaign |
| Iron Rabbit | UR | At battle start, deals 15 hits of {0}% ATK damage. Each hit on the same target increases damage  | umum |
| Magneto | UR | At battle start, releases a magnetic vortex that gathers all enemies on the field and stuns them | Arena |
| Zog・Everdark | UR | At the start of battle,deals 5 instances of true damage equal to {0}% ATK and 1 instance of true | Boss |
| Bone Eagle | SP | At battle start, applies chains to up to 5 enemies, stunning them for {0}s. | Arena |
| Fennec Fox | SP | At battle start, deals {0}% ATK damage per second in a 3x3 area around the target for 3s. | Dungeon, Campaign |
| Fire Owl | SP | At battle start, deals {0}% ATK damage in a 5x5 area around the target. This damage ignores {1}% | Dungeon, Campaign |
| Joyboy | SP | At battle start, all allied heroes recover {0}% ATK as HP per second and increase damage by {1}% | Rob Boss, Co-op |
| Kai | SP | At the start of battle, summon 2 clones of yourself to join the fight for 10 seconds. Each clone | Dungeon |
| Kong King Cat | SP | At battle start, deals 3 hits of {0}% ATK damage and adds damage equal to {1}% of the target's m | umum |
| Panda | SP | Summons a mirror image of the hero with the most Blessings. The mirror image lasts for 60 second | Campaign, Co-op |
| Robin | SP | At battle start, deals 10 hits of {0}% ATK damage, and each hit has a 30% chance to additionally | umum |
| Vern・Crimsonclaw | SP | At the start of battle, deals {0}% ATK damage to all enemies, this damage ignores {1}% DEF, and  | umum |

### Mount

Kedelapan mount memberi **stat yang identik** (ATK +300, DEF +150 di level maks) — yang
membedakan hanya efek uniknya. Jadi pilih berdasarkan efek, bukan angka.

| Mount | Efek unik |
|---|---|
| Unicorn | When our hero dies, restore 15% of the maximum HP to the ally with the lowest HP, increase final damage by 10% for 5 sec |
| Stegosaurus | Every 10 seconds, deal damage equal to 75% of attack power to a random enemy, and has a 25% chance to cause stun, preven |
| Simba | Every 12 seconds, deal damage equal to 40% of attack power to all enemies, and increase our units' final damage reductio |
| Blade Rhino | Our hero increases maximum HP by 4% during combat and increases reflect damage by 5%. |
| Holy Armored Beast | When our hero's HP is above 70%, increase final damage reduction by 10%, and gain a shield every 5 seconds equal to 50%  |
| Mammoth | When our hero's HP is below 30%, increase final damage reduction by 10%, and recover health every 5 seconds equal to 50% |
| Snowfield Giant Beast | The cold wind of the snowfield invades the battlefield; every 2 seconds, enemies have a 35% chance to be affected by Fro |
| Rudolph | Every 7 seconds, allies gain 20% attack speed and restore 8% mana per second for 3 seconds; enemies lose 20% attack spee |
