import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

from app import app

df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
df['date created'] =  pd.to_datetime(df['date created'])

#df2 = df
#df = df.rename(columns={'Peptide Seq Identified': 'Peptides', 'Retention length [s]': 'RetLen'})

layout = html.Div([

        html.H1(["HeLa Explorer"]),

        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='filter-dropdown',
                    options=[
                        {'label': 'all', 'value': 'all'},
                        {'label': 'noFAIMS/500ng/CPMS/2h only', 'value': 'nofaims'},
                        {'label': '1CV/500ng/CPMS/2h only', 'value': '1cv'},
                        {'label': '2CV/500ng/CPMS/2h only', 'value': '2cv'}
                    ],
                    value='1cv',
                    clearable=False
                )
            ], style={'display': 'inline-block', 'width': '66%'}),


        ]),

        html.Br(),

        html.Div([
            html.Label(["Select x axis data"]),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns.tolist()],
                value='Peptide Seq Identified'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log', 'Date', 'Category']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Label(["Select y axis data"]),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in  df.columns.tolist()],
                value='ProteinGroups'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log', 'Date', 'Category']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    
        

    html.Br(),

    html.Div([
            html.Label(["Select column for color coding"]),
            dcc.Dropdown(
                id='color-column',
                options=[{'label': i, 'value': i} for i in  df.columns.tolist()],
                value='FAIMS'
            )
            
        ],style={'width': '48%', 'display': 'inline-block'}),

    html.Br(),

    dcc.Graph(id='indicator-graphic'),

])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('color-column', 'value'),
    Input('filter-dropdown', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, color_column_name, filter):

    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])
    #df = df.rename(columns={'Peptide Seq Identified': 'Peptides', 'Retention length [s]': 'RetLen'})
    if filter == "2cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
    elif filter == "nofaims":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
    elif filter == "1cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
    else:
        dff = df

    fig = px.scatter(x=dff[str(xaxis_column_name)],
                     y=dff[str(yaxis_column_name)],
                     hover_name=dff['Filename'],
                     color=dff[str(color_column_name)])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', uirevision=True)

    fig.update_xaxes(title=xaxis_column_name,
                     type=str(xaxis_type).lower())

    fig.update_yaxes(title=yaxis_column_name,
                     type=str(yaxis_type).lower())

    return fig

