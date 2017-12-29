import requests
from bs4 import BeautifulSoup

def coinmarket_cap_coins():
  response = requests.get("https://coinmarketcap.com/all/views/all")
  soup = BeautifulSoup(response.text, "lxml")
  links = soup.select('.currency-name-container')

  get_href = lambda x: x.get('href').split('/')[-2]

  return [get_href(coin) for coin in links]
