import pandas as pd
import sqlite3
import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import psycopg2
import os
from config import host, dbname, db_user, db_password, sslmode

# Construct connection string
conn_string = "dbname={} user={} host={} password={} port='5432' sslmode={}".format(
    dbname, db_user, host, db_password, sslmode
)
conn = psycopg2.connect(conn_string)

df = pd.read_sql("select * from tweet_threats;", conn)

#Close when data extraction complete
conn.close()