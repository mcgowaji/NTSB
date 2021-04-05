import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import psycopg2
from app import app, server
from tabs import sidepanel, tab1, tab2, tab3
import os
from transforms import df
  
app.layout = sidepanel.layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')]
              )
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
       return tab2.layout
    elif tab == 'tab-3':
       return tab3.layout

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_tweet(n):
    # Construct connection string, connect to DB

    conn_string = "dbname={} user={} host={} password={} port='5432' sslmode={}".format(
        db_name, db_user, host, db_password, sslmode
    )
    conn = psycopg2.connect(conn_string)

    return html.Div([
                    html.P(tweet_df['text'][0])
                    ,html.P(tweet_df['text'][1])
                    ,html.P(tweet_df['text'][2])
            ])

if __name__ == '__main__':
    app.run_server(debug = True, port = 8000)

