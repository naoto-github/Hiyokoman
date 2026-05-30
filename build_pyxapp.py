"""
Build Hiyokoman.pyxapp and regenerate Hiyokoman.html

pyxel package takes a single APP_DIR, so we stage both hiyokoman_py/ and
the required hiyokoman_js/ subdirectories into a temp directory.

The ASSET_ROOT in constants.py resolves to:
  <app_dir>/hiyokoman_js   (parents[3] of constants.py)

Staging tree:
  staging/
    hiyokoman_py/   <- full source
    hiyokoman_js/
      images/
      original/

After packaging, the .pyxapp_startup_script is patched to use forward
slashes so the WASM (Linux) runtime can resolve the path.
"""
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

REPO = Path(__file__).parent
OUT  = REPO / "Hiyokoman.pyxapp"

# Subdirs of hiyokoman_js that the Python game actually reads
JS_INCLUDES = ["images", "original"]


def _fix_startup_path(pyxapp: Path) -> None:
    """Replace backslashes with forward slashes in .pyxapp_startup_script."""
    startup_name = None
    for name in zipfile.ZipFile(pyxapp).namelist():
        if name.endswith(".pyxapp_startup_script"):
            startup_name = name
            break
    if startup_name is None:
        return

    tmp = pyxapp.with_suffix(".tmp")
    with zipfile.ZipFile(pyxapp, "r") as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == startup_name:
                fixed = data.decode().replace("\\", "/")
                print(f"  startup_script: {data.decode().strip()!r} -> {fixed.strip()!r}")
                data = fixed.encode()
            zout.writestr(info, data)
    tmp.replace(pyxapp)


def main() -> None:
    with tempfile.TemporaryDirectory() as _tmp:
        staging = Path(_tmp) / "hiyokoman_py_stage"
        staging.mkdir()

        # 1. Copy the full hiyokoman_py tree
        print("Copying hiyokoman_py …")
        shutil.copytree(REPO / "hiyokoman_py", staging / "hiyokoman_py")

        # 2. Copy required hiyokoman_js subdirs
        print("Copying hiyokoman_js assets …")
        js_dst = staging / "hiyokoman_js"
        for subdir in JS_INCLUDES:
            src = REPO / "hiyokoman_js" / subdir
            if src.exists():
                shutil.copytree(src, js_dst / subdir)
            else:
                print(f"  WARNING: {src} not found, skipping")

        # 3. Package  (startup must be an absolute path inside staging)
        startup = str(staging / "hiyokoman_py" / "main.py")
        print(f"Running: pyxel package {staging} {startup}")
        subprocess.run(
            [sys.executable, "-m", "pyxel", "package", str(staging), startup],
            check=True,
        )

        # pyxel package creates <staging_basename>.pyxapp in CWD
        cwd = Path.cwd()
        generated = cwd / (staging.name + ".pyxapp")
        if not generated.exists():
            candidates = list(cwd.glob("*stage*.pyxapp"))
            if not candidates:
                print("ERROR: could not find generated .pyxapp")
                sys.exit(1)
            generated = candidates[0]

        # 4. Fix Windows backslash in startup script path
        print("Fixing startup script path separators …")
        _fix_startup_path(generated)

        shutil.move(str(generated), str(OUT))
        print(f"pyxapp → {OUT}")

    # 5. Regenerate HTML
    print("Running: pyxel app2html …")
    subprocess.run(
        [sys.executable, "-m", "pyxel", "app2html", str(OUT)],
        check=True,
    )

    # app2html creates <name>.html in CWD
    generated_html = Path.cwd() / (OUT.stem + ".html")
    if not generated_html.exists():
        print("WARNING: HTML not found at expected path, skipping patch")
    else:
        # 6. Inject required Pyodide packages
        html = generated_html.read_text(encoding="utf-8")
        if 'packages:' not in html:
            html = html.replace(
                'gamepad: "enabled", base64:',
                'gamepad: "enabled", packages: "numpy,Pillow", base64:',
            )
            generated_html.write_text(html, encoding="utf-8")
            print("Injected packages: numpy,Pillow")

        print(f"HTML  → {generated_html}")


if __name__ == "__main__":
    main()
