"""Convert vendor STEP files to SolidWorks files (the SolidWorks MCP cannot open STEP).

Usage: python convert_step_to_sldprt.py <file.step> [more.step ...]
SolidWorks must be running. The result is saved next to the STEP file with the same name.
A STEP file that already has a .SLDPRT/.SLDASM next to it is left alone (prints EXISTS).
"""
import os
import sys
import types

import pythoncom
import win32com.client

SW_DOC_ASSEMBLY = 2
SAVE_SILENT = 1


def _call(obj, name, *args):
    # late-bound COM exposes some no-argument methods as plain properties
    member = getattr(obj, name)
    return member(*args) if isinstance(member, types.MethodType) else member


def convert(sw, step_path):
    step_path = os.path.abspath(step_path)
    if not os.path.isfile(step_path):
        raise FileNotFoundError(step_path)
    base = os.path.splitext(step_path)[0]
    for existing in (base + ".SLDPRT", base + ".SLDASM"):
        if os.path.isfile(existing):
            # never import twice: an assembly may already have mates on this file
            return "EXISTS", existing
    # pywin32 returns the by-reference error code as a second value
    doc, error = sw.LoadFile4(step_path, "r", None, 0)
    if doc is None:
        raise RuntimeError(f"SolidWorks could not import {step_path} (error code {error})")
    title = _call(doc, "GetTitle")
    try:
        # shortcut: a multi-part STEP imports as an assembly and is saved as .SLDASM, untested;
        # upgrade if vendor assemblies need their component files managed.
        is_assembly = _call(doc, "GetType") == SW_DOC_ASSEMBLY
        out_path = base + (".SLDASM" if is_assembly else ".SLDPRT")
        save_error = doc.SaveAs3(out_path, 0, SAVE_SILENT)
        if save_error or not os.path.isfile(out_path) or os.path.getsize(out_path) == 0:
            raise RuntimeError(f"SolidWorks could not save {out_path} (error code {save_error})")
        return "OK    ", out_path
    finally:
        sw.CloseDoc(title)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    try:
        app = win32com.client.GetActiveObject("SldWorks.Application")
    except pythoncom.com_error:
        sys.exit("SolidWorks is not running. Start it, then run this again.")
    failed = 0
    for path in sys.argv[1:]:
        try:
            print(*convert(app, path))
        except Exception as exc:  # keep going so one bad file does not block the rest
            failed += 1
            print("FAIL", path, "-", exc)
    sys.exit(1 if failed else 0)
