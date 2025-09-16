#!/usr/bin/env python3
# Alfred Script Filter: Disk Space Audit
# Usage: keyword `disk` with optional query: [path] [depth] [limit] or flags --path= --depth= --limit=
import json, os, re, shlex, subprocess, sys
from pathlib import Path

def humanize_kbytes(kbytes: int) -> str:
    units = ["KB","MB","GB","TB","PB"]
    size = float(kbytes); idx = 0
    while size >= 1024 and idx < len(units)-1:
        size /= 1024.0; idx += 1
    return f"{int(size)} {units[idx]}" if idx == 0 else f"{size:.1f} {units[idx]}"

def parse_query(q: str):
    q = q.strip()
    path = os.path.expanduser(os.environ.get("HOME","~")); depth = 1; limit = 20
    if not q: return path, depth, limit
    mpath = re.search(r"--path=([^ ]+)", q); mdepth = re.search(r"--depth=(\d+)", q); mlimit = re.search(r"--limit=(\d+)", q)
    if mpath: path = os.path.expanduser(mpath.group(1))
    if mdepth: depth = int(mdepth.group(1))
    if mlimit: limit = int(mlimit.group(1))
    parts = [p for p in shlex.split(q) if not p.startswith("--")]
    if parts: path = os.path.expanduser(parts[0])
    if len(parts) >= 2 and parts[1].isdigit(): depth = int(parts[1])
    if len(parts) >= 3 and parts[2].isdigit(): limit = int(parts[2])
    return path, depth, limit

def run_du(path: str, depth: int, limit: int):
    cmd = ["/usr/bin/du", "-k", "-x", "-d", str(depth), path]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=False)
    except Exception as e:
        return [], str(e)
    lines = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    entries = []
    for ln in lines:
        parts = ln.split("\t", 1)
        if len(parts) != 2:
            parts = ln.split(maxsplit=1)
            if len(parts) != 2: continue
        k, p = parts
        try: k = int(k)
        except: continue
        entries.append((k, p))
    entries.sort(key=lambda t: (-t[0], t[1]))
    if limit > 0: entries = entries[:limit]
    return entries, ""

def make_items(entries):
    items = []
    for k, p in entries:
        size = humanize_kbytes(k)
        name = os.path.basename(p.rstrip("/")) or p
        items.append({
            "uid": f"{p}-{k}",
            "title": f"{size} — {name}",
            "subtitle": p,
            "arg": p,
            "type": "file",
            "quicklookurl": p
        })
    return items or [ {"title":"No results", "subtitle":"Try increasing depth or changing the path", "valid": False} ]

def main():
    query = os.environ.get("query","")
    path, depth, limit = parse_query(query)
    if not os.path.exists(path):
        print(json.dumps({"items":[{"title":"Path not found","subtitle":path,"valid":False}]})); return
    entries, err = run_du(path, depth, limit)
    if err:
        print(json.dumps({"items":[{"title":"Error running du","subtitle":err,"valid":False}]})); return
    print(json.dumps({"items": make_items(entries)}))

if __name__ == "__main__":
    q_from_stdin = sys.stdin.read()
    if q_from_stdin: os.environ["query"] = q_from_stdin.strip()
    else: os.environ["query"] = " ".join(sys.argv[1:]).strip()
    main()