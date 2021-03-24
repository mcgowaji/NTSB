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
from database import transforms
from config import dbname, db_user, host, db_password, sslmode


#Run Streaming script asynchronously to keep stream live
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

    # #Run Streaming script asynchronously to keep stream live
    # script_fn = 'twitter_api.py'
    # exec(open(script_fn).read())
    
    return html.Div([
                    html.P(tweet_df['text'][0])
                    ,html.P(tweet_df['text'][1])
                    ,html.P(tweet_df['text'][2])
            ])

if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = 8000)
