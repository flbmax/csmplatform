import pickle
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import time
import plotly.express as px
import datetime

# load data
data_message_system = pd.read_excel('health_score_message_system.xlsx')
data_login = pd.read_excel('health_score_login.xlsx')
data_database = pd.read_excel('health_score_database.xlsx')
data_team_message = pd.read_excel('health_score_team_message.xlsx')
data_collections = pd.read_excel('health_score_collections.xlsx')
data_attendance = pd.read_excel('health_score_attendance.xlsx')
data_game_score = pd.read_excel('health_score_game_score.xlsx')
data_activation = pd.read_excel('health_score_activation.xlsx')

# rename data
data_attendance = data_attendance.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "traj_month.attendance_ratio": "attendance"})

data_collections = data_collections.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "criteria": "collections"})

data_database = data_database.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "traj_month.num_added_col": "database"})

data_team_message = data_team_message.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "criteria": "team_message"})


data_game_score = data_game_score.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "criteria": "game_score"})

data_login = data_login.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "traj_month.criteria_login": "login"})

data_message_system = data_message_system.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "criteria": "message_system"})

data_activation = data_activation.rename(columns={
        "traj_month.traj_start": "traj_start", 
        "traj_month.traj_end": "traj_end", 
        "traj_month.club_id": "club_id", 
        "criteria": "activation"})

# merge data
data = data_login.merge(data_game_score[['club_id','date_start','game_score']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])
data = data.merge(data_attendance[['club_id','date_start','attendance']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])
data = data.merge(data_collections[['club_id','date_start','collections']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])
data = data.merge(data_database[['club_id','date_start','database']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])
data = data.merge(data_message_system[['club_id','date_start','message_system']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])
data = data.merge(data_team_message[['club_id','date_start','team_message']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])
data = data.merge(data_activation[['club_id','date_start','activation']], left_on = ['club_id','date_start'], right_on = ['club_id','date_start'])

# replace null values by 0
data = data.replace('-',0)

# special case for login as 1 was considered as a str
data.login = data.login.replace('1',1)

# add binary criteria
data["attendance_criteria"] = (data["attendance"].astype(int) >= 0.5).astype(int)
data["collections_criteria"] = (data["collections"].astype(int) >= 3).astype(int)
data["database_criteria"] = (data["database"].astype(int) >= 1).astype(int)
data["game_score_criteria"] = (data["game_score"].astype(float) > 0.5).astype(int)
data["login_criteria"] = (data["login"].astype(int) >= 1).astype(int)
data["message_system_criteria"] = (data["message_system"].astype(int) >= 1).astype(int)
data["team_message_criteria"] = (data["team_message"].astype(int) >= 0.3).astype(int)
data["activation_criteria"] = (data["activation"].astype(int) > 0.5).astype(int)

# add health score
data["health_score"] = data["attendance_criteria"]+data["collections_criteria"]+data["database_criteria"]+data["game_score_criteria"]+data["login_criteria"]+data["message_system_criteria"]+data["team_message_criteria"]+data["activation_criteria"]
data["health_score"] = round((data["health_score"]*100)/8,0)

data['month_start'] = [date[:7] for date in data['date_start']]
data['month_traj_start'] = [date.strftime('%Y-%m-%d %H:%M:%S')[:7] for date in data['traj_start']]
data['month_traj_end'] = [date.strftime('%Y-%m-%d %H:%M:%S')[:7] for date in data['traj_end']]


churn = pd.read_excel('health_score_churn.xlsx')
data = data.merge(churn[['club_id','churn']], left_on = ['club_id'], right_on = ['club_id'])

data.to_parquet('data_health_score.parquet', engine='pyarrow')


