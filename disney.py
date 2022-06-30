import requests
#import sqlalchemy as db
#import pd

url = "https://api.disneyapi.dev/characters"
response = requests.get(url)
data = response.json()

print(data)
#pd.DataFrame.from_dict(data)

#engine = db.create_engine('sqlite:///data_base_name.db')
#dataframe_name.to_sql('table_name', con=engine, if_exists='replace', index=False)

#query_result = engine.execute("SELECT * FROM table;").fetchall()
#print(pd.DataFrame(query_result))

'''
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
'''
