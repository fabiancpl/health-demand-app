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


def map(df,geojson):
    #Create the map:
    Map_Fig=px.choropleth_mapbox(df,                           #Data
                locations=df.columns[0],                       #Column containing the identifiers used in the GeoJSON file 
                color=df.columns[1],                           #Column giving the color intensity of the region
                geojson=geojson,                               #The GeoJSON file
                zoom=3.5,                                        #Zoom
                mapbox_style="carto-positron",                 #Mapbox style, for different maps you need a Mapbox account and a token
                center={"lat": 4.624335, "lon": -74.063644},   #Center
                color_continuous_scale='RdBu',            #Color Scheme
                opacity=0.5,                                   #Opacity of the map
                width=450, height=400
                )
    
    
    Map_Fig.update_layout(title='Health in Colmbia',
    paper_bgcolor="#F8F9F9",
    margin={"r":0,"t":0,"l":0,"b":0} )
    return dcc.Graph(figure=Map_Fig,id="colombia_map") 
    #return html.P('Hola',id="colombia_map")  # delete and uncomment 

def build_gener(total, men, women):
    return html.Div(
                id="gener",
                className="gener",
                children=[
                    dbc.Row(
                        html.P("Total Base: "+ str(total)), id="row-titel-gener"
                    ),
                    dbc.Row([
                        dbc.Col(
                        html.Img(id="woman-logo", src=app.get_asset_url("woman.png"))
                        ),
                        dbc.Col(html.Img(id="man-logo", src=app.get_asset_url("man.png"))),
                    ],id="row-gener-logo"),
                    dbc.Row([
                        dbc.Col([html.P(str(men)), html.P("Mujer ")]),
						dbc.Col([html.P(str(women)), html.P("Hombre ")]),
                    ],id="row-gener-values")
                                
                ]
            )

def generate_piechart(title_df,df):
    return  dcc.Graph(
                        id="piechart",
                        figure=(px.pie(df, values=df.columns[1], names=df.columns[0]).update_layout(
                            paper_bgcolor="#F8F9F9",
                            title=title_df,
                            autosize=True,           
                            margin={"r":0,"t":30,"l":0,"b":0},
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
                            #title="Health Demand",
                            autosize=True,           
                            margin={"r":0,"t":50,"l":0,"b":0},
                            showlegend=True,
                            legend=dict(
                                    yanchor="bottom",
                                    orientation="h",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01
                                )
                            ), id='Char_line')

def generate_bar_chart(df,title):
    df = df.sort_values(by=df.columns[1])
    return dcc.Graph(
                figure= px.bar(df, x=df.columns[0], y=df.columns[1]).update_layout(title=title ,paper_bgcolor="#F8F9F9"),
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

def generate_Stacked_barchar(df,title):
    df_tmp = pd.pivot_table(df[df.GrupoEdad !=  'NA'], values='Total', index=['GrupoEdad'],columns=['Sexo'], aggfunc=np.sum).reset_index()
    df_tmp['Index']=pd.to_numeric(df_tmp.GrupoEdad.str.split(',',expand=True)[0].str.split('[',expand=True)[1])
    df_tmp.sort_values(by='Index',inplace=True)
    layout = go.Layout( title = 'Victim people per age and sex',
                       yaxis = go.layout.YAxis( title = 'Age group' ),
                       xaxis = go.layout.XAxis(
                           #range = [ -40000, 60000 ],
                           title = 'Number of victim people'
                       ),
                       barmode = 'overlay',
                       bargap = 0.1
                      )

    data = [ go.Bar( y = df_tmp[ 'GrupoEdad' ].astype( str ),
                    x = df_tmp['Masculino']*-1,
                    orientation = 'h',
                    name = 'Men',
                    text = df_tmp[ 'Masculino' ],
                    hoverinfo = 'text',
                    marker = dict( color = '#beaed4' )
                   ),
            go.Bar( y = df_tmp[ 'GrupoEdad' ].astype( str ),
                   x = df_tmp[ 'Femenino' ],
                   orientation = 'h',
                   name ='Women',
                   text = df_tmp[ 'Femenino' ],
                   hoverinfo = 'text',
                   marker = dict( color = '#fdc086' )
                  ) 
           ]

    fig = go.Figure( dict( data = data, layout = layout ) ).update_layout(paper_bgcolor="#F8F9F9",
                                                                        #width=530,
                                                                        height=320,
                                                                        autosize=True,
                                                                        title=title,        
                                                                        margin={"r":0,"t":50,"l":0,"b":0},
                                                                        showlegend=True,
                                                                        legend=dict(
                                                                                yanchor="top",
                                                                                y=0.99,
                                                                                xanchor="left",
                                                                                x=0.01
                                                                            )
                                                                        )
    return dcc.Graph(
                figure=fig, id='stacked_plot'
            )

    
