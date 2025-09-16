#!/usr/bin/env python3
import csv, os, re, shlex, subprocess, sys, time
def humanize_kbytes(kbytes: int) -> str:
    units = ["KB","MB","GB","TB","PB"]; size=float(kbytes); idx=0
    while size>=1024 and idx<len(units)-1: size/=1024.0; idx+=1
    return f"{int(size)} {units[idx]}" if idx==0 else f"{size:.1f} {units[idx]}"
def parse_query(q: str):
    import os
    path=os.path.expanduser(os.environ.get("HOME","~")); depth=1; limit=20; q=q.strip()
    if not q: return path,depth,limit
    import re, shlex
    mpath=re.search(r"--path=([^ ]+)",q); mdepth=re.search(r"--depth=(\d+)",q); mlimit=re.search(r"--limit=(\d+)",q)
    if mpath: path=os.path.expanduser(mpath.group(1))
    if mdepth: depth=int(mdepth.group(1))
    if mlimit: limit=int(mlimit.group(1))
    parts=[p for p in shlex.split(q) if not p.startswith("--")]
    if parts: path=os.path.expanduser(parts[0])
    if len(parts)>=2 and parts[1].isdigit(): depth=int(parts[1])
    if len(parts)>=3 and parts[2].isdigit(): limit=int(parts[2])
    return path,depth,limit
def run_du(path, depth, limit):
    proc=subprocess.run(["/usr/bin/du","-k","-x","-d",str(depth),path], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=False)
    lines=[ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    entries=[]
    for ln in lines:
        parts=ln.split("\t",1)
        if len(parts)!=2:
            parts=ln.split(maxsplit=1)
            if len(parts)!=2: continue
        k,p=parts
        try: k=int(k)
        except: continue
        entries.append((k,p))
    entries.sort(key=lambda t:(-t[0],t[1]))
    return entries[:limit] if limit>0 else entries
def main():
    q=os.environ.get("query","").strip()
    if not q and len(sys.argv)>1: q=" ".join(sys.argv[1:]).strip()
    path,depth,limit=parse_query(q)
    if not os.path.exists(path):
        print("Path not found:",path,file=sys.stderr); sys.exit(1)
    rows=run_du(path,depth,limit)
    ts=time.strftime("%Y%m%d-%H%M%S")
    downloads=os.path.expanduser("~/Downloads"); os.makedirs(downloads, exist_ok=True)
    outpath=os.path.join(downloads,f"Disk-Audit-{ts}.csv")
    with open(outpath,"w",newline="") as f:
        w=csv.writer(f); w.writerow(["size_kb","size_human","path"])
        for k,p in rows: w.writerow([k,humanize_kbytes(k),p])
    print(outpath)
    try: subprocess.run(["/usr/bin/open","-a","Microsoft Excel",outpath],check=False)
    except Exception: subprocess.run(["/usr/bin/open",outpath],check=False)
if __name__=="__main__":
    data=sys.stdin.read().strip()
    if data: os.environ["query"]=data
    main()