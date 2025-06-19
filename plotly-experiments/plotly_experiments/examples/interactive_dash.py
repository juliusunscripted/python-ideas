# https://plotly.com/python/graph-objects/#what-about-dash

# %%
import plotly.graph_objects as go  # or plotly.express as px
from dash import Dash, dcc, html

# %%

fig_empty = go.Figure()  # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )


fig = go.Figure(data=[go.Bar(y=[2, 1, 3])], layout_title_text="A Figure")


app = Dash()
app.layout = html.Div([dcc.Graph(figure=fig_empty), dcc.Graph(figure=fig)])

# %%

app.run(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

# %%
