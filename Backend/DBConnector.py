import mysql.connector
from mysql.connector import Error


class DBConnector:

    def __init__(self):
        self.conn = None
        try:
            self.conn = mysql.connector.connect(host='localhost',
                                                database='newdb',
                                                user='root',
                                                password='dockertest123+')
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
