import logging
import psycopg2


class Postgres:

    def __init__(self, database=None, user=None, password=None):
        """
        This is the class constructor
        """
        self.database = database
        self.user = user
        self.password = password
        self._ready = False
        self.cursor = None
        self.conn = None
        return

    def connect(self):
        """
        This method handles connecting to the database and obtaining a cursor
        """
        try:
            self.conn = psycopg2.connect(dbname=self.database, user=self.user, password=self.password)
            self.cursor = self.conn.cursor()
            self._ready = True
        except:
            self._ready = False

        return self._ready

    def executeCommand(self, command):
        """
        This method executes and commits the SQL statements
        """
        if self._ready is False:
            logging.info("Not ready")
            return None
        logging.info(command)
        try:
            self.cursor.execute(command)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def createTable(self, table_name=None, table_list=[]):
        """
        This method can be used to create a table in the database
        """
        if (self._ready is False) or (table_name is None) or (len(table_list) == 0):
            return False

        table_string = """CREATE TABLE %s (""" % table_name
        for element in table_list:
            table_string += "%s %s," % (element[0], element[1])

        table_string = table_string[:-1]
        table_string += ");"

        return self.executeCommand(table_string)

    def insertData(self, table_name=None, values=None):
        """
        This method will insert one row of data into the database
        """
        if (table_name is None) or (self._ready is False):
            return False

        data_string = """INSERT INTO %s """ % table_name
        data_string += "VALUES(" "'%s', '%s'" ");" % (values[0], values[1])
        return self.executeCommand(data_string)

    def queryAllData(self, table_name=None):
        """
        This method will return all data from the table
        """
        if (table_name is None) or (self._ready is False):
            return

        data_string = """SELECT * FROM %s;""" % table_name
        self.executeCommand(data_string)

        if self.cursor.rowcount != 0:
            return self.cursor.fetchall()
        logging.error("Failed to query all data on " + table_name)
        return None

    def querySpecificData(self, table_name, query_data):
        """
        This method will return specific data from the table
        """
        if (table_name is None) or (self._ready is False) or (query_data is None):
            return

        data_string = """SELECT * FROM %s WHERE symbol = '%s';""" % (table_name, query_data)
        self.executeCommand(data_string)

        if self.cursor.rowcount != 0:
            return self.cursor.fetchone()
        logging.error("Failed to query %s on %s" % (query_data, table_name))
        return None





















