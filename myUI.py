import streamlit as st
import pickle
import pandas as pd
import numpy as np
import xgboost
from xgboost import XGBRegressor
pipe = pickle.load(open(r"C:\Users\ankus\T-20 Score predictor\pipe.pkl", "rb"))
teams = ['Australia',
 'India',
 'Bangladesh',
 'New Zealand',
 'South Africa',
 'England',
 'West Indies',
 'Pakistan',
 'Sri Lanka']
cities=['Johannesburg', 'Karachi', 'Dubai', 'Delhi', 'Southampton',
       'Mumbai', 'Galle', 'Melbourne', 'Taunton', 'Guyana', 'Colombo',
       'Mount Maunganui', 'Auckland', 'Kuala Lumpur', 'Chittagong',
       'Durban', 'Lauderhill', 'Mirpur', 'Christchurch', 'Potchefstroom',
       'Cardiff', 'Derby', 'Cape Town', 'Sharjah', 'Trinidad',
       'Chandigarh', 'Antigua', 'Sydney', 'Lahore', 'Nottingham', 'Perth',
       'Hamilton', 'St Lucia', 'Bangalore', 'Manchester', 'Canberra',
       'Sylhet', 'London', 'Barbados', 'Nagpur', 'Kolkata', 'Wellington',
       'Adelaide', 'Centurion', 'Pallekele', 'Birmingham', 'Abu Dhabi',
       'Chennai', 'Chelmsford', 'Brisbane', 'Bristol',
       'Chester-le-Street']
genders=['male', 'female']
st.title('T20I Score Predictor')
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))
gender = st.selectbox('Select gender',sorted(genders))
city = st.selectbox('Select venue',sorted(cities))
col3,col4,col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score')
with col4:
    overs = st.number_input('Overs completed (Model works better for >= 5)')
with col5:
    wickets = st.number_input('Wickets down')
last_five = st.number_input('Runs scored in last 5 overs')
if st.button('Predict Score'):
    balls_left = 120 - (overs*6)
    wickets_left = 10 -wickets
    crr = current_score/overs
    input_df = pd.DataFrame(
     {'gender': [gender], 'batting_team': [batting_team], 'bowling_team': [bowling_team],'city':city, 'current_score': [current_score],'balls_left': [balls_left], 'wickets_left': [wickets_left], 'crr': [crr], 'last_five': [last_five]})
    result = pipe.predict(input_df)
    st.header("Predicted Score - " + str(int(result[0])))