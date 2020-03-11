'''
This app creates a basic dashboard for EDS data using Dash.
'''


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime
import json

import edsEnums
from edsHandler import eds, edsStream

### CONSTANTS ###
MAXHISTORYDAYS = 31
DEFAULTHISTORYDAYS = 5
### CONSTANTS ###

def get_streams(edgedatastore):
    streams = edge.get_all_streams()
    return streams


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds()


# Load config for OCSHandler
with open('config.json') as json_data_file:
    edge = eds(json.load(json_data_file))

allStreams = get_streams(edge)
streamSelection = []
for stream in allStreams:
    streamSelection.append({'label': stream.name, 'value': stream.name})

initialData = allStreams[0].get_window_values((datetime.datetime.now() - datetime.timedelta(days=1)).isoformat(),datetime.datetime.now().isoformat())
initialX = []
initialY = []
for event in initialData:
    initialX.append(event['Time'])
    initialY.append(event['Temperature'])

# Dash configuration
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='EDS Dashboard',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    dcc.Graph(
        id='streams-line',
        figure={
            'data': [
                {'x': initialX, 'y': initialY, 'type': 'line', 'name': allStreams[0].name}
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    ),
    
    html.Label('Stream Selection'),
    dcc.Dropdown(
        id='streams-dropdown',
        options=streamSelection,
        value=[streamSelection[0]['value']],
        multi=True
    ),
    html.Label('Time Selection'),
    dcc.RangeSlider(
        id = 'streams-time',
        min = unix_time_millis(datetime.datetime.now() - datetime.timedelta(days=MAXHISTORYDAYS)),
        max = unix_time_millis(datetime.datetime.now()),
        value = [unix_time_millis(datetime.datetime.now() - datetime.timedelta(days=DEFAULTHISTORYDAYS)), unix_time_millis(datetime.datetime.now())]
    )
])


@app.callback(
    Output(component_id='streams-line', component_property='figure'),
    [Input(component_id='streams-dropdown', component_property='value'),
    Input(component_id='streams-time', component_property='value')]
)
def get_data(streamNames,timeRange):
    query = 'query=name:'
    for name in streamNames:
        query += name + '%20OR%20'

    query = query[:-5]

    streamArray = edge.get_streams(query)

    data = []
    for i in range(len(streamArray)):
        events = streamArray[i].get_window_values(datetime.datetime.utcfromtimestamp(timeRange[0]).isoformat(),datetime.datetime.utcfromtimestamp(timeRange[1]).isoformat())
        data.append({})
        data[i]['x'] = []
        data[i]['y'] = []
        data[i]['name'] = streamArray[i].name
        data[i]['type'] = 'line'
        for event in events:
            data[i]['x'].append(event['Time'])
            data[i]['y'].append(event['Temperature'])    

    figure = {
        'data': data,
        'layout': {
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }

    return figure


if __name__ == '__main__':
    # Run dash server
    app.run_server(debug=True,host='0.0.0.0')