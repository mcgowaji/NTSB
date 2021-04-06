import plotly.graph_objects as go
import plotly.express as px
import numpy as np


#Optional transformations
df.target = df.target.map({0:'No Injuries', 1:'Injured'})
df['Cluster Number'] = df['Cluster Number'].astype(int)


#Slice the '_probs' off of the columns
all_cluster_probs = all_cluster_probs.columns.map(lambda x: x[:-5])
#Get max value of cluster from cluster probability columns
all_cluster_probs = all_cluster_probs.idxmax(axis=1)

burst = px.sunburst(
    df,
    path=['Cluster Number', 'target'],

)
burst.update_traces(textinfo='label+percent parent')
burst.update_layout(title='Top Clusters and Injury Breakdown')
