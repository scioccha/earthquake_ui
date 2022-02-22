import pandas as pd
import wikipediaapi
import datetime

df = pd.read_csv("quake_data.csv")

one= df.loc[df['url']=='https://earthquake.usgs.gov/earthquakes/eventpage/us7000glex']

s_date = (one['date'])
teststart = s_date.to_string()

import pandas as pd
enddate = pd.to_datetime(s_date) + pd.DateOffset(days=5)

print(s_date)
newend = enddate.dt.strftime('%Y-%m-%d')
testend = newend.to_string()


import json


#print(new_data[0]['title'], new_data[0]['url'])

import subprocess
#subprocess.run(['python', 'news_test.py', "2022-02-15", "2022-02-18", "earthquake the Fiji Islands"])

subprocess.run(['python', 'news_test.py', teststart, testend, 'earthquake Polis Cyprus'])

def test_text():
    with open('news.txt') as f:
        raw_data = json.load(f)
        if raw_data['totalResults'] == 0:
            print("No recent news articles for this earthquake.")
            return

        new_data = raw_data['articles']
        for i in range(3):
            try:
                print(new_data[i]['title'], new_data[i]['url'])
            except IndexError:
                return

test_text()


