"""
Imports
"""
import mysql.connector
from mysql.connector import Error


class DBConnector:
    """
    Class which establishes the connection between the Controller and the MySQL Database
    The database will be running on a Docker image
    """
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

    def execute_query(self, query: str):
        """
        Method which executes a given query on the current MySQL Database
        :param query: The query that needs to be executed on the database
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
