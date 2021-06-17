import dash
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server