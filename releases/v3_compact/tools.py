import json, zipfile, os
from datetime import datetime

def export_memory(files, name=None):
    name = name or f'backup_{datetime.utcnow().isoformat()}.zip'
    with zipfile.ZipFile(name,'w') as z:
        for f in files:
            if os.path.exists(f): z.write(f)
    return name
