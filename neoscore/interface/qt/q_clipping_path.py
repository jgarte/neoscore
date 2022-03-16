from typing import Optional

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem

from neoscore.constants import DEBUG


class QClippingPath(QGraphicsPathItem):

    """A QGraphicsPathItem extension supporting horizontal path clipping.

    Works like a `QGraphicsPathItem` except that it renders a
    horizontal slice of the path. Rather than rendering the entire
    path, renders the region starting at a given `clip_start_x` and
    extending for a given `clip_width`. This rendered region is
    shifted leftward so it appears at the path's root position. This
    is useful for splitting a path into horizontal chunks and
    rendering them in different positions, for instance when drawing a
    staff which appears on multiple lines.

    `clip_start_x` and `clip_width` should not take into account
    scaling. For example if a rendered region of 50 points is required
    on a path with a scale of 2, `clip_width=50` should be passed.

    While the Qt superclass is mutable, this is intended to be treated
    immutably. Mutations after instantation will result unexpected
    behavior. Object mutations at higher abstraction levels should
    result in new Qt objects created.

    Internally, the clipping implementation is rather subtle in how it
    integrates with Qt's coordinate and painter systems. The item's
    bounding rect is adjusted to match the requested clip region. At
    render time, the painter translates its coordinate system leftward
    by the (internally scale-adjusted) `clip_start_x`. The painter's
    clip rect is then derived from the item's bounding rect, but
    shifted rightward to cancel out the painter's translation. These
    actions are all automatically scaled as necessary, since the scale
    is applied to the QClippingPath, not the painter.

    Note that clipping behavior does not play well with rotated items,
    and no API guarantees are currently given about it.
    """

    def __init__(
        self,
        qt_path: QPainterPath,
        clip_start_x: float = 0,
        clip_width: Optional[float] = None,
        scale: float = 1,
    ):
        """
        Args:
            qt_path: The path for the item. This value should
                be the same as in `QGraphicsPathItem.__init__()`
            clip_start_x: The local starting position for the path clipping region.
                This should not adjust for scaling, as that is performed
                automatically. Use `None` to render from the start.
            clip_width: The width of the path clipping region. This should not adjust
                for scaling, as that is performed automatically. Use `None` to render
                to the end
            scale: A scaling factor on the object's coordinate system.
        """
        super().__init__(qt_path)
        super().setScale(scale)
        self.clip_start_x = clip_start_x / scale
        self.clip_width = None if clip_width is None else clip_width / scale
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)
        self.padding = self.pen().width() / scale
        self.update_geometry()

    def boundingRect(self):
        # Seems like this is in logical space (pre-scaling)
        return self.bounding_rect

    def paint(self, painter: QPainter, *args, **kwargs):
        """Paint with automatic clipping.

        This is overridden from `QGraphicsPathItem.paint()`
        """
        if self.clip_start_x != 0:
            painter.translate(-self.clip_start_x, 0)
        if self.clip_width is not None:
            painter.setClipRect(self.clip_rect)
        if DEBUG:
            bounding_rect = self.bounding_rect
            if self.clip_start_x != 0:
                # Since painter is translated, cancel that out when
                # drawing the bounding rect
                bounding_rect = bounding_rect.translated(self.clip_start_x, 0)
            painter.setBrush(QBrush())
            painter.setPen(QPen(QColor("#ff0000"), 0))
            painter.drawRect(bounding_rect)

        super().paint(painter, *args, **kwargs)

    def update_geometry(self):
        self.prepareGeometryChange()
        path_bounding_rect = self.path().boundingRect()
        self.bounding_rect = QClippingPath.calculate_bounding_rect(
            path_bounding_rect,
            self.clip_start_x,
            self.clip_width,
            self.padding,
        )
        # Clip rect is used by painter, which translates by -clip_start_x
        # so we need to cancel that out here
        self.clip_rect = self.bounding_rect.translated(self.clip_start_x, 0)

    @staticmethod
    def calculate_bounding_rect(
        bounding_rect: QRectF,
        clip_start_x: float,
        clip_width: Optional[float],
        padding: float,
    ) -> QRectF:
        """Create a QRectF giving the bounding rect for the path.

        Args:
            bounding_rect: The full shape's bounding rectangle
            clip_start_x: The local starting position for the
                clipping region. Use `None` to render from the start.
            clip_width: The width of the clipping region.
                Use `None` to render to the end
            padding: Extra area padding to be added to all sides of the clipping area.
                This might be useful, for instance, for making sure thick pen strokes
                render completely.
        """
        resolved_clip_start_x = bounding_rect.x() + clip_start_x
        resolved_clip_width = (
            clip_width
            if clip_width is not None
            else bounding_rect.width() - resolved_clip_start_x
        )
        return QRectF(
            -padding,
            bounding_rect.y() - padding,
            resolved_clip_width + (padding * 2),
            bounding_rect.height() + (padding * 2),
        )