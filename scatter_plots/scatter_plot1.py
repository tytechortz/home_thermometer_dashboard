#######
# This plots 100 random data points (set the seed to 42 to
# obtain the same points we do!) between 1 and 100 in both
# vertical and horizontal directions.
######
import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np

np.random.seed(42)
random_x = np.random.randint(1,101,100)
random_y = np.random.randint(1,101,100)

data = [go.Scatter(
    x = random_x,
    y = random_y,
    mode = 'markers',
    marker = dict(
        size=12,
        color='rgb(51,204,153)',
        symbol= 'pentagon',
        line = {'width':2}
    ))]

layout = go.Layout(title='First Plot',
                    xaxis= {'title':'MY X AXIS'},
                    yaxis= dict(title='MY Y AXIS'),
                    hovermode='closest')

fig = go.Figure(data=data,layout=layout)
pyo.plot(fig, filename='scatter1.html')
