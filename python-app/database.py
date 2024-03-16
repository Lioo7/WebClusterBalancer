import mysql.connector
import logging


class Database:
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
            )
            self.cursor = self.connection.cursor()
            self.create_database('app_db')
            self.create_counter_table()
            self.create_access_log_table()
            if self.get_counter() == 0:
                self.insert_initial_count()
        except mysql.connector.Error as err:
            logging.error(f"Failed to connect to database: {err}")
            raise err

    def create_database(self, database_name):
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            self.connection.database = database_name
        except mysql.connector.Error as err:
            logging.error(f"Failed to create database: {err}")

    def create_counter_table(self):
        try:
            create_counter_table_query = """
            CREATE TABLE IF NOT EXISTS counter (
                id INT AUTO_INCREMENT PRIMARY KEY,
                count INT
            )
            """
            self.cursor.execute(create_counter_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Failed to create table: {err}")

    def create_access_log_table(self):
        try:
            create_access_log_table_query = """
            CREATE TABLE IF NOT EXISTS access_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                access_time DATETIME NOT NULL,
                client_ip VARCHAR(50) NOT NULL,
                internal_ip VARCHAR(50) NOT NULL
            )
            """
            self.cursor.execute(create_access_log_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Failed to create access log table: {err}")

    def insert_initial_count(self):
        try:
            self.cursor.execute("INSERT INTO counter (count) VALUES (0)")
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Failed to insert initial count: {err}")

    def get_counter(self):
        try:
            self.cursor.execute("SELECT count FROM counter")
            result = self.cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
        except mysql.connector.Error as err:
            logging.error(f"Failed to get counter count: {err}")
            return 0

    def increment_counter(self):
        try:
            current_count = self.get_counter()
            new_count = current_count + 1
            self.cursor.execute("UPDATE counter SET count = %s", (new_count,))
            self.connection.commit()
            return new_count
        except mysql.connector.Error as err:
            logging.error(f"Failed to increment counter: {err}")
            return current_count

    def record_access_log(self, access_time, client_ip, internal_ip):
        try:
            query = "INSERT INTO access_log (access_time, client_ip, internal_ip) VALUES (%s, %s, %s)"
            values = (access_time, client_ip, internal_ip)
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            logging.error(f"Failed to record access log: {err}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except mysql.connector.Error as err:
            logging.error(f"Failed to close database connection: {err}")
