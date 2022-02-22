import requests
import json
from datetime import datetime

#get today's date
now = datetime.now()
today = now.strftime("%Y-%m-%d")


"""
:param search_term -> string
:param from_date -> string YYYY-MM-DD (cannot be before last 30 days unless you have paid subscription)
:param to_date -> string YYYY-MM-DD
"""
def getNews(from_date = "2022-01-15", to_date = today, search_term=None):
    api_key = "2d719755f6344ec081bb6f9e86aa1bf2"
    if search_term is None:
        search_term = "earthquake"
    search_term = search_term.lower()
    url = f'https://newsapi.org/v2/everything?q={search_term}&from={from_date}&to={to_date}&apiKey={api_key}'
    news = requests.get(url).json()

    for item in news['articles']:
        if search_term in item['title']:
            print(item['title'])
            print(item['url'])


    #To get news in a json file, uncomment the following
    json_object = json.dumps(news)
    file1 = open("news.txt", "w")
    file1.write(json_object)
    file1.close()

from sys import argv
if __name__ == "__main__":
    getNews(argv[1], argv[2], argv[3])

#getNews("2022-12-08", "2022-12-20", "earthquake Ferndale California")
#getNews("2022-02-15", "2022-02-18", "earthquake the Fiji Islands")