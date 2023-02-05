import requests
from bs4 import BeautifulSoup

xml = requests.get("http://weather.tsukumijima.net/primary_area.xml")
soup = BeautifulSoup(xml.text, "html.parser")
for city_id in soup.findAll("pref"):
  print(city_id.city)
