import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc 
import dash_table
import pandas
from dash.dependencies import Input, Output
from app import app
from tabs import tab1, tab2, tab3

colors = {
    # 'background': '#e5e5e5',
        'background': 'white',
    'shadow': '2px 2px 2px 2px #000045',
    #     'paper': '#fffff9', #cream
    'paper': 'white',
    'text': 'black',
}

pretty_container = {
    'border-radius': '40px',
    'background-color': colors['background'],
    'margin': '10px',
    'padding': '10px',
    'box-shadow': colors['shadow'],
    'textAlign': 'center'
}

layout = html.Div([

    dbc.Row([
        dbc.Col(
            html.Div([
            html.Img(src=app.get_asset_url('Topologe Logo Alpha+ (1).png'),
                     style={'width': '50%'}

                     ),
            html.H2('Parler Topics & Networks'),

            html.Div([
                html.H4('Live Twitter Feed'),
                html.Div(id='live-update-text'),
            ],
            style = pretty_container
            ),

            ],
            style={'marginBottom': 50, 'marginTop': 25, 'marginLeft':15, 'marginRight':15}),
            width=3
        ),
    dbc.Col(html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label = 'NTSB Data Summary', value='tab-1'),
                    dcc.Tab(label = 'LDA Topic Map', value = 'tab-2'),
                    dcc.Tab(label = 'Feature Importance', value = 'tab-3'),
                ]),
            html.Div(id='tabs-content')
        ],
        style={'marginTop': 15, 'marginLeft': 15, 'marginRight': 15}),
        width=9
    )
    ]),
])

