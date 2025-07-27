# 🌟 NFotaku

Customize and rearrange your FL Studio folders with the help from the waifu of your dreams.

---

## ✨ features
- 🎨 pick a color for each subfolder
- 🔀 reorder folders via drag and drop
- 📄 auto-generate .nfo files with:
   - Color
   - IconIndex
   - HeightOfs
   - SortGroup
- 🎧 ambient music and UI for an immersive vibe

## 🧰 requirements
- Python 3.7+
- PyQt5

```bash
pip install pyqt5
```

## 🧵 usage
1. Run the program:
```bash
python3 main.py
```
2. Select your main drum kit folder

3. Reorder the subfolders how you want them to appear in FL

4. Pick colors (optional)

5. Click “Generate .nfo Files”

6. ✅ Done — check each subfolder for a .nfo

## 🛠️ building the executable
If you want to package nfomancer into a standalone app (Windows or macOS), use the included build.py script:

1. Make sure you have Python and PyInstaller installed globally:

```bash
pip install pyinstaller
```

2. Run the build script from the root project folder:

```bash
python build.py
```

- The script will bundle the app into a single executable with all assets and an icon

- Assets folders (assets/ and nfomancer/assets/) are included in the build

- After a successful build, check the dist/ folder for your app:

`dist/NFotaku.exe` on Windows

`dist/NFotaku` on macOS

*Note: The build script requires PyInstaller to be in your PATH. Also, ensure your folder paths have no strange spaces or characters.*

## 📁 file structure
```
nfotaku/
├── main.py
├── build.py
├── assets/                 # Global Assets
│   ├── icon.png            # App Icon
└── nfotaku/
    ├── logic.py
    ├── models.py
    ├── build.py
    └── assets/             # GUI assets
        ├── bg.gif          # background image
        └── bg.mp3          # optional audio loop

```

## 🛑 notes
- IconIndex, HeightOfs, and SortGroup are set in models.py and logic.py.
- FL Studio uses .nfo files to style folders inside the Browser pane.
- The executable bundles assets so you don’t need Python to run it.
- Feel free to tweak and remix.

## 🩸 credits
built by 1kikiluvv for appeal2heaven

## 🖤 license
MIT — do whatever