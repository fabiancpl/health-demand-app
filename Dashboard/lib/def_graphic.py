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
from sklearn import preprocessing

#server
from app import app_load

def map(df,geojson,df2,label2):
    #Create the map:
    Map_Fig=px.choropleth_mapbox(df,                           #Data
                locations=df.columns[0],                       #Column containing the identifiers used in the GeoJSON file 
                color=df.columns[2],                           #Column giving the color intensity of the region
                hover_name=df.columns[1],
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
    tmp_s = (df2.PromedioAnno-df2.PromedioAnno.min())/(df2.PromedioAnno.max()-df2.PromedioAnno.min())
    Map_Fig.add_trace(
    	go.Scattermapbox(
        	lat=df2.Lon,
	        lon=df2.Lat,
        	mode='markers',
        	marker=go.scattermapbox.Marker(
            		size=10*tmp_s
        	),
        	text=df2.Departamento +" <br>"+label2 +df2.PromedioAnno.map(str),textposition = "bottom right"
    	)
    )

    return dcc.Graph(figure=Map_Fig,id="colombia_map") 
    #return html.P('Hola',id="colombia_map")  # delete and uncomment 

def build_gener(total, women, men):
    return html.Div(
                id="gener",
                className="gener",
                children=[
                    dbc.Row(
                        html.P("Total Base: "+ str(total)), id="row-titel-gener",justify='center'
                    ),
                    dbc.Row([
                        dbc.Col(
                        html.Img(id="woman-logo", src=app_load.get_asset_url("woman.png"))
                        ),
                        dbc.Col(html.Img(id="man-logo", src=app_load.get_asset_url("man.png"))),
                    ],id="row-gener-logo",justify='center'),
                    dbc.Row([
                        dbc.Col([html.P(str(women)), ]),
						dbc.Col([html.P(str(men)), ]),
                    ],id="row-gener-values",justify='center')
                                
                ]
            )

def generate_piechart(title_df,df,id):
    return  dcc.Graph(
                        id=id,
                        figure=(px.pie(df, values=df.columns[1], names=df.columns[0]).update_layout(
                            paper_bgcolor="#F8F9F9",
                            title=title_df,
                            autosize=True,           
                            #margin={"r":0,"t":30,"l":0,"b":0},
                            showlegend=False,
                            ).update_yaxes(automargin=True)
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
    return dcc.Graph(figure=px.line(df, x=df.columns[0], y=df.columns[2], color=df.columns[1]).update_layout(
                            #paper_bgcolor="#F8F9F9",
                            autosize=True,           
                            #margin={"r":0,"t":0,"l":0,"b":50},
                            showlegend=True,
			    height=320,
			    legend=dict(
                                    yanchor="bottom",
                                    orientation="h",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01
                                ),
                            paper_bgcolor = 'rgba(0,0,0,0)',
                            plot_bgcolor = 'rgba(0,0,0,0)'
                            ).update_yaxes(automargin=True), id='Char_line')

def generate_bar_chart(df,title):
    df = df.sort_values(by=df.columns[1])
    return dcc.Graph(
                figure= px.bar(df, x=df.columns[0], y=df.columns[1]).update_layout(title=title ,paper_bgcolor="#F8F9F9", uniformtext_minsize=8, uniformtext_mode='hide'),
                id='Colombia_bar',
            )

def generate_violin_plot(df,column):
    fig = go.Figure()
    values = df[column].unique()
    for value in values:
        fig.add_trace(go.Violin(x=df[column][df[column] == value],
                                y=df['Total'][df[column] == value],
                                name=value,
                                box_visible=True,
                                meanline_visible=True))
    fig.update_layout(#paper_bgcolor="#F8F9F9",
                            title=column,
                            height=220,
 			    width=500,
                            autosize=True,           
                            margin={"r":0,"t":50,"l":0,"b":0},
                            showlegend=False,
                            paper_bgcolor = 'rgba(0,0,0,0)',
                            plot_bgcolor = 'rgba(0,0,0,0)').update_yaxes(automargin=True)
    return dcc.Graph(
                figure=fig, id='violin_plot'
            )

def generate_Stacked_barchar(df,title):
    df_tmp = pd.pivot_table(df[df.GrupoEdad !=  'NA'], values='Total', index=['GrupoEdad'],columns=['Sexo'], aggfunc=np.sum).reset_index()
    df_tmp['Index']=pd.to_numeric(df_tmp.GrupoEdad.str.split(',',expand=True)[0].str.split('[',expand=True)[1])
    df_tmp.sort_values(by='Index',inplace=True)
    layout = go.Layout( title = 'Personas Victimas por Edad y Sexo',
                       yaxis = go.layout.YAxis( title = 'Edad' ),
                       xaxis = go.layout.XAxis(
                           #range = [ -40000, 60000 ],
                           title = 'Número de Personas Victimas'
                       ),
                       barmode = 'overlay',
                       bargap = 0.1
                      )

    data = [ go.Bar( y = df_tmp[ 'GrupoEdad' ].astype( str ),
                    x = df_tmp['Masculino']*-1,
                    orientation = 'h',
                    name = 'Hombre',
                    text = df_tmp[ 'Masculino' ],
                    hoverinfo = 'text',
                    marker = dict( color = '#91b0ff' )
                   ),
            go.Bar( y = df_tmp[ 'GrupoEdad' ].astype( str ),
                   x = df_tmp[ 'Femenino' ],
                   orientation = 'h',
                   name ='Mujer',
                   text = df_tmp[ 'Femenino' ],
                   hoverinfo = 'text',
                   marker = dict( color = '#f23a87' )
                  ) 
           ]

    fig = go.Figure( dict( data = data, layout = layout ) ).update_layout(paper_bgcolor = 'rgba(0,0,0,0)',
                            						plot_bgcolor = 'rgba(0,0,0,0)',
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


def generate_treemap(df):
    return dcc.Graph(figure= px.treemap(df,path=[df.columns[0]],values=df.columns[1]).update_layout(
											height=320,
											margin={"r":0,"t":0,"l":0,"b":0},
											paper_bgcolor="#F8F9F9",
											autosize=True),id='treemap_plot') 
