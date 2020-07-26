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

def build_gener(total, men, women):
    return html.Div(
                id="gener",
                className="gener",
                children=[
                    dbc.Row(
                        html.P("Total Base: "+ str(total)), id="row-titel-gener"
                    ),
                    dbc.Row([
                        dbc.Col(html.Img(id="woman-logo", src=app.get_asset_url("woman.png"))),
                        dbc.Col(html.Img(id="man-logo", src=app.get_asset_url("man.png"))),
                    ],id="row-gener-logo"),
                    dbc.Row([
                        dbc.Col(html.P(str(men))),
                        dbc.Col(html.P(str(women))),
                    ],id="row-gener-values")
                                
                ]
            )

def generate_piechart(df):
    return  dcc.Graph(
                        id="piechart",
                        figure=(px.pie(df, values=df.columns[1], names=df.columns[0]).update_layout(
                            paper_bgcolor="#F8F9F9",
                            title='Etnias',
                            autosize=True,           
                            margin={"r":0,"t":0,"l":0,"b":0},
                            showlegend=False,
                            )
                        )
                    )

def generate_bar_h_chart(df):
    return dcc.Graph(
                        id="bar_h",
                        figure=(go.Figure(go.Bar(
                                x=df[df.columns[0]],
                                y=df[df.columns[1]],
                                marker_color=['#3a5544','#356046','#356046',
                                '#2c6b48','#006b38','#00723e','#00804b','#138752','#1f8e58',
                                '#439567','#6baa83','#90bfa1','#b5d4bf','#daeadf','#ffffff'],
                                #"lightgreen",
                                orientation='h'))).update_layout(
                            paper_bgcolor="#F8F9F9",
                            autosize=True,           
                            margin={"r":0,"t":0,"l":0,"b":0},
                            showlegend=False,
                            )
                    )

def generate_line_chart(df):
    return dcc.Graph(figure=px.line(df, x=df.columns[0], y=df.columns[2], color=df.columns[1]
            ).update_layout(
                            paper_bgcolor="#F8F9F9",
                            title="Health Demand",
                            autosize=True,           
                            margin={"r":0,"t":0,"l":0,"b":0},
                            showlegend=True,
                            ), id='Char_line')

def generate_bar_chart(df):
    return dcc.Graph(
                figure= px.bar(df, x='year', y='pop').update_layout(title='Health in Colombia'),
                id='Colombia_bar'
            )

def generate_violin_plot():
    df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/violin_data.csv")
    fig = go.Figure()
    days = ['Thur', 'Fri', 'Sat', 'Sun']
    for day in days:
        fig.add_trace(go.Violin(x=df['day'][df['day'] == day],
                                y=df['total_bill'][df['day'] == day],
                                name=day,
                                box_visible=True,
                                meanline_visible=True))
    fig.update_layout(paper_bgcolor="#F8F9F9",
                            title="Health Demand",
                            autosize=True,           
                            margin={"r":0,"t":50,"l":0,"b":0},
                            showlegend=False)
    return dcc.Graph(
                figure=fig, id='violin_plot'
            )


    