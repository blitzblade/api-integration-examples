import psycopg2
import os
from config import Config

config = Config()


dbname=config.DB_NAME#os.getenv('DB_NAME',"bitcoin_db")
user=config.DB_USER#os.getenv('DB_USER',"postgres")
host=config.DB_HOST#os.getenv('DB_HOST',"localhost")
password=config.DB_PASSWORD#os.getenv('DB_PASSWORD',"postgres")

def get_db_cursor():
    conn = psycopg2.connect(
        "dbname={dbname} user={user} host={host} password={password}".format(
            dbname=dbname,user=user,host=host,password=password))

    cursor = conn.cursor()
    return cursor


# cursor = get_db_cursor()
# cursor.execute("select name from crypto_currencies")
# cryptos = [crypto[0] for crypto in cursor.fetchall()]
# print(cryptos)



