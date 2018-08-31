import configparser
import logging
import sys
import time
import GoogleFinance
from PyQt4 import QtCore
from PyQt4 import QtGui
import UI


if __name__ == "__main__":

    # Safely create the log file
    try:
        logging.basicConfig(filename="mainController.log",
                            level=logging.DEBUG,
                            filemode="w",
                            format='%(asctime)s,%(levelname)s,%(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    except:
        print("Failed to open the log file")
        sys.exit()

    logging.info("The program has started")

    # Start the GUI
    app = QtGui.QApplication(sys.argv)
    gui = UI.UI()
    gui.show()
    app.exec_()

    logging.info("The program is done")
    sys.exit()







