import streamlit as st
import numpy as np
import pandas as pd
import joblib

model = joblib.load('work.joblib')
st.title('HOUSE PRICE PREDICTION')

form = st.form(key='form2')
location = form.selectbox("Enter a location", ["Andheri East Mumbai", 'Andheri East Nagpur', 'Andheri West Mumbai',
                                               'Andheri West Nagpur', 'Borivali Mumbai',
                                               'Dahisar Mumbai', 'Goregaon East Mumbai', 'Goregaon West Mumbai',
                                               'Kandivali West Mumbai', 'Kandivali East Mumbai', 'Khar Mumbai',
                                               'Juhu Mumbai', 'Malad Mumbai', 'Santacruz East Mumbai',
                                               'Santacruz West Mumbai', 'Chembur Mumbai', 'Dadar Mumbai',
                                               'Wadala Mumbai', 'Bhandup Mumbai',
                                               'Kurla Mumbai', 'Ghatkopar Mumbai', 'Powai Mumbai',
                                               'Vikhroli Mumbai'])
furnish = form.selectbox("Enter the furnishing", ['Furnished', 'Semi-Furnished', 'Unfurnished'])
size = form.number_input("Enter the size",step=1)
bhk = form.number_input("Enter bhk",step=1)
bath = form.number_input("Enter the number of bathroom",step=1)
park = form.number_input("Enter the number of parking",step=1)
prediction = None
columns = ['loc', 'furnishing', 'sqft', 'size', 'bath', 'parking']

submit_button = form.form_submit_button('Predict')
if submit_button:
    @st.cache_data
    def predict(location, furnish, size, bhk, bath, park):
        columns = ['loc', 'furnishing', 'sqft', 'size', 'bath', 'parking']
        row = [location, furnish, size, bhk, bath, park]
        X = pd.DataFrame([row], columns=columns)
        return model.predict(X)[0]

    prediction = predict(location, furnish, size, bhk, bath, park)
    st.markdown("<h2 style='text-align: center;'>Predicted price =  Rs. {}</h2>".format(prediction.round()),
                unsafe_allow_html=True)

