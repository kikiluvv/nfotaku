from pathlib import Path
from .models import KitFolder

def scan_subfolders(root_path):
    root = Path(root_path)
    return [f for f in root.iterdir() if f.is_dir()]

def write_nfo_file(main_folder: Path, folder_obj: KitFolder, sort_index: int):
    color_code = folder_obj.color.lstrip('#')
    content = f"""Color=${color_code}
IconIndex={folder_obj.icon_index}
HeightOfs={folder_obj.height_ofs}
SortGroup={folder_obj.sort_group - sort_index}
"""
    nfo_path = main_folder / f"{folder_obj.name}.nfo"
    nfo_path.write_text(content)
