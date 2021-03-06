from re import A
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import dash_daq as daq
import dash_table as dat
import yaml

from app import app

with open("settings.yml", 'r') as stream:
        settings = yaml.safe_load(stream)

### HELPER FUNCIONS ###
def style_histo(fig, filter, column_name, lowcut, highcut, min_pg, max_pg, newest_pg, divisor, reverse=False):

    if reverse == True:
        highcolor = settings['colorscheme']['badcolor']
        lowcolor = settings['colorscheme']['goodcolor']
    else:
        highcolor = settings['colorscheme']['goodcolor']
        lowcolor = settings['colorscheme']['badcolor']

    fig.update_layout(plot_bgcolor='white', 
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
            hovermode='closest')

    fig.update_yaxes(title='Count',
                     type='linear',
                     showgrid=True,
                     gridcolor='lightgrey')

    fig.update_xaxes(title=column_name,
                     type='linear',
                     showgrid=True,
                     gridcolor='lightgrey')

    # Draw #abe1d6, #f2f0dd and #f6d0a3 areas to quickly assess relative quality.
    if filter != 'all':
        fig.update_layout(shapes=[
            dict(
                type= 'rect',
                yref= 'paper', y0=0, y1=50,
                xref= 'x', x0=lowcut, x1=highcut,
                fillcolor = settings['colorscheme']['neutralcolor'],
                line_width = 0,
                opacity=1,
                layer='below'
            ),
            dict(
                type= 'rect',
                yref= 'paper', y0= 0, y1= 50,
                xref= 'x', x0=min_pg//divisor*divisor, x1= lowcut,
                fillcolor = lowcolor,
                line_width = 0,
                opacity=1,
                layer='below'
            ),
            dict(
                type= 'rect',
                yref= 'paper', y0= 0, y1= 50,
                xref= 'x', x0=highcut, x1=max_pg//divisor*divisor+divisor,
                fillcolor = highcolor,
                line_width = 0,
                opacity=1,
                layer='below'
            ),
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 50,
                xref= 'x', x0=newest_pg, x1=newest_pg,
                line = dict(
                    color='red',
                    dash='dot'
                )
            )
            ])
    else:
        fig.update_layout(shapes=[])
    return None

def style_dateplot(fig, filter, column_name, lowcut, highcut, min_pg, max_pg, divisor, reverse=False):

    if reverse == True:
        highcolor = settings['colorscheme']['badcolor']
        lowcolor = settings['colorscheme']['goodcolor']
    else:
        highcolor = settings['colorscheme']['goodcolor']
        lowcolor = settings['colorscheme']['badcolor']
    
    fig.update_layout(plot_bgcolor='white', 
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, 
            hovermode='closest')

    fig.update_yaxes(title=column_name,
                     type='linear',
                     showgrid=True,
                     gridcolor='lightgrey')

    fig.update_xaxes(title='Last 5 Helas',
                     type='category',
                     showgrid=True,
                     gridcolor='lightgrey')

    # Add extra trace for last hela in red increase marker size for all traces

    fig.add_scatter(x = [fig.data[0].x[-1]], y = [fig.data[0].y[-1]],
                     mode = 'markers',
                     marker = {'color':'red'},
                     showlegend = False,
                     hovertext=[fig.data[0].hovertext[-1]])

    fig.update_traces(marker=dict(size=10))

    # Draw #abe1d6, #f2f0dd and #f6d0a3 areas to quickly assess relative quality.

    if filter != 'all':
        fig.update_layout(shapes=[
            dict(
                type= 'rect',
                xref= 'paper', x0=0, x1=1,
                yref= 'y', y0=lowcut, y1=highcut,
                fillcolor = settings['colorscheme']['neutralcolor'],
                line_width = 0,
                opacity=1,
                layer='below'
            ),
            dict(
                type= 'rect',
                xref= 'paper', x0= 0, x1= 1,
                yref= 'y', y0=min_pg//divisor*divisor, y1= lowcut,
                fillcolor = lowcolor,
                line_width = 0,
                opacity=1,
                layer='below'
            ),
            dict(
                type= 'rect',
                xref= 'paper', x0= 0, x1= 1,
                yref= 'y', y0=highcut, y1=max_pg//divisor*divisor+divisor,
                fillcolor = highcolor,
                line_width = 0,
                opacity=1,
                layer='below'
            )])
            
    else:
        fig.update_layout(shapes=[])

    fig.update_traces(marker=dict(size=10))

    return None

