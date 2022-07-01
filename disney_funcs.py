import requests
import pandas as pd


def make_get_request(url):
    '''make request to Disney API'''
    response = requests.get(url)
    data = response.json()['data']
    pages = response.json()['totalPages']
    nextUrl = response.json()['nextPage']

    for i in range(148):
        response = requests.get(nextUrl)
        data = data + response.json()['data']
        if i == 147:
            break
        nextUrl = str(response.json()['nextPage'])
    return [data, pages]


def make_dict(character_name, data, pages):
    '''organize Disney data into a dictionary and find if character exists'''
    new_data = {}
    exists = 0
    for i in range(len(data)):
        entry = data[i]
        name = entry['name']
        if exists == 0 and name == character_name:
            exists = 1
        films = '\n'.join(entry['films'])
        shortFilms = '\n'.join(entry['shortFilms'])
        tvShows = '\n'.join(entry['tvShows'])
        videoGames = '\n'.join(entry['videoGames'])
        new_data[i] = [name, films, shortFilms, tvShows, videoGames]

    return [new_data, exists]


def print_info(character_name, films, short_films, tv_shows, games):
    '''print character information'''
    print(character_name + " appears in these films:\n" + films + "\n")
    print(character_name + " appears in these short films:\n" +
          short_films + "\n")
    print(character_name + " appears in these tv shows:\n" + tv_shows + "\n")
    print(character_name + " appears in these video games:\n" + games + "\n")


def retrieve_from_database(engine, character_name):
    '''queries to database'''
    film_result = engine.execute("SELECT films FROM disney_info WHERE" +
                                 " name = \'" + character_name +
                                 "\';").fetchall()
    s_film_result = engine.execute("SELECT shortFilms FROM disney_info WHERE" +
                                   " name = \'" + character_name +
                                   "\';").fetchall()
    tv_result = engine.execute("SELECT tvShows FROM disney_info WHERE" +
                               " name = \'" + character_name +
                               "\';").fetchall()
    game_result = engine.execute("SELECT videoGames FROM disney_info WHERE" +
                                 " name = \'" + character_name +
                                 "\';").fetchall()
    return [pd.DataFrame(film_result)[0][0], pd.DataFrame(s_film_result)[0][0],
            pd.DataFrame(tv_result)[0][0], pd.DataFrame(game_result)[0][0]]
