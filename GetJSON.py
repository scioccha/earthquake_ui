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

#Define lists to store relevant earthquake data
list_url = []
list_mag = []
list_place = []
list_datetime = []
list_intensity = []
list_sig = []
list_tsunami = []
latitude_list = []
longitude_list = []
depth_list = []

#city and region list will be extracted from "place" data
city_list=[]
region_list=[]

def add_feature_data(source):
    """
    Takes as a parameter a loaded USGS GeoJSON file and adds relevant elements to earthquake lists. Elements
    added are earthquake event url, magnitude, place, time, intensity (recorded as mmi), significance, and tsunami
    indicator. List of data formats and descriptions can be found here:
    https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
    """
    for i in source:
        list_url.append([i][0]["properties"]["url"])
        list_mag.append([i][0]["properties"]["mag"])
        list_place.append([i][0]["properties"]["place"])
        list_datetime.append([i][0]["properties"]["time"])
        list_intensity.append([i][0]["properties"]["mmi"])
        list_sig.append([i][0]["properties"]["sig"])
        list_tsunami.append([i][0]["properties"]["tsunami"])

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

def remove_white_space_special_chars(location):
    no_white_space = str.lstrip(re.sub(r"[^\w ]",' ', location))
    remove_region = re.sub(r"region",'',no_white_space)
    return unidecode.unidecode(remove_region)


def extract_city_and_region(place_list):
    for place in place_list:
        try:
            y= place.split('of',)[-1] # location is always after "of" in the string
            z = y.split(',',) #city and region are separated by a comma
            city,region = remove_white_space_special_chars(z[0]), remove_white_space_special_chars(z[-1])
            city_list.append(city)
            region_list.append(region)
        except AttributeError:
            city = remove_white_space_special_chars(str(place))
            city_list.append(city), region_list.append(str(place))

#Apply feature and geometry data functions to the quake features data:
add_feature_data(quake_features)
add_geometry_data(quake_features)
extract_city_and_region(list_place)



date_list = []
for t in list_datetime:
    date = datetime.datetime.fromtimestamp(t/1000.0, tz=datetime.timezone.utc)
    full_date = date.strftime('%Y-%m-%d %H:%M:%S')
    date = re.findall(r'\d{4}-\d{2}-\d{2}', full_date) #separate date from time
    date_list.append(date)

date_list = [i[0] for i in date_list] #remove additional brackets from date list


feature_dict= {'city':city_list, 'region':region_list,'magnitude':list_mag, 'url': list_url, 'place': list_place,
       'date':date_list, 'intensity': list_intensity, 'significance': list_sig, 'tsunami': list_tsunami,
               "latitude": latitude_list,"longitude" : longitude_list, "depth_km": depth_list}

#convert dictionary to a dataframe to a csv
df = pd.DataFrame.from_dict(feature_dict, orient="columns")
df.to_csv('quake_data.csv', index=False) #no indexing

