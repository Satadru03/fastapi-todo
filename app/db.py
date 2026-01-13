import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host = "localhost",
        database = "company_db",
        user = "postgres",
        password = "123@Password"
    )
    return conn