from dataclasses import dataclass
from pathlib import Path

@dataclass
class KitFolder:
    name: str
    path: Path
    color: str = "#74b956"        
    icon_index: int = 924         
    height_ofs: int = 15       
    sort_group: int = 100         
