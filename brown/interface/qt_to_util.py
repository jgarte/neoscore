"""Various helper functions to convert Qt objects to util objects"""


from PyQt5.QtCore import QPoint, QPointF, QRect, QRectF

from brown.utils.rect import Rect
from brown.utils.point import Point


def qt_point_to_point(qt_point, unit=None):
    """Create a Point from a QPoint or QPointF

    Args:
        qt_point (QPoint or QPointF): The source point
        unit (Unit): An optional unit to convert
            values to in the output `Point`. If omitted, values
            in the output `Point` will be plain `int` or `float` values.

    Returns: Point
    """
    if unit:
        return Point.with_unit(qt_point.x(), qt_point.y(),
                               unit=unit)
    else:
        return Point(qt_point.x(), qt_point.y())


def point_to_qt_point(point):
    """Create a QPoint from a Point

    Args:
        point (Point): The source point

    Returns: QPoint
    """
    return QPoint(int(point.x), int(point.y))


def point_to_qt_point_f(point):
    """Create a QPointF from a Point

    Args:
        point (Point): The source point

    Returns: QPointF
    """
    return QPointF(float(point.x), float(point.y))


def qt_rect_to_rect(qt_rect, unit=None):
    """Create a Rect from a QRect or QRectF

    Args:
        qt_rect (QRect or QRectF): The source rect
        unit (Unit): An optional unit to convert
            values to in the output `Rect`. If omitted, values
            in the output `Rect` will be plain `int` or `float` values.

    Returns: Rect
    """
    if unit:
        return Rect.with_unit(qt_rect.x(), qt_rect.y(),
                              qt_rect.width(), qt_rect.height(),
                              unit)
    else:
        return Rect(qt_rect.x(), qt_rect.y(),
                    qt_rect.width(), qt_rect.height())


def rect_to_qt_rect(rect):
    """Create a QRect from a Rect

    Args:
        rect (Rect): The source rect

    Returns: QRect
    """
    return QRect(int(rect.x), int(rect.y),
                 int(rect.width), int(rect.height))


def rect_to_qt_rect_f(rect):
    """Create a QRectF from a Rect

    Args:
        rect (Rect): The source rect

    Returns: QRectF
    """
    return QRectF(float(rect.x), float(rect.y),
                  float(rect.width), float(rect.height))