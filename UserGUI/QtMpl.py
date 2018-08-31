from PyQt4 import QtGui
import matplotlib
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg


class QtMpl (FigureCanvasQTAgg):
    """
    This class will plot a figure on the UI window
    """
    def __init__(self, parent):
        """
        class constructor
        """
        self.fig = matplotlib.figure.Figure()

        # Set date formatter and date locator
        self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        self.fig.gca().xaxis.set_major_locator(mdates.DayLocator())

        # Call parent constructor and set the parent
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)

        # Create a figure subplot
        self.subplot = self.fig.add_subplot(111)
        self.subplot.set_ylabel("Stock Price($)")
        self.subplot.set_xlabel("Date(MM/DD/YYYY)")
        self.subplot.set_title("Historical Stock Data Display")
        self.line = []

        # Set size expandable
        FigureCanvasQTAgg.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        # Update the geometry
        FigureCanvasQTAgg.updateGeometry(self)

    def addLine(self, x, y, title):
        """
        This method will add a line to the graph
        """
        self.line.append(self.subplot.plot(x, y, label=title))
        self.subplot.legend()
        self.fig.canvas.draw()
        self.fig.autofmt_xdate()
        return











