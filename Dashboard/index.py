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

#Data 
import math
import numpy as np
import datetime as dt
import pandas as pd
import urllib.request, json 

#Recall app
from app import app
from lib import colombia_map,rips_charts

# Build Functions

def get_df_from_url(url_in,sort_index=0):
    with urllib.request.urlopen(url_in) as url:
        data = json.loads(url.read().decode())
    df=pd.json_normalize(data)
    df.sort_values(by=[df.columns[sort_index]],inplace=True)
    return  df

def get_diseases():
    return get_df_from_url("http://127.0.0.1:5000/diseases",0)

def build_title():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Analysis of the Health Service’s Demand with a Differential Approach"),
                    html.H6("Exploratory Data Analysis and Prediction Model."),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    #html.Button(
                    #    id="learn-more-button", children="Team 61", n_clicks=0
                    #),
                    html.Img(id="logo", src=app.get_asset_url("DS4A_latam_logo.png")),
                ],
            ),
        ],
    )
    
def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Dashboard-tab",
                        label="Main Dashboard",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Model-tab",
                        label="Predition Model",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def build_tab_1():
    return [
        dbc.Row(id="dashboard-filters", 
            children=build_filters()
        ),
        dbc.Row(id="dashboar-container", 
            children=[
                build_left_column(),
                build_center_column(),
                build_right_column(),
            ]),
        ]

def build_tab_2():
    return [html.Div(html.H1("Under construction, excuse us. ")),
            ]

def build_filters():
    return [
            dbc.Col(
                generate_range_slider(),
                id="right-section-filters"
                ),
            dbc.Col(
                generate_checklist(),
                id="center-section-filters"
                ),
            dbc.Col(
                generate_dropdown(),
                id="left-section-filters"
                ),
            ]

def generate_dropdown():
    return dcc.Dropdown(
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value=['MTL', 'NYC'],
                multi=True
            )  

def generate_checklist():
    return dcc.Checklist(
                options=[
                    {'label': ' Victims', 'value': 'NYC'},
                    {'label': ' Oldest', 'value': 'MTL'},
                    {'label': ' With Dishabilities', 'value': 'SF'}
                ],
                value=['NYC', 'MTL'],
                labelStyle={'display': 'block'}
            )  

def generate_range_slider():
    return dcc.RangeSlider(
                        id='year-slider',
                        min=2016,#df['year'].min(),
                        max=2019,#df['year'].max(),
                        value=[2016,2019],#df['year'].min(),
                        marks={2016:"2016",2017:"2017",2018:"2018",2019:"2019"},
                        #{str(year): str(year) for year in df['year'].unique()},
                        step=None
                        )

def build_gener():
    return html.Div(
                id="gener",
                className="gener",
                children=[
                    dbc.Row(
                        html.P("Total Base: 12.960.410"), id="row-titel-gener"
                    ),
                    dbc.Row([
                        dbc.Col(html.Img(id="woman-logo", src=app.get_asset_url("woman.png"))),
                        dbc.Col(html.Img(id="man-logo", src=app.get_asset_url("man.png"))),
                    ],id="row-gener-logo"),
                    dbc.Row([
                        dbc.Col(html.P("5.480.205")),
                        dbc.Col(html.P("7.480.205")),
                    ],id="row-gener-values")
                                
                ]
            )

def generate_piechart():
    return  dcc.Graph(
                        id="piechart",
                        figure=(px.pie(px.data.tips(), values='tip', names='day').update_layout(
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

def generate_line_chart():
    return dcc.Graph(figure=px.line(px.data.gapminder().query("continent=='Oceania'")
                        , x="year", y="lifeExp", color='country').update_layout(
                            paper_bgcolor="#F8F9F9",
                            title="Health Demand",
                            autosize=True,           
                            margin={"r":0,"t":0,"l":0,"b":0},
                            showlegend=False,
                            )
                        , id='Char_line')

def generate_bar_chart():
    return dcc.Graph(
                figure=rips_charts.bar_fig, id='Colombia_bar'
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

def build_left_column():
    return dbc.Col( id="left-section-container",
                    children=[
                        html.H6("Services Demand"), 
                        generate_bar_chart(),
                        generate_line_chart(),
                    ]
                )

def build_center_column():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(build_gener(),id="col-gener"),
                                    dbc.Col(generate_piechart(),id="col-etnia"),
                                ]),
                             dbc.Row(
                                dcc.Graph(figure=colombia_map.Map_Fig,id="colombia_map")
                                , id='lower-center-section-container'
                                ),
                    ]        
                )

def build_right_column():
    return dbc.Col( id="right-section-container",
                    children=[
                        generate_violin_plot(),
                        html.H6("Top Diseases"), 
                        generate_bar_h_chart(get_diseases()),
                    ]        
                )

#Create Layout

app.layout = html.Div(
    id="big-app-container",
    children=[
    build_title(),
    html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        )
    ],
)

@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1()
    else:
        return build_tab_2()
    
if __name__ == "__main__":
    app.run_server(debug=True)