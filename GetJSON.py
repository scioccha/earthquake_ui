
#https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson

import json
import urllib.request as request
import pandas as pd
import datetime
import regex as re
import unidecode as unidecode

with request.urlopen("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=1970-01-01&endtime=2022-02-03&minmagnitude=6.5") as response:
    source = response.read()
    sig_quakes = json.loads(source) #read in data

quake_features = sig_quakes["features"] #all relevant data contained within "features" list

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

def add_feature_data(source):
    for i in source:
        magnitude = [i][0]["properties"]["mag"] #second type of related data: earthquake properties
        shaking_intensity = [i][0]["properties"]["mmi"]
        place = [i][0]["properties"]["place"]
        time = [i][0]["properties"]["time"]
        url = [i][0]["properties"]["url"]
        sig = [i][0]["properties"]["sig"]
        alert = [i][0]["properties"]["tsunami"]
        list_url.append(url) #add all defined variables to lists
        list_mag.append(magnitude)
        list_place.append(place)
        list_datetime.append(time)
        list_intensity.append(shaking_intensity)
        list_sig.append(sig)
        list_tsunami.append(alert)

def add_geometry_data(source):
    for i in source:
        longitude = [i][0]["geometry"]["coordinates"][0]
        latitude = [i][0]["geometry"]["coordinates"][1]
        depth = [i][0]["geometry"]["coordinates"][2]
        latitude_list.append(latitude)
        longitude_list.append(longitude)
        depth_list.append(depth)

add_feature_data(quake_features) #run the function for feature list
add_geometry_data(quake_features)

city_list=[]
region_list=[]
for place in list_place:
    x= place.split('of',) # location is always after "of" in the string
    y = x[-1]
    z = y.split(',',)#city and region are separated by a comma
    city_regex = re.sub(r"[^\w ]",' ', z[0]) #remove all special characters
    city_final = str.lstrip(city_regex) #remove beginning space
    city_final2 = unidecode.unidecode(city_final)
    region_regex = re.sub(r"[^\w ]",' ', z[-1]) #do the same for region
    region_final = str.lstrip(region_regex)
    city_list.append(str.rstrip(city_final2)) #remove any end spaces and add to list
    region_list.append(str.rstrip(region_final))

city_list = [re.sub(r"\s+", '-', file) for file in city_list] #replace spaces with dashes
region_list = [re.sub(r"\s+", '-', file) for file in region_list] #replace spaces with dashes

region_list = [re.sub(r"-region", '', file) for file in region_list] #fix naming issues in regions
region_list = [re.sub(r"(\w+) *-Peru", 'Peru', file) for file in region_list]
region_list = [re.sub(r"(\w+) *-Alaska", 'Alaska', file) for file in region_list]

city_list = [str(i or None) for i in city_list] #replace empty city names with None


date_list = []
for t in list_datetime:
    date = datetime.datetime.fromtimestamp(t/1000.0, tz=datetime.timezone.utc)
    full_date = date.strftime('%Y-%m-%d %H:%M:%S')
    date = re.findall(r'\d{4}-\d{2}-\d{2}', full_date) #separate date from time
    date_list.append(date)

date_list = [i[0] for i in date_list] #remove additional brackets from date list
date_list = [re.sub(r"\b0","", file) for file in date_list] #remove leading zeros

feature_dict= {'city':city_list, 'region':region_list,'magnitude':list_mag, 'url': list_url, 'place': list_place,
       'date':date_list, 'intensity': list_intensity, 'significance': list_sig, 'tsunami': list_tsunami,
               "latitude": latitude_list,"longitude" : longitude_list, "depth_km": depth_list}

#convert dictionary to a dataframe to a csv
df = pd.DataFrame.from_dict(feature_dict, orient="columns")
df.to_csv('r_quakes.csv', index=False) #no indexing