### READ DATA FROM EXCEL FILE ###

df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
df['date created'] =  pd.to_datetime(df['date created'])
df = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]

df2 = df.sort_values('date created', ascending=False)
df2 = df2.rename(columns={'Peptide Seq Identified': 'Peptides', 'Retention length [s]': 'RetLen'})

### LAYOUT ###

layout = html.Div([
    html.Div([
        html.H1(["HeLa Live View"]),

        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='filter-dropdown',
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

            html.Div([
                daq.ToggleSwitch(
                    id='my-toggle-switch',
                    value=True
                ),
                html.Div(id='toggle-switch-output', style={'text-align':'center'})
            ], style={'display': 'inline-block', 'width': '33%', 'float': 'right'})

        ]),

        html.Br(),
    
        dat.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in ['date created', 'Filename', 'ProteinGroups', 'Peptides', 'RetLen',
                'MS TIC', 'MS Base peak intensity', 'MS/MS TIC', 'MS/MS Base peak intensity', 'Uncalibrated mass error [ppm]', 'File size [MB]', 'amount', 'gradient length', 'producer', 'FAIMS'
                ]],
            data=df2.sort_values('date created', ascending=False).head(5).to_dict('records'),
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'ProteinGroups',
                    },
                    'backgroundColor': settings['colorscheme']['neutralcolor'],
                    'color': 'black'
                },
                {
                    'if': {
                        'filter_query': '{ProteinGroups} > 5200',
                        'column_id': 'ProteinGroups'
                    },
                    'backgroundColor': settings['colorscheme']['goodcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{ProteinGroups} < 5000',
                        'column_id': 'ProteinGroups'
                    },
                    'backgroundColor': settings['colorscheme']['badcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'column_id': 'Peptides',
                    },
                    'backgroundColor': settings['colorscheme']['neutralcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{Peptides} > 25000',
                        'column_id': 'Peptides'
                    },
                    'backgroundColor': settings['colorscheme']['goodcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{Peptides} < 23000',
                        'column_id': 'Peptides'
                    },
                    'backgroundColor': settings['colorscheme']['badcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'column_id': 'RetLen',
                    },
                    'backgroundColor': settings['colorscheme']['neutralcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{RetLen} > 22',
                        'column_id': 'RetLen'
                    },
                    'backgroundColor': settings['colorscheme']['badcolor'],
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{RetLen} < 20',
                        'column_id': 'RetLen'
                    },
                    'backgroundColor': settings['colorscheme']['goodcolor'],
                    'color': 'black'
                }


            ]
        ),

        html.Br(),

        html.Div([

            html.Div([
                dcc.Graph(id='pg-graphic-histo'),
            ], style={'display': 'inline-block', 'width': '33%'}),

            html.Div([
                dcc.Graph(id='pept-graphic-histo'),
            ], style={'display': 'inline-block', 'width': '33%'}),

            html.Div([
                dcc.Graph(id='rl-graphic-histo'),
            ], style={'display': 'inline-block', 'width': '33%'})

        ], id='histo-div', style={'display': 'block'}),

        html.Div([

            html.Div([
                dcc.Graph(id='pg-graphic-date'),
            ], style={'display': 'inline-block', 'width': '33%'}),

            html.Div([
                dcc.Graph(id='pept-graphic-date'),
            ], style={'display': 'inline-block', 'width': '33%'}),

            html.Div([
                dcc.Graph(id='rl-graphic-date'),
            ], style={'display': 'inline-block', 'width': '33%'})

        ], id='date-div', style={'display': 'none'}),
    
    ]),

])

