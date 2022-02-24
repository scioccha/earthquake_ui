import pandas as pd
import wikipediaapi
import datetime
import json
import subprocess

df = pd.read_csv("quake_data.csv")
one= df.loc[df['url']=='https://earthquake.usgs.gov/earthquakes/eventpage/us7000glex']


#def get_stuff(df, row):
#    s_date = df.iloc[row]['date']
#    enddate = ((pd.to_datetime(s_date) + pd.DateOffset(2)).date()).strftime('%Y-%m-%d')

#    search_term = "earthquake " + df.iloc[row]['city']
#    subprocess.run(['python', 'news_test.py', s_date, enddate, search_term])


def call_news_microservice(df, row):
    start_date = df.iloc[row]['date']
    end_date = ((pd.to_datetime(start_date) + pd.DateOffset(2)).date()).strftime('%Y-%m-%d')
    city = df.iloc[row]['city']
    region = df.iloc[row]['region']
    if city != region:
        search_term = "earthquake " + df.iloc[row]['city'] + " " + df.iloc[row]['region']
    else:
        search_term = "earthquake " + df.iloc[row]['region']
    subprocess.run(['python', 'news_test.py', start_date, end_date, search_term])


def read_news():
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
            
call_news_microservice(one, 0)
read_news()

#subprocess.run(['python', 'news_test.py', "2022-02-16", "2022-02-18", "earthquake the Fiji Islands"])