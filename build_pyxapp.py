"""
Build hiyokoman_py.pyxapp

pyxel package takes a single APP_DIR, so we stage both hiyokoman_py/ and
the required hiyokoman_js/ subdirectories into a temp directory.

The ASSET_ROOT in constants.py resolves to:
  <app_dir>/hiyokoman_js   (parents[3] of constants.py)

So the staging tree looks like:
  staging/
    hiyokoman_py/   <- full source
    hiyokoman_js/
      images/
      original/
      sound/        <- only needed at runtime for legacy pygame path;
                       pyxel-native audio doesn't use this
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).parent
OUT  = REPO / "hiyokoman_py.pyxapp"

# Subdirs of hiyokoman_js that the Python game actually reads
JS_INCLUDES = ["images", "original"]

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
        result = subprocess.run(
            [sys.executable, "-m", "pyxel", "package", str(staging), startup],
            check=True,
        )

        # pyxel package creates <staging_basename>.pyxapp in the CWD
        cwd = Path.cwd()
        generated = cwd / (staging.name + ".pyxapp")
        if not generated.exists():
            candidates = list(cwd.glob("*stage*.pyxapp"))
            if not candidates:
                print("ERROR: could not find generated .pyxapp")
                sys.exit(1)
            generated = candidates[0]

        shutil.move(str(generated), str(OUT))
        print(f"\nDone → {OUT}")


if __name__ == "__main__":
    main()
