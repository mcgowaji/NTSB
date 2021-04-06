import plotly.graph_objects as go
import plotly.express as px

num_topics = 21
cluster_labels = ['Cluster {}'.format(num+1) for num in range(num_topics)]
values = [cluster_labels, #1st col
  [[w[0] for w in topic] for index, topic in lda_long.show_topics(
    formatted=False, num_words= 5, num_topics = num_topics)]
         ]

#Cannot be put into a multiple subplot figure, must stand alone
cluster_labels = ['Cluster {}'.format(num+1) for num in range(num_topics)]
values = [
  cluster_labels, #1st col
  [[w[0] for w in topic] for index, topic in lda_long.show_topics(
    formatted=False, num_words= 7, num_topics = num_topics)]
         ]


chart_fig = go.Figure(data=[go.Table(
  columnorder = [1,2],
  columnwidth = [80,400],
  header = dict(
    values = [['<b>EXPENSES</b><br>as of July 2017'],
                  ['<b>Top 7 Words in Cluster</b>']],
    line_color='darkslategray',
    fill_color='royalblue',
    align=['left','center'],
    font=dict(color='white', size=12),
    height=40
  ),
  cells=dict(
    values=values,
    line_color='darkslategray',
    fill=dict(color=['paleturquoise', 'white']),
    align=['left', 'center'],
    font_size=12,
    height=30)
    )
])
