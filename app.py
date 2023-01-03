import pandas as pd
import datetime as dt
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_auth
import plotly.graph_objects as go
import tab1
import tab2
import tab3
from db_class import db


df = db()
df.merge()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

USERNAME_PASSWORD = [['user', 'pass']]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD)

app.layout = html.Div([html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Sprzedaż globalna', value='tab-1'),
        dcc.Tab(label='Produkty', value='tab-2'),
        dcc.Tab(label='Kanały sprzedaży', value='tab-3')
    ]),
    html.Div(id='tabs-content')], style={'width': '80%', 'margin': 'auto'})], style={'height': '100%'})


@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1.render_tab(df.merged)
    elif tab == 'tab-2':
        return tab2.render_tab(df.merged)
    elif tab == 'tab-3':
        return tab3.render_tab(df.merged)


## tab1 callbacks
@app.callback(Output('bar-sales', 'figure'), [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
def tab1_bar_sales(start_date, end_date):
    truncated = df.merged[(df.merged['tran_date'] >= start_date) & (df.merged['tran_date'] <= end_date)]
    grouped = truncated[truncated['total_amt'] > 0].groupby([pd.Grouper(key='tran_date', freq='M'), 'Store_type'])[
        'total_amt'].sum().round(2).unstack()

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(x=grouped.index, y=grouped[col], name=col, hoverinfo='text',
                             hovertext=[f'{y / 1e3:.2f}k' for y in grouped[col].values]))

    data = traces
    fig = go.Figure(data=data, layout=go.Layout(title='Przychody', barmode='stack', legend=dict(x=0, y=-0.5)))

    return fig


@app.callback(Output('choropleth-sales', 'figure'),
              [Input('sales-range', 'start_date'), Input('sales-range', 'end_date')])
def tab1_choropleth_sales(start_date, end_date):
    truncated = df.merged[(df.merged['tran_date'] >= start_date) & (df.merged['tran_date'] <= end_date)]
    grouped = truncated[truncated['total_amt'] > 0].groupby('country')['total_amt'].sum().round(2)

    trace0 = go.Choropleth(colorscale='Viridis', reversescale=True,
                           locations=grouped.index, locationmode='country names',
                           z=grouped.values, colorbar=dict(title='Sales'))
    data = [trace0]
    fig = go.Figure(data=data,
                    layout=go.Layout(title='Mapa', geo=dict(showframe=False, projection={'type': 'natural earth'})))

    return fig


## tab2 callbacks
@app.callback(Output('barh-prod-subcat', 'figure'), [Input('prod_dropdown', 'value')])
def tab2_barh_prod_subcat(chosen_cat):
    grouped = df.merged[(df.merged['total_amt'] > 0) & (df.merged['prod_cat'] == chosen_cat)].pivot_table(
        index='prod_subcat', columns='Gender', values='total_amt', aggfunc='sum').assign(
        _sum=lambda x: x['F'] + x['M']).sort_values(by='_sum').round(2)

    traces = []
    for col in ['F', 'M']:
        traces.append(go.Bar(x=grouped[col], y=grouped.index, orientation='h', name=col))

    data = traces
    fig = go.Figure(data=data, layout=go.Layout(barmode='stack', margin={'t': 20, }))
    return fig


## tab3 callbacks
@app.callback(Output('bar-weeksales', 'figure'), Input('week-range', 'value'))
def tab3_store_types(value):
    truncated = pd.DataFrame()
    for n in value:
        z = df.merged[(df.merged['day'] == n)]
        truncated = pd.concat([truncated, z], ignore_index=True)
    grouped = truncated[truncated['total_amt'] > 0].groupby([pd.Grouper(key='day'), 'Store_type'])[
        'total_amt'].sum().round(2).unstack()

    traces = []
    for col in grouped.columns:
        traces.append(go.Bar(x=grouped.index.values, y=grouped[col], name=col, hoverinfo='text',
                             hovertext=[f'{y / 1e3:.2f}k' for y in grouped[col].values]))

    data = traces
    fig = go.Figure(data=data, layout=go.Layout(title='Kanały sprzedaży', barmode='stack', legend=dict(x=0, y=-0.5), xaxis=dict(
                          ticktext=['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'],
                          tickvals=[0, 1, 2, 3, 4, 5, 6],
                          tickmode="array",
                          titlefont=dict(size=30)
    )
                                                )
                    )

    return fig


@app.callback(Output('choropleth-weeksales', 'figure'), Input('week-range', 'value'))
def tab3_choropleth_sales(value):
    truncated = pd.DataFrame()
    for n in value:
        z = df.merged[(df.merged['day'] == n)]
        truncated = pd.concat([truncated, z], ignore_index=True)
    grouped = truncated[truncated['total_amt'] > 0].groupby('country')['total_amt'].sum().round(2)

    trace0 = go.Choropleth(colorscale='Viridis', reversescale=True,
                           locations=grouped.index, locationmode='country names',
                           z=grouped.values, colorbar=dict(title='Sales'))
    data = [trace0]
    fig = go.Figure(data=data,
                    layout=go.Layout(title='Mapa', geo=dict(showframe=False, projection={'type': 'natural earth'})))

    return fig


@app.callback(Output('customers', 'figure'), Input('week-range', 'value'))
def tab3_customers(value):
    day = {
        0: 'Poniedziałek',
        1: 'Wtorek',
        2: 'Środa',
        3: 'Czwartek',
        4: 'Piątek',
        5: 'Sobota',
        6: 'Niedziela'
    }
    truncated = pd.DataFrame()
    for n in value:
        z = df.merged[(df.merged['day'] == n)]
        truncated = pd.concat([truncated, z], ignore_index=True)

    truncated.drop(truncated[truncated['total_amt'] < 0].index, inplace=True)

    fig = go.Figure(layout=go.Layout(title='Średnie zakupy na użytkownika', height=800, yaxis=dict(
                          title_text="Dni tygodnia",
                          ticktext=['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota', 'Niedziela'],
                          tickvals=[0, 1, 2, 3, 4, 5, 6],
                          tickmode="array",
                          titlefont=dict(size=30),
                      )))

    for day_v in value:
        fig.add_trace(go.Violin(y=truncated['day'][truncated['day'] == day_v],
                                x=truncated['total_amt'][truncated['day'] == day_v],
                                name=day[day_v],
                                box_visible=True,
                                meanline_visible=True
                                )
                      )
    fig.update_traces(orientation='h')
    return fig


@app.callback(Output('customers_age', 'figure'), Input('week-range', 'value'))
def tab3_customers_age(value):
    truncated = pd.DataFrame()
    for n in value:
        z = df.merged[(df.merged['day'] == n)]
        truncated = pd.concat([truncated, z], ignore_index=True)
    truncated['Age'] = truncated['DOB'].apply(lambda x: (dt.datetime.now().year - x.year))
    truncated['All'] = 7
    fig = go.Figure(layout=go.Layout(title='Średni wiek użytkownika', height=800, xaxis=dict(
        ticktext=["Struktura wiekowa kupujących w dane dni tygodnia"],
        tickvals=[7],
        tickmode="array",
        titlefont=dict(size=30)
    )
                          )
                    )

    fig.add_trace(go.Violin(x=truncated['All'][truncated['Gender'] == 'M'],
                            y=truncated['Age'],
                            name='Wiek mężczyzn',
                            side='negative',
                            box_visible=True,
                            meanline_visible=True
                            )
                  )
    fig.add_trace(go.Violin(x=truncated['All'][truncated['Gender'] == 'F'],
                            y=truncated['Age'],
                            name='Wiek kobiet',
                            side='positive',
                            box_visible=True,
                            meanline_visible=True
                            )
                  )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
