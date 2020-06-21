# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predict Hotel cancellations

            The rate of cancellations for hotels ranges from 20 - 40%, impacting revenue, 
            rate projections, and so forth.
            Can machine learning help hotels anticipate that a guest will cancel their 
            reservation?

            """
        ),
        dcc.Link(dbc.Button('Book a room and see!', color='primary'), href='/predictions')
    ],
    md=4,
)

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col(
    [
        html.Img(src='assets/Four-Seasons.jpg', className='img-fluid')
    ],
    style={'margin-top': '10px'}
)

layout = dbc.Row([column1, column2])