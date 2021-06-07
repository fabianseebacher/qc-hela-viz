import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import dash_daq as daq
import dash_table as dat

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

### HELPER FUNCIONS ###
def style_histo(fig, filter, column_name, lowcut, highcut, min_pg, max_pg, newest_pg, divisor, reverse=False):

    if reverse == True:
        highcolor = 'red'
        lowcolor = 'green'
    else:
        highcolor = 'green'
        lowcolor = 'red'

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

    # Draw green, yellow and red areas to quickly assess relative quality.
    if filter != 'all':
        fig.update_layout(shapes=[
            dict(
                type= 'rect',
                yref= 'paper', y0=0, y1=50,
                xref= 'x', x0=lowcut, x1=highcut,
                fillcolor = 'yellow',
                line_width = 0,
                opacity=0.2,
                layer='below'
            ),
            dict(
                type= 'rect',
                yref= 'paper', y0= 0, y1= 50,
                xref= 'x', x0=min_pg//divisor*divisor, x1= lowcut,
                fillcolor = lowcolor,
                line_width = 0,
                opacity=0.2,
                layer='below'
            ),
            dict(
                type= 'rect',
                yref= 'paper', y0= 0, y1= 50,
                xref= 'x', x0=highcut, x1=max_pg//divisor*divisor+divisor,
                fillcolor = highcolor,
                line_width = 0,
                opacity=0.2,
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
        highcolor = 'red'
        lowcolor = 'green'
    else:
        highcolor = 'green'
        lowcolor = 'red'
    
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

    # Draw green, yellow and red areas to quickly assess relative quality.

    if filter != 'all':
        fig.update_layout(shapes=[
            dict(
                type= 'rect',
                xref= 'paper', x0=0, x1=1,
                yref= 'y', y0=lowcut, y1=highcut,
                fillcolor = 'yellow',
                line_width = 0,
                opacity=0.2
            ),
            dict(
                type= 'rect',
                xref= 'paper', x0= 0, x1= 1,
                yref= 'y', y0=min_pg//divisor*divisor, y1= lowcut,
                fillcolor = lowcolor,
                line_width = 0,
                opacity=0.2
            ),
            dict(
                type= 'rect',
                xref= 'paper', x0= 0, x1= 1,
                yref= 'y', y0=highcut, y1=max_pg//divisor*divisor+divisor,
                fillcolor = highcolor,
                line_width = 0,
                opacity=0.2
            )])
            
    else:
        fig.update_layout(shapes=[])

    fig.update_traces(marker=dict(size=10))

    return None

### READ DATA FROM EXCEL FILE ###

df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto2.xlsx", engine='openpyxl')
df['date created'] =  pd.to_datetime(df['date created'])

df2 = df
df2 = df2.rename(columns={'Peptide Seq Identified': 'Peptides', 'Retention length [s]': 'RetLen'})

### LAYOUT ###

app.layout = html.Div([
    html.Div([
        html.H1(["HeLa Live View"]),

        html.Br(),
        
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
                    'backgroundColor': 'lightgoldenrodyellow',
                    'color': 'black'
                },
                {
                    'if': {
                        'filter_query': '{ProteinGroups} > 5200',
                        'column_id': 'ProteinGroups'
                    },
                    'backgroundColor': 'lightgreen',
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{ProteinGroups} < 5000',
                        'column_id': 'ProteinGroups'
                    },
                    'backgroundColor': 'lightpink',
                    'color': 'black'
                },

                {
                    'if': {
                        'column_id': 'Peptides',
                    },
                    'backgroundColor': 'lightgoldenrodyellow',
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{Peptides} > 25000',
                        'column_id': 'Peptides'
                    },
                    'backgroundColor': 'lightgreen',
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{Peptides} < 23000',
                        'column_id': 'Peptides'
                    },
                    'backgroundColor': 'lightpink',
                    'color': 'black'
                },

                {
                    'if': {
                        'column_id': 'RetLen',
                    },
                    'backgroundColor': 'lightgoldenrodyellow',
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{RetLen} > 22',
                        'column_id': 'RetLen'
                    },
                    'backgroundColor': 'lightpink',
                    'color': 'black'
                },

                {
                    'if': {
                        'filter_query': '{RetLen} < 20',
                        'column_id': 'RetLen'
                    },
                    'backgroundColor': 'lightgreen',
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
    Output('pg-graphic-date', 'figure')],
    [Input('filter-dropdown', 'value')])
def update_pg_graph(filter):
    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto2.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])

    if filter == "2cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
        lowcut = 5300
        highcut = 5500
    elif filter == "nofaims":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
        lowcut = 4500
        highcut = 4800
    elif filter == "1cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
        lowcut = 5000
        highcut = 5200
    elif filter == 'all':
        dff = df

    min_pg = dff['ProteinGroups'].min()
    max_pg = dff['ProteinGroups'].max()
    newest_pg = int(dff.sort_values('date created', ascending=False).head(1)['ProteinGroups'])
    df_new5 = dff.sort_values('date created', ascending=False).head(5).reset_index()
    df_new5.index = df_new5.index + 1

    # fig1

    fig = px.histogram(dff, x='ProteinGroups', nbins=40, color_discrete_sequence=['lightgrey'])
    column_name = 'ProteinGroups'
    style_histo(fig, filter, column_name, lowcut, highcut, min_pg, max_pg, newest_pg, 100, reverse=False)

    # fig2

    

    fig2 = px.scatter(x=df_new5['date created'][::-1],
                     y=df_new5['ProteinGroups'][::-1],
                     hover_name=df_new5['Filename'],
                     color_discrete_sequence=['grey'])
    style_dateplot(fig2, filter, column_name, lowcut, highcut, min_pg, max_pg, 100, reverse=False)

    return [fig,fig2]

