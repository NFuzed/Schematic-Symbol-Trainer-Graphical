from PySide6.QtWidgets import QWidget
from pathlib import Path

def load_style_sheet(file_name, widget):
    """Apply consistent styling to all components"""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent  # Go up two levels from utilities
    styles_dir = project_root / "styles"
    qss_file = styles_dir / file_name

    if qss_file.exists():
        with open(qss_file, "r", encoding="utf-8") as f:
            style = f.read()
            widget.setStyleSheet(style)
    else:
        print(f"Stylesheet not found: {qss_file}")