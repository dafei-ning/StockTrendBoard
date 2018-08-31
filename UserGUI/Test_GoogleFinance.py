import time
import logging
import nose
import GoogleFinance
import os


class Test_GoogleFinance:

    def __init__(self):
        """
        Class constructor
        """
        self.logcapture = nose.plugins.logcapture.LogCapture()
        self.logcapture.start()
        logging.basicConfig(filename="testlog.log",
                            level=logging.DEBUG,
                            filemode='w',
                            format='%(asctime)s,%(levelname)s,%(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        pass

    def setup(self):
        self.logcapture.begin()
        self.Teststart_date = time.strptime("30 October 2014", "%d %B %Y")
        self.i = GoogleFinance.GoogleFinance(symbol="goog", start_date=self.Teststart_date)

        #  the setup above give the following tests 3 answers to test:
        #  start_date: 2014-10-30 in structured format
        #  symbol: goog
        #  base_URL: "http://www.google.com/finance/historical?q="

    def teardown(self):
        self.logcapture.end()
        del(self.Teststart_date)
        del(self.i)
        logging.info("logcapture: %s " % (self.logcapture.formatLogRecords()))

    def test_ctor(self):
        """
        Test the constructor
        """
        assert self.i.symbol == "GOOG"
        assert self.i.start_date.tm_year == 2014
        assert self.i.start_date.tm_month == 10
        assert self.i.start_date.tm_date == 30

    def test_stock(self):
        """
        Test the get_historical_stock_data method
        """

        # Test when there is a correct filename
        filename_fortest = self.i.symbol + ".csv"
        try:
            self.i.get_historical_stock_data(filename_fortest)
            dir = os.path.join(os.getcwd(), filename_fortest)
            assert os.path.exists(dir)
        except:
            assert False

        # Test when the filename is None
        filename_fortest2 = None
        try:
            self.i.get_historical_stock_data(filename_fortest2)
            assert True
        except:
            assert False

        # Test when there is a wrong filename(with a wrong file type to open)
        filename_fortest3 = ""
        try:
            self.i.get_historical_stock_data(filename_fortest3)
            assert True
        except:
            assert False





