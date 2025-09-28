
import json, subprocess, sys, os
if not os.path.exists('DIST_MANIFEST.json'):
    print('no DIST_MANIFEST.json — run tools/pack_release.py first'); sys.exit(2)
manifest = json.loads(open('DIST_MANIFEST.json','r',encoding='utf-8').read())
missing=[p for p in manifest if not os.path.exists(p)]
if missing:
    print('Missing files:', missing); sys.exit(2)
ret = subprocess.call(['python','validators/validate_journal_enhanced.py'])
sys.exit(ret)
