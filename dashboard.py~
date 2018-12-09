import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table

app = dash.Dash()

df = pd.read_csv('../Users/jamesswank/tempoct18.txt')

app.layout = html.Div([
    dcc.Graph(
        id='tempoct18',
        figure={
            'data': [
                go.Scatter(
                    x = df['X'],
                    y = df['Y'],
                    mode = 'markers'
                    )
            ],
            'layout': go.Layout(
                title = 'Old Faithful Eruption Intervals v Durations',
                xaxis = {'title': 'Duration of eruption (minutes)'},
                yaxis = {'title': 'Interval to next eruption (minutes)'},
                hovermode='closest'
            )

        }
    )
])

if __name__ == '__main__':
    app.run_server()
