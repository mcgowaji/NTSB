import dash
import plotly
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
from utils import *

layout = html.Div([
    dbc.Row([
        #Display single narrative
        dbc.Col([
            html.H1('Select an Incident: '),
            html.Div(
                #Change this to incident/ACN Numbers
                dcc.Dropdown(
                    id='user-dropdown',
                    options=[{'label': ix, 'value': ix} for ix in range(highlights.shape[0])],
                    value= 0
                )
            ),
            html.Div(id = 'text-div'),
            html.Br(),
        ]),
        # Cluster wordmap
        dbc.Col([
            html.H1(id = 'cloud-title'),
            html.Div(html.Img(id = 'word-cloud')), 
        ])
    ]),
    dbc.Row([
        #Feature Importance bar graph
        dbc.Col([
            html.Div(
                dcc.Graph(figure = bar_figure)
            )
        ]),
        # Business case feature...
        dbc.Col([
            html.H1('shiny new feature')
        ])
    ])
])

@app.callback(
    [Output('text-div', 'children'),
    Output('cloud-title', 'children')],
    [Input('user-dropdown', 'value')]
)
def update_output(index):
    doc = highlights.Narrative.iloc[index]
    matches = highlights.Highlights.iloc[index]
    cluster_number = clusters['Cluster Number'].iloc[index]
    new_string = []
    color_spans = []
    idx = 0
    for word, start, end, (cluster, score) in matches:
        #Add span from beginning of doc to first match
        before_span = html.Span(doc[idx:start])
        new_string.append(before_span)
        idx = start
        lastidx = end
        color_span = html.Span(
            doc[idx:lastidx], 
            style = {'background-color': colors[cluster]}
        )
        new_string.append(color_span)
        #Conditional formatting for highlighting only words that
        # belong to this specific cluster
#         if cluster == cluster_number:
#             color_span = html.Span(
#                 doc[idx:lastidx], 
#                 style = {'background-color': colors[cluster]}
#             )

#             new_string.append(color_span)
        idx = lastidx
        
    #Add span from last match to end of document
    final_span = html.Span(doc[end:])
    new_string.append(final_span)
    
    processed = html.Div(new_string)
    title = f"Top words found in Cluster {int(cluster_number)}"
    return processed, title

@app.callback(
    Output('word-cloud', 'src'),
    [Input('user-dropdown', 'value')]
)

def generate_cloud(index):
    cluster_number = clusters['Cluster Number'].iloc[index]
    data = highlights[highlights['Cluster Number'] == cluster_number]
    stopwords = set(STOPWORDS).update(
        ['Reporter', 'stated', 'from', 'zzz', 'flight', 'aircraft']
    )
    #Compile string of all words in corpus
    word_bag = ''.join(y for y in [x for x in data.Narrative.values])
    wc = WordCloud(
        background_color = 'white',
        stopwords = stopwords,
    ).generate(text = word_bag)
    wc_img = wc.to_image()
    with BytesIO() as buffer:
        wc_img.save(buffer, 'png')
        img2 = base64.b64encode(buffer.getvalue()).decode()

    return "data:image/png;base64," + img2




