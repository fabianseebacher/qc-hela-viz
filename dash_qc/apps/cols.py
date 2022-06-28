import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from numpy import diff
import plotly.express as px

import dash_daq as daq
import pandas as pd

from app import app

df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
df['date created'] =  pd.to_datetime(df['date created'])

layout = html.Div([

        html.H1(["Columns"]),

        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='filter-dropdown-2',
                    options=[
                        {'label': 'all', 'value': 'all'},
                        {'label': 'noFAIMS/500ng/CPMS/2h only', 'value': 'nofaims'},
                        {'label': '1CV/500ng/CPMS/2h only', 'value': '1cv'},
                        {'label': '1CV/500ng/CPMS/1h only', 'value': '1cv_short'},
                        {'label': '2CV/500ng/CPMS/2h only', 'value': '2cv'}
                    ],
                    value='1cv',
                    clearable=False
                )
            ], style={'display': 'inline-block', 'width': '66%'}),


        ]),

        html.Br(),

        html.Div([
            html.Label(["Select column"]),
            dcc.Dropdown(
                id='col-selection',
                options=[{'label': i, 'value': i} for i in df['column'].unique().tolist()],
                value='unknown'
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            # html.Label(["Select y axis data"]),
            # dcc.Dropdown(
            #     id='yaxis-column',
            #     options=[{'label': i, 'value': i} for i in  df.columns.tolist()],
            #     value='ProteinGroups'
            # )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    
        

    html.Br(),

    html.Div([
            html.Div([
                html.Label(["Hide suspicious runs"]),
                daq.BooleanSwitch(
                    id='toggle-hide',
                    on=True
                )
            ],style={'width': '25%', 'display': 'inline-block', 'float': 'left'})
            
        ],style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
            # html.Div([
            #     html.Label(["Hide suspicious runs"]),
            #     daq.BooleanSwitch(
            #         id='toggle-hide',
            #         on=True
            #     )
            # ],style={'width': '25%', 'display': 'inline-block', 'float': 'left'})
            
        ],style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),

    html.Br(),

    dcc.Graph(id='column-graph'),

])

@app.callback(
    Output('column-graph', 'figure'),
    [Input('col-selection', 'value'),
    Input('filter-dropdown-2', 'value'),
    Input('toggle-hide', 'on')])
def update_graph_2(selected_column, filter, hide):

    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])
    if hide == True:
        # Filter out suspicious runs
        df = df[(df['ProteinGroups'] > 500) & (df['Peptide Seq Identified'] > 5000)]
    
    if filter == "2cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
    elif filter == "nofaims":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
    elif filter == "1cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
    elif filter == "1cv_short":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '1h')]
    else:
        dff = df
    
    dfc = dff.copy()
    dff = dff[dff['column'] == selected_column]

    fig = px.scatter(x=dff['date created'],
                     y=dff['ProteinGroups'],
                     hover_name=dff['Filename'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', uirevision=True)

    fig.update_xaxes(title='date created',
                     type='date')

    fig.update_yaxes(title='ProteinGroups',
                     type='linear')

    return fig

