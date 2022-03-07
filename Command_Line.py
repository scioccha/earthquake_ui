# Programmer: Alexandra Sciocchetti
# Course: CS 361
# Description: Command Line User Interface for Earthquake History database program


import pandas as pd
import datetime
import os
import subprocess
import json

#First Microservice: Calls and runs GetJSON.py to create the earthquake csv file
os.system('/Users/ascio/anaconda3/python.exe GetJSON.py')

#Print Welcome Messages (this is like the header to a homepage if it were a GUI)
print("Welcome to the Earthquake History. We are a database containing information "
      "about all significant (> 6.5 magnitude) earthquakes since 1970")
print("All earthquake data is sourced directly from the USGS Earthquake Database")
print(" ")
print("How would you like to start?")

def start():
    """
    Displays start menu options.
    """
    print("1. Search for past earthquakes in my region")
    print("2. Learn about recent significant earthquakes around the world")
    print("3. Exit App")
    start = input("Type in the number next to the selected option: ")
    if start == "1":
        past_earthquake_option()
    elif start == "2":
        recent_sig_option()
    elif start == "3":
        exit_app()

def exit_app():
    """
    Called from start() function when users want to exit the app. Displays exit message
    """
    print("Thanks for visiting, goodbye!")

def past_earthquake_option():
    """
    Gathers and displays data if users select the option to input a location and learn about past
    earthquakes in that location. Reads quake_data.csv, searches for location, returns search results,
    and provides users with possible next step options.
    """
    print("Input your city, state, or country (if outside the US) to search for past earthquakes, ")
    location = input("or input 'back' to return to the main menu: ")
    if location == 'back':
        start()
    df = pd.read_csv("quake_data.csv")
    region_df = df.loc[df['region']==location]
    if len(region_df) > 0:
        earthquake_rough_details(region_df, 1, location)
    elif len(region_df) == 0:
        city_df = df.loc[df['city']==location]
        if len(city_df)>0:
            earthquake_rough_details(city_df, 1, location)
    else:
        print("There have been no recorded earthquakes greater than 6.5 magnitude in ",location," since the year 1970")
        next_action = input("Enter a 1 to enter a different location, enter 'back' to return to the main menu: ")
        if next_action == "1":
            past_earthquake_option()
        else:
            start()


def recent_sig_option():
    """
    Function is called if users select the option to learn about recent significant earthquakes.
    Reads the quake data, calculates the date 30 days ago, and calls the earthquake_rough_details
    method.
    """
    df = pd.read_csv("quake_data.csv")
    start_date = (datetime.datetime.now() - datetime.timedelta(30)).date()
    thirty_days = df[(df['date']> str(start_date))]
    print("There were",len(thirty_days), "earthquakes of over 6.5 magnitude within the last thirty days.")
    print(" ")
    earthquake_rough_details(thirty_days, 0, None)


def earthquake_rough_details(df, criteria, location = None):
    """
    Takes a pandas dataframe and displays date, magnitude, and location for each earthquake (row). Criteria
     argument is used to display the appropriate message. Prints earthquake info and asks user to input the desired
     next step.
     """
    if criteria == 0:
        print("Here is some information about those earthquakes")
        print(" ")
    if criteria == 1:
        print("The following large earthquakes occurred near", location, "since the year 1970")
    for row in range(len(df)):
        print(row+1,'. Date:',df.iloc[row]['date'],'Magnitude:',df.iloc[row]['magnitude'], "Location:", df.iloc[row]['place'])
    print(" ")
    print("Would you like to learn more about any of these earthquakes?")
    next_step = input("Enter the number next to the earthquake to get more information about that specific event, or "
          "enter 'back' to return to the main menu: ")
    if next_step == "back":
        start()
    else:
        row = int(next_step)-1
        earthquake_in_depth(df, row, criteria, location)

def call_map_microservice(df, row):
    """
    Takes as parameters at pandas dataframe and a specified row, and returns a url with the correct coordinates
    that correspond to the earthquake in that row. URL is used to access map microservice
    """
    lat = str(df.iloc[row]['latitude'])
    long = str(df.iloc[row]['longitude'])
    localhost = 'http://localhost:5000/microservice/map/'
    url = localhost+lat+'&'+long
    return url


