import logging
from PyQt4 import QtCore
from PyQt4 import QtGui
import UI_about
import UI_central
import configparser
import sys
import time
import GoogleFinance
import Postgres
import requests
import bs4
import datetime


class UI(QtGui.QMainWindow):

    def __init__(self, parent=None, configuration=None):
        """
        UI constructor
        :param parent:
        :param configuration:
        """
        super(UI, self).__init__(parent)
        self.configuration = configuration

        # Create menu bar, file menu and help menu.
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        helpmenu = menubar.addMenu("&Help")

        # Create an exit action.
        exitAction = QtGui.QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Exit Application")
        filemenu.addAction(exitAction)
        exitAction.triggered.connect(QtGui.qApp.quit)

        # Create an about action.
        aboutAction = QtGui.QAction("&About", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutAction.setStatusTip("About")
        helpmenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.aboutAction)

        # Create a toolbar.
        self.toolbar = self.addToolBar("Exit")
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(aboutAction)

        # Set window title, size and show it.
        self.setWindowTitle("Learning Python Lab 9")
        self.resize(1000, 800)
        self.show()

        # Create UI_central instance.
        self.central = UI_central.UI_central()

        # Connect pushbutton to the method when clicked.
        self.connect(self.central.button, QtCore.SIGNAL("clicked()"), self.addButtonClicked)
        self.connect(self.central.button1, QtCore.SIGNAL("clicked()"), self.stockButtonClicked)

        # Set central widget.
        self.setCentralWidget(self.central)

        # Obtain the password and create a db instance.
        # password = os.getenv('PASSWORD')
        self.db = Postgres.Postgres(database="postgres", user="postgres", password="python")

        # Connect to the database.
        if self.db.connect() is False:
            logging.error("db connect failed")
            sys.exit()

        # Create a table.
        try:
            self.db.createTable(table_name="know_stocks", table_list=[("SYMBOL", "text"), ("SHARES", "integer")])
        except:
            logging.error("Failed to create the table know_stocks")
            sys.exit()

        # Get the entire know_stock table as a list with tuple elements and add stock symbol to combobox.
        l = self.db.queryAllData(table_name="know_stocks")

        try:
            for element in l:
                stock_symbol = element[0]
                self.central.combobox.addItem(stock_symbol)
        except:
            return

    def aboutAction(self):
        """
        Display the ABOUT GUI.
        """
        about = UI_about.UI_about()
        about.exec_()

        return

    def addButtonClicked(self):
        """
        When the Add button clicked, use this method.
        """
        # Get the date and convert it to a string.
        date = self.central.calendar.selectedDate()
        datestring = "{0} {1} {2}".format(date.day(), date.longMonthName(date.month()), date.year())

        # Get the stock symbol and convert it to upper case.
        stock = self.central.text1.text()
        stocksymbol = str(stock.upper())

        # Get the number of shares and convert it to integer.
        shares = self.central.text2.text()
        try:
            sharenumber = int(shares)
            if sharenumber < 0:
                sharenumber = 0
        except:
            sharenumber = 0

        # Parse the stock configuration file.
        config = configparser.ConfigParser()
        config.read("stocks.cfg")
        if config.has_section(stocksymbol):
            print("Configuration file already has this stock symbol:", stocksymbol)
            logging.info("Configuration file already has this stock symbol: " + stocksymbol)
        else:
            config.add_section(stocksymbol)
            config.set(stocksymbol, "SHARES", str(sharenumber))
            config.set(stocksymbol, "DATE", datestring)
            print("Stock added:", str(sharenumber), "shares of", stocksymbol, "on", datestring)
            logging.info("Stock added:" + str(sharenumber) + " shares of " + stocksymbol + " on " + datestring)

        # Safely open the stocks.cfg file for writing.
        try:
            with open("stocks.cfg", "w") as configfile:
                config.write(configfile)
        except:
            logging.error("Failed to write in the stocks.cfg file." + str(sharenumber) + "shares of" +
                          stocksymbol + "on" + datestring)
            sys.exit()

        # Convert date string to struct time.
        struct_time = time.strptime(datestring, "%d %B %Y")

        # Create an instance of GoogleFinance class.
        i = GoogleFinance.GoogleFinance(stocksymbol, struct_time)

        # Create a filename and call the get historical stock data method.
        filename = stocksymbol + ".csv"
        i.get_historical_stock_data(filename)

        # Create a table for the stock.
        try:
            self.db.createTable(table_name=stocksymbol, table_list=[("DATE", "date"), ("STOCK_PRICE", "money")])
        except:
            logging.error("Failed to create the table: " + stocksymbol)

        # Open and read the csv file downloaded. Insert data into the stock table.
        try:
            f = open(filename, "r")
            lines = f.readlines()
            for eachline in lines:
                list = eachline.split(',')
                if list[0] != "DATE":
                    self.db.insertData(table_name=stocksymbol, values=(list[0], list[4]))
        except:
            logging.error("Failed to open the file: " + filename)

        # Insert data into know_stocks table.
        self.db.insertData(table_name="know_stocks", values=(stocksymbol, str(sharenumber)))

        # Add stock symbol to the combobox.
        self.central.combobox.addItem(stocksymbol)

    def stockButtonClicked(self):
        """
        When the Display Officers button clicked, use this method.
        """
        # Clear text edit box and get the stock symbol from combobox.
        self.central.text3.clear()
        stocksymbol = self.central.combobox.currentText()

        URL = 'https://finance.yahoo.com/quote/{0}/profile?p={0}'.format(stocksymbol)

        # Safely get the web page using the above URL.
        try:
            r = requests.get(URL)
        except:
            logging.error("Failed to get the web page: " + URL)
            self.central.text3.setText("Failed to get the web page: " + URL)
            return

        # Safely turn the response from requests into soup.
        try:
            html = r.text.encode('utf-8')
            soup = bs4.BeautifulSoup(html, 'lxml')
        except:
            logging.error("Failed on the soup")
            self.central.text3.setText("Failed on the soup")
            return

        # Safely extract data from the table.
        try:
            table = soup.find_all("table")
            rows = table[0].find_all('tr')
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [str.text.strip() for str in cols]
                data.append([str for str in cols if str])

            textdisplay = ''

            for x in data:
                for y in x:
                    print(y)
                    textdisplay += y
                    textdisplay += '\n'
                    if y.isdigit():
                        textdisplay += '\n'
            self.central.text3.setText(textdisplay)

        except:
            logging.error("Failed to extract data from the table")
            self.central.text3.setText("Failed to extract data from the table")
            return

        self.updateGraph(symbol=stocksymbol)

    def updateGraph(self, symbol=None):
        """
        This method will update the graph when a new stock is chosen.
        """
        if symbol is None:
            return

        # Get all stock data back for the given symbol
        self.stock_data = self.db.queryAllData(table_name=symbol)

        # Create a list of prices and a list of dates
        self.prices = [x[1].strip('$') for x in self.stock_data]
        self.dates = [x[0] for x in self.stock_data]
        date_string = [x.strftime("%m/%d/%Y") for x in self.dates]
        self.x = [datetime.datetime.strptime(d, '%m/%d/%Y').date()
                  for d in date_string]

        # Create an instance of QtMpl
        self.mpl = self.central.mpl
        self.mpl.addLine(x=self.x, y=self.prices, title=symbol)

























