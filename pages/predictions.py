# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_daq as daq
import datetime as dt

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier

# Estimators
from joblib import load
price_estimator = load('models/price_model.joblib')
cxl_estimator = load('models/cancellation_model.joblib')

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Reservations

            Make a reservation. Then see an estimated price and the likelihood you will cancel. Change
            your selections to see how that will impact the estimates.

            """
        ),

    dcc.DatePickerSingle(
        id='arrival_date',
        min_date_allowed=dt.date.today(),
        max_date_allowed=dt.date(2022, 12, 31),
        initial_visible_month=dt.date.today(),
        date=dt.date.today()
    ),
    dcc.Markdown('Choose arrival date'),

    dcc.Dropdown(
        id='hotel',
        options=[
            {'label': 'City', 'value': 1},
            {'label': 'Resort', 'value': 2}
        ],
        value=1
    ),
    dcc.Markdown('Choose which location'),

    daq.NumericInput(
        id='num_nights',
        min=1,
        max=30,
        value=1
    ),  
    dcc.Markdown('Choose number of nights'),

    daq.NumericInput(
        id='num_adults',
        min=1,
        max=4,
        value=2
    ),
    dcc.Markdown('How many adults?'),

    dcc.Dropdown(
        id='meal_plan',
        options=[
            {'label': 'None', 'value': 0},
            {'label': 'Breakfast', 'value': 1},
            {'label': 'Breakfast and dinner', 'value': 2},
            {'label': 'Full meal plan','value': 3 }
        ],
        value=3
    ),
    dcc.Markdown('Choose a meal plan'),

    daq.NumericInput(
        id='num_cars',
        min=0,
        max=4,
        value=2
    ),
    dcc.Markdown('Available parking spaces'),

    daq.NumericInput(
        id='num_sr',
        min=0,
        max=5,
        value=2
    ),
    dcc.Markdown('How many special requests will you have?'),

    dcc.RadioItems(
        id='prev_stay',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0}
        ],
        value=1,
        labelStyle={'display': 'inline-block', 'padding': '5px'}
    ),
    dcc.Markdown('Have you stayed with us before?'),

    daq.NumericInput(
        id='num_prev_cxl',
        min=0,
        max=10,
        value=0
    ),  
    dcc.Markdown('Be honest, how many times you have cancelled reservations before?'),

    dcc.RadioItems(
        id='deposit_type',
        options=[
            {'label': 'None', 'value': 1},
            {'label': 'Refundable', 'value': 2},
            {'label': 'Non-refundable', 'value': 3}
        ],
        value=1,
        labelStyle={'display': 'inline-block', 'padding': '5px'}
    ),
    dcc.Markdown('Will you make a deposit?')

    #html.Button('Book it!', id='submit-reservation', n_clicks=0)
    

    ],
    md=4,
    )

column2 = dbc.Col(
    [
        html.Div(id='price-output'), 
        html.Div(id='cxl-output')
    ]
)

@app.callback(
    [Output('price-output', 'children'), Output('cxl-output', 'children')],
    [Input('arrival_date', 'date'), 
     Input('num_adults', 'value'),
     Input('num_nights', 'value'),
     Input('meal_plan', 'value'),
     Input('hotel', 'value'),
     Input('num_cars', 'value'),
     Input('num_sr', 'value'),
     Input('prev_stay', 'value'),
     Input('num_prev_cxl', 'value'),
     Input('deposit_type', 'value')],
)
def predict(arrival_date, num_adults, num_nights, meal_plan, hotel, num_cars,
            num_sr, prev_stay, num_prev_cxl, deposit_type):

    # Get the week of the year and lead time from the arrival date
    arrival = dt.datetime.strptime(arrival_date, '%Y-%m-%d')
    week = arrival.isocalendar()[1]
    lead_time = (arrival.date() - dt.date.today()).days

    # Features used in the model not exposed in this app, but will be hard coded
    market_seg = 1
    room_type_changed = False
    customer_type = 1
    days_in_waiting_list = 0
    booking_changes = 0

    # Input for the price model. Already encoded. 
    # ['arrival_date_week_number', 'hotel', 'adults', 'nights_stay']
    input1 = [week, hotel, num_adults, num_nights]

    # Get estimated price of this stay
    adr = round(price_estimator.predict([input1])[0] + meal_plan * 10, 2)
    total = round(adr * num_nights, 2)

    # Generate the output
    output1 = [html.P(f'Estimated nightly rate {adr} Euros', style={'text-align': 'center',
                                                                    'margin-top': '40px'}),
               html.P(f'Total cost {total} Euros', style={'text-align': 'center'})]

    # Input for the cancellation model. Rolls in the ADR from previous step
    input2 = [hotel, lead_time, week, num_adults, meal_plan, market_seg, prev_stay, 
        num_prev_cxl, booking_changes, deposit_type, days_in_waiting_list, 
        customer_type, adr, num_cars, num_sr, num_nights, room_type_changed]

    # Predict probabilities of staying, and cancelling
    probabilities = cxl_estimator.predict_proba([input2])

    # Generate the output as guage
    output2 = daq.Gauge(
            showCurrentValue=True,
            units="percentage points",
            value= probabilities[0][1] * 100,
            label=f'{round(probabilities[0][1] * 100, 2)} % probability of cancellation',
            size=280,
            labelPosition='bottom',
            max=100,
            min=0,
)  

    return output1, output2

layout = dbc.Row([column1, column2])