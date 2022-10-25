
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
# Connect to main app.py file

from PIL import Image

# Connect to your app pages

from dash_bootstrap_templates import load_figure_template

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.LUX],
                use_pages=True)
                #suppress_callback_exceptions=True)
server = app.server

app.css.config.serve_locally = True
load_figure_template('LUX')

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '0%',
    'padding': '20px 10p',
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#000000'
}


CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#000000'
}

ALLOWED_TYPES = (
    "text",
)

pil_image = Image.open("assets/Schermafbeelding 2022-08-08 om 15.38.03.png")



#content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

sidebar = html.Div(
    [
        html.H2('Sales Dashboard'),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),

                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        style={"margin-bottom": "220px","border-width": "0 0 1px 0"}
        ),
        html.Img(src=pil_image,height=200)
    ],
    style=SIDEBAR_STYLE,
)

app.layout = dbc.Container([
    dbc.Col(
        [
        sidebar
        ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

    dbc.Col(
        [
            dash.page_container
        ],style={"margin-left": "30px", "margin-right": "0px"})

])

if __name__ == '__main__':
    app.run(debug=False)