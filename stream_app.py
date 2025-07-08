import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import time
import plotly.express as px
import datetime
#from pycaret.classification import *

st.set_page_config(page_title="SE CSM Platform", page_icon='sporteasy_logo.png', layout="wide")
# load data
#data = pd.read_excel('data_health_score.xlsx')
# to accelerate the speed of the app
data = pd.read_parquet('data_health_score.parquet', engine='pyarrow')

_='''
# classification
s = setup(data[['club_id','login','game_score','attendance','collections','database','message_system','team_message','activation','churn']], target = 'churn', ignore_features = ['club_id'])
# pycaret by default train on 70%
best_model = compare_models(sort='F1')
tuned_best_model = tune_model(best_model)
plot_model(tuned_best_model, plot = 'feature')
plot_model(tuned_best_model, plot = 'confusion_matrix')
'''


st.title("Anticipation Churn")
st.sidebar.info('🚀 SportEasy Customer Success Platform')



club_id = st.sidebar.selectbox(
        'label',
        data["club_id"].unique().tolist(),
        placeholder='Select the id of the club',
        index=None,
        label_visibility="hidden")


data_club = data.loc[(data.club_id == club_id)]
tab1, tab2 = st.tabs(["Health Score", "Criteria Evolution"])

with tab1:

    fig = px.line(data_club, x="month_start", y="health_score", line_shape='spline')
    fig.update_yaxes(range=[0, 100]) 

    signing_date = data_club["month_traj_start"].unique()[0]
    # force to convert to ms due to a plotly known bug
    fig.add_vline(x=datetime.datetime.strptime(signing_date, "%Y-%m").timestamp() * 1000, 
                  line_width=3, 
                  line_dash="dash", 
                  line_color="green",
                  annotation_text="signing date",
                  annotation_font_color="green",
                  annotation_position="top")
    
    if data_club["churn"].unique()[0] == 1:
        churn_date = data_club["month_traj_end"].unique()[0]
        fig.add_vline(x=datetime.datetime.strptime(churn_date, "%Y-%m").timestamp() * 1000, 
                      line_width=3, 
                      line_dash="dash", 
                      line_color="red",
                      annotation_text= "churn date",
                      annotation_font_color="red",
                      annotation_position="top")
    
    fig.update_traces(mode='lines+markers', hovertemplate='%{x}<br>%{y}')
    
    st.plotly_chart(fig, use_container_width=False)
    
    
with tab2:
    row1 = st.columns(2)
    
    tile1 = row1[0].line_chart(data_club, 
                              x="month_start", 
                              y="activation", 
                              color="#94E3A8",
                              x_label="activation",
                              y_label="")
    
    tile2 = row1[1].line_chart(data_club, 
                              x="month_start", 
                              y="attendance", 
                              color="#94E3A8",
                              x_label="attendance",
                              y_label="")
    row2 = st.columns(2)
    tile3 = row1[0].line_chart(data_club, 
                              x="month_start", 
                              y="database", 
                              color="#94E3A8",
                              x_label="database",
                              y_label="")
    tile4 = row1[1].line_chart(data_club, 
                              x="month_start", 
                              y="game_score", 
                              color="#94E3A8",
                              x_label="game_score",
                              y_label="")
    
    row3 = st.columns(2)
    tile5 = row1[0].line_chart(data_club, 
                              x="month_start", 
                              y="login", 
                              color="#94E3A8",
                              x_label="login",
                              y_label="")
    tile6 = row1[1].line_chart(data_club, 
                              x="month_start", 
                              y="message_system", 
                              color="#94E3A8",
                              x_label="message_system",
                              y_label="")
    
    row4 = st.columns(2)
    tile7 = row1[0].line_chart(data_club, 
                              x="month_start", 
                              y="team_message", 
                              color="#94E3A8",
                              x_label="team_message",
                              y_label="")
    
    tile8 = row1[0].line_chart(data_club, 
                              x="month_start", 
                              y="collections", 
                              color="#94E3A8",
                              x_label="collections",
                              y_label="")