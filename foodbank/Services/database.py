import psycopg2
import psycopg2.extras
class DatabaseConnection:
    @classmethod
    def databaseConnection(cls):
        conn = psycopg2.connect(database="foodbank", user = "postgres", password = "postgres", host = "localhost")
        return conn
