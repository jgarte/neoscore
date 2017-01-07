from PyQt5 import QtGui

from brown.utils.units import GraphicUnit


class PenInterface:
    """Interface for a generic drawing pen controlling path outline appearance.

    Currently only solid colors are supported.
    """

    def __init__(self, color, thickness=None):
        """
        Args:
            color (Color): The color for the pen
            thickness (Unit): The stroke thickness of the pen
        """
        # HACK: Initialize color to bright red to this not being set
        #       by color setter
        self._qt_object = QtGui.QPen(QtGui.QColor('#FF0000'))
        self.thickness = thickness
        self.color = color

    ######## PUBLIC PROPERTIES ########

    @property
    def color(self):
        """Color: The color for the pen"""
        return self._color

    @color.setter
    def color(self, color):
        self._color = color
        self._qt_object.setColor(QtGui.QColor(color.red,
                                              color.green,
                                              color.blue,
                                              color.alpha))

    @property
    def thickness(self):
        """Unit: The drawing thickness of the pen.

        If set to None, the value defaults to 0, a cosmetic pixel width.
        """
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if value is None:
            value = 0
        self._thickness = value
        self._qt_object.setWidthF(
            float(GraphicUnit(self._thickness)))
