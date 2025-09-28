
# Build DIST_MANIFEST.json with hashes and zip
import hashlib, json, os, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)
manifest = {}
for p in ROOT.rglob('*'):
    if p.is_file() and "dist" not in p.parts:
        h=hashlib.sha256(p.read_bytes()).hexdigest()
        manifest[str(p.relative_to(ROOT))]=h
(ROOT/"DIST_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
with zipfile.ZipFile(DIST/'nia_full_v3.zip','w', zipfile.ZIP_DEFLATED) as z:
    for rel in manifest.keys():
        z.write(ROOT/rel, arcname=rel)
print("Built dist/nia_full_v3.zip")
