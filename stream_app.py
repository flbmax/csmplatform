import pickle
import streamlit as st
import pandas as pd

add_selectbox = st.sidebar.selectbox("Choose the club_id",("1","2","3","4"))

st.sidebar.info('SE CSM Plaform')
st.title("Predicting Churn")

