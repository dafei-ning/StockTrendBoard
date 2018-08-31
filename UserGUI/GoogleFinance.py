import urllib.request
import datetime
import logging


class GoogleFinance:

    def __init__(self, symbol=None, start_date=None):
        """
        Class constructor
        """
        self.symbol = symbol
        self.start_date = start_date
        self.base_url = "https://finance.google.com/finance/historical?q="
        return

    def get_historical_stock_data(self, filename=None):

        today = datetime.datetime.today()
        URL = self.base_url + self.symbol
        URL += "&startdate=%s-%s-%s" % ("2017", "1", "4")
        URL += "&enddate=%s-%s-%s" % (today.year, today.month, today.day)
        URL += "&output=csv"

        self.URL = URL
        logging.info(URL)

        url_data = urllib.request.urlopen(URL)
        csv = (url_data.read()).decode("utf-8-sig").encode("utf-8")
        if filename != None:
            try:
                f = open(filename, "w")
                f.write(csv.decode("utf-8"))
                f.close()
            except:
                logging.error("Failed to open the file: ", filename)
        return




