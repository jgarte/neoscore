import json

from brown import config
from brown.core.document import Document
from brown.core.font import Font
from brown.utils.exceptions import FontRegistrationError
from brown.interface.app_interface import AppInterface

"""The global state of the application."""

_app_interface = None

default_font = None
"""Font: The default font to be used in `Text` objects."""

document = None
"""Document: The global document root object."""

registered_music_fonts = {}

registered_text_fonts = {}

# Color of background between and around pages. (Not yet implemented)
_display_background_color = '#dddddd'
# Background color of pages themselves. (Not yet implemented)
_display_paper_color = '#ffffff'


def setup(initial_paper=None):
    """Initialize the application and set up the global state.

    This initializes the global `Document` and a back-end
    AppInterface instance.

    This should be called once at the beginning of every script using `brown`;
    calling this multiple times in one script will cause unexpected behavior.

    Args:
        initial_paper (Paper): The paper to use in the document.
            If `None`, this defaults to `config.DEFAULT_PAPER_TYPE`

    Returns: None
    """
    global _app_interface
    global default_font
    global paper
    global document
    global registered_text_fonts
    document = Document(initial_paper)
    _app_interface = AppInterface(document)
    _register_default_fonts()
    default_font = Font(config.DEFAULT_TEXT_FONT_NAME,
                        config.DEFAULT_TEXT_FONT_SIZE,
                        1, False)


def register_font(font_file_path):
    """Register a font file with the application.

    If highly consistent typesetting is a concern for your score and
    you wish to use non-standard fonts (e.g. Times New Roman), it is
    recommended that you distribute your fonts with `brown` scripts
    whenever possible, and call this immediately after `brown.setup()`.

    If successful, this makes the font available for use in `Font` objects,
    to be referenced by the family name embedded in the font file.

    Args:
        font_file_path (str): A path to a font file. Currently only
            TrueType and OpenType fonts are supported.

    Returns: None

    Raises: FontRegistrationError: If the font could not be loaded.
        Typically, this is because the given path does not lead to
        a valid font file.
    """
    AppInterface.register_font(font_file_path)

def register_music_font(font_name, font_file_path, metadata_path):
    """Register a music font with the application.

    Args:
        font_name (str): The canonical name of this font.
            This is used as a dict key for the font metadata
            in `brown.registered_music_fonts`.
        font_file_path (str): A path to a font file.
        metadata_path (str): A path to a SMuFL metadata JSON file
            for this font. The standard SMuFL format for this file name
            will be {lowercase_font_name}_metadata.json.

    Returns: None
    """
    global registered_music_fonts
    register_font(font_file_path)
    try:
        with open(metadata_path, 'r') as metadata_file:
            metadata = json.load(metadata_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            'Music font metadata file {} could not be found'.format(
                metadata_path))
    except json.JSONDecodeError as e:
        e.msg = ('Invalid JSON metadata in music font '
                 'metadata file {}'.format(metadata_path))
        raise e
    registered_music_fonts[font_name] = metadata
    return metadata


def show():
    """Show a preview of the score in a GUI window.

    The current implementation is pretty limited in features,
    but this could/should be extended in the future once
    the API/interface/Qt bindings are more stable.

    Returns: None
    """
    global document
    global _app_interface
    document._render()
    _app_interface.show()


def render_pdf(path):
    """Render the score as a pdf.

    Args:
        path (str): The output score path.
            If a relative path is provided, it will be
            relative to the current working directory.
    """
    global document
    global _app_interface
    document._render()
    _app_interface.render_pdf((page.page_index for page in document.pages),
                              path)


def _register_default_fonts():
    register_music_font(config.DEFAULT_MUSIC_FONT_NAME,
                        config.DEFAULT_MUSIC_FONT_PATH,
                        config.DEFAULT_MUSIC_FONT_METADATA_PATH)
    register_font(config.DEFAULT_TEXT_FONT_REGULAR_PATH)
    register_font(config.DEFAULT_TEXT_FONT_BOLD_PATH)
    register_font(config.DEFAULT_TEXT_FONT_ITALIC_PATH)
    register_font(config.DEFAULT_TEXT_FONT_BOLD_ITALIC_PATH)
