import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
from app import app


layout =html.Div(
    html.Iframe(src=app.get_asset_url('ldavis_prepared_8.html'),
                style=dict(height = "80vh", width="100%")
                )
)

