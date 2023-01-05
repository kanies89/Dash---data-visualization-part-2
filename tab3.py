from dash import dcc
from dash import html
from db_class import day
import plotly.graph_objects as go


def day_list():
    x = []
    for i, el in enumerate(list(day.values())):
        x.append(dict(label=el, value=i))
    return x

def render_tab(df):
    layout = html.Div([html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
                       html.Div([
                           dcc.Checklist(id="week-range",
                                         options=day_list(),
                                         value=list(day.keys())
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


print(list(day.values()))

print(dict(list(enumerate(list(day.values())))))
print(enumerate(dict(labels=list(day.keys()), values=1)))