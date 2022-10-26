import dash
from dash import dcc, html, callback, Output, Input

import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pathlib
import numpy as np


dash.register_page(__name__, path='/Jaarlijks', name='Jaarlijks', title= "Jaarlijks") # '/' is home page

month_name = ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni',
       'Juli', 'Augustus', 'September', 'Oktober', 'November', 'December']
df = pd.read_csv('Orders-Tabel 1.csv',sep=";",decimal=',')
df["OrderDate"] = pd.to_datetime(df["Order Date"])
df["OrderYear"] = df.OrderDate.dt.year
df["OrderMonth"] = df.OrderDate.dt.month_name()
df["OrderMonthNr"] = df.OrderDate.dt.month
df["ShipDate"] = pd.to_datetime(df["Ship Date"])
def replace_all(text, dic):
    for i, j in dic.items():
        text = text.str.replace(i, j)
    return text

dic={
    "June": "Juni",
    "January": "Januari",
    "February": "Februari",
    "March": "Maart",
    "May": "Mei",
    "July": "Juli",
    "August": "Augustus",
    "October": "Oktober"
}

df.OrderMonth = replace_all(df.OrderMonth,dic)


TEXT_STYLE = {
    #'textAlign': 'center',
    'color': '#000000'
}

layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                html.H2('Jaarlijkse analyse',
                        style=TEXT_STYLE)]),
            dbc.Col([
                html.P("Kies een jaar",style={"margin-top": "10px", "width": "100%"}),
                dcc.Dropdown(np.sort(df.OrderYear.unique()), np.sort(df.OrderYear.unique())[0], id="year_dropdown"),
            ]),
        ]),

        dbc.Row([
            html.Hr(style={"margin-top": "30px","border-width": "0 0 1px 0"}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([html.P("Totaal aantal klanten", style={"text-decoration": "underline"})]),
                dbc.Row([html.P(id="ncust", style={"margin-bottom": "20px","margin-right": "10px"}),])
            ]),
            dbc.Col([
                dbc.Row([html.P(id="text_1", style={"text-decoration": "underline"})]),
                dbc.Row([html.P(id="norders", style={"margin-bottom": "20px","margin-right": "10px"})])
            ]),
            dbc.Col([
                dbc.Row([html.P("Gemiddelde verzendtijd", style={"text-decoration": "underline"})]),
                dbc.Row([html.P(id="avg_ship", style={"margin-bottom": "20px","margin-right": "10px"})])
            ])
        ]),
        dbc.Row([
            html.Hr(style={"border-width": "0 0 1px 0"}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    html.P("Kies een filter",style={"margin-top": "10px"}),
                    dcc.Dropdown(["Bestellingen","Omzet", "Winst", "Gemiddelde winst"], "Bestellingen", id="filter_dropdown_1"),
                ]),
                dcc.Graph(id="rel_1", figure = {})
            ],width=8),
            dbc.Col([
                dbc.Row([
                    html.P("Kies een filter",style={"margin-top": "10px"}),
                    dcc.Dropdown(["Regio","Verzendmethode", "Categorie", "Segment"], "Regio", id="filter_dropdown_2"),
            ]),
                dbc.Row([
                    dcc.Graph(id="bar_graph", figure = {})
                 ]),
            ],width=4),
            dbc.Row([
                ##dcc.Graph(id="best_months_year", figure = {})
            ])
        ]),



])

@callback(
    Output("ncust",  "children"),
    [Input("year_dropdown","value")],
    )
def print_output(year_chosen):
    if year_chosen > 0:
        ncust = len(df[df["OrderYear"]==year_chosen]["Customer ID"].unique())
        return ncust

    if year_chosen == 0:
        raise dash.exceptions.PreventUpdate

@callback(
    Output("text_1","children"),
    [Input("filter_dropdown_1", "value")]
    )
def print_text(filter_dropdown):
    if filter_dropdown == "Bestellingen":
        return "Totaal aantal bestellingen"
    if filter_dropdown == "Omzet":
        return "Totaal omzet"
    if filter_dropdown == "Winst":
        return "Totale winst"
    if filter_dropdown == "Gemiddelde winst":
        return "Gemiddelde winst"
@callback(
    Output("norders",  "children"),
    [Input("year_dropdown","value")],
    [Input("filter_dropdown_1","value")]
    )
