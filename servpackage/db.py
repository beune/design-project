"""
Imports
"""
import mysql.connector
from mysql.connector import Error


class DBConnector:
    """
    Class which establishes the connection between the Controller and the MySQL Database
    The database will be running on a Docker image
    Queries are used using the CRUD convention (CREATE, READ, UPDATE, DELETE)
    """

    def __init__(self):
        self.conn = None
        with open('../password.txt') as f:
            passwd = f.read()
        try:
            self.conn = mysql.connector.connect(host='localhost',
                                                database='db',
                                                user='root',
                                                password=passwd,
                                                port=3306)
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)

    def create(self, query: str) -> None:
        """
        Method which executes a given CREATE query on the current MySQL Database
        :param query: The create query that needs to be executed on the database
        """

    def read(self, query: str) -> object:
        """
        Method which executes a given READ query on the current MySQL Database
        :param query: The read query that needs to be executed on the database
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()

    def update(self, query: str) -> None:
        """
        Method which executes a given UPDATE query on the current MySQL Database
        :param query: The update query that needs to be executed on the database
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def delete(self, query: str) -> None:
        """
        Method which executes a given DELETE query on the current MySQL Database
        :param query: The delete query that needs to be executed on the database
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


if __name__ == "__main__":
    db = DBConnector()
    db.update("INSERT INTO reports (report_text) VALUES ('TESTSTRING')")
