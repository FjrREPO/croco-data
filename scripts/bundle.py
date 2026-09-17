"""Read Oopsie Croco's obfuscated YooAsset/UnityFS bundles.

Obfuscation: every 500th byte of the file is XORed with a 15-byte keystream,
indexed by (file_offset / 500) % 15. Undo that and the file is a stock
UnityFS bundle. (Offset 0 is included, which is why these files start with
0xB8 instead of 'U'.)
"""
import struct, lz4.block

KEY = bytes([0xED, 0x35, 0xC9, 0x4D, 0x50, 0xDA, 0x6B, 0xD0,
             0x08, 0x63, 0xE6, 0x74, 0xB8, 0x8F, 0xB7])
STRIDE = 500


def decrypt(data):
    b = bytearray(data)
    for i in range(0, len(b), STRIDE):
        b[i] ^= KEY[(i // STRIDE) % len(KEY)]
    return bytes(b)


def parse(path):
    buf = decrypt(open(path, "rb").read())
    if buf[:7] != b"UnityFS":
        raise ValueError("not a UnityFS bundle")
    size, ci, ui, flags = struct.unpack_from(">qiii", buf, 30)
    p = 50
    if flags & 0x200:                       # block info padded to 16 bytes
        p += (16 - p % 16) % 16
    bi = buf[p:p + ci]
    if flags & 0x3F:
        bi = lz4.block.decompress(bi, uncompressed_size=ui)
    q = 16                                   # skip uncompressed-data hash
    nb = struct.unpack_from(">i", bi, q)[0]; q += 4
    blocks = []
    for _ in range(nb):
        u, c, f = struct.unpack_from(">iiH", bi, q); q += 10
        blocks.append((u, c, f))
    nn = struct.unpack_from(">i", bi, q)[0]; q += 4
    nodes = []
    for _ in range(nn):
        off, sz, nf = struct.unpack_from(">qqI", bi, q); q += 20
        e = bi.index(b"\0", q)
        nodes.append((bi[q:e].decode(), off, sz)); q = e + 1
    start = p + ci
    start += (16 - start % 16) % 16
    return dict(buf=buf, blocks=blocks, nodes=nodes, data_start=start, flags=flags)


def decompress(info):
    buf, off = info["buf"], info["data_start"]
    parts = []
    for u, c, f in info["blocks"]:
        chunk = buf[off:off + c]; off += c
        parts.append(chunk if (f & 0x3F) == 0
                     else lz4.block.decompress(chunk, uncompressed_size=u))
    return b"".join(parts)


def nodes_of(path):
    """-> [(name, bytes)] for every file packed inside the bundle."""
    info = parse(path)
    raw = decompress(info)
    return [(n, raw[o:o + s]) for n, o, s in info["nodes"]]
