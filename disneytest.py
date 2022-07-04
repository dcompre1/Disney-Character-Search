import unittest
from disney_funcs import make_get_request, make_dict, retrieve_from_database
import sqlalchemy as db

url = "https://api.disneyapi.dev/characters"
my_dict = [{"films": ["afilm1", "afilm2", "afilm3"],
            "shortFilms": ["asFilm1", "asFilm2"],
            "tvShows":["aShow1", "aShow2"],
            "videoGames": ["avg1", "avg2", "avg3"],
            "name":"characterA"},
           {"films": ["bfilm1"],
            "shortFilms": [],
            "tvShows":["bShow1", "bShow2"],
            "videoGames": ["bvg1"],
            "name":"characterB"},
           {"films": [],
            "shortFilms": [],
            "tvShows":["cShow1", "cShow2"],
            "videoGames": [],
            "name":"characterC"}]
new_dict = {0: ["characterA", "afilm1\nafilm2\nafilm3",
                "asFilm1\nasFilm2", "aShow1\naShow2",
                "avg1\navg2\navg3"],
            1: ["characterB", "bfilm1", "",
                "bShow1\nbShow2", "bvg1"],
            2: ["characterC", "",
                "",
                "cShow1\ncShow2", ""]}
char1 = "characterA"
char2 = "characterB"
char3 = "characterC"
char4 = "characterD"


class disneytest(unittest.TestCase):
    def test_make_get_request(self):
        result = make_get_request(url)
        self.assertEqual(result[1], 149)

    def test_make_dict(self):
        result = make_dict(char1, my_dict)
        self.assertEqual(result[1], 1)
        self.assertEqual(result[0], new_dict)
        result = make_dict(char4, my_dict)
        self.assertEqual(result[1], 0)

    def test_retrieve_from_database(self):
        engine = db.create_engine('sqlite:///Disney.db')
        info = retrieve_from_database(engine, "Cinderella")
        self.assertEqual(info[0], "Rodgers & Hammerstein's Cinderella")
        info = retrieve_from_database(engine, "Billy, Goat, and Gruff")
        self.assertEqual(info[1], "Lamp Life")
        info = retrieve_from_database(engine, "Little John")
        self.assertEqual(info[3], "Disney Emoji Blitz")
        info = retrieve_from_database(engine, "Zeus")
        self.assertEqual(info[2], "DuckTales (2017 series)")


if __name__ == '__main__':
    unittest.main()
