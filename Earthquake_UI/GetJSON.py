# Programmer: Alexandra Sciocchetti
# Course: CS 361
# Description: JSON parsing/data cleaning microservice that takes USGS GeoJSON data and
#               reformats the data in a way that is easy to query from a database

#Load Packages:
import json
import urllib.request as request
import pandas as pd
import datetime
import regex as re
import unidecode as unidecode

#Get data from USGS
with request.urlopen("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=1970-01-01&endtime=2022-03-07&minmagnitude=6.5") as response:
    source = response.read()
    sig_quakes = json.loads(source) #read in data
    quake_features = sig_quakes["features"] #all relevant data contained within "features" list

#Define attribute lists to store relevant earthquake data
url_list, place_list = [], []
mag_list, intensity_list, significance_list = [], [], []
tsunami_list, depth_list = [], []
latitude_list, longitude_list = [], []

#city and region list will be extracted from "place" data. Date list will be extracted from datetime
city_list, region_list, date_list=[], [], []


def convert_date_time(milliseconds):
    """
    Takes date object (string) which records earthquake time in milliseconds from the epoch and
    converts it to a UTC date in the %Y-%m-%d format
    """
    date = datetime.datetime.fromtimestamp(milliseconds/1000.0, tz=datetime.timezone.utc).strftime('%Y-%m-%d')
    return date


def add_feature_data(source):
    """
    Takes as a parameter a loaded USGS GeoJSON file and adds relevant elements to earthquake lists. Elements
    added are earthquake event url, magnitude, place, time, intensity (recorded as mmi), significance, and tsunami
    indicator. List of data formats and descriptions can be found here:
    https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
    """
    for i in source:
        #the following attributes do not need to be edited, and are added straight to attribute lists
        url_list.append([i][0]["properties"]["url"])
        mag_list.append([i][0]["properties"]["mag"])
        intensity_list.append([i][0]["properties"]["mmi"])
        significance_list.append([i][0]["properties"]["sig"])
        place_list.append([i][0]["properties"]["place"])
        tsunami_list.append([i][0]["properties"]["tsunami"])

        #date attribute needs to be converted to a UTC date (from milliseconds past the epoch)
        date_milliseconds = [i][0]["properties"]["time"]
        date_list.append(convert_date_time(date_milliseconds))

def add_geometry_data(source):
    """
    Similar to add_feature_data, takes a loaded GeoJSON file and extracts earthquake latitude, longitude, and
    depth which are stored as a three element tuple within the earthquake geometry dictionary. Elements are added
    to relevant lists.
    """
    for i in source:
        latitude_list.append([i][0]["geometry"]["coordinates"][1])
        longitude_list.append([i][0]["geometry"]["coordinates"][0])
        depth_list.append([i][0]["geometry"]["coordinates"][2])

def remove_extra_chars(location):
    """
    Takes a string location and removes leading whitespace, a 'region' tag, and all special
    characters (using the unidecode module). Returns the cleaned string.
    """
    no_white_space = str.lstrip(re.sub(r"[^\w ]",' ', location))
    remove_region = re.sub(r"region",'',no_white_space)
    return unidecode.unidecode(remove_region)


def extract_city_and_region(places):
    """
    Takes the earthquake place list, which is a list of strings that contain the location of the
    earthquake, splits them into separate strings for city and region, removes additional white space
    and special characters, and adds them to the city and region lists.
    """
    for location in places:
        #In 99% of cases, earthquake location is located after 'of' in the string.
        #Try splitting this way, then use remove_white_space method to further clean
        try:
            city_region = (location.split('of',)[-1]).split(',')
            city,region = remove_extra_chars(city_region[0]), remove_extra_chars(city_region[-1])
            city_list.append(city)
            region_list.append(region)
        #If there is no 'of' in place (which will cause an AttributeError) then no splitting needs to occur
        except AttributeError:
            city = remove_extra_chars(str(location))
            city_list.append(city), region_list.append(str(location))


#Apply feature and geometry data functions to the quake data:
add_feature_data(quake_features)
add_geometry_data(quake_features)
extract_city_and_region(place_list)

#Create feature dictionary
feature_dict= {'city':city_list, 'region':region_list,'magnitude':mag_list, 'url': url_list, 'place': place_list,
       'date':date_list, 'intensity': intensity_list, 'significance': significance_list, 'tsunami': tsunami_list,
               "latitude": latitude_list,"longitude" : longitude_list, "depth_km": depth_list}

#convert dictionary to a dataframe to a csv
df = pd.DataFrame.from_dict(feature_dict, orient="columns")
df.to_csv('quake_data.csv', index=False) #no indexing

