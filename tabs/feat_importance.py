from sklearn.inspection import permutation_importance
import plotly.graph_objects as go
import plotly.express as px


#Feature importances
perm_importance = permutation_importance(model, X_test, y_test)
sorted_idx = perm_importance.importances_mean.argsort()
bar_fig = px.bar(
    x=perm_importance.importances_mean[sorted_idx],
    y= df.columns[sorted_idx],
    orientation='h'
)

bar_fig.update_layout(
    title_text='Feature Importance',
    xaxis_title='Importance Ratings',
    yaxis_title='Variable'

)
