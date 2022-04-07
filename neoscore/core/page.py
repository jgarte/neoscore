from __future__ import annotations

from typing import TYPE_CHECKING

from neoscore.core.brush import Brush
from neoscore.core.color import Color
from neoscore.core.paper import Paper
from neoscore.core.path import Path
from neoscore.core.pen import Pen
from neoscore.core.pen_pattern import PenPattern
from neoscore.core.point import ORIGIN, PointDef
from neoscore.core.positioned_object import PositionedObject
from neoscore.core.rect import Rect
from neoscore.core.units import ZERO, Mm

if TYPE_CHECKING:
    from neoscore.core.document import Document


_PREVIEW_OUTLINE_COLOR = Color("#551155")
_PREVIEW_SHADOW_COLOR = Color(0, 0, 0, 80)


class Page(PositionedObject):

    """A document page.

    All manually created `PositionedObject`s will have a `Page` as their
    ancestor. All `Page`s are children of the global document.

    `Page` objects are automatically created by `Document` and should
    not be manually created or manipulated.
    """

    def __init__(
        self, pos: PointDef, document: Document, page_index: int, paper: Paper
    ):
        """
        Args:
            pos: The position of the top left corner
                of this page in canvas space. Note that this refers to the
                real corner of the page, not the corner of its live area
                within the paper margins.
            document: The global document. This is used as
                the Page object's parent.
            page_index: The index of this page. This should be
                the same index this Page can be found at in the document's
                `PageSupplier`. This should be a positive number.
            paper: The type of paper this page uses.
        """
        super().__init__(pos, document)
        self._document = document
        self._page_index = page_index
        self.paper = paper

    @property
    def page_index(self):
        """The index of this page in its managing `PageSupplier` object."""
        return self._page_index

    @property
    def bounding_rect(self) -> Rect:
        """The page bounding rect, positioned relative to the page."""
        return Rect(
            -self.paper.margin_left,
            -self.paper.margin_top,
            self.paper.width,
            self.paper.height,
        )

    def display_geometry(self, background_brush: Brush):
        """Create child objects which graphically show the page geometry.

        This is useful for interactive views, but should typically not
        be called in PDF and image export contexts.
        """
        # Create page rect
        bounding_rect = self.bounding_rect
        page_preview_rect = Path.rect(
            (bounding_rect.x, bounding_rect.y),
            self,
            bounding_rect.width,
            bounding_rect.height,
            background_brush,
            pen=Pen(_PREVIEW_OUTLINE_COLOR),
        )
        page_preview_rect.z_index = -999999999999
        page_drop_shadow_rect = Path.rect(
            (Mm(1), Mm(1)),
            page_preview_rect,
            bounding_rect.width,
            bounding_rect.height,
            Brush(_PREVIEW_SHADOW_COLOR),
            Pen.no_pen(),
        )
        page_drop_shadow_rect.z_index = page_preview_rect.z_index - 1
        live_area_bounding_rect = Rect(
            ZERO, ZERO, self.paper.live_width, self.paper.live_height
        )
        live_area_preview_rect = Path.rect(
            ORIGIN,
            self,
            self.paper.live_width,
            self.paper.live_height,
            Brush.no_brush(),
            pen=Pen(_PREVIEW_OUTLINE_COLOR, pattern=PenPattern.DOT),
        )
