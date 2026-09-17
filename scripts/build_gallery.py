"""Generate gallery.html — a standalone Tailwind page showing every unit.

Icons are referenced straight out of icons/, so the page must stay next to
that folder. Data is inlined (file:// blocks fetch), art is not.
"""
import json, html
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project

IDX = json.load(open("icons/index.json"))
LOC = json.load(open("tables/_Localization_EN.json"))
UNITS = {u["UnitID"]: u for u in json.load(open("tables/TableUnitCard.json"))}
SKINS = json.load(open("tables/TableUnitSkin.json"))
CARDS = {c["SkillID"]: c for c in json.load(open("tables/TableSkillCard.json"))}
CATS = ["heroes", "pets", "monsters", "summons", "troops"]
HEROES = [dict(r, cat=c) for c in CATS for r in json.load(open(f"out/{c}.json"))]

ROLE_ID = {"Assistance": 1, "Mage": 2, "Assassin": 3, "Archer": 4,
           "Warrior": 5, "Summon": 6, "Control": 7, "Calamity": 8}
RARITY = {"SSS": "#d09a1f", "SS": "#8f5bc4", "S": "#3480c4",
          "A": "#46996b", "B": "#6b7c86", "C": "#8a847c", "D": "#8a847c"}


def icon(*names):
    for n in names:
        if n and n in IDX:
            return "icons/" + IDX[n]
    return None


def main():
    per_unit = {}
    for s in SKINS:
        per_unit.setdefault(s["UnitID"], []).extend([s["SkinHead"], s["SkinIcon"]])

    rows = []
    for h in HEROES:
        u = UNITS[h["id"]]
        skills = []
        for s in h["skills"] + h["passives"]:
            c = CARDS.get(s["id"], {})
            skills.append({
                "n": s["name"], "d": s["desc"], "k": s.get("kind", "skill"),
                "i": icon(c.get("SkillIcon"), f"Icon_Skill_{s['id']}",
                          f"Icon_Skill_{s['id'] + 10}"),
            })
        bless = [{"n": b["name"], "d": b["desc"], "q": b["quality"],
                  "i": icon(b["icon"])} for b in h.get("blessings", [])]
        if not h["name"]:
            continue
        rows.append({
            "id": h["id"], "name": h["name"], "epithet": h["unit_name"],
            "rarity": h["rarity"], "q": h["quality"], "role": h["role"],
            "race": h["race"], "cat": h["cat"], "cost": h["cost"],
            "hp": h["hp"], "atk": h["atk"], "def": h["defense"],
            "spd": h["atk_speed"], "rng": h["atk_range"],
            "por": h["icon"],
            "roleIcon": icon(f"Icon_Profession_{ROLE_ID.get(h['role'], 0)}"),
            "frame": icon(f"FormationQualityBg_{h['quality']}"),
            "skills": skills, "bless": bless,
        })

    stats = {k: icon(v) for k, v in
             {"hp": "co_icon1_HP", "atk": "co_icon1_attack",
              "def": "co_icon1_def", "spd": "co_icon1_speed"}.items()}

    page = TEMPLATE.replace("__ROWS__", json.dumps(rows, ensure_ascii=False)) \
                   .replace("__STATS__", json.dumps(stats)) \
                   .replace("__RARITY__", json.dumps(RARITY))
    open("gallery.html", "w").write(page)
    art = sum(1 for r in rows if r["por"])
    ski = sum(1 for r in rows for s in r["skills"] if s["i"])
    print(f"gallery.html: {len(rows)} units ({art} with portraits), "
          f"{ski} skill icons wired")


