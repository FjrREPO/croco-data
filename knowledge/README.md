# knowledge/ — korpus untuk chatbot Oopsie Croco

Semua yang dibutuhkan chatbot di gamegw.xyz, dibangun dari tabel game sendiri
(dump APK v1.8.6, data 2026-07-28).

## Isi folder

| File | Untuk apa |
|---|---|
| `knowledge.jsonl` | **Korpus retrieval — ini yang di-embed.** 112 chunk, satu per baris. |
| `SYSTEM-PROMPT.md` | System prompt siap tempel, termasuk aturan anti-halusinasi. |
| `UNKNOWNS.md` | Yang **tidak** dijawab data ini. Baca sebelum menyalahkan bot yang menolak menjawab. |
| `TIERLIST.md` | Panduan tier & lineup versi manusia. |
| `ENCOUNTERS.md` | Resistensi kelas + lineup per encounter (story, co-op, dungeon, bos, endless). |
| `SUBSTITUSI.md` | "Tidak punya X, pakai siapa" untuk ke-34 hero. |

Regenerasi: `python scripts/build_knowledge.py` dari root project (ENCOUNTERS/SUBSTITUSI dari `build_encounters.py` / `build_subs.py`).

## Bentuk satu chunk

```json
{
  "id": "hero:150401",
  "game": "croco",
  "type": "hero",
  "title": "Artemis — Goddess of the Hunt",
  "text": "Artemis, dikenal juga sebagai \"Goddess of the Hunt\", hero UR kelas Archer…",
  "confidence": "fact",
  "source": "Oopsie Croco v1.8.6, dump APK 2026-07-28",
  "hero": "Artemis",
  "epithet": "Goddess of the Hunt",
  "profession": "Archer",
  "rarity": "UR",
  "aliases": ["Artemis", "Goddess of the Hunt"]
}
```

**`confidence` adalah field terpenting.** 104 chunk berlabel `fact` (dibaca dari tabel) dan 8
berlabel `inference` (tier list dan saran lineup). System prompt mewajibkan bot menandai mana yang
penilaian — supaya pemain tidak memperlakukan tebakan sebagai angka resmi.

## Sebaran chunk

| Tipe | Jumlah | Isi |
|---|---|---|
| `hero` | 34 | Satu per hero playable: stat, skill, level unlock, blessing, pengganti sekelas |
| `pet` | 38 | Efek tiap pet |
| `class` | 8 | Tangga profesi, bond, musuh yang lemah/kuat terhadapnya |
| `mount` | 8 | Efek unik tiap mount |
| `mech` | 8 | Bond, slot, resist, blessing, level unlock, buff co-op, roster, mekanik langka |
| `mode` | 7 | Aturan tiap mode |
| `segment` | 6 | Rencana per segmen spender + cara menentukan segmen |
| `gacha` | 1 | Peluang tarikan dan pity |
| `opinion` | 2 | Tier list dan aturan lineup — keduanya `inference` |

Tiap chunk **berdiri sendiri**: chunk hero sudah memuat daftar penggantinya, jadi pertanyaan
"kalau tidak punya Artemis pakai siapa" terjawab dari satu hasil retrieval saja.

## Cara memakai

Project ini sudah memakai OpenAI (`scripts/translate.ts`, `scripts/build-glossary.ts`), jadi
contoh di bawah mengikutinya.

**1. Embed sekali, simpan vektornya.**

```ts
const chunks = (await readFile("knowledge/knowledge.jsonl", "utf8"))
  .trim().split("\n").map((l) => JSON.parse(l));

// Embed `title` + `text` bersama: judul memuat nama dan julukan hero,
// dan pemain mencari dengan dua-duanya.
const input = chunks.map((c) => `${c.title}\n${c.text}`);
```

112 chunk berukuran rata-rata 960 karakter — cukup kecil untuk disimpan di mana saja, termasuk
sebagai kolom JSON di Turso.

**2. Saat menjawab, ambil 5–8 chunk teratas** dan sisipkan ke `{{RETRIEVED_CHUNKS}}` di
`SYSTEM-PROMPT.md`. Sertakan `confidence` tiap chunk di teks yang disisipkan — prompt-nya
bergantung pada itu.

**3. Filter dengan metadata kalau pertanyaannya jelas sasarannya.** `type: "segment"` untuk
pertanyaan rencana, `profession` untuk pertanyaan kelas, `rarity` untuk "hero UR apa saja".

## Tanpa retrieval

Seluruh korpus sekitar 110 ribu karakter (~30 ribu token). Muat sekali jalan di context window
model modern, jadi untuk versi pertama kamu bisa melewatkan embedding dan menempelkan semuanya.
Retrieval baru berguna kalau game kedua ikut ditambahkan.
