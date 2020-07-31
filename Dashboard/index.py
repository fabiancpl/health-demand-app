#!/usr/bin/env python3.7
# # Basics Requirements
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

#
from datetime import datetime
import os.path
from os import path

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
        print("json")
        with open(file, encoding='UTF-8') as f:
            data = json.load(f)
            df = pd.DataFrame.from_dict(data, orient='columns')
            df.Total = pd.to_numeric(df.Total)
        return df

def get_cachedf(resource):
    endpoint = resource.replace('_','/')
    now = datetime.now()
    date = now.strftime("%Y_%m_%d")
    full_file = f"data/{resource}_{date}.csv"
    if path.exists(full_file):
        print('File')
        return pd.read_csv(full_file, delimiter='|')
    else:
        print('Service')
        df = get_df_from_url(f"http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/{endpoint}",0)
        df.to_csv(f"{full_file}",sep="|",index=False)
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
    df['AnnoMes']= df.Anno + '-' + df.Mes
    return df.groupby(['AnnoMes','TipoAtencion'])[['Total']].sum().reset_index()

def get_discapacidad(df):
    df_tmp =  df.Discapacidad.value_counts().to_frame().reset_index()
    df_tmp.rename(columns={str(df_tmp.columns[0]):'Discapacidad', str(df_tmp.columns[1]):'Count'},inplace=True)
    return df_tmp;


def get_TipoAtencion(df):
    df_tmp =  df.groupby('TipoAtencion')[['Total']].sum().reset_index()
    df_tmp.rename(columns={str(df_tmp.columns[0]):'TipoAtencion', str(df_tmp.columns[1]):'Count'},inplace=True)
    return df_tmp;

def load_data():
    start = time.time()
    # Data
    global df_data_ruv,df_data_rips1,df_data_rips2,geojson
    with open('./data/polygon_colombia.json', encoding='UTF-8') as geo:
        geojson = json.loads(geo.read())
    df_data_ruv = get_cachedf('ruv')# get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/ruv",'./data/ruv.json')
    df_data_rips1 = get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/rips/annomes",'./data/rips1.json')
    df_data_rips2 = get_cachedf('rips')#get_data_summary("http://ec2-3-129-71-228.us-east-2.compute.amazonaws.com/api/priv/rips/",'./data/rips2.json')
    df_data_ruv.Total = pd.to_numeric(df_data_ruv.Total)
    df_data_rips1.Total = pd.to_numeric(df_data_rips1.Total)
    df_data_rips2.Total = pd.to_numeric(df_data_rips2.Total)
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
                    #html.Img(id="logo", src=app.get_asset_url("DS4A_latam_logo.png")),
                    html.Img(id="logo", src=app.get_asset_url("ministeriodesaludlogo.png"), style={'height':'100%', 'width':'100%'}),
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
            children=build_filters_tab1()
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
            children=build_filters_tab2()
        ),
        dbc.Row(id="dashboar-container", 
            children=[
                build_left_column_tab2(),
                build_center_column_tab2(),
                #build_right_column_tab2(),
            ]),
        ]

def build_tab_3():
    return [
        dbc.Row(id="dashboard-filters", 
            children=build_filters_tab3()
        ),
        dbc.Row(id="dashboar-container", 
            children=[
                build_left_column_tab3(),
                build_center_column_tab3(),
            ]),
        ]

# def build_tab_3():
    # return [
            # html.Div(html.H1("Under construction, excuse us. "),id='test'),
            # ]

def build_filters_tab1():
    return [                
            dbc.Col([
				dbc.Row(dbc.Alert("El Registro Único de Víctimas (RUV) es el registro en donde se incluye las declaraciones \
								   de víctimas,  que se maneja a través del Formato Único de Declaración (FUD), para luego \
								   responder a esta población con la asistencia a que tienen derecho según la Ley 1448 de 2011.", color="primary"), id="RUV-definition"),
								   
                dbc.Row(
                generate_checklist('checklist_tab1'), id="center-section-filters", justify="center"),
				],
                id="RUVandchecklist"
                ),
                
            dbc.Col(
                generate_dropdown('dropdown_tab1'),
                id="left-section-filters"
                ),
            ]

