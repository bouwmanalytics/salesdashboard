import dash_core_components as dcc
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import base64
import datetime
import io
from calendar import month_name
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import plotly.graph_objs as go
dash.register_page(__name__, path='/voorspellingen', name='Voorspellingen') # '/' is home page

df = pd.read_csv('Orders-Tabel 1.csv',sep=";",decimal=',')
df["OrderDate"] = pd.to_datetime(df["Order Date"])
df["OrderYear"] = df.OrderDate.dt.year
df["OrderMonth"] = df.OrderDate.dt.month_name()
df["OrderMonthNr"] = df.OrderDate.dt.month
df["OrderDayNr"] = df.OrderDate.dt.day

df2 = df.copy()
df2["Segment"] = pd.Categorical(df2.Segment)
df2['Segment'] = df2.Segment.cat.codes

df2["Ship Mode"] = pd.Categorical(df2["Ship Mode"])
df2['Ship Mode'] = df2["Ship Mode"].cat.codes

df2["Category"] = pd.Categorical(df2["Category"])
df2['Category'] = df2["Category"].cat.codes

df2["Sub-Category"] = pd.Categorical(df2["Sub-Category"])
df2['Sub-Category'] = df2["Sub-Category"].cat.codes

df2["Region"] = pd.Categorical(df2["Region"])
df2['Region'] = df2["Region"].cat.codes

df2["Year_Month"] = df["OrderDate"] = pd.to_datetime(df["OrderDate"]).dt.to_period('M')
df2.sort_values(by="Year_Month",inplace=True)
df2.reset_index(inplace=True)

X = df2[['Region', 'Category', 'Sub-Category', 'Sales', 'Quantity', 'Discount',
       'OrderYear', 'OrderMonthNr',"OrderDayNr"]]
y = df2["Profit"]


X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=40)
model = RandomForestRegressor(random_state = 40)
best_params = {'n_estimators': 200,
 'min_samples_split': 2,
 'min_samples_leaf': 1,
 'max_depth': 70,
 'bootstrap': True}
model.set_params(**best_params)
model.fit(X_train,y_train)
TEXT_STYLE = {
    #'textAlign': 'center',
    'color': '#000000'
}


def generate_results_dataset(preds, ci, months):
    df = pd.DataFrame(index=months)
    df['prediction'] = preds
    if ci >= 0:
        df['upper'] = preds + ci
        df['lower'] = preds - ci
    else:
        df['upper'] = preds - ci
        df['lower'] = preds + ci

    return df

layout = html.Div(
    [
        dbc.Row([
            dbc.Col([
                html.H2('Voorspellingen',
                        style=TEXT_STYLE)]),
            dbc.Col([
                html.P("Kies een jaar",style={"margin-top": "10px", "width": "100%"}),
                dcc.Dropdown([2018,2019,2020,2021,2022], 2018, id="year_dropdown"),
            ]),

        ]),
        dbc.Row([
            dcc.Graph(id="prediction_graph", figure={})
        ])



])

@callback(
    Output("prediction_graph",  "figure"),
    [Input("year_dropdown", "value")],
)
def get_graph(year):
    alpha = 0.05
    test = X.sample(400, random_state=42)
    test.OrderYear = year
    residuals = y_train - model.predict(X_train)
    ci = np.quantile(residuals, 1 - alpha)
    preds = model.predict(test)
    dff = generate_results_dataset(preds, ci, test.OrderMonthNr)
    pred = dff.groupby("OrderMonthNr")["prediction"].sum()
    upper = dff.groupby("OrderMonthNr")["upper"].sum()
    lower = dff.groupby("OrderMonthNr")["lower"].sum()
    months = np.array(range(1, 13))
    fig = px.line(x=months, y=pred, title="Winst voorspelling in 2020")
    fig.update_traces(line_color='black', line_width=1)
    fig.add_traces(go.Scatter(x=months, y=lower,
                              line=dict(color='grey'),
                              fill='tonexty',
                              name="Lagere 95% confidence interval"))
    fig.add_traces(go.Scatter(x=months, y=upper,
                              # line = dict(color='red'),
                              fill='tonexty',
                              name="Hogere 95% confidence interval",
                              line=dict(color="#ffe476")))

    fig.update_traces(line_color='black', line_width=2)
    fig.update_layout(xaxis_title="Maand",
                      yaxis_title="Winst")
    fig.update_layout(legend_traceorder="reversed")
    fig.data[1].line.color = "blue"
    fig.data[2].line.color = "blue"

    return fig


