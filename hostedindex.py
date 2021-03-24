import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import sqlite3
import pandas as pd
import psycopg2
from app import app
from tabs import sidepanel, tab1, tab2
import os
#import the API keys from the config file, or from Heroku config vars.
try:
    from config import dbname, db_user, host, db_password, sslmode
except ModuleNotFoundError:
    host = os.environ['HOST']
    print(host)
    dbname = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    sslmode = os.environ['SSL_MODE']

#Run Streaming script asynchronously for live updates
script_fn = 'twitter_api.py'
exec(open(script_fn).read())
    
app.layout = sidepanel.layout

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')]
              )
def render_content(tab):
    if tab == 'tab-1':
        return tab1.layout
    elif tab == 'tab-2':
       return tab2.layout
    #Add 3rd tab if necessary
    # elif tab == 'tab-3':
    #    return tab3.layout

@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_tweet(n):
    # Construct connection string
    conn_string = "dbname={} user={} host={} password={} port='5432' sslmode={}".format(
        dbname, db_user, host, db_password, sslmode
    )
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    
    sql = '''select text from unique_threats
                    where text not like 'RT %'
                    order by date desc
                    LIMIT 5;'''
    tweet_df = pd.read_sql(sql, conn)
    
    return html.Div([
                    html.P(tweet_df['text'][0])
                    ,html.P(tweet_df['text'][1])
                    ,html.P(tweet_df['text'][2])
            ])

if __name__ == '__main__':
    app.run_server(debug = False)
