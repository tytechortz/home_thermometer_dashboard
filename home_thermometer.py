#######
# Objective: build a dashboard that imports OldFaithful.csv
# from the data directory, and displays a scatterplot.
# The field names are:
# 'D' = date of recordings in month (in August),
# 'X' = duration of the current eruption in minutes (to nearest 0.1 minute),
# 'Y' = waiting time until the next eruption in minutes (to nearest minute).
######

# Perform imports here:
import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import dash  
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd




# Launch the application:
app = dash.Dash()

# Create a DataFrame from the .csv file:
df = pd.read_csv('../../tempjan19.txt')



# Create a Dash layout that contains a Graph component:
app.layout = html.Div([
    dcc.Graph(
        id='home_thermo',
        figure={
            'data': [
                go.Scatter(
                    x = df[0],
                    y = df[1],
                    mode = 'markers'
                )
            ],
            'layout': go.Layout(
                title = 'Home Temperature',
                xaxis = {'title': 'Date'},
                yaxis = {'title': 'Temperature'},
                hovermode='closest'
            )
        }
    )
])


# Add the server clause:
if __name__ == '__main__':
    app.run_server()