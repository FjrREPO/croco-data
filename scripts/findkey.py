"""Recover the 15-byte keystream this game XORs into every 500th file byte."""
import glob, bundle
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # semua path relatif ke root project
from repair import produced

PERIOD = 15
STRIDE = 500
KEY = {0: 0xED, 1: 0x35, 2: 0xC9, 3: 0x4D, 5: 0xDA, 9: 0x63, 10: 0xE6}


def apply_known(src, start, key):
    """XOR back the bytes whose key index is known; return unknown key indices."""
    src = bytearray(src)
    unknown = []
    for q in range(start, start + len(src)):
        if q % STRIDE:
            continue
        k = (q // STRIDE) % PERIOD
        if k in key:
            src[q - start] ^= key[k]
        else:
            unknown.append((q - start, k))
    return src, unknown


def sweep(paths, key):
    """One bootstrap pass: solve blocks that have a single unknown key index."""
    votes = {}
    for p in paths:
        try:
            info = bundle.parse(p)
        except Exception:
            continue
        buf, o = info["buf"], info["data_start"]
        for u, c, f in info["blocks"]:
            start = o; o += c
            if (f & 0x3F) == 0:
                continue
            src, unk = apply_known(buf[start:start + c], start, key)
            if len(unk) != 1:
                continue
            pos, kidx = unk[0]
            if kidx in key:
                continue
            orig = src[pos]
            good = [v for v in range(256)
                    if (src.__setitem__(pos, v), produced(src, u, b"") == u)[1]]
            src[pos] = orig
            if len(good) == 1:
                votes.setdefault(kidx, {}).setdefault(orig ^ good[0], 0)
                votes[kidx][orig ^ good[0]] += 1
    return votes


if __name__ == "__main__":
    paths = sorted(glob.glob("raw/builtin/assets/BuildinFiles/*.bundle"))
    key = dict(KEY)
    for rnd in range(6):
        missing = [j for j in range(PERIOD) if j not in key]
        if not missing:
            break
        print(f"round {rnd}: missing {missing}")
        votes = sweep(paths, key)
        if not votes:
            print("  no new evidence"); break
        for kidx, tally in sorted(votes.items()):
            best = max(tally.items(), key=lambda kv: kv[1])
            print(f"  key[{kidx}] = 0x{best[0]:02x}  (votes {tally})")
            key[kidx] = best[0]
    print("\nKEY =", [hex(key.get(j, 0)) for j in range(PERIOD)])
