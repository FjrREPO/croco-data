"""Decompress one of the game's bundles into the files packed inside it."""
import sys, os
import bundle

if __name__ == "__main__":
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "extract"
    os.makedirs(out, exist_ok=True)
    for name, data in bundle.nodes_of(src):
        path = os.path.join(out, name)
        open(path, "wb").write(data)
        print("wrote", path, len(data))
