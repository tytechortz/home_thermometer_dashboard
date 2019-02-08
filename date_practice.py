import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from dateutil.relativedelta import relativedelta
import plotly.graph_objs as go
import requests
import pandas as pd 
import time
# import datetime
from datetime import datetime

app = dash.Dash(__name__)



if __name__ == '__main__':
    app.run_server()