def print_output(year_chosen, filter_dropdown):
    if year_chosen > 0:
        if filter_dropdown == "Bestellingen":
            norders = np.round(df.groupby("OrderYear")["Order ID"].nunique()[year_chosen],2)
            return norders

        if filter_dropdown == "Omzet":
            nsales = np.round(df.groupby("OrderYear")["Sales"].sum()[year_chosen],2)
            return nsales

        if filter_dropdown == "Winst":
            profit = np.round(df.groupby("OrderYear")["Profit"].sum()[year_chosen],2)
            return profit
        if filter_dropdown == "Gemiddelde winst":
            avg_profit = np.round(df.groupby("OrderYear")["Profit"].mean()[year_chosen],2)
            return avg_profit
        else:
            raise dash.exceptions.PreventUpdate
    if year_chosen == 0:
        raise dash.exceptions.PreventUpdate

@callback(
    Output("avg_ship",  "children"),
    [Input("year_dropdown","value")],
    )
def print_output(year_chosen):
    if year_chosen > 0:
        avg_ship = np.mean(df[df.OrderYear == year_chosen]["ShipDate"] - df[df.OrderYear == year_chosen]["OrderDate"])
        return str(avg_ship)

    if year_chosen == 0:
        raise dash.exceptions.PreventUpdate


