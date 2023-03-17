"""A class for limiting the axis of the plotted signals."""
import numpy as np


class Graph_data_container:
    """Class for uniformal plots.

    This takes 3 arguments x, y and a label for the legend.
    Args
    -------
    _x: np.ndarray
        What will be plotted in the x axis (2d)
    _y: np.ndarray
        What will be plotted in the y axis (2d)
    label: str
        The legend information for the figure.
        Be short (2d)
    """

    def __init__(self,
                 _x: np.ndarray,
                 _y: np.ndarray,
                 label: str) -> None:
        """Initialize constructor for x, y values."""
        self.x = _x
        self.y = _y
        self.label = label

    @property
    def xs_lim(self):
        """Adapts the limit of the x axis in respect to the input given."""
        x_l = np.floor(np.log10(max(1, min(self.x))))
        x_u = np.ceil(np.log10(max(1, max(self.x))))
        return [10**x_l, 10**x_u]

    @property
    def ys_lim(self):
        """Adapts the limit of the y axis in respect to the input given."""
        x_l = np.floor(np.log10(min(self.y)))-1
        x_u = np.ceil(np.log10(max(self.y)))+1
        return [10**x_l, 10**x_u]

    @property
    def extrema(self):
        """Return the extreme values for x and y.

        [x_min, x_max, y_min, y_max]
        Returns:
            _type_: _description_
        """
        return [self.x.min(), self.x.max(), self.y.min(), self.y.max()]
