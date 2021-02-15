import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import pandas as pd
import sqlite3 as sl

con = sl.connect('test.db')
query1 = 'SELECT Country as Country, count(DISTINCT ip) as "Distinct IPs", count(ip) as "Probes" from probes group by country'
df = pd.read_sql_query(query1, con)
query2 = 'SELECT ip as IP, city as City, region as Region, country as Country, time as Time, statuscode as "HTTP Response", requestmethod as Method, requestprotocol as Protocol, requestpath as Path from probes ORDER BY country, city, ip'
df2 = pd.read_sql_query(query2, con)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

fig = px.bar(df, y=["Distinct IPs", "Probes"], x="Country", orientation='v', height=500, barmode="stack", range_y=[0,100])
#fig2 = px.

app.layout = html.Div(children=[
    html.H1(children='Traefik Probes'),

    html.Div(children='''
        Text here
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    html.Div(children='''
        Raw Log Data
    '''),

    html.Div(
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

#			style_cell={'width': '300px',
#			'height': '60px',
#			'textAlign': 'left'}
        ),   
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