def build_filters_tab2():
    return [
    
			dbc.Col([
				dbc.Row(dbc.Alert("Los Registros Individuales de Prestación de Servicios de Salud – RIPS, son\
								   el conjunto de datos mínimos y básicos que el Sistema General de \
								   Seguridad Social en salud requiere para los procesos de dirección, regulación \
								   , control y soporte que sirven para restablecer politicas de salud, reformular la cobertura y mejorar la oferta de servicios de salud en el país"
								   ,color="primary"), id="RIP-definition"),
                
                dbc.Row(
					[
						dbc.Col(generate_range_slider('range_slider_tab2'), id="right-section-filters"),
						dbc.Col(generate_checklist('checklist_tab2'), id="center-section-filters"),
					], id="Checklistandslider",
                ),
				],
                id="ripandchecklist"
                ),
                                
            dbc.Col(
                generate_dropdown('dropdown_tab2'),
                id="left-section-filters"
                ),
            ]

def build_filters_tab3():
    return [
    
			dbc.Col([
				dbc.Row(dbc.Alert("Los Registros Individuales de Prestación de Servicios de Salud – RIPS, son\
								   el conjunto de datos mínimos y básicos que el Sistema General de \
								   Seguridad Social en salud requiere para los procesos de dirección, regulación \
								   , control y soporte que sirven para restablecer politicas de salud, reformular la cobertura y mejorar la oferta de servicios de salud en el país"
								   ,color="primary"), id="RIP-definition"),
                
                dbc.Row(
					[
						#dbc.Col(generate_range_slider('range_slider_tab2'), id="right-section-filters"),
						dbc.Col(generate_checklist_enfermedades('checklist_tab2'), id="center-section-filters"),
					], id="Checklistandslidertab3",
                ),
				],
                id="ripandchecklist"
                ),
                                
            dbc.Col(
                generate_dropdown_discapacidades('dropdown_tab2'),
                id="left-section-filters"
                ),
            ]

def generate_dropdown(id_html):
    tmp_df = df_data_ruv.groupby(['CodigoDepartamento','Departamento'])[['Total']].sum().reset_index().drop('Total',1)
    tmp_df.rename(columns={tmp_df.columns[0]:'value',tmp_df.columns[1]:'label'},inplace=True)
    return dcc.Dropdown(id=id_html,
                options=tmp_df.to_dict('records'),
                value=tmp_df[tmp_df.columns[0]].tolist(),
                multi=True
            )  

def generate_dropdown_discapacidades(id_html):
    tmp_df = df_data_ruv.groupby(['CodigoDepartamento','Departamento'])[['Total']].sum().reset_index().drop('Total',1)
    tmp_df.rename(columns={tmp_df.columns[0]:'value',tmp_df.columns[1]:'label'},inplace=True)
    return dcc.Dropdown(id=id_html,
                options=tmp_df.to_dict('records'),
                value=tmp_df[tmp_df.columns[0]].tolist(),
                multi=False 
            )  

def generate_checklist(id_html):
    return dcc.Checklist(id=id_html,
                options=[
                    {'label': ' Victims', 'value': 'EsVictima'},
                    {'label': ' Oldest', 'value': 'EsAdultoMayor'},
                    {'label': ' With Ethnicity', 'value': 'PerteneceEtnia'},
                    {'label': ' With Dishabilities', 'value': 'TieneDiscapacidad'}
                ],
                value=['EsVictima','EsAdultoMayor', 'PerteneceEtnia', 'TieneDiscapacidad'],
                labelStyle={'display': 'block'}
            )  

def generate_checklist_enfermedades(id_html):
    return dbc.FormGroup(
		[
		dbc.Label("Seleccione una enfermedad"),
		dcc.RadioItems(
                options=[
                    {'label': 'Enfermedad 1', 'value': 1},
                    {'label': 'Enfermedad 2', 'value': 2},
                    {'label': 'Enfermedad 3', 'value': 3},
                    {'label': 'Enfermedad n', 'value': 4}
                ],
                value=1,
                id=id_html,
                labelStyle={'display': 'block'},
                #justify="center",
            ),
         ]
    )

def generate_range_slider(id_html):
    return dcc.RangeSlider(
                        id=id_html,
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
                        ],id='upper-left-section-container', justify="center"),
                        dbc.Row(children=[
                        dbc.Col(id='col-pie-Discapacidad'),
                        ], id='lower-left-section-container', justify="center"),
                    ]
                )

