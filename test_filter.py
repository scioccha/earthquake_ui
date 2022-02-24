import pandas as pd
import wikipediaapi
import datetime
import json
import subprocess

df = pd.read_csv("quake_data.csv")

one= df.loc[df['url']=='https://earthquake.usgs.gov/earthquakes/eventpage/us7000glex']

s_date = one.iloc[0]['date']
enddate = ((pd.to_datetime(s_date) + pd.DateOffset(2)).date()).strftime('%Y-%m-%d')
print(s_date)
print(enddate)


#testend = enddate.strftime('%Y-%m-%d')

#print(testend)


#subprocess.run(['python', 'news_test.py', "2022-02-16", "2022-02-18", "earthquake the Fiji Islands"])

subprocess.run(['python', 'news_test.py', s_date, enddate, 'earthquake the Fiji Islands'])

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


