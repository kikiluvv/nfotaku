from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QListWidget, QListWidgetItem, QColorDialog, QGraphicsDropShadowEffect, QDialog, QGridLayout
)
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QColor, QFont, QIcon, QPainter, QMovie
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent,  QMediaPlaylist

import sys
from pathlib import Path
from nfotaku.logic import scan_subfolders, write_nfo_file
from nfotaku.models import KitFolder


class IconPickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🎛️ Choose Icon")
        self.setStyleSheet("background-color: #111; color: #eee;")
        layout = QGridLayout()
        self.setLayout(layout)

        self.selected_index = None
        icon_size = 48
        cols = 8
        total_icons = 50

        assets_dir = Path(__file__).parent / "assets" / "icons"

        for i in range(total_icons):
            icon_path = assets_dir / f"{i}.png"
            btn = QPushButton()
            btn.setFixedSize(icon_size, icon_size)

            if icon_path.exists():
                pixmap = QPixmap(str(icon_path)).scaled(
                    icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                btn.setIcon(QIcon(pixmap))
                btn.setIconSize(pixmap.rect().size())
            else:
                btn.setText(str(i))

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #222;
                    border: 1px solid #555;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #444;
                    border-color: #aaa;
                }
            """)
            btn.clicked.connect(lambda _, idx=i: self.choose_icon(idx))
            layout.addWidget(btn, i // cols, i % cols)

    def choose_icon(self, index):
        self.selected_index = index
        self.accept()


class NFotakuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌟 NFotaku")
        self.setGeometry(100, 100, 800, 600)

        assets_dir = Path(__file__).parent / "assets"
        gif_path = assets_dir / "bg.gif"
        fallback_image_path = assets_dir / "tits.png"
        self.set_background(gif_path, fallback_image_path)


        music_path = assets_dir / "bg.mp3"
        if music_path.exists():
            self.playlist = QMediaPlaylist()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(str(music_path))))
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

            self.player = QMediaPlayer()
            self.player.setPlaylist(self.playlist)
            self.player.setVolume(30)
            self.player.play()
        else:
            print(f"[Warning] Music file not found: {music_path}")

        self.selected_path = None
        self.folders: list[KitFolder] = []
        self.gradient_base = None  # (start_hex, end_hex)

        self.layout = QVBoxLayout()
        self.label = QLabel("🌟 NFotaku — waifu folder tool")
        self.label.setFont(QFont("Courier New", 24))
        self.label.setStyleSheet("""
            color: #b0b0ff;
            font-weight: bold;
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 255, 255, 180))  # soft blue glow
        shadow.setOffset(0, 0)
        self.label.setGraphicsEffect(shadow)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label)

        self.open_folder_label = QLabel("")
        self.open_folder_label.setFont(QFont("Courier New", 12))
        self.open_folder_label.setStyleSheet(
            "color: #e0e0e0; padding: 6px; font-size: 24px;")
        self.open_folder_label.setAlignment(Qt.AlignCenter)
        self.open_folder_label.hide()
        self.layout.addWidget(self.open_folder_label)

        self.select_button = QPushButton("📁 Select Folder")
        self.style_glassy_button(self.select_button)
        self.select_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_button)

        self.folder_list = QListWidget()
        self.folder_list.setDragDropMode(QListWidget.InternalMove)
        self.folder_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 0.25);
                color: #e0e0e0;
                font-family: 'Courier New';
                font-size: 14px;
                border: 1.5px solid rgba(255, 255, 255, 0.4);
                border-radius: 10px;
            }
            QListWidget::item:selected {
                background-color: rgba(255, 255, 255, 0.3);
                color: #000;
            }
            QListWidget::item {
                background-color: rgba(0, 0, 0, 0);
            }
        """)
        self.layout.addWidget(self.folder_list)

        color_icon_row = QHBoxLayout()

        self.gradient_button = QPushButton("🌈 Pick Gradient")
        self.style_glassy_button(self.gradient_button)
        self.gradient_button.setFixedHeight(40)
        self.gradient_button.clicked.connect(self.pick_gradient)
        color_icon_row.addWidget(self.gradient_button)

        self.color_button = QPushButton("🎨 Pick Color")
        self.style_glassy_button(self.color_button)
        self.color_button.setFixedHeight(40)
        self.color_button.clicked.connect(self.pick_color)
        color_icon_row.addWidget(self.color_button)

        self.icon_button = QPushButton("🖼️ Pick Icon")
        self.style_glassy_button(self.icon_button)
        self.icon_button.setFixedHeight(40)
        self.icon_button.clicked.connect(self.pick_icon)
        color_icon_row.addWidget(self.icon_button)

        self.layout.addLayout(color_icon_row)

        self.generate_button = QPushButton("📄 Generate .nfo Files")
        self.style_glassy_button(self.generate_button)
        self.generate_button.clicked.connect(self.generate_nfo_files)
        self.layout.addWidget(self.generate_button)

        self.help_button = QPushButton("🧾 Help / Instructions")
        self.style_glassy_button(self.help_button)
        self.help_button.clicked.connect(self.show_help)
        self.layout.addWidget(self.help_button)

        footer = QLabel("1kikiluvv - appeal2heaven")
        footer.setAlignment(Qt.AlignCenter)
        footer.setFont(QFont("Courier New", 10))
        footer.setStyleSheet("color: #c9c9c7; padding: 8px; font-style: italic; font-size: 14px;")
        self.layout.addWidget(footer)

        self.setLayout(self.layout)

    def set_background(self, gif_path, fallback_image_path):
        self.fallback_image_path = fallback_image_path

        if hasattr(self, 'bg_label'):
            self.bg_label.deleteLater()

        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.lower()

        self.bg_movie = QMovie(str(gif_path))
        self.bg_movie.setScaledSize(self.size())
        self.bg_movie.setCacheMode(QMovie.CacheAll)
        self.bg_movie.setCacheMode(QMovie.CacheAll)
        self.bg_movie.setPaused(False)
        # REMOVE self.bg_movie.setLoopCount(1)  # <-- no such method in PyQt5

        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.show()

        self.bg_movie.frameChanged.connect(self.stop_gif_at_end)
        self.bg_movie.finished.connect(self.switch_to_static_background)
        self.bg_movie.start()

    def stop_gif_at_end(self, frame_number):
        if self.bg_movie.loopCount() == 1:
            if frame_number == self.bg_movie.frameCount() - 1:
                self.bg_movie.stop()
                self.switch_to_static_background()


    def switch_to_static_background(self):
        if hasattr(self, "fallback_image_path") and self.fallback_image_path.exists():
            pixmap = QPixmap(str(self.fallback_image_path)).scaled(
                self.width(), self.height(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            )
            self.bg_label.setPixmap(pixmap)

    def style_glassy_button(self, button):
        button.setStyleSheet("""
            QPushButton {
                color: #e0e0e0;
                background-color: rgba(0, 0, 0, 0.3);
                border: 1.5px solid rgba(255, 255, 255, 0.4);
                border-radius: 12px;
                font-family: 'Courier New';
                font-size: 16px;
                padding: 10px 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
                color: #fff;
                border-color: rgba(255, 255, 255, 0.7);
                font-weight: bold;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.25);
                color: #fff;
                border-color: rgba(255, 255, 255, 0.9);
            }
        """)
        button.setCursor(Qt.PointingHandCursor)


    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Kit Folder")
        if path:
            self.selected_path = path
            self.label.setText(f"Selected: {path}")
            self.load_subfolders()
        else:
            self.open_folder_label.hide()

    def load_subfolders(self):
        self.folder_list.clear()
        subpaths = scan_subfolders(self.selected_path)
        self.folders = [KitFolder(f.name, f) for f in subpaths]

        for folder in self.folders:
            item = QListWidgetItem(folder.name)
            item.setData(Qt.UserRole, folder)

            if folder.color and folder.color.lower() != "#000000":
                item.setIcon(QIcon(self.make_color_icon(folder.color)))

            if folder.icon_index is not None:
                item.setText(f"{folder.name} [icon {folder.icon_index}]")

            self.folder_list.addItem(item)

    def make_color_icon(self, hex_color: str) -> QPixmap:
        pixmap = QPixmap(20, 20)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        color = QColor(hex_color)
        color.setAlpha(200)
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, 20, 20)
        painter.end()
        return pixmap

    def pick_color(self):
        selected_item = self.folder_list.currentItem()
        if not selected_item:
            return

        color = QColorDialog.getColor()
        if color.isValid():
            folder = selected_item.data(Qt.UserRole)
            folder.color = color.name()
            selected_item.setIcon(QIcon(self.make_color_icon(color.name())))
            self.gradient_base = None  # clear gradient if setting solid

    def pick_gradient(self):
        color1 = QColorDialog.getColor()
        if not color1.isValid():
            return
        color2 = QColorDialog.getColor()
        if not color2.isValid():
            return

        self.gradient_base = (color1.name(), color2.name())
        self.label.setText("🌈 Gradient ready — will apply on .nfo generation")
        self.apply_gradient_to_list()

    def apply_gradient_to_list(self):
        if not self.gradient_base or self.folder_list.count() == 0:
            return

        start_hex, end_hex = self.gradient_base
        total = self.folder_list.count()

        for i in range(total):
            item = self.folder_list.item(i)
            folder = item.data(Qt.UserRole)
            t = i / max(1, total - 1)
            color = self.interpolate_color(start_hex, end_hex, t)
            folder.color = color
            item.setIcon(QIcon(self.make_color_icon(color)))

    def pick_icon(self):
        selected_item = self.folder_list.currentItem()
        if not selected_item:
            return

        dialog = IconPickerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            icon_index = dialog.selected_index
            folder = selected_item.data(Qt.UserRole)
            folder.icon_index = icon_index
            selected_item.setText(f"{folder.name} [icon {icon_index}]")

    def generate_nfo_files(self):
        self.play_gif_once_then_static()
        if not self.selected_path:
            self.label.setText("⚠️ Select a kit folder first")
            return

        main_path = Path(self.selected_path)
        new_order = []

        for i in range(self.folder_list.count()):
            item = self.folder_list.item(i)
            folder = item.data(Qt.UserRole)
            new_order.append(folder)

        # 🎨 apply interpolated gradient
        if self.gradient_base:
            start_hex, end_hex = self.gradient_base
            for idx, folder in enumerate(new_order):
                t = idx / max(1, len(new_order) - 1)
                folder.color = self.interpolate_color(start_hex, end_hex, t)

        print("\n[DEBUG] Final folder order:")
        for idx, folder in enumerate(new_order, start=1):
            print(
                f"  {idx}. {folder.name} — Color: {folder.color} IconIndex: {folder.icon_index}"
            )
            write_nfo_file(main_path, folder, idx)

        self.label.setText("✨ .nfo files cast into the main kit folder")

    def interpolate_color(self, start_hex: str, end_hex: str, t: float) -> str:
        s = QColor(start_hex)
        e = QColor(end_hex)
        r = int(s.red() + (e.red() - s.red()) * t)
        g = int(s.green() + (e.green() - s.green()) * t)
        b = int(s.blue() + (e.blue() - s.blue()) * t)
        return f"#{r:02x}{g:02x}{b:02x}"

    def show_help(self):
        help_text = """
        <h2 style='color:#eee; font-family: "Courier New", monospace; margin-bottom: 20px;'>
            🌟 NFotaku — How To Use
        </h2>
        <ul style="
            line-height: 2.0; 
            font-size: 16px; 
            font-family: 'Courier New', monospace; 
            padding-left: 20px;
            color: #ccc;
            ">
            <li style="margin-bottom: 12px;">
                <b>📁 Select Folder</b> — Choose the main kit folder you want to enchant.
            </li>
            <li style="margin-bottom: 12px;">
                <b>🌈 Pick Gradient</b> — Pick two colors to fade across your subfolders.
            </li>
            <li style="margin-bottom: 12px;">
                <b>🎨 Pick Color</b> — Set a custom solid color for one folder (clears gradient).
            </li>
            <li style="margin-bottom: 12px;">
                <b>🖼️ Pick Icon</b> — Choose a glyph/icon for the selected folder.
            </li>
            <li style="margin-bottom: 12px;">
                <b>📄 Generate .nfo Files</b> — Create magical <code style='color:#c9c9c7;'>.nfo</code> files inside each subfolder.
            </li>
            <li style="margin-bottom: 12px;">
                <b>🔀 Drag & Drop Folders</b> — Change folder order before generating files.
            </li>
        </ul>
        <p style='
            color:#ddd; 
            font-style: italic; 
            font-weight: 600; 
            margin-top: 25px; 
            font-family: "Courier New", monospace;
            '>
            Colors and icons are remembered and used in your .nfo rituals.
        </p>
        """

        dialog = QDialog(self)
        dialog.setWindowTitle("🧾 How to Use NFotaku")
        dialog.setStyleSheet("""
            background-color: #121212; 
            color: #eee; 
            border-radius: 12px;
            padding: 20px;
            min-width: 450px;
        """)
        layout = QVBoxLayout()
        label = QLabel(help_text)
        label.setWordWrap(True)
        label.setTextFormat(Qt.RichText)
        layout.addWidget(label)
        close_button = QPushButton("🔮 Close")
        self.style_glassy_button(close_button)
        close_button.setFixedHeight(40)
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def resizeEvent(self, event):
        if hasattr(self, 'bg_movie'):
            self.bg_movie.setScaledSize(self.size())
            self.bg_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def play_gif_once_then_static(self):
        if hasattr(self, "bg_movie"):
            self.bg_movie.stop()
            self.bg_movie.jumpToFrame(0)
            self.bg_movie.start()



def launch_nfotaku():
    app = QApplication(sys.argv)
    window = NFotakuGUI()
    window.show()
    sys.exit(app.exec_())
