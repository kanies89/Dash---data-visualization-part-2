from dash import dcc
from dash import html
import plotly.graph_objects as go


def render_tab(df):
    layout = html.Div([html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
                       html.Div([
                           dcc.Checklist(id="week-range",
                                         options=[
                                             {'label': 'Poniedziałek', 'value': 0},
                                             {'label': 'Wtorek', 'value': 1},
                                             {'label': 'Środa', 'value': 2},
                                             {'label': 'Czwartek', 'value': 3},
                                             {'label': 'Piątek', 'value': 4},
                                             {'label': 'Sobota', 'value': 5},
                                             {'label': 'Niedziela', 'value': 6}
                                         ],
                                         value=[0, 1, 2, 3, 4, 5, 6]
                                         ),
                           html.Div([html.Div([dcc.Graph(id='bar-weeksales')], style={'width': '50%'}),
                                     html.Div([dcc.Graph(id='choropleth-weeksales')], style={'width': '50%'})],
                                    style={
                                        'display': 'flex',
                                        'verticalAlign': 'top'
                                    })
                       ]),
                       html.Div([html.Div([dcc.Graph(id='customers')], style={'width': '70%'}),
                                 html.Div([dcc.Graph(id='customers_age')], style={'width': '30%'})],
                                style={
                                    'display': 'flex',
                                    'verticalAlign': 'top'
                                })
                       ])

    return layout
