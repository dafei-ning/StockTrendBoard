from PyQt4 import QtCore
from PyQt4 import QtGui
import QtMpl


class UI_central(QtGui.QDialog):

    def __init__(self, parent=None):
        """
        UI central constructor
        :param parent:
        """
        super(UI_central, self).__init__(parent)

        # Create label, textedit, calendar and pushbutton.
        self.label1 = QtGui.QLabel("Stock:")
        self.text1 = QtGui.QLineEdit()
        self.label2 = QtGui.QLabel("How many?")
        self.text2 = QtGui.QLineEdit()
        self.calendar = QtGui.QCalendarWidget()
        self.button = QtGui.QPushButton("Add")

        # Create a first HBoxLayout and add above each element in order.
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.label1)
        hbox.addWidget(self.text1)
        hbox.addWidget(self.label2)
        hbox.addWidget(self.text2)
        hbox.addWidget(self.calendar)
        hbox.addWidget(self.button)

        # Create label, combobox and pushbutton.
        self.label3 = QtGui.QLabel("Known Stocks")
        self.combobox = QtGui.QComboBox()
        self.button1 = QtGui.QPushButton("Display Officers")

        # Create a second HBoxLayout and add above each element in order.
        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(self.label3)
        hbox1.addWidget(self.combobox)
        hbox1.addWidget(self.button1)

        # Create label and textedit.
        self.label4 = QtGui.QLabel("Officers and Directors")
        self.text3 = QtGui.QTextEdit()

        # Create a third HBoxLayout and add above each element in order.
        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(self.label4)
        hbox2.addWidget(self.text3)

        # Create a VBoxLayout element and all three hbox to the vbox.
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.widget = QtGui.QWidget(self)

        # Create an instance of QtMpl class and add it to vbox
        self.mpl = QtMpl.QtMpl(self.widget)
        vbox.addWidget(self.mpl)

        self.setLayout(vbox)




