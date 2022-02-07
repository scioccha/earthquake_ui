# Programmer: Alexandra Sciocchetti
# Course: CS 361
# Description: Command Line User Interface for Earthquake History database program


import pandas as pd
from datetime import date
import datetime

print("Welcome to the Earthquake History. We are a database containing information "
      "about all significant (> 6.5 magnitude) earthquakes since 1970")

print("How would you like to start?")

def options():
    print("1. Search for past earthquakes in my region")
    print("2. Learn about recent significant earthquakes around the world")
    start = input("Type in the number next to the selected option: ")
    if start == "1":
        past_earthquake_option()
    elif start == "2":
        recent_sig_option()

def past_earthquake_option():
    print("Input your city, state, or country (if outside the US) to search for past earthquakes, ")
    location = input("or input the number 2 to return to the main menu: ")
    if location == '2':
        options()
    df = pd.read_csv("r_quakes.csv")
    region_df = df.loc[df['region']==location]
    if len(region_df) > 0:
        print(region_df.head())
    elif len(region_df) == 0:
        city_df = df.loc[df['city']==location]
        if len(city_df)>0:
            print(city_df.head())
    else:
        print("There have been no recorded earthquakes greater than 6.5 magnitude in ",location," since the year 1970")
        next_action = input("Enter a 1 to enter a different location, enter a 2 to return to the main menu: ")
        if next_action == "1":
            past_earthquake_option()
        else:
            options()


def recent_sig_option():
    df = pd.read_csv("r_quakes.csv")
    start_date = (datetime.datetime.now() - datetime.timedelta(30)).date()
    thirty_days = df[(df['date']> str(start_date))]
    print("There were",len(thirty_days), "earthquakes of over 6.5 magnitude within the last thirty days.")
    print(thirty_days.head())

    print("Would you like to get more information about any of these earthquakes?")

    #prompt user to type in the city/region
    #will need a back button option to get back to this page


def earthquake_details():
    pass

def earthquake_map():
    pass

def location_wiki():
    pass

def earthquake_news():
    pass


options()

