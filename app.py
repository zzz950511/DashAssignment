import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv('assets/students.csv')
list_of_names = df['Name'].unique()


def generate_Dropdown(list_of_students):
    return dcc.Dropdown(
        id='student_name',
        options=[{'label': i, 'value': i} for i in list_of_students],
        value=''
    )

def getSum(subjectName):
    sum=0
    GroupDataSubject=df[df['Subject'] == subjectName]
    Marks=GroupDataSubject['Mark']
    for mark in Marks:
        # type(int(mark))
        sum +=mark
    avg= sum/ (len(Marks))
    return round(avg,2)

mAdvWebTech = getSum('Awt')
mBDLA = getSum('P2P')
mLA = getSum('IoT')
mLAVA = getSum('NIO')



def getDuration(subjectName):
    sum=0
    GroupDataSubject=df[df['Subject'] == subjectName]
    Durations=GroupDataSubject['Duration']
    for duration in Durations:
        sum +=duration
    avg= sum/ (len(Durations))
    return round(avg,2)

dAdvWebTech = getDuration('Awt')
dBDLA = getDuration('P2P')
dLA = getDuration('IoT')
dLAVA = getDuration('NIO')


app.layout = html.Div(children=[
    html.Div(className=' container row', children=[
        html.Div(className='row', children=[
            html.Div(className='six columns',
                children=[
                    html.H1('Dash Assignment', style={'color': 'black','float':'left'})
                ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns',
                children=[
                    html.H1('Select Students', style={'color': 'black','float': 'left','font-size':'16pt'})
                ]),
            html.Div(className='four columns',
                children=[
                    html.H1('Last clicked course information', style={'color': 'black', 'float': 'left','font-size':'16pt'})
                ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns',
                children=[
                    generate_Dropdown(list_of_names),
                ]),
            html.Div(className='four columns',
                children=[
                    html.H1('No course clicked ingrades graph', style={'color': 'darkgrey', 'float': 'left','font-size':'12pt'}),
                    html.H1('No course clicked ingrades graph', style={'color': 'darkgrey', 'float': 'left','font-size':'12pt'})

                ]),
        ]),
            html.Div(className='twelve columns', style={'marginTop': 50, },
            children=([

                dcc.Graph(id='bar_chart', className='six columns'),
                dcc.Graph(id='dot_chart', className='six columns', )

            ])),

    ])
])

colors = {'marker_color': '#6495ED', 'menBar': '#00008B', 'text': '#FFFFF'}

@app.callback(
    Output('bar_chart', 'figure'),
    [Input('student_name', 'value')])
def update_graph(student_name_value):
    group_data_by_name = df[df['Name'] == student_name_value]
    if group_data_by_name.empty:
        return{
                'data': [dict(
                x=['Awt', 'P2P', 'IoT', 'NIO'],
                y=[ mAdvWebTech, mBDLA, mLA, mLAVA],

                marker={'color': colors['marker_color']},
                type = 'bar'

            )],
                        'layout': dict(
                xaxis={
                    'title': 'Grades',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='Students average grades',
            )
            }
    else:
        return {
            'data': [dict(
                x=group_data_by_name['Subject'].unique(),
                y=group_data_by_name['Mark'],
                marker={'color': colors['marker_color']},
                type = 'bar'

            )],
            'layout': dict(
                xaxis={
                    'title': 'Grades',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='{} grades'.format(student_name_value),
            )
        }



@app.callback(
    Output('dot_chart', 'figure'),
    [Input('student_name', 'value')])
def dot_Chart(student_name_value):
    group_data_by_name = df[df['Name'] == student_name_value]
    if group_data_by_name.empty:
        return{
                'data': [dict(
                x=['Awt', 'P2P', 'IoT', 'NIO'],
                y=[ dAdvWebTech, dBDLA, dLA, dLAVA],
                mode='markers',
                marker={
                    'size':15,
                    'line':{'width':0.5,'color': colors['marker_color'] }
                    },
                type = 'scatter'

            )],
                        'layout': dict(
                xaxis={
                    'title': 'Hours spend per week',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='Average weekly hours spend by students',
            )
            }
    else:
        return {
            'data': [dict(
                x=group_data_by_name['Subject'].unique(),
                y=group_data_by_name['Duration'],
                mode='markers',
                marker={
                    'size':15,
                    'line':{'width':0.5,'color': colors['marker_color'] }
                    },
                type = 'scatter'

            )],
            'layout': dict(
                xaxis={
                    'title': 'Hours spend per week',
                    'style': {
                        'marginRight': 30,
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                },
                yaxis={
                    'title': 'Courses',
                    'style': {
                        'margin': {'l': 0, 'b': 50, 't': 0, 'r': 50},
                    },
                    'font': {
                        'color': colors['text'],
                        'size': 16,
                    },
                    'dtick': 0.5, #scale y-axis
                },
                margin={'l': 40, 'b': 60, 't': 30, 'r': 0},
                title='Average weekly hours spend by ' + student_name_value,
            )
        }
        

if __name__ == '__main__':
    app.run_server(debug=True)