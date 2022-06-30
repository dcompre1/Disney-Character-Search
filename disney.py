import requests
import sqlalchemy as db
import pandas as pd

character_name = input("Please enter a character name: ")
while character_name.strip().isdigit():
	character_name = input("That is not a valid character name, please enter a new name:")

#TODO: consider making these requests into a separate function
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
#TODO: consider making a function for this loop
exists = False
for i in range(pages):
	entry = data[i]
	name = entry['name']
	if exists == False and name == character_name:
		exists = True
	films = '\n'.join(entry['films'])
	shortFilms = '\n'.join(entry['shortFilms'])
	tvShows = '\n'.join(entry['tvShows'])
	videoGames = '\n'.join(entry['videoGames'])
	new_data[i] = [name, films, shortFilms, tvShows, videoGames]

if exists == False:
	print("The name you entered is not a Disney Character")
else:
	#TODO: make this into a function to create_database
	disneydf = pd.DataFrame.from_dict(new_data, orient='index', columns=['name', 'films', 'shortFilms', 'tvShows', 'videoGames'])

	engine = db.create_engine('sqlite:///Disney.db')
	disneydf.to_sql('disney_info', con=engine, if_exists='replace', index=False)

	#TODO: make a function to retrieve this data from database
	film_result = engine.execute("SELECT films FROM disney_info WHERE name = \'" + character_name + "\';").fetchall()
	s_film_result = engine.execute("SELECT shortFilms FROM disney_info WHERE name = \'" + character_name + "\';").fetchall()
	tv_result = engine.execute("SELECT tvShows FROM disney_info WHERE name = \'" + character_name + "\';").fetchall()
	game_result = engine.execute("SELECT videoGames FROM disney_info WHERE name = \'" + character_name + "\';").fetchall()

	#TODO: make a print function to do this 
	print(character_name + " appears in these films:\n" + pd.DataFrame(film_result)[0][0] + "\n")
	print(character_name + " appears in these short films:\n" + pd.DataFrame(s_film_result)[0][0] + "\n")
	print(character_name + " appears in these tv shows:\n" + pd.DataFrame(tv_result)[0][0] + "\n")
	print(character_name + " appears in these video games:\n" + pd.DataFrame(game_result)[0][0] + "\n")
