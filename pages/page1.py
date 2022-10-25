import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pathlib


import numpy as np
from calendar import month_name
from dash_bootstrap_templates import load_figure_template
external_stylesheets = ['dbc.themes.BOOTSTRAP']
load_figure_template("LUX")

dash.register_page(__name__, path='/Algemeen', name='Algemeen') # '/' is home page


df = pd.read_csv('Orders-Tabel 1.csv',sep=";",decimal=',')
df["OrderDate"] = pd.to_datetime(df["Order Date"])
df["OrderYear"] = df.OrderDate.dt.year
df["OrderMonth"] = df.OrderDate.dt.month_name()
df["OrderMonthNr"] = df.OrderDate.dt.month
TEXT_STYLE = {
    #'textAlign': 'center',
    'color': '#000000'
}


layout = html.Div([
    dbc.Row([
            dbc.Col([
                html.H2('Algemene Analyse',
                        style={"margin-top": "40px"})]),
            dbc.Col([
                html.Button("Uitleg", id="btn-download-txt", style = {"margin-top": "40px",'display': 'inline-block','margin-left': '350px'}),
                dcc.Download(id="download-text")
            ])
        ]),
    dbc.Row([
            html.Hr(style={"margin-top": "30px","border-width": "0 0 1px 0"}),
        ]),
    dbc.Row([
        html.P("Kies een filter",style={"margin-top": "10px"}),
        dcc.Dropdown(["Orders","Sales", "Profit", "Average Profit"], "Orders", id="filter_dropdown"),
        ]),

    dbc.Row([
        dbc.Col([dcc.Graph(id='line_graph', figure={}) ]),
        dbc.Col([dcc.Graph(id="line_graph_2", figure= {})]),

    ]),
    dbc.Row([
        html.Hr(style={"margin-top": "30px", "border-width": "0 0 1px 0"}),
    ]),
    dbc.Row([
        dcc.Dropdown(["Staten", "Steden", "Sub-Categorieën", "Producten"], "Staten", id="dropdown_2"),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar_chart_best', figure={}),
        ]),
        dbc.Col([
            dcc.Graph(id='bar_chart_worst', figure={}),
        ])
    ])

])


@callback(
    Output("line_graph",  "figure"),
    [Input("filter_dropdown","value")],
)
def get_graph(filter_chosen):
    if filter_chosen == "Orders":
        norders_years = df.groupby("OrderYear")["Order ID"].nunique()
        fig_norders = px.bar(norders_years, x=norders_years.index, y=norders_years.values,text=np.round(norders_years.values,2))
        fig_norders.update_layout(xaxis_title="Jaar",
                                  yaxis_title="Totale bestellingen", title="Totaal aantal bestellingen per jaar")
        return fig_norders

    if filter_chosen == "Sales":
        sales_years = df.groupby("OrderYear")["Sales"].sum()
        fig_sales_years = px.bar(sales_years, x=sales_years.index, y=sales_years.values,text=np.round(sales_years.values,2))
        fig_sales_years.update_layout(xaxis_title="Jaar",
                                      yaxis_title="Totale omzet", title="Totale omzet per jaar")
        return fig_sales_years
    if filter_chosen == "Profit":
        profit_years = df.groupby("OrderYear")["Profit"].sum()
        fig_profit_years = px.bar(profit_years, x=profit_years.index, y=profit_years.values,text=np.round(profit_years.values,2))
        fig_profit_years.update_layout(xaxis_title="Jaar",
                                       yaxis_title="Totale winst", title="Totale winst per jaar")

        return fig_profit_years
    if filter_chosen == "Average Profit":
        avg_profit_years = df.groupby("OrderYear")["Profit"].mean()
        fig_avg_profit_years = px.bar(avg_profit_years, x=avg_profit_years.index, y=avg_profit_years.values,text=np.round(avg_profit_years.values,2))
        fig_avg_profit_years.update_layout(xaxis_title="Jaar",
                                           yaxis_title="Gemiddelde winst", title="Gemiddelde winst per bestelling per jaar")

        return fig_avg_profit_years

    else:
        raise dash.exceptions.PreventUpdate

@callback(
    Output("line_graph_2",  "figure"),
    [Input("filter_dropdown","value")],
)
def get_graph(filter_chosen):
    if filter_chosen == "Orders":
        norders_month = df.groupby("OrderMonth")["Order ID"].nunique()
        norders_month = norders_month.sort_values(ascending=False).head(5)
        fig_norders = px.bar(norders_month, x=norders_month.index, y=norders_month.values , text=np.round(norders_month.values,2))
        fig_norders.update_layout(xaxis_title="Maand",
                                  yaxis_title="Totale bestellingen", title="Totaal aantal bestellingen per maand")
        return fig_norders

    if filter_chosen == "Sales":
        sales_month = df.groupby("OrderMonth")["Sales"].sum()
        sales_month = sales_month.sort_values(ascending=False).head(5)
        fig_sales_years = px.bar(sales_month, x=sales_month.index, y=sales_month.values,text=np.round(sales_month.values,2))
        fig_sales_years.update_layout(xaxis_title="Maand",
                                      yaxis_title="Totale omzet", title="Totale omzet per maand")
        return fig_sales_years
    if filter_chosen == "Profit":
        profit_month = df.groupby("OrderMonth")["Profit"].sum()
        profit_month = profit_month.sort_values(ascending=False).head(5)
        fig_profit_month = px.bar(profit_month, x=profit_month.index, y=profit_month.values, text=np.round(profit_month.values,2))
        fig_profit_month.update_layout(xaxis_title="Maand",
                                       yaxis_title="Totale winst", title="Totale winst per maand")

        return fig_profit_month
    if filter_chosen == "Average Profit":
        avg_profit_month = df.groupby("OrderMonth")["Profit"].mean()
        avg_profit_month = avg_profit_month.sort_values(ascending=False).head(5)
        fig_avg_profit_month = px.bar(avg_profit_month, x=avg_profit_month.index, y=avg_profit_month.values, text=np.round(avg_profit_month.values,2))
        fig_avg_profit_month.update_layout(xaxis_title="Maand",
                                           yaxis_title="Gemiddelde winst", title="Gemiddelde winst per bestelling per maand")

        return fig_avg_profit_month

    else:
        raise dash.exceptions.PreventUpdate

@callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dict(content="Op deze pagina is de algemene analyse te vinden. Hier zijn de verschillende KPI's van elk jaar tegen elkaar geplot in de eerste grafiek."
                        "In de tweede grafiek zijn de percentuele verschillen te vinden. Zoals te zien is stijgen zowel de bestellingen, omzet als winst elk jaar gestaag."
                        " Alleen de gemiddelde winst is in het laatste jaar gedaald. Een verdere analyse is nodig om te zien waarom dit zo is. Hier later meer over!",



                filename="hello.txt")


@callback(
    Output("bar_chart_best",  "figure"),
    [Input("dropdown_2","value")],
)
def get_graph(filter_chosen):
    if filter_chosen == "Staten":
        best_states = df.groupby("State")["Profit"].mean().sort_values(ascending=False).head(5)
        fig = px.bar(best_states, x=best_states.index, y=best_states.values,
                                 text=np.round(best_states.values, 2))
        fig.update_layout(xaxis_title="Staat",
                                      yaxis_title="Winst", title="De staten met de hoogste gemiddelde winst")
        return fig
    if filter_chosen == "Steden":
        best_cities = df.groupby("City")["Profit"].mean().sort_values(ascending=False).head(5)
        fig = px.bar(best_cities, x=best_cities.index, y=best_cities.values,
                     text=np.round(best_cities.values, 2))
        fig.update_layout(xaxis_title="Stad",
                          yaxis_title="Winst", title="De steden met de hoogste gemiddelde winst")
        return fig

    if filter_chosen == "Sub-Categorieën":
        best_cities = df.groupby("Sub-Category")["Profit"].mean().sort_values(ascending=False).head(5)
        fig = px.bar(best_cities, x=best_cities.index, y=best_cities.values,
                     text=np.round(best_cities.values, 2))
        fig.update_layout(xaxis_title="Stad",
                          yaxis_title="Winst", title="De sub-categorieën met de hoogste gemiddelde winst")
        return fig
    if filter_chosen == "Producten":
        best_cities = df.groupby("Product Name")["Profit"].mean().sort_values(ascending=False).head(5)
        fig = px.bar(best_cities, x=best_cities.index, y=best_cities.values,
                     text=np.round(best_cities.values, 2))
        fig.update_layout(xaxis_title="Stad",
                          yaxis_title="Winst", title="De producten met de hoogste gemiddelde winst")
        return fig
    else:
        raise dash.exceptions.PreventUpdate


@callback(
    Output("bar_chart_worst",  "figure"),
    [Input("dropdown_2","value")],
)
def get_graph(filter_chosen):
    if filter_chosen == "Staten":
        best_states = df.groupby("State")["Profit"].mean().sort_values(ascending=True).head(5)
        fig = px.bar(best_states, x=best_states.index, y=best_states.values,
                                 text=np.round(best_states.values, 2))
        fig.update_layout(xaxis_title="Staat",
                                      yaxis_title="Winst", title="De staten met de laagste gemiddelde winst")
        return fig
    if filter_chosen == "Steden":
        best_cities = df.groupby("City")["Profit"].mean().sort_values(ascending=True).head(5)
        fig = px.bar(best_cities, x=best_cities.index, y=best_cities.values,
                     text=np.round(best_cities.values, 2))
        fig.update_layout(xaxis_title="Stad",
                          yaxis_title="Winst", title="De steden met de laagste gemiddelde winst")
        return fig

    if filter_chosen == "Sub-Categorieën":
        best_cities = df.groupby("Sub-Category")["Profit"].mean().sort_values(ascending=True).head(5)
        fig = px.bar(best_cities, x=best_cities.index, y=best_cities.values,
                     text=np.round(best_cities.values, 2))
        fig.update_layout(xaxis_title="Stad",
                          yaxis_title="Winst", title="De sub-categorieën met de laagste gemiddelde winst")

        return fig

    if filter_chosen == "Producten":
        best_cities = df.groupby("Product Name")["Profit"].mean().sort_values(ascending=True).head(5)
        fig = px.bar(best_cities, x=best_cities.index, y=best_cities.values,
                     text=np.round(best_cities.values, 2))
        fig.update_layout(xaxis_title="Stad",
                          yaxis_title="Winst", title="De producten met de laagste gemiddelde winst")
        return fig
    else:
        raise dash.exceptions.PreventUpdate


