"""
Create a class to check MySQL connectivity.
"""
import mysql.connector

class MySQLCheck:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def check_connection(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if conn.is_connected():
                print("Connected to MySQL database")
                return True
            else:
                print("Failed to connect to MySQL database")
                return False
        except mysql.connector.Error as error:
            print("Failed to connect to MySQL database: {}".format(error))
            return False
if __name__ == "__main__":
    host = "localhost"
    user = "root"
    password = "123456"
    database = "test"
    my_check = MySQLCheck(host, user, password, database)
    my_check.check_connection()