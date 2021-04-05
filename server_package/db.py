"""
Imports
"""
import mysql.connector
from mysql.connector import Error


class DBConnector:
    """
    Class which establishes the connection between the Controller and the MySQL Database
    The database will be running on a Docker image
    For now there is only a Create and a Read method
    """

    def __init__(self):
        with open('/run/secrets/db-password') as f:
            passwd = f.read()
        try:
            self.conn = mysql.connector.connect(host='mysql',
                                                database='db',
                                                user='root',
                                                password=passwd,
                                                port=3306)
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)

    def create(self, env: str, jsonrep: str):
        """
        Method which executes a given CREATE query on the current MySQL Database
        :param env: The current environment
        :param jsonrep: The json representation of the tree
        """
        cursor = self.conn.cursor()
        args = (env, jsonrep)
        query = "INSERT INTO db.reports (environment, tree_json) VALUES (%s, %s);"
        cursor.execute(query, args)
        self.conn.commit()
        cursor.close()

    def read(self) -> object:
        """
        Method which executes a given READ query on the current MySQL Database
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM db.reports;")
        self.conn.commit()
        res = cursor.fetchall()
        cursor.close()
        return res
