import sys
import os
import flask
import jinja2
import Postgres


# Collection of global variables
app = flask.Flask(__name__)
env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, 'templates'))
app.secret_key = 'RaNdOmVaLuE520'

# Create a postgres instance db
password = os.getenv('PASSWORD')
db = Postgres.Postgres(database="postgres", user="postgres", password="python")

if db.connect() is False:
        sys.exit(1)


def ask_for_stocks():
    """
    This method will display the ask_stocks page
    """
    template = env.get_template('ask_stocks.html')
    html = template.render(ADDR=flask.request.environ['REMOTE_ADDR'],
                           CLIENT=flask.request.environ['HTTP_USER_AGENT'])
    return html


def have_this_stocks(stock):
    """
    This method will let us know if the database has this stock
    """
    stock = str(stock)
    try:
        j = db.querySpecificData(table_name="know_stocks", query_data=stock)
        if j == None or j == False:
            return False
        return True
    except:
        print("Failed to know if this stock exits in the database")
        return False


def get_stock_data(stock):
    """
    This method will return the stock information from the database
    """
    stock = str(stock)
    try:
        DATA = db.queryAllData(table_name=stock)
        return DATA
    except:
        print("Failed to get the stock data from the database")
        return False


def display_historical_stocks():
    """
    This method will display the stock information
    """
    stock_symbol = str(flask.request.form['SYMBOL'])
    stock_symbol = stock_symbol.upper()

    if have_this_stocks(stock_symbol) is False:
        template = env.get_template('error.html')
        html = template.render(ERROR="Error: The stock " '%s ' "doesn't exist in the know_stocks table" % stock_symbol,
                               ADDR=flask.request.environ['REMOTE_ADDR'],
                               CLIENT=flask.request.environ['HTTP_USER_AGENT'])
        return html
    else:
        if get_stock_data(stock_symbol) is False:
            template = env.get_template('error.html')
            html = template.render(ERROR="Error: Unable to obtain " '%s ' "data" % stock_symbol,
                                   ADDR=flask.request.environ['REMOTE_ADDR'],
                                   CLIENT=flask.request.environ['HTTP_USER_AGENT'])
            return html
        else:
            DATA = get_stock_data(stock_symbol)
            template = env.get_template('display_stocks.html')
            html = template.render(USER=stock_symbol,
                                   DATA=DATA,
                                   ADDR=flask.request.environ['REMOTE_ADDR'],
                                   CLIENT=flask.request.environ['HTTP_USER_AGENT'])
            return html


@app.route('/', methods=['GET', 'POST'])
def front_page():
    """
    This method will show the front page
    """
    if flask.request.method == 'POST':
        html = display_historical_stocks()
    else:
        html = ask_for_stocks()
    return html


@app.errorhandler(404)
def page_not_found(error=None):
    """
    This method will handle 404 error
    """
    template = env.get_template('error.html')
    html = template.render(ERROR="Error: 404",
                           ADDR=flask.request.environ['REMOTE_ADDR'],
                           CLIENT=flask.request.environ['HTTP_USER_AGENT'])
    return html


if __name__ == "__main__":
    """
    Application entry point
    """
    use_debugger = True
    app.run(debug=True)










