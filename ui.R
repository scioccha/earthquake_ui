#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(googleway)
library(tidyverse)

api_key <- "AIzaSyB-oVXGc_AVmckNYeLMWmjSx0GSip9rAVs"

system('/Users/ascio/anaconda3/python.exe GetJSON.py')

library(readr)
sig_quakes <- read.csv("sig_quakes.csv")
sig_quakes$Combined<-paste(sig_quakes$magnitude,sig_quakes$place,sep=" magnitude, ")


# Define UI for application that draws a histogram
shinyUI(fluidPage(

    # Application title
    titlePanel(h1("Big Earthquake News",h4("Learn about recent large earthquakes around the world. Click on a red icon to get started."))),
    
    map <- google_map(
        key = api_key, data = sig_quakes) %>%
        add_markers(lat = 'latitude', lon = 'longitude', info_window = 'Combined')
    
))


#https://www.gislounge.com/a-guide-to-building-interactive-google-maps-with-r-shiny/
#https://mastering-shiny.org/action-dynamic.html
#https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php


