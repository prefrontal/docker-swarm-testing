from time import sleep
import requests

url = "http://X.X.X.X:Y"

while True:
	data = requests.get(url)
	print(data.text)
	sleep(0.1)
