from dash import dcc
from dash import html
import plotly.graph_objects as go

day = {
    0: 'Poniedziałek',
    1: 'Wtorek',
    2: 'Środa',
    3: 'Czwartek',
    4: 'Piątek',
    5: 'Sobota',
    6: 'Niedziela'
}


def render_tab(df):
    layout = html.Div([html.H1('Kanały sprzedaży', style={'text-align': 'center'}),
                       html.Div([
                           dcc.RangeSlider(id='week-range', min=0, max=6, step=1, marks=day,
                                           value=[df['day'].min(), df['day'].max()]),
                           html.Div([html.Div([dcc.Graph(id='bar-weeksales')], style={'width': '50%'}),
                                     html.Div([dcc.Graph(id='choropleth-sales')], style={'width': '50%'})],
                                    style={'display': 'flex'})
                       ])])

    return layout
