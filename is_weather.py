import requests

class WeatherResponder:
  def __init__(self):
    with open("data/place_code.txt", "r", encoding="utf_8")as file:
      lines = file.readlines()

    new_lines = []
    for line in lines:
      line = line.rstrip("\n")
      if (line != ""):
        new_lines.append(line)
    separate = []
    for line in new_lines:
      sp = line.split("\t")
      separate.append(sp)
    self.place_code = dict(separate)

  def is_weather(self, place):
    if place in self.place_code:
      return self.get_weather(self.place_code[place])

    else:
      return("そこはわかんねえべ")

  def get_weather(self, code):
    url = "http://weather.tsukumijima.net/api/forecast"
    payload = { "city": code }
    weather_data = requests.get(url, params = payload).json()
    forecast = "天気予報だよぉ～～～～\n"
    for weather in weather_data["forecasts"]:
      forecast += ("\n"
      + weather["dateLabel"] + "の天気は" + weather["telop"]
      )
    return forecast
