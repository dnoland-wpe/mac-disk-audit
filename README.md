# Disk Audit (Alfred Workflow)

Fast, scriptable disk space audits on macOS using `du`, surfaced through Alfred with powerful actions.

## Features
- Keyword: `disk`
- Live list of largest folders/files (file actions enabled)
- **⌘ Command** modifier: open selected path in **Terminal**
- **⌥ Option** modifier: export the current audit to **CSV** in `~/Downloads` and auto-open in **Excel**
- **Hotkey (Cmd+Shift+D)**: run the audit against the **frontmost Finder window path**

## Install
1. Download the latest `.alfredworkflow` from `workflow/Disk-Audit-Pro.alfredworkflow`.
2. Double-click to import into Alfred.
3. In Alfred, type `disk`.

## Usage
- `disk` → audit Home, depth 1, top 20
- `disk ~/Downloads` → audit Downloads
- `disk ~/Downloads 2` → set depth to 2
- `disk / 1 30` → audit root, depth 1, top 30
- Flags: `--path=... --depth=... --limit=...`

## End User Guide

### Installation
- Double-click `workflow/Disk-Audit-Pro.alfredworkflow` and import to Alfred.

### How to Use
- Open Alfred and type `disk` to scan your Home folder.
- Use examples above for other paths and depths.

### Modifiers
- **⌘ Command**: open the selected path in Terminal.
- **⌥ Option**: export to CSV (saved in `~/Downloads`) and auto-open in Excel.

### Hotkey
- **Cmd+Shift+D** runs the audit on the frontmost Finder folder (customizable in Alfred).

### Tips
- Start with depth 1 for speed; raise depth for more detail.
- Large scans (like `/`) can take longer.
- Results are interactive: use arrow keys, Return to open.

### Support
- Requires Alfred 5 with Powerpack.
- If Excel isn’t installed, CSV opens in your default app.

## Development
Sources live in `workflow/`:
- `audit.py` — Script Filter logic
- `export.py` — CSV export + Excel open
- `finder_path.sh` — gets frontmost Finder path for the hotkey
- `info.plist` — Alfred workflow graph
- `README.md` — workflow-specific notes

### Local build
```
./scripts/build.sh
```
This repackages the `.alfredworkflow` from the sources in `workflow/` into `dist/`.

### Release
```
./scripts/release.sh 1.2.0
```
Creates a versioned bundle `Disk-Audit-1.2.0.alfredworkflow` in `dist/` and adds a Git tag.

## License
MIT
# mac-disk-audit
