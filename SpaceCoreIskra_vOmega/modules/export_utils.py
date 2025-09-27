import json, zipfile, os
def export_md(entries,path):
    with open(path,"w",encoding="utf-8") as f:
        for e in entries: f.write(e.get("answer","") + "\\n\\n")
def zip_files(files,zipname):
    with zipfile.ZipFile(zipname,"w",zipfile.ZIP_DEFLATED) as z:
        for f in files:
            if os.path.exists(f): z.write(f, arcname=os.path.basename(f))
