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
        
            ## The Process

            Behind the scenes, here are two predictive models. When you enter your details on the previous page, the first model will estimate a price. A decision tree regressor takes in 4
            inputs to approximate an average nightly rate for your stay. 

            That estimate is then fed together with 16 other inputs to a second model, a random forest classifier,
            which then predicts the probability that you will ultimately cancel the reservation.

            Both models are trained on a data set of nearly 120,000 reservations made for two years at two chain hotels in Portugal. The two hotels are not named, specifically, but one is urban, and the second a resort location. The two data sets were initially compiled by [*Nuno Antonio,
            Ana de Almeida, and Luis Nunes*]
            (https://www.sciencedirect.com/science/article/pii/S2352340918315191), 
            for "the development of prediction models to classify a 
            hotel booking's likelihood to be canceled...[and] due to the characteristics of the variables included 
            in these datasets, their use [also] goes beyond this cancellation prediction problem." They were derived from the PMS (Property Management System) of each hotel from the original SQL database tables. The
            resulting datasets were later concatenated into one dataset and cleaned by Thomas Mock and 
            Antoine Bichatand, and published on [*Kaggle by Jesse Mostipak*]
            (https://www.kaggle.com/jessemostipak/hotel-booking-demand).


            #### Data Cleaning

            Although in relatively good condition, the data was still in need of some repair. One issue I 
            found was that a fair number of observations were mislabeled. The original target consisted of three 
            classes: 'Check-Out' (the guest had indeed stayed), 'Canceled' (in which they had formally canceled 
            their reservation), and 'No-Show' (never arrived without contacting the hotel or booking service). 
            On closer observation, several cases labeled as 'Check-Out,' where the date at which the status of 
            the reservation was changed was identical with the arrival date, suggesting the guest had not stayed. 
            I relabeled them as cancellations.
            Additionally, there were several cases in which the guest checked out prematurely. Such is not uncommon 
            in the 
            hotel industry. From my experience: a guest may need to attend to an emergency perhaps, or she may 
            have been dissatisfied with her stay. In either case, these are generally not reclassified as 
            cancellations, and I have left them as is.

            Also, there were a fair number of outliers in certain of the features, such as ADR (Average Daily Rate).  
            There were untenable values (0 or 54,000) and invalid values such as several adults (maximum 55). Such 
            values were treated as missing data, to be imputed later in the model building process. Country and arrival 
            dates were dropped as likely sources of data leakage. Generally, the countries of origin of hotel guests 
            are only known and recorded at the time of check-in, and as a result, a disproportionate number of 
            cancellations were classified as Portuguese, only because the hotels are in Portugal, potentially 
            resulting in the model readily overfitting.
            Specific dates can result in similar issues. However, a feature giving the numbered week of the year 
            was provided, and as it could provide information about the seasonality of the bookings, and improve 
            predictability. As a result, it has been retained. The final features used can be seen to the right 
            rated by their relative significance towards the results of the predictive model.

            #### Rate Estimation

            The rates are estimated using a decision tree regressor, based on the distribution of ADRs in the dataset. 
            The ADR column from the original dataset was dropped, and the model was trained to predict
            rates. The accuracy of it is an approximate mean absolute error of 24 Euros, so any price it 
            quotes will be within that margin of error. At this point, we did not attempt to adjust rates 
            to accommodate the average rate increases from year to year. However, the results should be 
            adequate for this demonstration.

            ![](assets/prices.jpg)



            """
        ),

    ],
)

column2 = dbc.Col(
    [
        html.P(
            [
                html.Img(src='assets/targets.jpg', className='img-fluid')
            ] 
        ),

        dcc.Markdown(
            """
            #### Cancellation Prediction

            While building the classification model to predict cancellations the most difficult issue arose
            from the relative imbalance of the two classes (check-out vs. canceled). An overall
            accuracy of aproximately 85% was readily obtained with a random forest classifier, however the 
            recall or sensitivity - the rate at which cancellations were accurately predicted as opposed
            to check-outs - was initially low. This can be seen in the scores below.

            ![Initial confusion matrix](assets/confusion1.jpg)

            Different strategies were explored to better balance the accurate classification of the 
            cases, including over sampling the minority class (cancellations) and undersampling the
            majority class (check-outs). The latter strategy seemed best: while the overall accuracy 
            was reduced by aproximately 1%, the true positive predictions of both classes became more 
            in balance. This would give us greater confidence in our ability to project the likelihood
            of new reservations in turn being canceled.

            ![Final confusion matrix](assets/confusion2.jpg)

            ![Distribution of actual and predicted outcomes](assets/balance.jpg)


            """
        ),

        
        html.Img(src='assets/ROC.jpg', className='img-fluid', style={'height': '300px', 'width': '400px',
                                                                    'margin-left': '20px'}),
        
        
    ], 
    style={'margin-top': '30px'}

)

layout = dbc.Row([column1, column2])