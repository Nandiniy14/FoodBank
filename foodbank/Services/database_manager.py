import psycopg2
import psycopg2.extras
class DatabaseManager:
    @classmethod
    def database_connection(cls):
        conn = psycopg2.connect(database="foodbank", user = "postgres", password = "postgres", host = "localhost")
        return conn
