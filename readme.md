# 🧙‍♂️ nfomancer

Customize and rearrange your FL Studio folders with a little bit of magic.

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
🧵 usage
Run the program:

bash
Copy
Edit
python3 main.py
Select your main drum kit folder

Reorder the subfolders how you want them to appear in FL

Pick colors (optional)

Click “Generate .nfo Files”

✅ Done — check each subfolder for a .nfo

🛠️ building the executable
If you want to package nfomancer into a standalone app (Windows or macOS), use the included build.py script:

Make sure you have Python and PyInstaller installed globally:

bash
Copy
Edit
pip install pyinstaller
Run the build script from the root project folder:

bash
Copy
Edit
python build.py
The script will bundle the app into a single executable with all assets and an icon:

On Windows, it picks the .ico icon and uses correct path separators

On macOS, it picks the .png icon

Assets folders (assets/ and nfomancer/assets/) are included in the build

After a successful build, check the dist/ folder for your app:

dist/NFotaku.exe on Windows

dist/NFotaku on macOS

Note: The build script requires PyInstaller to be in your PATH. Also, ensure your folder paths have no strange spaces or characters.

📁 file structure
css
Copy
Edit
nfomancer/
├── main.py
├── logic.py
├── models.py
├── build.py
├── assets/
│   ├── icon.png           # macOS app icon
│   ├── icon.ico           # Windows app icon
│   ├── tits.png           # background image
│   └── ambient.wav        # optional audio loop
└── nfomancer/
    └── assets/            # GUI assets folder
🛑 notes
IconIndex, HeightOfs, and SortGroup are set in models.py and logic.py.

FL Studio uses .nfo files to style folders inside the Browser pane.

The executable bundles assets so you don’t need Python to run it.

Feel free to tweak and remix — it’s your ritual.

🩸 credits
built by 1kikiluvv for appeal2heaven

🖤 license
MIT — do whatever you want