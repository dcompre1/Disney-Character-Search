import sqlalchemy as db
import disney_funcs
import pandas as pd

character_name = input("Please enter a character name: ")
while character_name.strip().isdigit():
    character_name = input("That is not a valid character name\
	, please enter a new name:")

#request to API
req_result = disney_funcs.make_get_request("https://api.disneyapi.dev/characters")
data = req_result[0]
pages = req_result[1]

#make dictionary of Disney data
dict_result = disney_funcs.make_dict(character_name, data, pages)
exists = dict_result[1]
new_data = dict_result[0]

if exists is False:
	print("The name you entered is not a Disney Character")
else:
	disneydf = pd.DataFrame.from_dict(new_data, orient='index', columns=['name', 'films', 'shortFilms', 'tvShows', 'videoGames'])
	engine = db.create_engine('sqlite:///Disney.db')
	disneydf.to_sql('disney_info', con=engine, if_exists='replace', index=False)

	#getting character information from database
	character_info = disney_funcs.retrieve_from_database(engine, character_name)
	films = character_info[0]
	short_films = character_info[1]
	tv_shows = character_info[2]
	video_games = character_info[3]

	#print information about character
	disney_funcs.print_info(character_name, films, short_films, tv_shows, video_games)
