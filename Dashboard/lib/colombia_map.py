# Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc 

from datetime import datetime as dt
import json
import numpy as np
import pandas as pd
import geopandas as gpd

#Recall app
from app import app


def map(df):
    with open('data\\polygon_colombia.json') as geo:
        geojson = json.loads(geo.read())
    #Create the map:
    Map_Fig=px.choropleth_mapbox(df,               #Data
                locations=df.columns[0],                #Column containing the identifiers used in the GeoJSON file 
                color=df.columns[1],                           #Column giving the color intensity of the region
                geojson=geojson,                          #The GeoJSON file
                zoom=4,                                   #Zoom
                mapbox_style="white-bg",                  #Mapbox style, for different maps you need a Mapbox account and a token
                center={"lat": 4.0902, "lon": -72.7129},  #Center
                color_continuous_scale="YlGn",            #Color Scheme
                opacity=0.5,                              #Opacity of the map
                )


    Map_Fig.update_layout(title='Health in Colmbia',
    paper_bgcolor="#F8F9F9",
    margin={"r":0,"t":0,"l":0,"b":0} )
    return Map_Fig



    