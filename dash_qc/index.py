import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import yaml

from app import app
from apps import explorer, qc


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("HeLa QC", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Live View", href="/apps/qc", active="exact", external_link=True),
                dbc.NavLink("Explorer", href="/apps/explorer", active="exact", external_link=True),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url", refresh=False), sidebar, content])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/explorer':
        return explorer.layout
    elif pathname == '/apps/qc':
        return qc.layout
    else:
        return '404'

if __name__ == '__main__':
    with open("settings.yml", 'r') as stream:
        settings = yaml.safe_load(stream)
    app.run_server(debug=False, host=settings['ip'], port=settings['port']) 

##############





