import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import plotly.express as px
import pandas as pd
import sqlite3 as sl

con = sl.connect('test.db')
query1 = 'SELECT country_long as Country, count(DISTINCT ip) as "Distinct IPs", count(ip) as "Probes" from probes group by country_long'
df = pd.read_sql_query(query1, con)
query2 = 'SELECT ip as IP, city as City, region as Region, country_long as Country, time as Time, statuscode as "HTTP Response", requestmethod as Method, requestprotocol as Protocol, requestpath as Path from probes ORDER BY country_long, city, ip'
df2 = pd.read_sql_query(query2, con)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def calc_column_height(dfy):
    l = len(dfy)
    c = 0
    high = 0
    while c < l:
        if dfy.iloc[c]['Distinct IPs'] + dfy.iloc[c]['Probes'] > high:
            high = dfy.iloc[c]['Distinct IPs'] + dfy.iloc[c]['Probes']
        c = c + 1
    high = high + (10 - (high  % 10))
    return high

fig = px.bar(df, y=["Distinct IPs", "Probes"], x="Country", orientation='v', height=500, barmode="stack", range_y=[0,calc_column_height(df)])

app.layout = html.Div(children=[
    html.H1(children='Traefik Probes'),

    html.Div(children='''
        Text here
    '''),

    dcc.Graph(
        id='location-graph',
        figure=fig
    ),



    html.Div(children='''
        Raw Log Data
    '''),

    html.Div(children=
        dash_table.DataTable(
    		id='table',
			style_data={
            'whitespace': 'normal',
			'height': 'auto',
			'textAlign': 'left'},

			columns=[{"name": i, "id": i} for i in df2.columns],
			data=df2.to_dict('records'),
            style_header={
                'textAlign': 'left'},

            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'Path',
                    },
                    'whiteSpace': 'normal',
                    'height': 'auto',   
                },
                {
                    'if': {
                        'column_id': 'Country',
                    },
                    'textAlign': 'center',
                },
                {
                    'if': {
                        'column_id': 'HTTP Response',
                    },
                    'textAlign': 'center',
                },
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ]
        ),
    ),
    dcc.Interval(
    id='interval-component',
    interval=3*1000, # in milliseconds
    n_intervals=0
    )
])

@app.callback(Output('location-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):
    update_con = sl.connect('test.db')
    update_df = pd.read_sql_query(query1, update_con)
    fig = px.bar(update_df, y=["Distinct IPs", "Probes"], x="Country", orientation='v', height=500, barmode="stack", range_y=[0,calc_column_height(update_df)])
    x = calc_column_height(update_df)
    fig.update_layout(transition_duration=500)
    return fig

@app.callback(Output('table', 'data'),
    Input('interval-component', 'n_intervals'))
def update_table(n):
    update_con = sl.connect('test.db')
    update_df2 = pd.read_sql_query(query2, update_con)
    return update_df2.to_dict('records')



if __name__ == '__main__':
    app.run_server(debug=True)
#    x = calc_column_height(df)
#    print(df, x)