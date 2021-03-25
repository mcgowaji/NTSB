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
from app import app, server
from tabs import sidepanel, tab1, tab2
from twitter_api import do_query
import os

#Create table before filling with streaming tweets
#Run only once
# threat_table = '''CREATE TABLE IF NOT EXISTS unique_threats (
#     tweet_id CHAR(19) PRIMARY KEY,
#     date TIMESTAMP,
#     username VARCHAR,
#     is_retweet BOOL,
#     is_quote BOOL,
#     text VARCHAR,
#     quoted_text VARCHAR,
#     hashtags TEXT []
# );
# '''
#
# do_query(threat_table)

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
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
    cursor = conn.cursor()
    
    sql = '''select text from unique_threats
                    where text not like 'RT %'
                    order by date desc
                    LIMIT 5;'''
    tweet_df = pd.read_sql(sql, conn)
    print(tweet_df)
    return html.Div([
                    html.P(tweet_df['text'][0])
                    ,html.P(tweet_df['text'][1])
                    ,html.P(tweet_df['text'][2])
            ])

if __name__ == '__main__':
    app.run_server(debug = True)
