import dash
from dash import dcc, html, callback, Output, Input

import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import pathlib
import numpy as np
from calendar import month_name

dash.register_page(__name__, path='/Jaarlijks', name='Jaarlijks', title= "Jaarlijks") # '/' is home page

df = pd.read_csv('Orders-Tabel 1.csv',sep=";",decimal=',')
df["OrderDate"] = pd.to_datetime(df["Order Date"])
df["OrderYear"] = df.OrderDate.dt.year
df["OrderMonth"] = df.OrderDate.dt.month_name()
df["OrderMonthNr"] = df.OrderDate.dt.month
df["ShipDate"] = pd.to_datetime(df["Ship Date"])
TEXT_STYLE = {
    #'textAlign': 'center',
    'color': '#000000'
}

layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                html.H2('Yearly Analysis',
                        style=TEXT_STYLE)]),
            dbc.Col([
                html.P("Choose a year",style={"margin-top": "10px", "width": "100%"}),
                dcc.Dropdown(np.sort(df.OrderYear.unique()), np.sort(df.OrderYear.unique())[0], id="year_dropdown"),
            ]),
        ]),

        dbc.Row([
            html.Hr(style={"margin-top": "30px","border-width": "0 0 1px 0"}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([html.P("Total customers", style={"text-decoration": "underline"})]),
                dbc.Row([html.P(id="ncust", style={"margin-bottom": "20px","margin-right": "10px"}),])
            ]),
            dbc.Col([
                dbc.Row([html.P(id="text_1", style={"text-decoration": "underline"})]),
                dbc.Row([html.P(id="norders", style={"margin-bottom": "20px","margin-right": "10px"})])
            ]),
            dbc.Col([
                dbc.Row([html.P("Average shipping time", style={"text-decoration": "underline"})]),
                dbc.Row([html.P(id="avg_ship", style={"margin-bottom": "20px","margin-right": "10px"})])
            ])
        ]),
        dbc.Row([
            html.Hr(style={"border-width": "0 0 1px 0"}),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    html.P("Choose a filter",style={"margin-top": "10px"}),
                    dcc.Dropdown(["Orders","Sales", "Profit", "Average Profit"], "Orders", id="filter_dropdown_1"),
                ]),
                dcc.Graph(id="rel_1", figure = {})
            ],width=8),
            dbc.Col([
                dbc.Row([
                    html.P("Choose a filter",style={"margin-top": "10px"}),
                    dcc.Dropdown(["Region","Ship Mode", "Category", "Segment"], "Region", id="filter_dropdown_2"),
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
    if filter_dropdown == "Orders":
        return "Total Orders"
    if filter_dropdown == "Sales":
        return "Total Sales"
    if filter_dropdown == "Profit":
        return "Total Profit"
    if filter_dropdown == "Average Profit":
        return "Average profit"
@callback(
    Output("norders",  "children"),
    [Input("year_dropdown","value")],
    [Input("filter_dropdown_1","value")]
    )
def print_output(year_chosen, filter_dropdown):
    if year_chosen > 0:
        if filter_dropdown == "Orders":
            norders = np.round(df.groupby("OrderYear")["Order ID"].nunique()[year_chosen],2)
            return norders

        if filter_dropdown == "Sales":
            nsales = np.round(df.groupby("OrderYear")["Sales"].sum()[year_chosen],2)
            return nsales

        if filter_dropdown == "Profit":
            profit = np.round(df.groupby("OrderYear")["Profit"].sum()[year_chosen],2)
            return profit
        if filter_dropdown == "Average Profit":
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
    if filter1_chosen == "Average Profit":
        if filter2_chosen == "Region":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_region = []
                for i in sorted(df_year["Region"].unique()):
                    profits_region.append(df_year[df_year["Region"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Region"].unique()), y = profits_region, title=f"Average profit per region in {year_chosen}", text=np.round(profits_region,2))
                fig.update_layout(xaxis_title="Region",
                                  yaxis_title="Average Profit", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Ship Mode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    profits_shipmode.append(df_year[df_year["Ship Mode"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=profits_shipmode, text=np.round(profits_shipmode,2),
                             title=f"Average profit per ship mode in {year_chosen}")
                fig.update_layout(xaxis_title="Ship Mode",
                                  yaxis_title="Average Profit", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Category":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_category = []
                for i in sorted(df_year["Category"].unique()):
                    profits_category.append(df_year[df_year["Category"] == i]["Profit"].mean())
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=profits_category, text=np.round(profits_category,2),
                             title=f"Average profit per category in {year_chosen}")
                fig.update_layout(xaxis_title="Category",
                                  yaxis_title="Average Profit", )
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
                             title=f"Average profit per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="AverageProfit", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate

    if filter1_chosen == "Profit":
        if filter2_chosen == "Region":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_region = []
                for i in sorted(df_year["Region"].unique()):
                    profits_region.append(df_year[df_year["Region"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Region"].unique()), y=profits_region, text=np.round(profits_region,2),
                             title=f"Profit per region in {year_chosen}")
                fig.update_layout(xaxis_title="Region",
                                  yaxis_title="Profit", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Ship Mode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    profits_shipmode.append(df_year[df_year["Ship Mode"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=profits_shipmode, text=np.round(profits_shipmode,2),
                             title=f"Profit per ship mode in {year_chosen}")
                fig.update_layout(xaxis_title="Ship Mode",
                                  yaxis_title="Profit", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Category":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                profits_category = []
                for i in sorted(df_year["Category"].unique()):
                    profits_category.append(df_year[df_year["Category"] == i]["Profit"].sum())
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=profits_category, text=np.round(profits_category,2),
                             title=f"Profit per category in {year_chosen}")
                fig.update_layout(xaxis_title="Category",
                                  yaxis_title="Profit", )
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
                             title=f"Profit per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Profit", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate

    if filter1_chosen == "Orders":
        if filter2_chosen == "Region":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_region = []
                for i in sorted(df_year["Region"].unique()):
                    orders_region.append(len(df_year[df_year["Region"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Region"].unique()), y=orders_region, text=np.round(orders_region,2),
                             title=f"Orders per region in {year_chosen}")
                fig.update_layout(xaxis_title="Region",
                                  yaxis_title="Orders", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Ship Mode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    orders_shipmode.append(len(df_year[df_year["Ship Mode"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=orders_shipmode, text=np.round(orders_shipmode,2),
                             title=f"Orders per ship mode in {year_chosen}")
                fig.update_layout(xaxis_title="Ship Mode",
                                  yaxis_title="Orders", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Category":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                orders_category = []
                for i in sorted(df_year["Category"].unique()):
                    orders_category.append(len(df_year[df_year["Category"] == i]["Order ID"].unique()))
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=orders_category, text=np.round(orders_category,2),
                             title=f"Orders per category in {year_chosen}")
                fig.update_layout(xaxis_title="Category",
                                  yaxis_title="Profit", )
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
                             title=f"Orders per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Orders", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        else:
            raise dash.exceptions.PreventUpdate

    if filter1_chosen == "Sales":
        if filter2_chosen == "Region":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_region = []
                for i in sorted(df_year["Region"].unique()):
                    sales_region.append(df_year[df_year["Region"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Region"].unique()), y=sales_region, text=np.round(sales_region,2),
                             title=f"Sales per region in {year_chosen}")
                fig.update_layout(xaxis_title="Region",
                                  yaxis_title="Sales", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Ship Mode":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_shipmode = []
                for i in sorted(df_year["Ship Mode"].unique()):
                    sales_shipmode.append(df_year[df_year["Ship Mode"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Ship Mode"].unique()), y=sales_shipmode,text=np.round(sales_shipmode,2),
                             title=f"Sales per ship mode in {year_chosen}")
                fig.update_layout(xaxis_title="Ship Mode",
                                  yaxis_title="Sales", )
                return fig

            if year_chosen == 0:
                raise dash.exceptions.PreventUpdate

        if filter2_chosen == "Category":
            if year_chosen > 0:
                df_year = df[df["OrderYear"] == year_chosen]
                sales_category = []
                for i in sorted(df_year["Category"].unique()):
                    sales_category.append(df_year[df_year["Category"] == i]["Sales"].sum())
                fig = px.bar(x=sorted(df_year["Category"].unique()), y=sales_category, text=np.round(sales_category,2),
                             title=f"Sales per category in {year_chosen}")
                fig.update_layout(xaxis_title="Category",
                                  yaxis_title="Sales", )
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
                             title=f"Sales per segment in {year_chosen}")
                fig.update_layout(xaxis_title="Segment",
                                  yaxis_title="Sales", )
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
        if filter_chosen == "Profit":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            profits_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                profits_month.append(df_year[df_year["OrderMonth"] == i]["Profit"].sum())

            fig = px.line(x=months, y=profits_month, title=f"Profit per month in {year_chosen}")
            fig.update_layout(xaxis_title="Month",
                            yaxis_title="Profit")
            return fig

        if filter_chosen == "Sales":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            sales_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                sales_month.append(df_year[df_year["OrderMonth"] == i]["Sales"].sum())

            fig = px.line(x=months, y=sales_month, title=f"Sales per month in {year_chosen}")
            fig.update_layout(xaxis_title="Month",
                              yaxis_title="Sales")
            return fig

        if filter_chosen == "Orders":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            orders_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                orders_month.append(len(df_year[df_year["OrderMonth"] == i]["Order ID"].unique()))

            fig = px.line(x=months, y=orders_month, title=f"Orders per month in {year_chosen}")
            fig.update_layout(xaxis_title="Month",
                              yaxis_title="Orders")
            return fig

        if filter_chosen == "Average Profit":
            month_lookup = list(month_name)
            df_year = df[df["OrderYear"] == year_chosen]
            avg_profits_month = []
            months = sorted(df_year["OrderMonth"].unique(), key=month_lookup.index)
            for i in months:
                avg_profits_month.append(df_year[df_year["OrderMonth"] == i]["Profit"].mean())

            fig = px.line(x=months, y=avg_profits_month, title=f"Profit per month in {year_chosen}")
            fig.update_layout(xaxis_title="Month",
                              yaxis_title="Average Profit")
            return fig

        else:
            raise dash.exceptions.PreventUpdate

    if year_chosen == 0:
        raise dash.exceptions.PreventUpdate



