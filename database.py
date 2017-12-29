import sqlite3
import pandas as pd

def setup_connection_and_tables():
  conn = sqlite3.connect("histories.db")
  cur = conn.cursor()

  create_coins = "CREATE TABLE IF NOT EXISTS coins (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR);"
  create_histories = "CREATE TABLE IF NOT EXISTS histories (id INTEGER PRIMARY KEY AUTOINCREMENT, history_date DATE, open REAL, high REAL, low REAL, close REAL, volume INTEGER, market_cap INTEGER, coin_id INTEGER);"
  cur.execute(create_coins)
  cur.execute(create_histories)

  return cur, conn

def db_coins_saved(cursor):
  select_coins = "SELECT name FROM coins"
  saved_coins = cursor.execute(select_coins).fetchall()
  return [x[0] for x in saved_coins]

def save_coin_history(coin, cursor, conn):
  df = pd.read_html("https://coinmarketcap.com/currencies/%s/historical-data/?start=20120428&end=20171227" % coin, parse_dates=["Date"])[0]

  cursor.execute("INSERT INTO coins('name') VALUES('%s')" % coin)
  conn.commit()

  df.columns = ['history_date', 'open', 'high', 'low', 'close', 'volume', 'market_cap']

  df['coin_id'] = cursor.lastrowid
  df.to_sql('histories', conn, index=False, if_exists='append')
  print("Added coin: %s" % coin)
