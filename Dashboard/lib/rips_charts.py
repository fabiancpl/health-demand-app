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


##############################
#bar Layout
##############################


data_canada = px.data.gapminder().query("country == 'Canada'")
bar_fig = px.bar(data_canada, x='year', y='pop')
bar_fig.update_layout(title='Health in Colombia',
paper_bgcolor="#F8F9F9",
margin={"r":0,"t":0,"l":0,"b":0})

##############################
#line Layout
##############################

df = px.data.iris()
line_fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", facet_col="species",
                 title="Adding Traces To Subplots Witin A Plotly Express Figure")

reference_line = go.Scatter(x=[2, 4],
                            y=[4, 8],
                            mode="lines",
                            line=go.scatter.Line(color="gray"),
                            showlegend=False)

line_fig.add_trace(reference_line, row=1, col=1)
line_fig.add_trace(reference_line, row=1, col=2)
line_fig.add_trace(reference_line, row=1, col=3)
line_fig.update_layout(paper_bgcolor="#F8F9F9")


##############################
# Filter Layout
##############################

# Load data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv")
df.columns = [col.replace("AAPL.", "") for col in df.columns]

# Create figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(x=list(df.Date), y=list(df.High)))

# Set title
fig.update_layout(
    title_text="Time series with range slider and selectors"
)

# Add range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ),paper_bgcolor="#F8F9F9"
)



##############################
# Slider bar
##############################

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

def sliderBar():
    return [
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )]
    
@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     size="pop", color="continent", hover_name="country", 
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500,paper_bgcolor="#F8F9F9")

    return fig


body = html.Div([
    dbc.Row(
        dbc.Col(html.Div(dbc.Alert("Here could be the description or the filters", color="primary")))
    ),
    dbc.Row([
            dbc.Col(dcc.Graph(figure=bar_fig , id='Colombia_bar')),
            dbc.Col(dcc.Graph(figure=line_fig , id='Colombia_line')),
            dbc.Col(html.Div(sliderBar()))
            ])
        ])
        
        
        

def chart_col():
    return html.Div([
    dcc.Graph(figure=fig,id='Colombia_c')
    ], className="colombia_c")

