import dash
from dash import dcc, html, callback, Output, Input, dash_table

import dash_bootstrap_components as dbc


import pandas as pd

df = pd.read_csv('/Users/nielsbouwman/Downloads/Orders-Tabel 1.csv',sep=";",decimal=',')
df["OrderDate"] = pd.to_datetime(df["Order Date"])
df["OrderYear"] = df.OrderDate.dt.year
df["OrderMonth"] = df.OrderDate.dt.month_name()
df["OrderMonthNr"] = df.OrderDate.dt.month

dash.register_page(__name__, path='/', name='Home', title= "Home") # '/' is home page
TEXT_STYLE = {
    #'textAlign': 'center',
    'color': '#000000'
}

layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                html.H2('Home',
                        style=TEXT_STYLE)]),
        ]),
        dbc.Row([
            html.Hr(style={"margin-top": "30px","border-width": "0 0 1px 0"}),
        ]),
        dbc.Row([
            html.P("Dit dashboard is een voorbeeld van de dashboards die gemaakt kunnen worden bij Bouwmanalytics. Uiteraard kunnen er in overleg elementen worden toegevoegd of weggelaten.  "
                   "De dataset die is gebruikt voor dit dashboard is gevonden op internet. Het is een dataset met gegevens van een webwinkel uit de USA. "
                   "De dataset is gebruikt om te demonstreren wat er mogelijk is bij Bouwmanalytics. Uiteraard zal er, in het geval van een daadwerkelijke overeenkomst, ook nog uitleg gegeven worden bij de grafieken en cijfers. Dit zodat het voor iedereen duidelijk is wat de cijfers betekenen en waar de eventuele winst te behalen valt."
                   " De eerste vijf rijen van bepaalde kolommen van de tabel van de data zijn hieronder weergegeven:")
        ]),

        dbc.Row([
            dash_table.DataTable(data = df[["Order ID", "Segment", "Category", "Sales", "OrderYear"]].head().to_dict('records'))
        ])
])