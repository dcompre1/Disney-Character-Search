import requests

url = "https://api.disneyapi.dev/characters"
response = requests.get(url)
data = response.json()

for i in range(10):
    film = data['data'][i]['films']
    tv = data['data'][i]['tvShows']
    if len(tv) == 0:
        continue
    else:
        print(str(data['data'][i]['name']) + " appears in " + str(tv))
    if len(film) == 0:
        continue
    else:
        print(str(data['data'][i]['name']) + " appears in " + str(film))
