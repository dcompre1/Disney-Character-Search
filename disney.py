import requests
import sqlalchemy as db
import pandas as pd

#USER CAN ENTER A CHARACTERS NAME AND RECEIVE ALL THE INFO ABOUT THE CHARACTER
#TODO: MODULARIZE DIFF PARTS LIKE DATABASE STUFF, USER INPUT, PRINT OUTPUT, GET DATA CAN ALL BE FUNCTIONS DUDE 
#character_name = input("Please enter a character name: ")
#TODO: VALIDATE USER INPUT, MAKES SURE ITS A STRING

url = "https://api.disneyapi.dev/characters"
response = requests.get(url)
data = response.json()['data']
pages = response.json()['totalPages']
nextUrl = response.json()['nextPage']

for i in range(pages - 2):
	response = requests.get(nextUrl)
	data = data + response.json()['data']
	nextUrl = str(response.json()['nextPage'])

#reorganize data into a dictionary 
new_data = {}
#make values lists, put category names into database as columns
for i in range(7):
	entry = data[i]
	films = ' '.join(entry['films'])
	shortFilms = ' '.join(entry['shortFilms'])
	tvShows = ' '.join(entry['tvShows'])
	videoGames = ' '.join(entry['videoGames'])
	parkAttractions = ' '.join(entry['parkAttractions'])
	allies = ' '.join(entry['allies'])
	enemies = ' '.join(entry['enemies'])
	name = entry['name']
	del entry['url']
	del entry['imageUrl']
	del entry['_id']
	del entry['name']
	new_data[name] = [films, shortFilms, tvShows, videoGames, parkAttractions, allies, enemies]

print(new_data)

#TODO: make this into a function to create_database
disneydf = pd.DataFrame.from_dict(new_data, orient='index', columns=['films', 'shortFilms', 'tvShows', 'videoGames', 'parkAttractions', 'allies', 'enemies'])

engine = db.create_engine('sqlite:///Disney.db')
disneydf.to_sql('disney_info', con=engine, if_exists='replace', index=False)

query_result = engine.execute("SELECT * FROM disney_info;").fetchall()
#print(pd.DataFrame(query_result))

