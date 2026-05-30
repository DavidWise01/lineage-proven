"""
verify.py — Verify SHA-256 hashes of all lineage evidence files
ROOT0-LINEAGE-MANIFEST-v1.0

Usage: python verify.py
"""
import hashlib, json, sys, os

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    manifest_path = "manifest.json"
    if not os.path.exists(manifest_path):
        print("ERROR: manifest.json not found. Run from repo root.")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    evidence = manifest.get("evidence", [])
    ok = True
    print(f"\n  LINEAGE VERIFICATION — {manifest.get('format', '?')}")
    print(f"  {len(evidence)} exhibits\n")

    for e in evidence:
        path = e["canonical"]
        expected = e["sha256"]
        if not os.path.exists(path):
            print(f"  MISSING  {e['id']}  {path}")
            ok = False
            continue
        actual = sha256_file(path)
        if actual == expected:
            print(f"  OK       {e['id']}  {expected[:16]}…  {path}")
        else:
            print(f"  MISMATCH {e['id']}")
            print(f"           expected: {expected}")
            print(f"           actual:   {actual}")
            ok = False

    print()
    if ok:
        print("  RESULT: ALL EXHIBITS VERIFIED — lineage intact")
    else:
        print("  RESULT: VERIFICATION FAILED — one or more exhibits altered or missing")
    print()
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
