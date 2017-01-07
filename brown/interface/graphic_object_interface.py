from abc import ABC

from brown.config import config
from brown.interface.pen_interface import PenInterface
from brown.interface.brush_interface import BrushInterface
from brown.utils.units import GraphicUnit
from brown.utils.point import Point
from brown.utils.color import Color


class GraphicObjectInterface(ABC):
    """Interface for a generic graphic object.

    This is a top-level abstract interface class.
    """
    def __init__(self, pos, pen=None, brush=None, parent=None):
        """
        Must define and set:

            self._qt_object = # Some subclass of QGraphicsItem
            self.x = x
            self.y = y
            self.parent = parent

        Args:
            pos (Point[GraphicUnit] or tuple): The position of the path root
                relative to the document.
            pen (PenInterface): The pen to draw outlines with.
            brush (BrushInterface): The brush to draw outlines with.
        """
        raise NotImplementedError

    ######## PUBLIC PROPERTIES ########

    @property
    def pos(self):
        """Point[GraphicUnit]: The position of the object."""
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = Point.with_unit(value, unit=GraphicUnit)
        self._qt_object.setX(self.pos.x.value)
        self._qt_object.setY(self.pos.y.value)

    @property
    def x(self):
        """GraphicUnit: The x position relative to the document"""
        return self.pos.x

    @x.setter
    def x(self, value):
        self.pos.x = GraphicUnit(value)
        self._qt_object.setX(self.pos.x.value)

    @property
    def y(self):
        """GraphicUnit: The y position relative to the document"""
        return self.pos.y

    @y.setter
    def y(self, value):
        self.pos.y = GraphicUnit(value)
        self._qt_object.setY(self.pos.y.value)

    @property
    def pen(self):
        """
        PenInterface: The pen to draw outlines with
        """
        return self._pen

    @pen.setter
    def pen(self, value):
        if value:
            if isinstance(value, str):
                value = PenInterface(value)
            elif isinstance(value, PenInterface):
                pass
            else:
                raise TypeError
        else:
            value = PenInterface(Color(*config.DEFAULT_PEN_COLOR))
        self._pen = value
        self._qt_object.setPen(self._pen._qt_object)

    @property
    def brush(self):
        """
        BrushInterface: The brush to draw outlines with
        """
        return self._brush

    @brush.setter
    def brush(self, value):
        if value:
            if isinstance(value, str):
                value = BrushInterface(value)
            elif isinstance(value, BrushInterface):
                pass
            else:
                raise TypeError
        else:
            value = BrushInterface(Color(*config.DEFAULT_BRUSH_COLOR))
        self._brush = value
        self._qt_object.setBrush(self._brush._qt_object)

    @property
    def parent(self):
        """The interface of the parent object."""
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value
        if value is not None:
            self._qt_object.setParentItem(value._qt_object)
        else:
            self._qt_object.setParentItem(None)

    ######## PUBLIC METHODS ########

    def render(self):
        """Render the object to the scene.

        Returns: None
        """
        raise NotImplementedError
