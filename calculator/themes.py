import os
from pathlib import Path

def get_theme_path():
    return os.path.join(Path(__file__).parent, "theme.json")