TEMPLATE = r"""<!doctype html>
<html lang="en" class="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Oopsie Croco — Character Gallery</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>tailwind.config = { darkMode: 'class' }</script>
</head>
<body class="bg-stone-100 dark:bg-[#0d1512] text-stone-800 dark:text-stone-200 antialiased">

<div class="max-w-7xl mx-auto px-4 py-8">
  <header class="flex flex-wrap items-end gap-4 border-b-2 border-stone-800 dark:border-stone-200 pb-4">
    <h1 class="text-3xl sm:text-4xl font-bold tracking-tight flex-1">
      Oopsie Croco <span class="text-emerald-600 dark:text-emerald-400">Character Gallery</span>
    </h1>
    <p id="tally" class="text-xs font-mono text-stone-500 dark:text-stone-400"></p>
    <button id="theme" class="text-xs font-mono px-3 py-1.5 rounded border border-stone-300 dark:border-stone-700
      hover:border-emerald-500 hover:text-emerald-600 dark:hover:text-emerald-400">Theme</button>
  </header>

  <div class="sticky top-0 z-20 flex flex-wrap gap-2 items-center py-3
              bg-stone-100 dark:bg-[#0d1512] border-b border-stone-300 dark:border-stone-800">
    <input id="q" type="search" placeholder="Search name, epithet, role, or skill…"
      class="flex-1 min-w-[190px] px-3 py-2 rounded border text-sm
             bg-white dark:bg-[#131d19] border-stone-300 dark:border-stone-700
             focus:outline-none focus:ring-2 focus:ring-emerald-500">
    <select id="role" class="px-3 py-2 rounded border text-sm bg-white dark:bg-[#131d19]
             border-stone-300 dark:border-stone-700"><option value="">All roles</option></select>
    <select id="rarity" class="px-3 py-2 rounded border text-sm bg-white dark:bg-[#131d19]
             border-stone-300 dark:border-stone-700"><option value="">All rarities</option></select>
    <select id="cat" class="px-3 py-2 rounded border text-sm bg-white dark:bg-[#131d19]
             border-stone-300 dark:border-stone-700"></select>
  </div>

  <div id="grid" class="grid gap-4 mt-5
       grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"></div>

  <p class="mt-10 pt-4 border-t border-stone-300 dark:border-stone-800 text-xs
            text-stone-500 dark:text-stone-400">
    Stats are level-1 template values and are uniform within a rarity — skills are what
    separate heroes of the same rank. The <code>Icon_Skill_*</code> art belongs to the
    <em>blessing</em> system (<code>TableBless.BlessIcon</code>), which is why most hero
    skills show a dashed placeholder: the game ships no icon for them. Entries the game
    describes but never titles are marked "Untitled effect"; per-level notes are marked
    "Level upgrade". Images load from <code>icons/</code>, so keep this file next to that folder.
  </p>
</div>

<script>
const ROWS = __ROWS__;
const STATS = __STATS__;
const RARITY = __RARITY__;
const $ = (s) => document.querySelector(s);

const CATS = ["heroes", "pets", "monsters", "summons", "troops"];
CATS.forEach(c => $("#cat").add(new Option(
  `${c[0].toUpperCase() + c.slice(1)} (${ROWS.filter(r => r.cat === c).length})`, c)));
[...new Set(ROWS.map(r => r.role))].sort().forEach(r => $("#role").add(new Option(r, r)));
["SSS","SS","S","A","B","C","D"].filter(r => ROWS.some(x => x.rarity === r))
  .forEach(r => $("#rarity").add(new Option(r, r)));

const esc = (s) => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function statCell(label, key, value, tone) {
  const ic = key && STATS[key] ? `<img src="${STATS[key]}" alt="" class="w-3 h-3">` : "";
  return `<div class="flex flex-col">
    <span class="font-mono text-sm font-semibold tabular-nums ${tone || ""}">${value}</span>
    <span class="flex items-center gap-1 text-[9px] uppercase tracking-wider
                 text-stone-500 dark:text-stone-400">${ic}${label}</span>
  </div>`;
}

function card(r) {
  const initials = r.name.replace(/[^A-Za-z ]/g, "").split(/\s+/)
    .filter(Boolean).slice(0, 2).map(w => w[0]).join("") || "?";
  const por = r.por
    ? `<img src="${r.por}" alt="${esc(r.name)}" loading="lazy"
            class="w-16 h-16 rounded object-cover bg-stone-200 dark:bg-stone-800 shrink-0">`
    : `<div class="w-16 h-16 rounded grid place-items-center text-xl font-bold text-white shrink-0"
            style="background:${RARITY[r.rarity] || "#777"}">${initials}</div>`;

  // the game titles only some entries; the rest are described but never named,
  // or are per-level upgrade notes. Label them rather than inventing a title.
  const KIND = { effect: "Untitled effect", upgrade: "Level upgrade" };
  const skills = r.skills.map(s => `
    <li class="flex gap-2.5 py-2 border-t border-stone-200 dark:border-stone-800">
      ${s.i ? `<img src="${s.i}" alt="" loading="lazy" class="w-8 h-8 rounded shrink-0">`
            : `<span class="w-8 h-8 rounded shrink-0 border border-dashed
                     border-stone-300 dark:border-stone-700" title="no icon in game data"></span>`}
      <div class="min-w-0">
        ${s.n ? `<p class="text-[13px] font-semibold leading-tight">${esc(s.n)}</p>`
              : `<p class="text-[10px] font-mono uppercase tracking-wider
                    text-stone-400 dark:text-stone-500">${KIND[s.k] || "Effect"}</p>`}
        <p class="text-[12px] text-stone-600 dark:text-stone-400 leading-snug">${esc(s.d || "—")}</p>
      </div>
    </li>`).join("");

  const BQ = { 1: "#5c6b75", 2: "#3480c4", 3: "#8f5bc4", 4: "#d09a1f", 5: "#c2661f" };
  const bless = r.bless.map(b => `
    <li class="flex gap-2.5 py-2 border-t border-stone-200 dark:border-stone-800">
      ${b.i ? `<img src="${b.i}" alt="" loading="lazy" class="w-8 h-8 rounded shrink-0
                    ring-1" style="--tw-ring-color:${BQ[b.q] || "#666"}">`
            : `<span class="w-8 h-8 rounded shrink-0 bg-stone-200 dark:bg-stone-800"></span>`}
      <div class="min-w-0">
        <p class="text-[13px] font-semibold leading-tight">${esc(b.n)}</p>
        <p class="text-[12px] text-stone-600 dark:text-stone-400 leading-snug">${esc(b.d || "—")}</p>
      </div>
    </li>`).join("");

  return `<article class="rounded-lg border border-stone-200 dark:border-stone-800
        bg-white dark:bg-[#131d19] p-4 border-l-4 shadow-sm"
        style="border-left-color:${RARITY[r.rarity] || "#777"}">
    <div class="flex gap-3">
      ${por}
      <div class="min-w-0 flex-1">
        <div class="flex items-baseline gap-2">
          <h2 class="font-bold text-lg leading-tight">${esc(r.name)}</h2>
          <span class="text-[10px] font-mono font-bold px-1.5 py-0.5 rounded text-white shrink-0"
                style="background:${RARITY[r.rarity] || "#777"}">${r.rarity}</span>
        </div>
        ${r.epithet && r.epithet !== r.name
          ? `<p class="text-xs italic text-stone-500 dark:text-stone-400">${esc(r.epithet)}</p>` : ""}
        <p class="flex items-center gap-1.5 mt-1 text-[11px] font-mono uppercase
                  text-stone-500 dark:text-stone-400">
          ${r.roleIcon ? `<img src="${r.roleIcon}" alt="" class="w-4 h-4">` : ""}
          ${[r.role, r.race, r.cost ? `cost ${r.cost}` : ""]
            .filter(v => v && v !== "-").map(esc).join(" · ") || r.cat}
        </p>
      </div>
    </div>

    <div class="grid grid-cols-4 gap-2 my-3 py-2 border-y border-stone-200 dark:border-stone-800">
      ${statCell("HP", "hp", r.hp?.toLocaleString() ?? "—", "text-emerald-600 dark:text-emerald-400")}
      ${statCell("ATK", "atk", r.atk ?? "—", "text-orange-600 dark:text-orange-400")}
      ${statCell("DEF", "def", r.def ?? "—")}
      ${statCell("Range", null, r.rng ?? "—")}
    </div>

    ${r.skills.length ? `<details>
      <summary class="cursor-pointer text-[11px] font-mono uppercase tracking-wider
                      text-stone-500 dark:text-stone-400 hover:text-emerald-600
                      dark:hover:text-emerald-400">${r.skills.length} skills</summary>
      <ul class="mt-1">${skills}</ul>
    </details>` : `<p class="text-[11px] font-mono text-stone-400">no skills</p>`}
    ${r.bless.length ? `<details class="mt-1">
      <summary class="cursor-pointer text-[11px] font-mono uppercase tracking-wider
                      text-stone-500 dark:text-stone-400 hover:text-emerald-600
                      dark:hover:text-emerald-400">${r.bless.length} blessings</summary>
      <ul class="mt-1">${bless}</ul>
    </details>` : ""}
  </article>`;
}

function render() {
  const q = $("#q").value.trim().toLowerCase();
  const role = $("#role").value, rar = $("#rarity").value, cat = $("#cat").value;
  const list = ROWS.filter(r =>
    r.cat === cat && (!role || r.role === role) && (!rar || r.rarity === rar) &&
    (!q || [r.name, r.epithet, r.role, r.race, ...r.skills.map(s => s.n + " " + s.d)]
      .concat(r.bless.map(b => b.n + " " + b.d)).join(" ").toLowerCase().includes(q)));
  list.sort((a, b) => b.q - a.q || a.name.localeCompare(b.name));
  $("#grid").innerHTML = list.map(card).join("") ||
    `<p class="col-span-full py-16 text-center text-stone-500">Nothing matches that filter.</p>`;
  $("#tally").textContent =
    `${list.length} shown · ${ROWS.length} units total · ${ROWS.filter(r => r.por).length} with art`;
}

["#q", "#role", "#rarity", "#cat"].forEach(s => {
  $(s).addEventListener(s === "#q" ? "input" : "change", render);
});
$("#theme").onclick = () => document.documentElement.classList.toggle("dark");
render();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