# Update peptide graphs
@app.callback(
    [Output('pept-graphic-histo', 'figure'),
    Output('pept-graphic-date', 'figure')],
    [Input('filter-dropdown', 'value')])
def update_pept_graph(filter):

    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto2.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])

    if filter == "2cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
        lowcut = 32000
        highcut = 35000
    elif filter == "nofaims":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
        lowcut = 28000
        highcut = 30000
    elif filter == "1cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
        lowcut = 23000
        highcut = 25000
    elif filter == 'all':
        dff = df

    column_name = 'Peptide Seq Identified'
    min_pg = dff['Peptide Seq Identified'].min()
    max_pg = dff['Peptide Seq Identified'].max()
    newest_pg = int(dff.sort_values('date created', ascending=False).head(1)['Peptide Seq Identified'])
    df_new5 = dff.sort_values('date created', ascending=False).head(5).reset_index()
    df_new5.index = df_new5.index + 1

    fig = px.histogram(dff, x='Peptide Seq Identified', nbins=40, color_discrete_sequence=['lightgrey'])
    
    style_histo(fig, filter, column_name, lowcut, highcut, min_pg, max_pg, newest_pg, 1000, reverse=False)
    
    # Fig2
    
    fig2 = px.scatter(x=df_new5['date created'][::-1],
                     y=df_new5['Peptide Seq Identified'][::-1],
                     hover_name=df_new5['Filename'],
                     color_discrete_sequence=['grey'])
    style_dateplot(fig2, filter, column_name, lowcut, highcut, min_pg, max_pg, 1000, reverse=False)

    return [fig,fig2]

# Update retention length graphs
@app.callback(
    [Output('rl-graphic-histo', 'figure'),
    Output('rl-graphic-date', 'figure')],
    [Input('filter-dropdown', 'value')])
def update_rl_graph(filter):

    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto2.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])

    if filter == "2cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
        lowcut = 27
        highcut = 30
    elif filter == "nofaims":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
        lowcut = 20
        highcut = 22
    elif filter == "1cv":
        dff = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
        lowcut = 20
        highcut = 22
    elif filter == 'all':
        dff = df

    column_name = 'Retention length [s]'
    min_pg = dff['Retention length [s]'].min()
    max_pg = dff['Retention length [s]'].max()
    newest_pg = int(dff.sort_values('date created', ascending=False).head(1)['Retention length [s]'])
    df_new5 = dff.sort_values('date created', ascending=False).head(5).reset_index()
    df_new5.index = df_new5.index + 1
    
    fig = px.histogram(dff, x='Retention length [s]', nbins=40, color_discrete_sequence=['lightgrey'])

    style_histo(fig, filter, column_name, lowcut, highcut, min_pg, max_pg, newest_pg, 10, reverse=True)

    # Fig2

    fig2 = px.scatter(x=df_new5['date created'][::-1],
                     y=df_new5['Retention length [s]'][::-1],
                     hover_name=df_new5['Filename'],
                     color_discrete_sequence=['grey']
                     )

    style_dateplot(fig2, filter, column_name, lowcut, highcut, min_pg, max_pg, 10, reverse=True)

    return [fig,fig2]

@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('filter-dropdown', 'value')])
def update_table(filter):
    ### Filter table to only show the data corresponding to the dropdown filter.
    df = pd.read_excel("N:\IDO_Proteomics_CellBiol\Temporary Backup_MS PC_Drive D/hela_auto2.xlsx", engine='openpyxl')
    df['date created'] =  pd.to_datetime(df['date created'])
    if filter == "2cv":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '2CV') & (df['gradient length'] == '2h')]
    elif filter == "nofaims":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == 'noFAIMS') & (df['gradient length'] == '2h')]
    elif filter == "1cv":
        df3 = df[(df['amount'] == 500) & (df['producer'] == 'CPMS') & (df['FAIMS'] == '1CV') & (df['gradient length'] == '2h')]
    else:
        df3 = df
    return df3.rename(columns={'Peptide Seq Identified': 'Peptides', 'Retention length [s]': 'RetLen'}).sort_values('date created', ascending=False).head(5).to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False, host="146.107.176.137", port="8052")