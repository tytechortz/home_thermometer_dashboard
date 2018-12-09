import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import dash_table

app = dash.Dash()

df = pd.read_csv('./data/tempoct18.txt')

app.layout = html.Div([
    dcc.Graph(
        id='tempoct18',
        figure={
            'data': [
                go.Scatter(
                    x = df[df.columns[0]],
                    y = df[df.columns[1]],
                    mode = 'lines'
                    )
                ]
            }
    )
])


if __name__ == '__main__':
    app.run_server()
