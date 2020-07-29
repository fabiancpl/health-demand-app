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

# Endpoionts functions

def read_json(url_in):
    with urllib.request.urlopen(url_in) as url:
        data = json.loads(url.read().decode('UTF-8'))
    return data

def get_df_from_url(url_in,sort_index=0):
    df=pd.json_normalize(read_json(url_in))
    df.sort_values(by=[df.columns[sort_index]],inplace=True)
    df.Total = pd.to_numeric(df.Total)
    return  df

def get_data_summary(url, file):
    try:
        #print (0/0)   # Delete 
        return get_df_from_url(url,0)
    except:
        with open(file, encoding='UTF-8') as f:
            data = json.load(f)
            df = pd.DataFrame.from_dict(data, orient='columns')
            df.Total = pd.to_numeric(df.Total)
        return df
    
def total_vic(df):
    return df.Total.sum()

def total_men(df):
    return df[df['Sexo']=='Masculino'].Total.sum()

def total_women(df):
    return df[df['Sexo']=='Femenino'].Total.sum()

def get_Etnia(df):
    df_tmp = df.Etnia.value_counts().to_frame().reset_index()
    df_tmp.rename(columns={str(df_tmp.columns[0]):'Etnia', str(df_tmp.columns[1]):'Count'},inplace=True)
    return df_tmp
    
def get_map_info(df):
    try:
        return df.groupby('CodigoDepartamento')[['Total']].sum().reset_index()
    except:
        return df.groupby('Departamento')[['Total']].sum().reset_index()


def get_rips_Anno_Mes_TA(df):
    df['AnnoMes']= df.Anno + df.Mes
    return df.groupby(['AnnoMes','TipoAtencion'])[['Total']].sum().reset_index()

def get_discapacidad(df):
    df_tmp =  df.Discapacidad.value_counts().to_frame().reset_index()
    df_tmp.rename(columns={str(df_tmp.columns[0]):'Discapacidad', str(df_tmp.columns[1]):'Count'},inplace=True)
    return df_tmp;


def get_TipoAtencion(df):
    df_tmp =  df.TipoAtencion.value_counts().to_frame().reset_index()
    df_tmp.rename(columns={str(df_tmp.columns[0]):'TipoAtencion', str(df_tmp.columns[1]):'Count'},inplace=True)
    return df_tmp;

def load_data():
    start = time.time()
    # Data
    global df_data_ruv,df_data_rips1,df_data_rips2,geojson,df_data_ruv_o,df_data_rips1_o,df_data_rips2_o
    with open('data\\polygon_colombia.json', encoding='UTF-8') as geo:
        geojson = json.loads(geo.read())
    df_data_ruv = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/ruv",'./data/ruv.json')
    df_data_ruv_o = df_data_ruv.copy()
    df_data_rips1 = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/rips/annomes",'./data/rips1.json')
    df_data_rips1_o = df_data_rips1.copy()
    df_data_rips2 = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/rips/",'./data/rips2.json')
    df_data_rips2_o = df_data_rips2.copy()
    end = time.time()
    print(end - start)


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
    return [dbc.Row(id="dashboard-filters", 
            children=build_filters()
            ),
            html.Div(html.H1("Under construction, excuse us. "),id='test'),
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
                    {'label': 'Bogota', 'value': 'NYC'},
                    {'label': 'Cali', 'value': 'MTL'},
                    {'label': 'Medellin', 'value': 'SF'}
                ],
                value=['MTL', 'NYC'],
                multi=True
            )  

def generate_checklist():
    return dcc.Checklist(id='filter-checklist',
                options=[
                    {'label': ' Victims', 'value': 'EsVictima'},
                    {'label': ' Oldest', 'value': 'EsAdultoMayor'},
                    {'label': ' With Ethnicity', 'value': 'PerteneceEtnia'},
                    {'label': ' With Dishabilities', 'value': 'TieneDiscapacidad'}
                ],
                value=['EsVictima','EsAdultoMayor', 'PerteneceEtnia', 'TieneDiscapacidad'],
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
                        dbc.Row(children=[
                        dbc.Col(id="col-piramide"),
                        def_graphic.generate_piechart('Discapacidad',get_discapacidad(df_data_ruv)),
                        #def_graphic.generate_line_chart(),
                        
                        ]),
                    ]
                )

def build_center_column_tab1():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(id="col-gener"),
                                    dbc.Col(id="col-etnia"),
                                ]),
                             dbc.Row(id='lower-center-section-container',
                                children=[
                                dbc.Col(id='col-map'), 
                                ]),
                    ]
                )


def build_left_column_tab2():
    return dbc.Col( id="left-section-container",
                    children=[
                        html.H6("Services Demand"), 
                        def_graphic.generate_bar_chart(get_TipoAtencion(df_data_rips1)),
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
                                    dbc.Col(def_graphic.generate_piechart('Etnia',get_Etnia(df_data_rips2)),id="col-etnia"),
                                ]),
                             dbc.Row(
                                def_graphic.map(get_map_info(df_data_rips1),geojson)
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


# Update Functions
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

@app.callback([
    Output("col-gener", "children"),
    Output("col-etnia", "children"),
    Output("col-map", "children"),
    Output("col-piramide", "children"),],
    [Input("filter-checklist", "value")],
)
def update_output(value):
    if not value:
        tmp_df = pd.DataFrame(columns=df_data_ruv.columns)
    elif 'EsVictima' in value:
        tmp_df = df_data_ruv
    else:
        tmp_df = df_data_ruv
        for i in value:
            tmp_df = tmp_df[tmp_df[i]=='Si']
    gener = def_graphic.build_gener(total_vic(tmp_df),
                                        total_men(tmp_df),
                                        total_women(tmp_df)                                    
                                    )
    etnia = def_graphic.generate_piechart('Etnias',get_Etnia(tmp_df))
    map = def_graphic.map(get_map_info(tmp_df),geojson)
    piramide = def_graphic.generate_Stacked_barchar(tmp_df,'Piramide Poblacional')
    return gener,etnia, map, piramide
    # return 'You have selected "{}"'.format(value)


if __name__ == "__main__":
    load_data()
    app.run_server(debug=True)