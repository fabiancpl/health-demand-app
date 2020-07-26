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

# Data libraries
import math
import numpy as np
import datetime as dt
import pandas as pd
import urllib.request, json 
import time

#Recall app
from app import app
from lib import def_graphic

#### delete after integration
data = [{"x": 23,"y":"CARIES DE LA DENTINA"},{    "x": 114,     "y": "HIPERTENSION"  },   {    "x": 630,     "y": "GASTRITIS"  },   {    "x": 720,     "y": "VAGINITIS"  },   {    "x": 530,     "y": "GINGIVITIS"  },   {    "x": 400,     "y": "LUMBAGO"  },   {    "x": 305,     "y": "INFECCION URINARIA"  },   {    "x": 213,     "y": "CEFALEA"  },   {    "x": 810,     "y": "DOLOR PELVICO"  }]
df_diseases = pd.DataFrame.from_dict(data, orient='columns')
df_diseases.sort_values(by=[df_diseases.columns[0]],inplace=True)
data_canada = px.data.gapminder().query("country == 'Canada'")
RIPS = pd.read_csv("./data/RIPS.txt", sep=";", nrows=1000000)
RIPS['FechaAtencion'] = pd.to_datetime(RIPS['FechaAtencion'], format='%Y%m%d')
RIPS['Year'] = pd.DatetimeIndex(RIPS.FechaAtencion).year

# IndDiscapacidad
# IndAdultoMayor
# IndEtnia
# IndVictima	

# Endpoionts functions

def get_df_from_url(url_in,sort_index=0):
    with urllib.request.urlopen(url_in) as url:
        data = json.loads(url.read().decode())
    df=pd.json_normalize(data)
    df.sort_values(by=[df.columns[sort_index]],inplace=True)
    df.Total = pd.to_numeric(df.Total)
    return  df

def get_data_summary(url, file):
    try:
        return get_df_from_url(url,0)
    except:
        with open(file) as f:
            data = json.load(f)
            df = pd.DataFrame.from_dict(data, orient='columns')
            df.Total = pd.to_numeric(df.Total)
        return df
    
def total_vic(df):
    return df.Total.sum()

def get_Etnia(df):
    df_tmp = df.Etnia.value_counts().to_frame().reset_index()
    df_tmp.rename(columns={str(df_tmp.columns[0]):'Etnia', str(df_tmp.columns[1]):'Count'})
    return df_tmp
    
def get_map_info(df):
    try:
        return df.groupby('CodigoDepartamento')[['Total']].sum().reset_index()
    except:
        return df.groupby('Departamento')[['Total']].sum().reset_index()


def get_rips_Anno_Mes_TA(df):
    df['AnnoMes']= df.Anno + df.Mes
    return df.groupby(['AnnoMes','TipoAtencion'])[['Total']].sum().reset_index()

# Update Functions

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('filter-checklist', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


# Data
df_data_ruv = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/ruv",'./data/ruv.json')
df_data_rips1 = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/rips/annomes",'./data/rips1.json')
df_data_rips2 = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/rips/",'./data/rips2.json')

# Build Functions

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
                        label="Dashboard RUV",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Dashboard-tab2",
                        label="Dashboard RIPS",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Model-tab",
                        label="Predition Model",
                        value="tab3",
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
                build_left_column_tab1(),
                build_center_column_tab1(),
                #build_right_column(),
            ]),
        ]

def build_tab_2():
    return [
        dbc.Row(id="dashboard-filters", 
            children=build_filters()
        ),
        dbc.Row(id="dashboar-container", 
            children=[
                build_left_column_tab2(),
                build_center_column_tab2(),
                build_right_column_tab2(),
            ]),
        ]

def build_tab_3():
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
    return dcc.Dropdown(id='filter-dropdown',
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                value=['MTL', 'NYC'],
                multi=True
            )  

def generate_checklist():
    return dcc.Checklist(id='filter-checklist',
                options=[
                    {'label': ' Victims', 'value': 'WV'},
                    {'label': ' Oldest', 'value': 'WO'},
                    {'label': ' With Ethnicity', 'value': 'WE'},
                    {'label': ' With Dishabilities', 'value': 'WD'}
                ],
                value=['WV', 'WO', 'WE', 'WD'],
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

def build_left_column_tab1():
    return dbc.Col( id="left-section-container",
                    children=[
                        html.H6("Services Demand"), 
                        def_graphic.generate_bar_chart(data_canada),
                        #def_graphic.generate_line_chart(),
                    ]
                )

def build_center_column_tab1():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(def_graphic.build_gener(total_vic(df_data_ruv),
                                        total_vic(df_data_ruv)/2,
                                        total_vic(df_data_ruv)/2                                    
                                    ),id="col-gener"),
                                    dbc.Col(def_graphic.generate_piechart(get_Etnia(df_data_ruv)),id="col-etnia"),
                                ]),
                             dbc.Row(
                                dcc.Graph(figure=def_graphic.map(get_map_info(df_data_ruv)),
                                id="colombia_map")
                                , id='lower-center-section-container'
                                ),
                    ]        
                )


def build_left_column_tab2():
    return dbc.Col( id="left-section-container",
                    children=[
                        html.H6("Services Demand"), 
                        def_graphic.generate_bar_chart(data_canada),
                        def_graphic.generate_line_chart(get_rips_Anno_Mes_TA(df_data_rips1)),
                    ]
                )

def build_center_column_tab2():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(def_graphic.build_gener(total_vic(df_data_rips1),
                                        total_vic(df_data_rips1)/2,
                                        total_vic(df_data_rips1)/2                                    
                                    ),id="col-gener"),
                                    dbc.Col(def_graphic.generate_piechart(get_Etnia(df_data_rips2)),id="col-etnia"),
                                ]),
                             dbc.Row(
                                dcc.Graph(figure=def_graphic.map(get_map_info(df_data_rips1)),
                                id="colombia_map")
                                , id='lower-center-section-container'
                                ),
                    ]        
                )

def build_right_column_tab2():
    return dbc.Col( id="right-section-container",
                    children=[
                        def_graphic.generate_violin_plot(),
                        html.H6("Top Diseases"), 
                        def_graphic.generate_bar_h_chart(df_diseases),
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
    elif tab_switch == "tab2":
        return build_tab_2()
    else:
        return build_tab_3()
    
if __name__ == "__main__":
    app.run_server(debug=True)