def call_news_microservice(df, row):
    """Takes as parameters a pandas dataframe and a specified row (int), formats google search parameters
    based on the location of the earthquake in the specified row, and calls news microservice using the
    search parameters"""
    start_date = df.iloc[row]['date']
    end_date = ((pd.to_datetime(start_date) + pd.DateOffset(2)).date()).strftime('%Y-%m-%d')
    city = df.iloc[row]['city']
    region = df.iloc[row]['region']
    #Check to see if the recorded city is the same as the region, if so, only include the region in the search term
    if city != region:
        search_term = "earthquake " + df.iloc[row]['city'] + " " + df.iloc[row]['region']
    else:
        search_term = "earthquake " + df.iloc[row]['region']
    #Call news microservice through subprocess call. Specify language, program, arguments
    subprocess.run(['python', 'news_test.py', start_date, end_date, search_term])

def read_news():
    """Takes no parameters. Opens news.txt file and reads and displays top three results (if there are
    at least three), otherwise displays a "no results" message"""
    with open('news.txt') as file:
        news_data = json.load(file)
        if news_data['totalResults'] == 0:
            print("No recent news articles for this earthquake.")
            return

        articles = news_data['articles']
        for i in range(3):
            try:
                print(articles[i]['title'], articles[i]['url'])
            except IndexError:
                return


def call_wiki_microservice(df, row):
    """Takes as parameters pandas dataframe and row number, and formats wikipedia search parameters based on
    the location of the earthquake in that row. Calls wikipedia microservice using search params"""
    city = df.iloc[row]['city']
    region = df.iloc[row]['region']
    #Check if city is equal to region, this determines the location argument
    if city != region:
        place = ", ".join([city, region])
        ans = subprocess.run(['python', 'wiki_api_requests.py', place, 'Geology'])
    else:
        ans = subprocess.run(['python', 'wiki_api_requests.py', region, 'Geology'])

def earthquake_in_depth(df, row, criteria, location = None):
    """Takes as parameters pandas data frame, specified row, numerical criteria (either 0 or 1) and
    and optional string location. Prints information for the specified earthquake (determined by dataframe
    and row) and calls map, news, and wikipedia microservices to return additional information. Provides user
    with the option to return to search or return to the main menu"""
    #Check for tsunami and print out earthquake details
    tsunami = 'No'
    if df.iloc[row]['tsunami'] == 1:
        tsunami = 'Yes'
    date = df.iloc[row]['date']
    thirty_days = (datetime.datetime.now() - datetime.timedelta(30)).date()
    print(" ")
    print('Here are some further details: ')
    print("Earthquake date:", df.iloc[row]['date'])
    print("Earthquake location:", df.iloc[row]['place'])
    print("Earthquake magnitude:", df.iloc[row]['magnitude'])
    print("Earthquake intensity:", df.iloc[row]['intensity'])
    print("Depth at which the earthquake began to rupture (in kilometers):", df.iloc[row]['depth_km'])
    print("Significance (scale of 0 to 1000):", df.iloc[row]['significance'])
    print("Tsunami warning?:", tsunami)
    print(" ")
    print("Links related to this earthquake:")
    print("USGS event page:", df.iloc[row]['url'])

    #Call microservices (and print informative messages)
    map = call_map_microservice(df, row)
    print("Map of earthquake location:", map)
    if date > str(thirty_days):
        print("News articles related to this earthquake: ")
        call_news_microservice(df, row)
        read_news()
    print(" ")
    print("Here is some information about the nearest town or region, sourced from wikipedia:")
    call_wiki_microservice(df, row)

    #Let user specify where they want to go next:
    next_action = input("Enter 1 to go back to queried list of earthquakes, 2 to return to the start menu: ")
    if next_action == "1":
        earthquake_rough_details(df, criteria, location)
    else:
        start()



if __name__ == '__main__':
    start()


