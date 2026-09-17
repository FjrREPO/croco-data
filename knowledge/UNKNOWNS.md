# Yang TIDAK dijawab data ini

Daftar ini sama pentingnya dengan korpusnya. Setiap baris di sini adalah tempat sebuah chatbot
akan mulai menebak kalau tidak diberi tahu bahwa datanya memang tidak ada.

## Tidak ada di dump sama sekali

| Pertanyaan | Kenapa tidak bisa dijawab |
|---|---|
| "Bond nambah berapa persen?" | Bond memberi skill (`AEIDs` → `SkillIDs`), bukan bonus stat — `AttrIDs` kosong. Skill-skill itu tidak punya teks di lokalisasi, jadi besarannya tidak terbaca. |
| "Hero mana yang win rate-nya tertinggi?" | Tidak ada win rate, log tempur, atau data pemain di dump. Semua urutan tier adalah pembacaan teks skill. |
| "Chapter 150 lawan apa?" | `TableLevel` berhenti di ChapterID 9071. Dari 1.000 baris `TableChapter`, 928 tidak punya satu level pun. Story yang terdefinisi cuma Tutorial + Ch 1–71. |
| "Damage hero A vs hero B berapa?" | Stat dasar level 1 seragam per rarity (semua UR 7200/480/240, semua SP 5400/360/180). Angka itu tidak membedakan hero dalam rarity yang sama. |
| "Skill ini naik berapa per level?" | Hanya level unlock yang tercatat (Lv12/15/20/25). Skala per level tidak ada di tabel yang dibaca. |

## Ada tapi tidak bisa ditafsirkan

| Hal | Masalahnya |
|---|---|
| Rentang atribut resist 6-digit (`400002`, `400003`, …) | 14 unit memakainya, tapi `Attribute_400002` dan kawan-kawannya **tidak ada di lokalisasi**. Tandanya berlawanan dengan rentang 5-digit yang terverifikasi, jadi unit-unit ini sengaja dilewatkan daripada ditebak. |
| Angka HP Guild Boss (150 → 1775) | Satuannya tidak jelas — kemungkinan pengali, bukan HP mentah. |
| Efek unik mount | Teksnya ada, tapi tidak ada angka pembanding antar mount selain stat yang memang identik. |

## Batas metode, bukan batas data

| Hal | Batasnya |
|---|---|
| Urutan tier per mode | Dihitung dari frekuensi kata di teks skill. Hero yang kuat lewat satu angka besar bisa kalah peringkat dari hero yang menyebut "shield" belasan kali. |
| **Bounty Hunter kemungkinan dinilai terlalu rendah** | Panduan komunitas menempatkannya di core team. Kekuatannya di DPS single-target berkelanjutan lewat tumpukan Ammunition, dan metode frekuensi kata tidak menangkap itu. Kalau penilaian di korpus berbeda dari panduan komunitas, **ikuti panduan komunitas**. |
| Susunan bond untuk 6–8 slot | Perpanjangan logis dari `RequiredCount: 2`, bukan sesuatu yang diuji. |
| Batas segmen spender | F2P/low/mid/sultan/whale adalah konvensi komunitas, bukan kategori di dalam game. Yang berasal dari data hanya peluang gacha yang mendasarinya. |

## Versi

Dump: **Oopsie Croco v1.8.6, diambil 2026-07-28**. Kalau pemain melaporkan hero, chapter, atau
mekanik yang tidak ada di sini, kemungkinan besar game-nya sudah di-patch dan dump perlu diambil
ulang — bukan pemainnya yang salah ingat.
