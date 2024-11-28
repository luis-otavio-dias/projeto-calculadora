from pathlib import Path

# Modulo referente a variaveis que podem ser utilizadas em outros modulos

# Paths
ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / "files"
WINDOW_ICON_PATH = FILES_DIR / "icon.png"

# Sizing
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TEXT_MARGIN = 15
MINIMUM_WIDTH = 500

# Colors
PRIMARY_COLOR = "#1e81b0"
DARKER_PRIMARY_COLOR = "#16658a"
DARKEST_PRIMARY_COLOR = "#115270"