### CALLBACKS ### 

# Plot type toggle switch 
@app.callback(
    dash.dependencies.Output('toggle-switch-output', 'children'),
    [dash.dependencies.Input('my-toggle-switch', 'value')])
def update_output(value):
    if value == True:
        return 'Histogram Mode'
    else: 
        return 'Dateplot Mode'

# Show or hide histograms / dateplots ###
@app.callback(
   [dash.dependencies.Output(component_id='histo-div', component_property='style'),
   dash.dependencies.Output(component_id='date-div', component_property='style')],
   [dash.dependencies.Input(component_id='my-toggle-switch', component_property='value')])
def show_hide_histo(visibility_state):
    if visibility_state == True:
        return [{'display': 'block'}, {'display': 'none'}]
    if visibility_state == False:
        return [{'display': 'none'}, {'display': 'block'}]

# Update protein group graphs
@app.callback(
    [Output('pg-graphic-histo', 'figure'),
    Output('pg-graphic-date', 'figure'),
    Output('pept-graphic-histo', 'figure'),
    Output('pept-graphic-date', 'figure'),
    Output('rl-graphic-histo', 'figure'),
    Output('rl-graphic-date', 'figure')],
    [Input('filter-dropdown', 'value')])
def update_pg_graph(filter):

    with open("settings.yml", 'r') as stream:
        settings = yaml.safe_load(stream)

    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])

    if filter == "2cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
        thresholds = settings['2cv_2h_thresholds']
    elif filter == "nofaims":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
        thresholds = settings['nofaims_2h_thresholds']
    elif filter == "1cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
        thresholds = settings['1cv_2h_thresholds']
    elif filter == "1cv_short":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '1h')]
        thresholds = settings['1cv_1h_thresholds']
    elif filter == 'all':
        dff = df
        thresholds = settings['all_thresholds']

    min_prot = dff['ProteinGroups'].min()
    max_prot = dff['ProteinGroups'].max()
    newest_prot = int(dff.sort_values('date created', ascending=False).head(1)['ProteinGroups'])
    
    min_pept = dff['Peptide Seq Identified'].min()
    max_pept = dff['Peptide Seq Identified'].max()
    newest_pept = int(dff.sort_values('date created', ascending=False).head(1)['Peptide Seq Identified'])

    min_rt = dff['Retention length [s]'].min()
    max_rt = dff['Retention length [s]'].max()
    newest_rt = float(dff.sort_values('date created', ascending=False).head(1)['Retention length [s]'])


    df_new5 = dff.sort_values('date created', ascending=False).head(5).reset_index()
    df_new5.index = df_new5.index + 1

    # proteins histogram
    fig = px.histogram(dff, x='ProteinGroups', nbins=40, color_discrete_sequence=['lightgrey'])
    style_histo(fig, filter, 'ProteinGroups', thresholds[1], thresholds[0], min_prot, max_prot, newest_prot, 100, reverse=False)

    # proteins dateplot
    fig2 = px.scatter(x=df_new5['date created'][::-1], y=df_new5['ProteinGroups'][::-1], hover_name=df_new5['Filename'], color_discrete_sequence=['grey'])
    style_dateplot(fig2, filter, 'ProteinGroups', thresholds[1], thresholds[0], min_prot, max_prot, 100, reverse=False)

    # peptide histogram
    fig3 = px.histogram(dff, x='Peptide Seq Identified', nbins=40, color_discrete_sequence=['lightgrey'])
    style_histo(fig3, filter, 'Peptide Seq Identified', thresholds[3], thresholds[2], min_pept, max_pept, newest_pept, 1000, reverse=False)
    
    # peptide dateplot
    fig4 = px.scatter(x=df_new5['date created'][::-1], y=df_new5['Peptide Seq Identified'][::-1], hover_name=df_new5['Filename'], color_discrete_sequence=['grey'])
    style_dateplot(fig4, filter, 'Peptide Seq Identified', thresholds[3], thresholds[2], min_pept, max_pept, 1000, reverse=False)

    # retention length histogram
    fig5 = px.histogram(dff, x='Retention length [s]', nbins=40, color_discrete_sequence=['lightgrey'])
    style_histo(fig5, filter, 'Retention length [s]', thresholds[5], thresholds[4], min_rt, max_rt, newest_rt, 10, reverse=True)

    # retention length dateplot
    fig6 = px.scatter(x=df_new5['date created'][::-1], y=df_new5['Retention length [s]'][::-1], hover_name=df_new5['Filename'], color_discrete_sequence=['grey'])
    style_dateplot(fig6, filter, 'Retention length [s]', thresholds[5], thresholds[4], min_rt, max_rt, 10, reverse=True)

    return [fig,fig2,fig3,fig4,fig5,fig6]

