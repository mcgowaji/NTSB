import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_table
from app import app
from database import transforms
import networkx as nx

first_graph = pd.read_json('graph_files/TedCruz_graph.json')
first_nodes =  pd.DataFrame.from_records(first_graph['nodes'])
graph_layout = go.Layout(
    paper_bgcolor='#d2d2d2', # transparent background
    plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
    hovermode = 'closest',
    showlegend = False,
    width = 1200,
    height = 800,
    xaxis =  {'showgrid': False, 'zeroline': False, 'showticklabels': False},
    yaxis = {'showgrid': False, 'zeroline': False, 'showticklabels': False},
)
politicians = {
                'TedCruz' : 'Ted Cruz',
                'mattgaetz' :  'Matt Gaetz',
                'POTUS' : 'Joseph R. Biden',
                'VP' : 'Kamala Harris',
                'HawleyMO': 'Josh Hawley' ,
                'Jim_Jordan': 'Jim Jordan' ,
                'AOC': 'Alexandria Ocasio-Cortez',
                'BernieSanders' : 'Bernie Sanders',
                'LeaderMcConnell': 'Mitch McConnell',
                'Mike_Pence': 'Mike Pence'
                }
layout = html.Div([
            # id='table-paging-with-graph-container',
            # className="five columns"
    dbc.Row([
        dbc.Col(html.Div('Select person/group from list: '), width = 3),
        dbc.Col(
            dcc.Dropdown(
                id='user-dropdown',
                options=[{'label': val, 'value': key} for key, val in politicians.items()],
                value= 'TedCruz'
            ),
        width = 3
        ),
        dbc.Col(html.Div('Select total matches: '), width = '10vw'),
        dbc.Col([
        dcc.Input(id="total_input", type="number", debounce=True),
        ], width = 4
        ),
    ]),
     dcc.Graph(id='network-graph')
])


@app.callback(
    Output('network-graph', 'figure'),
    [Input('user-dropdown', 'value'),
     Input('total_input', 'value')]
)
def draw_network(user, total):
    '''Extract data from json file and render centrality graph,
    where color represents connection score and size represents that entity's follower count.

    Args:
        user - username of an entity in original graph

    Returns:
        graph - Networkx eigenvector centrality graph '''

    c_graph = pd.read_json('graph_files/{}_graph.json'.format(user))

    #Filter down to total_value if specified
    if total:
        c_graph = c_graph[:total]

    n = c_graph.shape[0]

    edges = pd.DataFrame.from_records(c_graph['links'])
    nodes = pd.DataFrame.from_records(c_graph['nodes'])

    H = nx.from_pandas_edgelist(edges, 'source', 'target', edge_attr='weight')
    # Set size & weight attributes from each DataFrame
    node_attr = nodes.set_index('id').to_dict('index')
    edge_attr = edges.set_index('target').to_dict('index')
    size_rank = dict(
        zip(
            nodes.sort_values(by='size', ascending=False)['size'], range(1, n + 1)
        )
    )
    pos = nx.spring_layout(H)

    ## Reformatting for Plotly figure
    edge_x = []
    edge_y = []
    for edge in H.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5,
                  color='white'
                  ),
        hoverinfo='none',
        mode='lines'
    )

    # Draw nodes from x, y positions found in pos
    node_x = []
    node_y = []
    for node in pos:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_df = pd.DataFrame({
        'x': node_x,
        'y': node_y,
        'text': nodes['name'].values,
        'followers': nodes['size'].values,
        'size_rank': [size_rank[value] for value in nodes['size'].values]
    })
    # Normalize values for better size weighting
    norms = (node_df['followers'] - node_df['followers'].min()) / (
                node_df['followers'].max() - node_df['followers'].min())
    node_trace = go.Scatter(
        x=node_df['x'],
        y=node_df['y'],
        showlegend=False,
        mode='markers+text',
        text=nodes['name'].values,
        textfont_color = 'black',
        customdata=node_df['followers'],
        hovertemplate='<b>%{text}</b><br>' +
                      'Connection Score: %{marker.color:.2f}<br>' +
                      'Followers: %{customdata}',
        marker=dict(
            color=100 * edges['weight'].values,
            showscale=True,
            colorscale='Jet',
            cmin=0,
            # Set max to first non-center weight
            cmax=100 * edges['weight'].values[1],
            #             size = 80 - 80*node_df['size_rank']/n,
            size=100 * norms * node_df['size_rank'],
            line_width=2,
            colorbar=dict(
                thickness=15,
                title='Strength of Connection',
                xanchor='left',
                titleside='right'
            ),
        )
    )

    fig = go.Figure(data=[node_trace, edge_trace], layout = graph_layout)
    fig.update_layout(
        title={
            'text': 'Top Mentions of {}'.format(node_attr[user]['name']),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    return fig
