import sqlite3
import requests

class DB_connector():
    def __init__(self, file_name, link_list):
        self.file_name = file_name
        connection = sqlite3.connect(file_name, 5)
        cur = connection.cursor()
        cur.execute("CREATE TABLE websites (link TEXT);")
        for el in link_list:
            com = "INSERT INTO websites (link) VALUES (?);"
            cur.execute(com, (el,))
        connection.commit()
        connection.close()
    def get_links(self):
        connection = sqlite3.connect(self.file_name, 5)
        cur = connection.cursor()
        cur.execute("SElECT link FROM websites;")
        connection.commit()
        res = cur.fetchall()
        return res

class Pages_analyzer():
    def __init__(self, DB_connector, query):
        self.DB_connector = DB_connector
        self.query = query

    def calculate_score(self, link):
        response = requests.get(link)
        text = response.text
        count = text.lower().count(self.query.lower())
        return count

    def get_scores(self):
        scores = {}
        links = DB_connector.get_links(self)
        for el in links:
            scores[el] = self.calculate_score(el)
        return scores

def run(file_name, link_list, query):
    DB_connector1 = DB_connector(file_name, link_list)
    Pages_analyzer1 = Pages_analyzer(DB_connector1, query)
    scores = Pages_analyzer1.get_scores()
    scores = dict(sorted(scores.items(), key=lambda item: item[1]))
    print(scores)


if __name__ == '__main__':
    link_list = ['https://pl.wikipedia.org/wiki/Pozna%C5%84', 'https://pl.wikipedia.org/wiki/Ziemniak',
                 'https://pl.wikipedia.org/wiki/Most']
    file_name = 'project.sl3'
    query = 'Poznan'
    run(file_name, link_list, query)