def build_center_column_tab1():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(id="col-gener", width=10.00),
                                    dbc.Col(id="col-etnia"),
                                ], justify="center"),
                             dbc.Row(id='lower-center-section-container',
                                children=[
                                dbc.Col(id='col-map'), 
                                ], justify="center"),
                    ]
                )

def build_left_column_tab2():
    return dbc.Col( id="left-section-container",
                    children=[
						def_graphic.generate_line_chart(get_rips_Anno_Mes_TA(df_data_rips1)),
                        def_graphic.generate_bar_chart(get_TipoAtencion(df_data_rips1),'Tipo Atencion'),
                    ],
                )

def build_center_column_tab2():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(def_graphic.build_gener(total_vic(df_data_rips1),
                                        total_vic(df_data_rips1)/2,
                                        total_vic(df_data_rips1)/2                                    
                                    ),id="col-gener", width=10.00),
                                    dbc.Col(def_graphic.generate_piechart('Etnia',get_Etnia(df_data_rips2)), id="col-etnia"),
                                ], justify="center",
                                ),
                             dbc.Row(
                                dbc.Col(
                                def_graphic.map(get_map_info(df_data_rips1),geojson)
                                , id='lower-center-section-container'
                                ), align="center",
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


def build_left_column_tab3():
    return dbc.Col( id="left-section-container",
                    children=[
						def_graphic.generate_line_chart(get_rips_Anno_Mes_TA(df_data_rips1)),
                        def_graphic.generate_bar_chart(get_TipoAtencion(df_data_rips1),'Tipo Atencion'),
                    ],
                )

def build_center_column_tab3():
    return dbc.Col( id="center-section-container",
                    children=[
                            dbc.Row(id="upper-center-section-container",
                                children=[
                                    dbc.Col(def_graphic.build_gener(total_vic(df_data_rips1),
                                        total_vic(df_data_rips1)/2,
                                        total_vic(df_data_rips1)/2                                    
                                    ),id="col-gener", width=10.00),
                                    dbc.Col(def_graphic.generate_piechart('Etnia',get_Etnia(df_data_rips2)), id="col-etnia"),
                                ], justify="center",
                                ),
                             dbc.Row(
                                dbc.Col(
                                def_graphic.map(get_map_info(df_data_rips1),geojson)
                                , id='lower-center-section-container'
                                ), align="center",
                                ),
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
        ),
    html.Div(
		dcc.Markdown('''
			**DISCLAIMER:** Este Sitio web es puesto a disposición por 
			el equipo 61 del curso DS4A sólo con fines pedagógicos e 
			informativos y no para proporcionar asesoramiento legal o 
			clínico. El usuario comprende que la información contiene 
			declaraciones que constituyen pronósticos y no representan 
			la opinión del ministerio de salud y protección social de 
			Colombia.	
			'''),
			),
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
    Output("col-piramide", "children"),
    Output("col-pie-Discapacidad", "children"),],
    [Input("checklist_tab1", "value"),
    Input("dropdown_tab1", "value"),],
)
def update_output(value,value_dropdown):
    if not value:
        tmp_df = pd.DataFrame(columns=df_data_ruv.columns)
    elif 'EsVictima' in value:
        tmp_df = df_data_ruv
    else:
        tmp_df = df_data_ruv
        for i in value:
            tmp_df = tmp_df[tmp_df[i]=='Si']
    tmp_df = tmp_df[tmp_df.CodigoDepartamento.apply(lambda x : x in value_dropdown)]
    gener = def_graphic.build_gener(total_vic(tmp_df),
                                        total_men(tmp_df),
                                        total_women(tmp_df)                                    
                                    )
    etnia = def_graphic.generate_piechart('Etnias',get_Etnia(tmp_df))
    map = def_graphic.map(get_map_info(tmp_df),geojson)
    piramide = def_graphic.generate_Stacked_barchar(tmp_df,'Piramide Poblacional')
    discapacidad = def_graphic.generate_piechart('Discapacidad',get_discapacidad(tmp_df))
    return gener,etnia, map, piramide,discapacidad


if __name__ == "__main__":
    load_data()
    app.run_server(debug=True)
