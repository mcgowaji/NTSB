import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output


layout = html.Div(
    dbc.Row([
        #Display single narrative
        dbc.Col([
            html.Div('Narrative Select list'),

        ]),
        # Cluster wordmap
        dbc.Col([
            html.Div('clusters'),
        ])
    ]),
    dbc.Row([
        #Feature Importance bar graph
        dbc.Col([
            html.Div('Feature importance')
        ]),
        # Business case feature...
        dbc.Col([
            html.Div('shiny new feature')
        ])
    ])
)




