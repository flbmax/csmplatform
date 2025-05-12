import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
#from pycaret.classification import *

st.title("Anticipation Churn")
st.sidebar.info('🚀 SportEasy Customer Success Plaform')

data = pd.read_excel('health_score_attendance_criteria.xlsx')
data = data.rename(columns={"traj_month.traj_end": "traj_end", "[traj_month.attendance_ratio]": "attendance"})
data = data.rename(columns={"traj_month.club_id": "club_id", "traj_month.traj_start": "traj_start"})

club_id = st.sidebar.selectbox(
        'label',
        data["club_id"].unique().tolist(),
        placeholder='Select the id of the club',
        index=None,
        label_visibility="hidden")


data_club = data.loc[(data.club_id == club_id)]
data_club['month_start'] = [date[:7] for date in data_club['date_start']]
data_club['size'] = 10000*data_club['attendance']

tab1, tab2 = st.tabs(["Health Score", "Criteria Evolution"])

with tab1:
    chart_data = data_club[['month_start','attendance','size']]
    #st.line_chart(chart_data, x="month_start", y="attendance", color="#94E3A8")
    point_selector = alt.selection_point("point_selection")
    interval_selector = alt.selection_interval("interval_selection")
    chart = (
        alt.Chart(chart_data)
        .mark_line()
        .encode(x="month_start", 
                y="attendance", 
                tooltip=["month_start", "attendance"]).add_params(point_selector, interval_selector)
        )
    
    st.altair_chart(chart)

with tab2:
    row1 = st.columns(2)
    row2= st.columns(2)
    row3= st.columns(2)
    row4= st.columns(2)
    
    for col in row1 + row2 + row3 + row4:
        tile = col.line_chart(chart_data, 
                              x="month_start", 
                              y="attendance", 
                              color="#94E3A8",
                              x_label="attendance",
                              y_label="")
    

    #chart_data = data_club[['month_start','game_score']]
    #st.line_chart(chart_data, x="month_start", y="game_score", color="#94E3A8")
    