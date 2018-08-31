from PyQt4 import QtCore
from PyQt4 import QtGui


class UI_about(QtGui.QDialog):

    def __init__(self, parent=None):
        """
        UI about constructor
        :param parent:
        """
        super(UI_about, self).__init__(parent)
        self.about_info = QtGui.QLabel("This is a Python program for stock view\nDafei Ning\nFor more information:\nningdafei@gmail.com")
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.about_info)
        self.setLayout(vbox)
        self.setWindowTitle("About this program")
