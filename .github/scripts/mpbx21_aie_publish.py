#!/usr/bin/env python3
"""Promote the due AIE scheduled guide into /guides/ and append sitemap.xml.
No LLM. Safe to run repeatedly (add-only)."""
from __future__ import annotations
import os, subprocess, sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SRC = Path("scheduled/guides/ml-system-design-interview-strategies/index.html")
DST = Path("guides/ml-system-design-interview-strategies/index.html")
LOC = "https://aie.valenx.org/guides/ml-system-design-interview-strategies/"
DUE = "2026-11-28"
SM = Path("sitemap.xml")

def today() -> str:
    override = os.environ.get("MPBX21_TODAY") or os.environ.get("INPUT_TODAY") or ""
    if override.strip():
        return override.strip()
    return str(datetime.now(ZoneInfo("America/Los_Angeles")).date())

def main() -> int:
    day = today()
    if not SRC.exists():
        print("nothing scheduled"); return 0
    if day < DUE:
        print(f"not due ({day} < {DUE})"); return 0
    if DST.exists():
        print("already public"); return 0
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_bytes(SRC.read_bytes())
    t = SM.read_text(encoding="utf-8")
    if LOC not in t:
        i = t.rfind("</urlset>")
        if i < 0:
            print("sitemap missing </urlset>", file=sys.stderr); return 2
        SM.write_text(t[:i] + f"  <url><loc>{LOC}</loc><lastmod>{DUE}</lastmod></url>\n" + t[i:], encoding="utf-8")
    subprocess.check_call(["git", "config", "user.name", "mpbx21-scheduler"])
    subprocess.check_call(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])
    subprocess.check_call(["git", "add", str(DST), str(SM)])
    subprocess.check_call(["git", "commit", "-m", f"publish AIE guide ml-system-design-interview-strategies (publishDate {DUE})"])
    subprocess.check_call(["git", "push"])
    print("published", LOC)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
