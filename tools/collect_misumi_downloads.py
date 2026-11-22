"""Collect manually downloaded MISUMI STEP files into AI concept design/standard_parts/.

Usage:
  python collect_misumi_downloads.py list [--open]     show what still has to be downloaded (--open opens the MISUMI search pages)
  python collect_misumi_downloads.py collect [--hours 24]   copy, unzip and rename the downloads to the BOM file names
  python collect_misumi_downloads.py selftest

Reads the Standard rows of BOM.xlsx (Part_Number, CAD_File_Expected). A download belongs to a part when its
file name (or, for a zip, a STEP file inside it) contains the part number. Only files in the top level of the
downloads folder changed in the last --hours are looked at. Downloads are copied, never moved or deleted.
"""
import argparse
import os
import re
import sys
import tempfile
import time
import webbrowser
import zipfile

import openpyxl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "AI concept design")
STEP_EXT = (".step", ".stp")
MODEL_EXT = STEP_EXT + (".sldprt",)  # MISUMI also offers SolidWorks format, which needs no conversion
# shortcut: keyword search URL of the Malaysian MISUMI site, not confirmed; upgrade if MISUMI changes it
SEARCH_URL = "https://my.misumi-ec.com/vona2/result/?Keyword={}"


def bom_parts(bom_path):
    ws = openpyxl.load_workbook(bom_path, read_only=True).active
    rows = ws.iter_rows(values_only=True)
    head = next(rows)
    col = {name: head.index(name) for name in ("Part_Number", "Type", "CAD_File_Expected")}
    parts = []
    for row in rows:
        if row[col["Type"]] != "Standard" or not row[col["CAD_File_Expected"]]:
            continue
        pn = str(row[col["Part_Number"]]).strip()
        target = os.path.normpath(os.path.join(os.path.dirname(bom_path), str(row[col["CAD_File_Expected"]])))
        parts.append((pn, target))
    return parts


def converted(target):
    base = os.path.splitext(target)[0]
    return any(os.path.isfile(base + ext) for ext in (".SLDPRT", ".SLDASM"))


def matches(pn, name):
    # part number as a whole token: CB5-40 must not match CB5-400 or XCB5-40; '-' may come as '_' or ' '
    body = r"[-_ ]?".join(re.escape(piece) for piece in re.split(r"[-_ ]", pn))
    return re.search(r"(?<![A-Za-z0-9])" + body + r"(?![0-9])", name, re.IGNORECASE) is not None


def model_file(path, pn):
    """(bytes, ".STEP" or ".SLDPRT") for part pn from a downloaded model file or .zip, or (None, None)."""
    name = os.path.basename(path)
    if name.lower().endswith(MODEL_EXT):
        if not matches(pn, name):
            return None, None
        with open(path, "rb") as f:
            return f.read(), kind(name)
    with zipfile.ZipFile(path) as zf:
        models = [m for m in zf.namelist() if m.lower().endswith(MODEL_EXT)]
        hits = [m for m in models if matches(pn, os.path.basename(m))]
        if not hits and len(models) == 1 and matches(pn, name):
            hits = models  # zip named after the part holding one model with a generic name
        # read bytes only: nothing is extracted, so paths inside the zip cannot escape the target
        return (zf.read(hits[0]), kind(hits[0])) if len(hits) == 1 else (None, None)


def kind(name):
    return ".SLDPRT" if name.lower().endswith(".sldprt") else ".STEP"


def recent_downloads(folder, hours):
    since = time.time() - hours * 3600
    files = [e for e in os.scandir(folder)
             if e.is_file() and e.name.lower().endswith(MODEL_EXT + (".zip",)) and e.stat().st_mtime >= since]
    return [e.path for e in sorted(files, key=lambda e: e.stat().st_mtime, reverse=True)]


def collect(parts, downloads):
    used, report = set(), []
    for pn, target in parts:
        if "UNCONFIRMED" in pn.upper():
            report.append(("SKIP", pn, "part number unconfirmed in the BOM - model it or download by hand"))
        elif os.path.isfile(target) or converted(target):
            report.append(("EXISTS", pn, target))
        else:
            for path in downloads:  # newest first
                try:
                    data, ext = model_file(path, pn)
                except zipfile.BadZipFile:
                    continue
                if data:
                    if ext == ".STEP" and not data.lstrip().startswith(b"ISO-10303-21"):
                        report.append(("FAIL", pn, f"{os.path.basename(path)} is not a STEP file"))
                        break
                    out = os.path.splitext(target)[0] + ext
                    with open(out, "wb") as f:
                        f.write(data)
                    used.add(path)
                    report.append(("OK", pn, out))
                    break
            else:
                report.append(("MISSING", pn, "no download found with this part number in its name"))
    unmatched = [p for p in downloads if p not in used]
    return report, unmatched


def selftest():
    assert matches("CB5-40", "CB5-40.stp") and matches("CB5-40", "misumi_cb5_40_STEP.zip")
    assert not matches("CB5-40", "CB5-400.stp") and not matches("LBNR6", "SLBNR6.stp")
    with tempfile.TemporaryDirectory() as tmp:
        step = b"ISO-10303-21;\nHEADER;"
        z = os.path.join(tmp, "WL12-55.zip")
        with zipfile.ZipFile(z, "w") as zf:
            zf.writestr("model/part.stp", step)
        target = os.path.join(tmp, "PusherClampSpring_WL12-55.STEP")
        z2 = os.path.join(tmp, "CB5-40_SOLIDWORKS.zip")
        with zipfile.ZipFile(z2, "w") as zf:
            zf.writestr("CB5-40.SLDPRT", b"sw")
        report, unmatched = collect([("WL12-55", target), ("MPBZ8-12", os.path.join(tmp, "x.STEP")),
                                     ("UNCONFIRMED (ISO 7093)", os.path.join(tmp, "y.STEP")),
                                     ("CB5-40", os.path.join(tmp, "Screw_CB5-40.STEP"))], [z, z2])
        assert [r[0] for r in report] == ["OK", "MISSING", "SKIP", "OK"] and unmatched == []
        assert report[3][2].endswith("Screw_CB5-40.SLDPRT")
        with open(target, "rb") as f:
            assert f.read() == step
    print("selftest OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=("list", "collect", "selftest"))
    ap.add_argument("--bom", default=os.path.join(ROOT, "BOM.xlsx"))
    ap.add_argument("--downloads", default=r"D:\Download")
    ap.add_argument("--hours", type=float, default=24)
    ap.add_argument("--open", action="store_true", help="list: open each MISUMI search page in the browser")
    args = ap.parse_args()
    if args.action == "selftest":
        return selftest()

    parts = bom_parts(os.path.abspath(args.bom))
    if args.action == "list":
        for pn, target in parts:
            done = os.path.isfile(target) or converted(target)
            state = "DONE" if done else "SKIP" if "UNCONFIRMED" in pn.upper() else "TODO"
            print(f"{state:8}{pn:20}  {SEARCH_URL.format(pn) if state == 'TODO' else os.path.basename(target)}")
            if args.open and state == "TODO":
                webbrowser.open(SEARCH_URL.format(pn))
        return

    report, unmatched = collect(parts, recent_downloads(args.downloads, args.hours))
    for state, pn, detail in report:
        print(f"{state:8}{pn:20}  {detail}")
    for path in unmatched:
        print(f"UNUSED  {'':20}{path}")
    sys.exit(1 if any(r[0] in ("MISSING", "FAIL") for r in report) else 0)


if __name__ == "__main__":
    main()
