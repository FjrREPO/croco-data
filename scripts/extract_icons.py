"""Export every icon/sprite the game ships, keeping the asset folder layout.

Covers hero portraits, skill icons, and all UI metadata art (rarity frames,
role badges, stat icons, currencies, ...). Sprites packed inside atlases are
written out individually too, so names line up with the table fields
(TableUnitCard.HeadIcon, TableSkillCard.SkillIcon, ...).
"""
import json, os, sys, collections
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project
import UnityPy
import bundle
from manifest import load

MANIFEST = "raw/builtin/assets/BuildinFiles/PackageManifest_GameData_2026_07_28_17_44_19.bytes"
BUNDLE_DIR = "raw/builtin/assets/BuildinFiles"
OUT = "icons"
# asset folders worth rasterising; everything else is 3D/FX/audio noise
KEEP = ("/Icons/", "/SpriteAssets/", "/TmpAtlas/", "/UI/")


def main(out=OUT, roots=KEEP):
    head, assets, bundles = load(MANIFEST)

    # bundle hash -> folder to write its sprites into
    targets = {}
    for a in assets:
        if not any(r in a["path"] for r in roots):
            continue
        h = bundles[a["bundle"]]["hash"]
        sub = os.path.dirname(a["path"]).replace("Assets/GameData/", "")
        targets.setdefault(h, collections.Counter())[sub] += 1

    index, skipped = {}, 0
    for i, (h, subs) in enumerate(sorted(targets.items()), 1):
        path = os.path.join(BUNDLE_DIR, h + ".bundle")
        if not os.path.exists(path):
            continue
        sub = subs.most_common(1)[0][0]          # dominant folder for this bundle
        dest = os.path.join(out, sub)
        os.makedirs(dest, exist_ok=True)
        tmp = "/tmp/_icons.bundle"
        try:
            open(tmp, "wb").write(bundle.decrypt(open(path, "rb").read()))
            env = UnityPy.load(tmp)
        except Exception:
            skipped += 1
            continue
        for o in env.objects:
            if o.type.name not in ("Sprite", "Texture2D"):
                continue
            try:
                d = o.read()
                img = d.image
            except Exception:
                continue
            if not d.m_Name or img.width < 4 or img.height < 4:
                continue
            f = os.path.join(dest, d.m_Name + ".png")
            if os.path.exists(f) and o.type.name == "Texture2D":
                continue                          # prefer the Sprite crop
            img.save(f)
            index[d.m_Name] = os.path.relpath(f, out)
        if i % 100 == 0:
            print(f"  {i}/{len(targets)} bundles, {len(index)} images", file=sys.stderr)

    json.dump(index, open(os.path.join(out, "index.json"), "w"), indent=1)
    print(f"{len(index)} images -> {out}/  ({skipped} bundles skipped)")
    return index


if __name__ == "__main__":
    main(*sys.argv[1:])
