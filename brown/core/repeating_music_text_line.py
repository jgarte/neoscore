from brown.core.music_text import MusicText
from brown.core.spanner import Spanner
from brown.utils.parent_point import ParentPoint
from brown.utils.point import Point


class RepeatingMusicTextLine(MusicText, Spanner):

    """A spanner of repeating music text over its length.

    Currently only perfectly horizontal spanners are supported.
    Additionally, the stop position should be to the right of the start.

    TODO: Implement text spanners that are not perfectly horizontal.
    TODO: Support stop.x < start.x
    """

    def __init__(self, start, stop, text, font=None, scale_factor=1):
        """
        Args:
            start (ParentPoint or tuple init args):
            stop (ParentPoint or tuple init args):
            text (str, tuple, MusicChar, or list of these):
                The text to be repeated over the spanner,
                represented as a str (glyph name), tuple
                (glyph name, alternate number), MusicChar, or a list of them.
            font (MusicFont): The music font to be used. If not specified,
                the font is taken from the ancestor staff.
            scale_factor (float): A hard scaling factor to be applied
                in addition to the size of the music font.
        """
        start = (start if isinstance(start, ParentPoint)
                 else ParentPoint(*start))
        stop = (stop if isinstance(stop, ParentPoint)
                else ParentPoint(*stop))
        # init the MusicText to ask it how wide a single
        # repetition of `text` is in order to calculate how many
        # repetitions are needed to cover the spanner.
        MusicText.__init__(self,
                           Point(start.x, start.y),
                           text,
                           start.parent,
                           font,
                           scale_factor)
        Spanner.__init__(self, Point(stop.x, stop.y), stop.parent)
        self.repeating_music_chars = self.music_chars
        self.repeating_text = self.text
        repetitions = self._repetitions_needed
        self.music_chars = self.music_chars * repetitions
        self._text = self.text * repetitions

    ######## PUBLIC PROPERTIES ########

    @property
    def length(self):
        return self.spanner_x_length

    ######## PRIVATE PROPERTIES ########

    @property
    def _repetitions_needed(self):
        """int: The number of text repetitions needed to cover the line.

        This value rounds down, such that the real length of the drawn
        text will always be <= self.length.
        """
        base_width = self._char_list_bounding_rect(
            self.repeating_music_chars).width
        return int((self.length / base_width).value)
