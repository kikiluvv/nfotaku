import sys
import subprocess
from pathlib import Path

def build_app():
    project_dir = Path(__file__).parent.resolve()
    main_script = project_dir / "main.py"

    mac_icon = project_dir / "assets" / "icon.png"
    win_icon = project_dir / "assets" / "icon.png"

    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--clean",
        "--name", "NFotaku"
    ]

    sep = ";" if sys.platform == "win32" else ":"

    # Add root assets folder (global icons)
    root_assets = project_dir / "assets"
    if root_assets.exists():
        cmd += ["--add-data", f"{str(root_assets)}{sep}assets"]
    else:
        print("[Warning] root assets folder not found, skipping")

    # Add nfomancer/gui assets folder
    gui_assets = project_dir / "nfomancer" / "assets"
    if gui_assets.exists():
        # The destination folder inside the bundle will be "nfomancer/assets"
        cmd += ["--add-data", f"{str(gui_assets)}{sep}nfomancer/assets"]
    else:
        print("[Warning] nfomancer assets folder not found, skipping")

    # Add platform-specific icon
    if sys.platform == "darwin" and mac_icon.exists():
        cmd += ["--icon", str(mac_icon)]
    elif sys.platform == "win32" and win_icon.exists():
        cmd += ["--icon", str(win_icon)]
    else:
        print(f"[Warning] Unsupported platform '{sys.platform}' or icon not found")

    cmd.append(str(main_script))

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("Build succeeded! Check the 'dist' folder for your app.")
    else:
        print("Build failed!")
        print(result.stdout)
        print(result.stderr)

if __name__ == "__main__":
    build_app()
