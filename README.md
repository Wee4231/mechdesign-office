# MechDesign: spring-loaded pusher

A mechanical design done by a team of Claude Code agents driving SolidWorks. The project instructions are in `CLAUDE.md`, the agents in `.claude/agents/`.

## Live mini office

Watch the team work in a 3D office: https://claude.ai/artifact/QE446GrGsiQdHxMfZeenBd

The Director takes your request, five specialists show their progress at their desks, and you can click a person to see what they are doing. The link is private: only the owner (and anyone they share it with) can open it.

`mini_office/index.html` is a copy of that page. Opened on its own it shows everyone as idle, because the live status comes from the artifact's database.

## The design

| Phase | Agent | Result |
|---|---|---|
| 1 Sizing | sizing-engineer | `AI concept design/01_Sizing_Calculations.md` |
| 2 Standard parts | bom-specialist | `AI concept design/BOM.xlsx` |
| 2.5 CAD download | cad-downloader | files in `AI concept design/standard_parts/` |
| 3 Custom parts | cad-modeler | `AI concept design/custom_parts/*.SLDPRT` |
| 4 Assembly | assembly-inspector | `AI concept design/SpringLoadedPusher_Assembly.SLDASM` and screenshots |

Units are mm, g, s. Parts are named for what they do.

## Rebuilding the standard parts

The MISUMI CAD files are not in this repo. Download each part listed in `BOM.xlsx` (SolidWorks or STEP format) into `D:\Download`, then with SolidWorks running:

```
python tools/collect_misumi_downloads.py collect
```

It copies and renames them into `AI concept design/standard_parts/`. `python tools/collect_misumi_downloads.py list` shows what is still missing. The assembly opens once those files are in place.
