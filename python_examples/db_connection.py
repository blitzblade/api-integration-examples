import psycopg2
dbname="bitcoin_db"
user="postgres"
host="localhost"
password="postgres"

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