@app.callback(
    [dash.dependencies.Output('table', 'data'), dash.dependencies.Output('table', 'style_data_conditional')],
    [dash.dependencies.Input('filter-dropdown', 'value')])
def update_table(filter):
    
    with open("settings.yml", 'r') as stream:
        settings = yaml.safe_load(stream)

    ### Filter table to only show the data corresponding to the dropdown filter.
    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto.xlsx", engine='openpyxl')
    tlist = [5200, 5000, 25000, 23000, 22, 20]
    df['date created'] =  pd.to_datetime(df['date created'])
    if filter == "2cv":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
        tlist = settings['2cv_2h_thresholds']
    elif filter == "nofaims":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
        tlist = settings['nofaims_2h_thresholds']
    elif filter == "1cv":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
        tlist = settings['1cv_2h_thresholds']
    elif filter == "1cv_short":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '1h')]
        tlist = settings['1cv_1h_thresholds']
    else:
        df3 = df
        tlist = settings['all_thresholds']

    if filter == 'all':
        current_style = None
    else:
        current_style = [
            {
                        'if': {
                            'column_id': 'ProteinGroups',
                        },
                        'backgroundColor': settings['colorscheme']['neutralcolor'],
                        'color': 'black'
                    },
                    {
                        'if': {
                            'filter_query': '{ProteinGroups} > '+str(tlist[0]),
                            'column_id': 'ProteinGroups'
                        },
                        'backgroundColor': settings['colorscheme']['goodcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'filter_query': '{ProteinGroups} < '+str(tlist[1]),
                            'column_id': 'ProteinGroups'
                        },
                        'backgroundColor': settings['colorscheme']['badcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'column_id': 'Peptides',
                        },
                        'backgroundColor': settings['colorscheme']['neutralcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'filter_query': '{Peptides} > '+str(tlist[2]),
                            'column_id': 'Peptides'
                        },
                        'backgroundColor': settings['colorscheme']['goodcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'filter_query': '{Peptides} < '+str(tlist[3]),
                            'column_id': 'Peptides'
                        },
                        'backgroundColor': settings['colorscheme']['badcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'column_id': 'RetLen',
                        },
                        'backgroundColor': settings['colorscheme']['neutralcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'filter_query': '{RetLen} > '+str(tlist[4]),
                            'column_id': 'RetLen'
                        },
                        'backgroundColor': settings['colorscheme']['badcolor'],
                        'color': 'black'
                    },

                    {
                        'if': {
                            'filter_query': '{RetLen} < '+str(tlist[5]),
                            'column_id': 'RetLen'
                        },
                        'backgroundColor': settings['colorscheme']['goodcolor'],
                        'color': 'black'
                    }
        ]
    
    return [df3.rename(columns={'Peptide Seq Identified': 'Peptides', 'Retention length [s]': 'RetLen'}).sort_values('date created', ascending=False).head(5).to_dict('records'), current_style]

