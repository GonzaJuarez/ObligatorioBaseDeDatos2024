import pymysql

from API.env import MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE

connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    port=int(MYSQL_PORT),
)
try:
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE};")
    connection.commit()
except Exception as e:
    print(f"Ocurrió un error: {e}")

