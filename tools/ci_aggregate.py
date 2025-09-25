#!/usr/bin/env python3
import os, sys, json, subprocess
VALIDATOR=os.path.join(os.path.dirname(__file__),"validate_journal_enhanced.py")
PROJECTS=["SpaceCoreIskra_vΩ","GrokCoreIskra_vΓ","GeminiResonanceCore","Aethelgard-vΩ","Kimi-Ω-Echo","IskraNexus-v1"]
def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    return p.returncode,p.stdout
def main():
    root=os.getcwd(); report={"root":root,"projects":[]}; fail=False
    for name in PROJECTS:
        pj={"name":name}; j=os.path.join(root,name,"JOURNAL.jsonl"); s=os.path.join(root,name,"SHADOW_JOURNAL.jsonl")
        if not os.path.exists(j): pj["status"]="SKIP"; pj["reason"]="no JOURNAL.jsonl"
        else:
            cmd=[sys.executable,VALIDATOR,j]; 
            if os.path.exists(s): cmd+=["--shadow",s]
            code,out=run(cmd); pj["status"]="OK" if code==0 else "FAIL"; pj["output"]=out.strip(); fail|=(code!=0)
        report["projects"].append(pj)
    print(json.dumps(report,ensure_ascii=False,indent=2)); sys.exit(1 if fail else 0)
if __name__=="__main__": main()
