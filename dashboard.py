import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from PIL import Image

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import json

# df = pd.read_csv('HIST_PAINEL_COVIDBR_13mai2021.csv', sep=';')
# df_states = df[(~df['estado'].isna()) & (df['codmun'].isna())]
# df_brasil = df[df['regiao'] == 'Brasil']
# df_states.to_csv('df_states.csv')
# df_brasil.to_csv('df_brasil.csv')

df_states = pd.read_csv(r'df_states.csv')
df_brasil = pd.read_csv(r'df_brasil.csv')

brasil_states = json.load(open(r"brazil_geo.json", 'r'))

df_states_ = df_states[df_states['data'] == '2021-05-13']
df_data = df_states[df_states['estado'] == 'AL']

select_column = {'casosAcumulado':'Acumulate cases',
                 'casosNovos':'New cases',
                 'obitosAcumulado':'Total deaths',
                 'obitosNovos':'Deaths per day',}

path_logo = Image.open('logo_ufal.png')

#=================================================================================================================
# SETTINGGS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig = px.choropleth_mapbox(df_states_,
                           locations='estado',
                           color='casosAcumulado', geojson=brasil_states,
                           color_continuous_scale='Bluered',
                           opacity=0.4,
                           center={'lat':-12.827619, 'lon':-50.487157},
                           hover_data={'estado':True, 'casosNovos':True, 'casosAcumulado':True, 'obitosNovos':True, 'obitosAcumulado':True},
                           zoom=3
                           )

fig.update_layout(
    paper_bgcolor='#242424',
    autosize = True,
    margin=go.Margin(l=0, r=0, t=0, b=0),
    showlegend = False,
    mapbox_style='carto-darkmatter'
)


fig2 = go.Figure(layout={'template':'plotly_dark'})
fig2.add_trace(go.Scatter(x=df_data['data'], y=df_data['casosAcumulado']))
fig2.update_layout(
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    autosize= True,
    margin = {'l':10, 'r':10, 't':10, 'b':10}
)
#=================================================================================================================
# Layout

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([html.Img(id='logo', src=path_logo, height=50),
                      html.H5('COVID DATA'),
                      dbc.Button('BRASIL', color='primary', id='location-buttom', size='lg'),   
            ], style={}),

            html.P('Date info:', style={'margin-top': '40px'}),

            html.Div(id='dic-test', children=[
                    dcc.DatePickerSingle(id='date_picker',
                                        initial_visible_month=df_brasil['data'].min(),
                                        min_date_allowed=df_brasil['data'].min(),
                                        max_date_allowed=df_brasil['data'].max(),
                                        date=df_brasil['data'].max(),
                                        display_format='MMM D, YYYY',
                                        style={'border': '0px solid black'}
                    )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Recovered cases'),
                            html.H3(style={'color':'#adfc92'}, id='recovered_cases_text'),
                            html.Span('In follow-up at the date'),
                            html.H5(id='in_follow-up_text'),
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px',
                                                        'box-shadow':'0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)',
                                                        'color': '#FFFFFF'})
                ], md=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span('Total confirmed cases'),
                        html.H3(style={'color':'#389df6'}, id='confirmed_cases_text'),
                        html.Span('New cases at the date'),
                        html.H5(id='new_cases_text'),
                    ])
                ], color='light', outline=True, style={'margin-top': '10px',
                                                       'box-shadow':'0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)',
                                                       'color': '#FFFFFF'})
            ], md=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span('Deaths'),
                        html.H3(style={'color':'#df2935'}, id='deaths_text'),
                        html.Span('Deaths at the date'),
                        html.H5(id='deaths_date_text'),
                    ])
                ], color='light', outline=True, style={'margin-top': '10px',
                                                       'box-shadow':'0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)',
                                                       'color': '#FFFFFF'})
            ], md=4),
            ]),


            html.Div([
                html.P('Select the data you wish to check:', style={'margin-top': '25px'}),
                dcc.Dropdown(id='location_dropdowm',
                            options=[{'label': j, 'value':i} for i, j in select_column.items()],
                            value='casosNovos',
                            style={'margin-top': '10px'},
                            
                            ),
                dcc.Graph(id='scatter-chart', figure=fig2),
            ])   
        ], md=5, style={'paddig': '25px', 'background-color': '#242424'}),

    
        dbc.Col([
            dcc.Loading(id='loading-1', type ='default',
            children = [
                dcc.Graph(id='cloropleth-map', figure=fig, style={'height':'100vh', 'margin-right':'1opx'})
                ]
            )
        ], md=7)
    ])
, fluid=True)

#=================================================================================================================
#Interactivity

# With data-picker to update texts
@app.callback(
        [
        Output('recovered_cases_text','children'),
        Output('in_follow-up_text','children'),
        Output('confirmed_cases_text','children'),
        Output('new_cases_text','children'),
        Output('deaths_text','children'),
        Output('deaths_date_text','children')
        ],

        [Input('date_picker', 'date'), Input('location-buttom', 'children')]
)
def display_status(date, location):
    if location == 'BRASIL':
        df_data_on_date = df_brasil[df_brasil['data'] == date]
    else:
        df_data_on_date = df_states[(df_states['estado'] == location) & (df_states["data"] == date)]

    recovered = '-' if  df_data_on_date['Recuperadosnovos'].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(',','.')
    follow_ups = '-' if  df_data_on_date['emAcompanhamentoNovos'].isna().values[0] else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(',','.')
    acumulate_cases = '-' if  df_data_on_date['casosAcumulado'].isna().values[0] else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(',','.')
    new_cases = '-' if  df_data_on_date['casosNovos'].isna().values[0] else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(',','.')
    acumulated_deaths = '-' if  df_data_on_date['obitosAcumulado'].isna().values[0] else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(',','.')
    new_deaths = '-' if  df_data_on_date['obitosNovos'].isna().values[0] else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(',','.')


    return(
        recovered,
        follow_ups,
        acumulate_cases,
        new_cases,
        acumulated_deaths,
        new_deaths
    )

#With location-picker
@app.callback(Output('scatter-chart','figure'),
              [Input('location_dropdowm', 'value'), Input('location-buttom', 'children')]
)
def PlotLineOutPut(plot_type, location):
    if location == 'BRASIL':
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[df_states['estado'] == location]


    bar_plots = ['casosNovos', 'obitosNovos']
    fig2 = go.Figure(layout={'template':'plotly_dark'})
    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location['data'], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location['data'], y=df_data_on_location[plot_type]))

    fig2.update_layout(
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        autosize= True,
        margin = {'l':10, 'r':10, 't':10, 'b':10}
    )

    return fig2

# With data-picker to update map
@app.callback(Output("cloropleth-map", "figure"), 
              [Input("date_picker", "date")]
)
def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brasil_states, 
        center={'lat':-12.827619, 'lon': -50.487157},
        zoom=4, color="casosAcumulado", color_continuous_scale="Bluered", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "estado": False,'obitosAcumulado':True}
        )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    
    return fig

# With click on map to update location button
@app.callback(Output('location-buttom','children'),
              [Input('cloropleth-map', 'clickData'), Input('location-buttom', 'n_clicks')]
)
def updateLoc(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != 'location-buttom.n_clicks':
        state = click_data['points'][0]['location']
        return '{}'.format(state)
    else:
        return 'BRASIL'

if __name__ == '__main__':
    app.run_server(debug=True)