import mysql.connector
import logging
from mysql.connector.pooling import MySQLConnectionPool


class Database:
    def __init__(self, host, port, user, password, pool_size=5, pool_name='app_pool'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.pool_size = pool_size
        self.pool_name = pool_name
        self.pool = None
        self.connect()

    def connect(self):
        try:
            self.pool = MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
        except mysql.connector.Error as err:
            logging.error(f"Failed to connect to database: {err}")
            raise err

    def get_connection(self):
        return self.pool.get_connection()

    def create_database(self, database_name):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            conn.commit()
            cursor.close()
            conn.close()

            # set the connection to use the created database
            self.pool.set_config(database=database_name)

        except mysql.connector.Error as err:
            logging.error(f"Failed to create database: {err}")

    def create_counter_table(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            create_counter_table_query = """
            CREATE TABLE IF NOT EXISTS counter (
                id INT AUTO_INCREMENT PRIMARY KEY,
                count INT
            )
            """
            cursor.execute(create_counter_table_query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            logging.error(f"Failed to create table: {err}")

    def create_access_log_table(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            create_access_log_table_query = """
            CREATE TABLE IF NOT EXISTS access_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                access_time DATETIME NOT NULL,
                client_ip VARCHAR(50) NOT NULL,
                internal_ip VARCHAR(50) NOT NULL
            )
            """
            cursor.execute(create_access_log_table_query)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            logging.error(f"Failed to create access log table: {err}")

    def insert_initial_count(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO counter (count) VALUES (0)")
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            logging.error(f"Failed to insert initial count: {err}")

    def get_counter(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT count FROM counter")
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                return result[0]
            else:
                return -1
        except mysql.connector.Error as err:
            logging.error(f"Failed to get counter count: {err}")
            return -1

    def increment_counter(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            current_count = self.get_counter()
            new_count = current_count + 1
            cursor.execute("UPDATE counter SET count = %s", (new_count,))
            conn.commit()
            cursor.close()
            conn.close()
            return new_count
        except mysql.connector.Error as err:
            logging.error(f"Failed to increment counter: {err}")
            return current_count

    def record_access_log(self, access_time, client_ip, internal_ip):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO access_log (access_time, client_ip, internal_ip) VALUES (%s, %s, %s)"
            values = (access_time, client_ip, internal_ip)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            logging.error(f"Failed to record access log: {err}")

    def create_tables(self, database_name='app_db'):
        self.create_database(database_name)
        self.create_counter_table()
        self.create_access_log_table()
        if self.get_counter() < 0:
            self.insert_initial_count()
