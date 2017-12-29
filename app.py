from database import *
from scrape import *

cursor, connection = setup_connection_and_tables()

saved_coins = db_coins_saved(cursor)
online_coins = coinmarket_cap_coins()

coins_to_be_saved = [x for x in online_coins if x not in saved_coins]

for coin in coins_to_be_saved:
  save_coin_history(coin, cursor, connection)
