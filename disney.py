import requests

url = "https://api.disneyapi.dev/characters"
response = requests.get(url)
data = response.json()

print(data['data'][1]['tvShows'])
url2 = data['data'][1]['url']

print(url2)

