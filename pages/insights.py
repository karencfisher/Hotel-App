# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Insights

            "Data science," John Kelleher and Brendan Tierney write,"encompasses a set of principles, 
            problem definitions, algorithims, and processes for extracting nonobvious and useful patterns 
            from large data sets." Why, one may ask, what is the purpose of constructing machine 
            learning models? One reason is of course we hope to predict future occurences, given some
            insight from the past. A buisiness such as a hotel will want to forecast future buisiness,
            including revenue, and choose appropriate strategies, such as deposit and cancellation policies.
            Another reason is to also understand *why*. Not just if we can predict a particular reservation
            will or not be cancelled, but if we can understand if there are factors that make a
            cancellation more or less likely. And when data science becomes interesting is, as Kelleher
            and Tierney suggest, is when the patterns it reveals are "nonobvious." In a sense it seeks
            to find patterns in apparent chaos: patterns we may not as readily see or intuit. (However,
            at this point in its evolution, machine learning may grasp statistical intelligence, it
            has not even begun to develop causal intelligence.)

            Having experience in the hotel industry for a number of years (and thus possessing some degree
            of 'domain knowledge'), I have wondered what factors lead to cancellations, and especially
            'no-shows' which are a small subset of cancellations for the purpose of this project. Does
            rate affect cancellations? The lead time (the interval between when a booking is made and the
            arrival date)? Of course, often customers have other, unforeseen circumstances that alter their
            plans and cancel their reservations. Such would seeimingly be inevitably unpredictable, at least 
            from out perspective. However, are there patterns that can be discerned? 

            We'll look briefly of a couple of the features which sway the model in deciding a reservation
            is more likely to be cancelled.

            #### Lead Time

            Lead time is the days between when a reservation is booked and the actual arrival date. This I
            expected to play a role in cancellations. After all, life happens in the meantime when we make
            the best of plans. From the chart upper right it is third in importance. It also has a positive
            correlation (longer the time, the more likely to be canceled).

            """
        ),

        html.P(
            [
                html.Img(src='assets/pdp_lead.jpg', className='img-fluid')
            ] 
        ),

        dcc.Markdown(
            """
            #### Parking Spaces

            This is one I did not forsee: the impact of availability or lack of parking spaces. While
            it is not as significant on the upper right chart, it has a significant impact on the
            application on this site. Try it: all other aspects of a reservation being unchanged, lower
            the available parking to zero and see the result. The correlation is negative, in that
            the larger the parking availability, the lower the potential of cancellation.

            """

        ),

        html.P(
            [
                html.Img(src='assets/pdp_parking.jpg', className='img-fluid')
            ] 
        )

    ],
)

column2 = dbc.Col(
    [
        html.P(
            [
                html.Img(src='assets/shap_summary.jpg', className='img-fluid')
            ] 
        ),

        dcc.Markdown(
            """
            #### Deposits

            One unexpected suggestion arising from this model concerned deposits. Intutively, one would 
            expect that a non-refundable deposit on a service (such as a hotel stay, and airline trip, and
            so forth) would disuade customers from cancelling, as they would lose money. Or is it that
            the hotels correctly assess deposits on occassions when they anticipate a higher chance of
            cancellations? In the above shapley plot, which shows how much each feature in the data set
            influences the model's predictions, deposit type comes in first. 

            Below one can see the specific importance of deposit type on the outcomes.

            """
        ),

        html.P(
            [
                html.Img(src='assets/pdp_deposit.jpg', className='img-fluid')
            ] 
        ),

        dcc.Markdown(
            """
            And on a specific case, in which it plays strongly in the prediction of cancellation.
            """
        ),

        html.P(
            [
                html.Img(src='assets/shap_prediction.jpg', className='img-fluid')
            ] 
        ),

        dcc.Markdown(
            """
            #### Previous Cancellations

            One factor I had not thought of was a customer having a history of cancellations. Yet it seems
            to take a large role. On the Prediction page, one can see that readily, by increasing the number
            of previous cancellations. In the above shapley plot, also, it is the largest contribution to
            that one prediction of cancellation.

            """
        ),

        html.P(
            [
                html.Img(src='assets/pdp_cxl.jpg', className='img-fluid')
            ] 
        ),


    ], 
    style={'margin-top': '30px'}
)

layout = dbc.Row([column1, column2])