@callback(
    Output("bar_graph",  "figure"),
    [Input("year_dropdown", "value")],
    [Input("filter_dropdown_1","value")],
    [Input("filter_dropdown_2","value")],
)
def get_graph(year_chosen, filter1_chosen, filter2_chosen):
    if filter1_chosen == "Gemiddelde winst":
        if filter2_chosen == "Regio":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_region = []
                for i in sorted(df_year["Region"].unique()):
                    profits_region.append(df_year[df_year["Region"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Region"].unique()), y = profits_region, title=f"Gemiddelde winst per regio in {year_chosen}", text=np.round(profits_region,2))
                fig.update_layout(xaxis_title="Regio",
                                  yaxis_title="Gemiddelde winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Verzondmethode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    profits_shipmode.append(df_year[df_year["Ship Mode"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=profits_shipmode, text=np.round(profits_shipmode,2),
                             title=f"Gemiddelde winst per verzendmethode in {year_chosen}")
                fig.update_layout(xaxis_title="Verzendmethode",
                                  yaxis_title="Gemiddelde winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Categorie":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_category = []
                for i in sorted(df_year["Category"].unique()):
                    profits_category.append(df_year[df_year["Category"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=profits_category, text=np.round(profits_category,2),
                             title=f"Gemiddelde winst per categorie in {year_chosen}")
                fig.update_layout(xaxis_title="Categorie",
                                  yaxis_title="Gemiddelde winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate
        if filter2_chosen == "Segment":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_segment = []
                for i in sorted(df_year["Segment"].unique()):
                    profits_segment.append(df_year[df_year["Segment"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Segment"].unique()), y=profits_segment, text=np.round(profits_segment,2),
                             title=f"Gemiddelde winst per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Gemiddelde winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate

    if filter1_chosen == "Winst":
        if filter2_chosen == "Regio":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_region = []
                for i in sorted(df_year["Region"].unique()):
                    profits_region.append(df_year[df_year["Region"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Region"].unique()), y=profits_region, text=np.round(profits_region,2),
                             title=f"Winst per regio in {year_chosen}")
                fig.update_layout(xaxis_title="Regio",
                                  yaxis_title="Winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Verzendmethode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    profits_shipmode.append(df_year[df_year["Ship Mode"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=profits_shipmode, text=np.round(profits_shipmode,2),
                             title=f"Winst per verzendmethode in {year_chosen}")
                fig.update_layout(xaxis_title="Verzendmethode",
                                  yaxis_title="Winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Categorie":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_category = []
                for i in sorted(df_year["Category"].unique()):
                    profits_category.append(df_year[df_year["Category"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=profits_category, text=np.round(profits_category,2),
                             title=f"Winst per categorie in {year_chosen}")
                fig.update_layout(xaxis_title="Categorie",
                                  yaxis_title="Winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate
        if filter2_chosen == "Segment":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_segment = []
                for i in sorted(df_year["Segment"].unique()):
                    profits_segment.append(
                        df_year[df_year["Segment"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Segment"].unique()), y=profits_segment,text=np.round(profits_segment,2),
                             title=f"Winst per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Winst", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate

    if filter1_chosen == "Bestellingen":
        if filter2_chosen == "Regio":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_region = []
                for i in sorted(df_year["Region"].unique()):
                    orders_region.append(len(df_year[df_year["Region"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Region"].unique()), y=orders_region, text=np.round(orders_region,2),
                             title=f"Bestellingen per regio in {year_chosen}")
                fig.update_layout(xaxis_title="Regio",
                                  yaxis_title="Bestellingen", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Verzendmethode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    orders_shipmode.append(len(df_year[df_year["Ship Mode"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=orders_shipmode, text=np.round(orders_shipmode,2),
                             title=f"Bestellingen per verzendmethode in {year_chosen}")
                fig.update_layout(xaxis_title="Verzendmethode",
                                  yaxis_title="Bestellingen", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Categorie":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_category = []
                for i in sorted(df_year["Category"].unique()):
                    orders_category.append(len(df_year[df_year["Category"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=orders_category, text=np.round(orders_category,2),
                             title=f"Bestellingen per categorie in {year_chosen}")
                fig.update_layout(xaxis_title="Categorie",
                                  yaxis_title="Bestellingen", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate
        if filter2_chosen == "Segment":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_segment = []
                for i in sorted(df_year["Segment"].unique()):
                    orders_segment.append(
                        len(df_year[df_year["Segment"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Segment"].unique()), y=orders_segment,text=np.round(orders_segment,2),
                             title=f"Bestellingen per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Bestellingen", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate

    if filter1_chosen == "Omzet":
        if filter2_chosen == "Regio":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_region = []
                for i in sorted(df_year["Region"].unique()):
                    sales_region.append(df_year[df_year["Region"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Region"].unique()), y=sales_region, text=np.round(sales_region,2),
                             title=f"Omzet per regio in {year_chosen}")
                fig.update_layout(xaxis_title="Regio",
                                  yaxis_title="Omzet", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Verzendmethode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    sales_shipmode.append(df_year[df_year["Ship Mode"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=sales_shipmode,text=np.round(sales_shipmode,2),
                             title=f"Omzet per verzendmethode in {year_chosen}")
                fig.update_layout(xaxis_title="Verzendmethode",
                                  yaxis_title="Omzet", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Categorie":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_category = []
                for i in sorted(df_year["Category"].unique()):
                    sales_category.append(df_year[df_year["Category"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=sales_category, text=np.round(sales_category,2),
                             title=f"Omzet per categorie in {year_chosen}")
                fig.update_layout(xaxis_title="Categorie",
                                  yaxis_title="Omzet", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate
        if filter2_chosen == "Segment":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_segment = []
                for i in sorted(df_year["Segment"].unique()):
                    sales_segment.append(
                        df_year[df_year["Segment"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Segment"].unique()), y=sales_segment, text=np.round(sales_segment,2),
                             title=f"Omzet per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Omzet", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate
    else:
        raise dash.exceptions.PreventUpdate



@callback(
    Output("rel_1",  "figure"),
    [Input("year_dropdown","value")],
    [Input("filter_dropdown_1","value")],
    )
def make_fig(year_chosen, filter_chosen):
    if year_chosen > 0:
        if filter_chosen == "Winst":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            profits_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                profits_month.append(df_year[df_year["OrderMonth"] == i]["Profit"].sum())

            fig = px.line(x=months, y=profits_month, title=f"Winst per maand in {year_chosen}")
            fig.update_layout(xaxis_title="Maand",
                            yaxis_title="Winst")
            return fig

        if filter_chosen == "Omzet":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            sales_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                sales_month.append(df_year[df_year["OrderMonth"] == i]["Sales"].sum())

            fig = px.line(x=months, y=sales_month, title=f"Omzet per maand in {year_chosen}")
            fig.update_layout(xaxis_title="Maand",
                              yaxis_title="Omzet")
            return fig

        if filter_chosen == "Bestellingen":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            orders_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                orders_month.append(len(df_year[df_year["OrderMonth"] == i]["Order ID"].unique()))

            fig = px.line(x=months, y=orders_month, title=f"Bestellingen per maand in {year_chosen}")
            fig.update_layout(xaxis_title="Maand",
                              yaxis_title="Bestellingen")
            return fig

        if filter_chosen == "Gemiddelde winst":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            avg_profits_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                avg_profits_month.append(df_year[df_year["OrderMonth"] == i]["Profit"].mean())

            fig = px.line(x=months, y=avg_profits_month, title=f"Gemiddelde winst per maand in {year_chosen}")
            fig.update_layout(xaxis_title="Maand",
                              yaxis_title="Gemiddelde winst")
            return fig

        else:
            raise dash.exceptions.PreventUpdate

    if year_chosen == 0:
        raise dash.exceptions.PreventUpdate



