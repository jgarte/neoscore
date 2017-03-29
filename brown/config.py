"""Common configuration values and default settings."""

import os

from brown.utils.units import Mm, Inch, GraphicUnit
from brown.core.stroke_pattern import StrokePattern
from brown.core.fill_pattern import FillPattern
from brown.utils.color import Color


######## Constants that really shouldn't be changed ########

BROWN_ROOT_DIR = os.path.join(os.path.dirname(__file__))
RESOURCES_DIR = os.path.join(BROWN_ROOT_DIR, 'resources')

######## Defaults ##########################################

# Default pen properties
DEFAULT_PEN_COLOR = Color(0, 0, 0)
DEFAULT_PEN_THICKNESS = GraphicUnit(0)  # GraphicUnits
DEFAULT_PEN_PATTERN = StrokePattern.SOLID

# Default brush properties
DEFAULT_BRUSH_COLOR = Color(0, 0, 0, 255)
DEFAULT_PATH_BRUSH_COLOR = Color(0, 0, 0, 0)
DEFAULT_BRUSH_PATTERN = FillPattern.SOLID

# Paper type
DEFAULT_PAPER_TYPE = 'Letter'

# Visual gap between pages on the canvas
# (This has no effect on exported documents)
PAGE_DISPLAY_GAP = Mm(150)

# Text Font
DEFAULT_TEXT_FONT_NAME = 'Cormorant Garamond'
DEFAULT_TEXT_FONT_SIZE = Mm(2)
DEFAULT_TEXT_FONT_WEIGHT = 1
DEFAULT_TEXT_FONT_ITALIC = False

# Music Glyph Font
DEFAULT_MUSIC_FONT_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'Bravura.otf')
DEFAULT_MUSIC_FONT_METADATA_PATH = os.path.join(
    RESOURCES_DIR, 'fonts', 'bravura_metadata.json')
DEFAULT_MUSIC_FONT_NAME = 'Bravura'

# Print PPI
PRINT_DPI = Inch._conversion_rate

# Staff Height
DEFAULT_STAFF_UNIT = Mm(1)