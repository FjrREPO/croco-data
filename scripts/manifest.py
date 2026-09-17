"""Parse a YooAsset 1.4.x binary PackageManifest."""
import struct


class R:
    def __init__(self, b):
        self.b, self.i = b, 0

    def u8(self):
        v = self.b[self.i]; self.i += 1; return v

    def u16(self):
        v = struct.unpack_from("<H", self.b, self.i)[0]; self.i += 2; return v

    def i32(self):
        v = struct.unpack_from("<i", self.b, self.i)[0]; self.i += 4; return v

    def i64(self):
        v = struct.unpack_from("<q", self.b, self.i)[0]; self.i += 8; return v

    def s(self):
        n = self.u16()
        v = self.b[self.i:self.i + n].decode("utf-8", "replace"); self.i += n; return v

    def sarr(self):
        return [self.s() for _ in range(self.u16())]

    def i32arr(self):
        return [self.i32() for _ in range(self.u16())]


def load(path):
    r = R(open(path, "rb").read())
    sign = r.i32()
    ver = r.s()
    head = dict(sign=sign, manifest_version=ver)
    head["enable_addressable"] = bool(r.u8())
    head["location_to_lower"] = bool(r.u8())
    head["include_guid"] = bool(r.u8())
    head["output_name_style"] = r.i32()
    head["package_name"] = r.s()
    head["package_version"] = r.s()

    assets = []
    for _ in range(r.i32()):
        a = dict(address=r.s(), path=r.s(), guid=r.s(), tags=r.sarr(),
                 bundle=r.i32(), deps=r.i32arr())
        assets.append(a)

    bundles = []
    for _ in range(r.i32()):
        b = dict(name=r.s(), hash=r.s(), crc=r.s(), size=r.i64(),
                 raw=bool(r.u8()), load=r.u8(), tags=r.sarr(), deps=r.i32arr())
        bundles.append(b)
    return head, assets, bundles


if __name__ == "__main__":
    import sys
    head, assets, bundles = load(sys.argv[1])
    print(head)
    print(f"assets={len(assets)} bundles={len(bundles)}")
    print("sample asset:", assets[0])
    print("sample bundle:", bundles[0])
