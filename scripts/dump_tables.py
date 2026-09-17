"""Dump every Table* ScriptableObject from the game's tables bundle to JSON."""
import os, json, sys
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project
import UnityPy
import bundle

BUNDLE = "raw/builtin/assets/BuildinFiles/ddac25f022ec94586c4cded4572eacc3.bundle"
OUT = "tables"


def main(src=BUNDLE, out=OUT):
    os.makedirs(out, exist_ok=True)
    tmp = "/tmp/_tables_decrypted.bundle"
    open(tmp, "wb").write(bundle.decrypt(open(src, "rb").read()))
    env = UnityPy.load(tmp)
    n = 0
    for o in env.objects:
        if o.type.name != "MonoBehaviour":
            continue
        try:
            d = o.read_typetree()
        except Exception as e:
            print("  skip:", e); continue
        name = d.get("m_Name")
        if not name:
            continue
        rows = d.get("mDataList", d)
        json.dump(rows, open(os.path.join(out, name + ".json"), "w"),
                  ensure_ascii=False, indent=1)
        n += 1
        if isinstance(rows, list):
            print(f"{name}: {len(rows)} rows")
    print("wrote", n, "tables to", out)


if __name__ == "__main__":
    main(*sys.argv[1:])
