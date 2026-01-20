# Part 1: Imports, Styles, DLS Table, Player Loading, Team Class, AI Teams, Session State Initialization

import streamlit as st
import random
import time
import math
import pandas as pd

st.set_page_config(page_title="🏏 IPL Director: Mega Auction + Match Simulator", layout="wide")
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton > button {width: 100%;}
    .player-card {border: 1px solid #ddd; padding: 10px; border-radius: 10px; text-align: center;}
    .auctioneer {font-weight: bold; color: #FF4B4B;}
    .bid-button {background-color: #4CAF50; color: white;}
    .pass-button {background-color: #f44336; color: white;}
    </style>
""", unsafe_allow_html=True)

# DLS Resource Table
dls_table = [
    [100.0, 96.9, 95.6, 91.7, 87.7, 83.5, 79.2, 75.1, 71.5, 68.3, 65.0, 61.3, 57.9, 54.0, 49.3, 41.7, 36.2, 30.8, 25.4, 19.7, 13.7],  # wk 0
    [93.0, 90.9, 86.7, 82.3, 78.2, 74.3, 70.7, 67.4, 63.7, 59.9, 56.0, 52.3, 48.3, 44.2, 40.2, 38.5, 33.4, 28.0, 22.8, 17.2, 11.3],
    [87.9, 87.7, 82.9, 78.9, 75.3, 70.9, 67.3, 63.6, 60.2, 56.6, 52.6, 47.9, 44.3, 40.2, 37.4, 35.7, 31.0, 26.1, 21.1, 15.5, 9.7],
    [81.3, 83.0, 78.7, 73.8, 70.5, 66.9, 63.7, 60.3, 56.8, 53.3, 50.1, 46.1, 41.7, 37.4, 35.4, 33.0, 28.6, 24.1, 19.4, 14.1, 8.5],
    [72.2, 76.9, 73.2, 69.7, 66.4, 62.6, 59.3, 56.2, 52.9, 49.7, 46.0, 42.5, 38.9, 35.0, 32.1, 31.7, 27.3, 22.4, 17.7, 12.7, 7.3],
    [59.9, 68.3, 65.4, 62.8, 60.2, 57.4, 54.6, 51.5, 47.5, 43.9, 40.8, 37.8, 34.9, 33.8, 32.1, 29.0, 25.5, 20.7, 16.5, 11.9, 6.7],
    [44.8, 56.5, 54.2, 52.2, 50.3, 48.4, 46.4, 44.3, 41.9, 39.3, 36.1, 33.1, 30.2, 28.3, 27.2, 24.2, 21.5, 18.3, 14.4, 10.6, 6.0],
    [29.7, 42.0, 40.2, 38.7, 37.4, 36.2, 35.0, 33.8, 32.6, 31.3, 30.0, 28.6, 26.1, 23.4, 23.4, 20.0, 17.0, 14.2, 11.6, 9.3, 5.2],
    [17.6, 27.2, 25.7, 24.6, 23.5, 22.7, 21.8, 20.2, 19.4, 18.6, 16.7, 15.7, 14.5, 12.2, 10.0, 14.5, 12.2, 10.0, 7.9, 6.2, 4.2],
    [0.0, 15.3, 13.9, 12.8, 12.0, 11.2, 10.5, 9.8, 9.1, 8.5, 7.9, 7.2, 6.6, 5.9, 5.2, 5.2, 4.4, 3.5, 2.5, 1.6, 0.9],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

# FULL PLAYER DATA (all from your original query)
@st.cache_data
def load_players():
    data = [
        ('Jos Buttler', 'England', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Jos+Buttler', {'matches': 96, 'runs': 3223, 'avg': 37.92, 'wickets': 0}),
        ('Shreyas Iyer', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Shreyas+Iyer', {'matches': 101, 'runs': 2776, 'avg': 31.55, 'wickets': 0}),
        ('Rishabh Pant', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rishabh+Pant', {'matches': 98, 'runs': 2858, 'avg': 34.67, 'wickets': 0}),
        ('Kagiso Rabada', 'South Africa', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Kagiso+Rabada', {'matches': 69, 'wickets': 106, 'economy': 8.32, 'runs': 206}),
        ('Arshdeep Singh', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Arshdeep+Singh', {'matches': 51, 'wickets': 65, 'economy': 8.77, 'runs': 76}),
        ('Mitchell Starc', 'Australia', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Mitchell+Starc', {'matches': 34, 'wickets': 51, 'economy': 8.08, 'runs': 97}),
        ('Yuzvendra Chahal', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Yuzvendra+Chahal', {'matches': 145, 'wickets': 187, 'economy': 7.66, 'runs': 205}),
        ('Liam Livingstone', 'England', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Liam+Livingstone', {'matches': 32, 'runs': 827, 'avg': 29.53, 'wickets': 13}),
        ('David Miller', 'South Africa', 'BAT', 'Capped', 1.5, 'https://via.placeholder.com/200?text=David+Miller', {'matches': 121, 'runs': 2714, 'avg': 33.92, 'wickets': 0}),
        ('KL Rahul', 'India', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=KL+Rahul', {'matches': 118, 'runs': 4163, 'avg': 46.77, 'wickets': 0}),
        ('Mohammad Shami', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Mohammad+Shami', {'matches': 110, 'wickets': 127, 'economy': 8.37, 'runs': 127}),
        ('Mohammad Siraj', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Mohammad+Siraj', {'matches': 79, 'wickets': 79, 'economy': 8.65, 'runs': 79}),
        ('Harry Brook', 'England', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Harry+Brook', {'matches': 11, 'runs': 190, 'avg': 21.11, 'wickets': 0}),
        ('Devon Conway', 'New Zealand', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Devon+Conway', {'matches': 23, 'runs': 924, 'avg': 48.63, 'wickets': 0}),
        ('Jake Fraser-Mcgurk', 'Australia', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Jake+Fraser-Mcgurk', {'matches': 9, 'runs': 330, 'avg': 36.67, 'wickets': 0}),
        ('Aiden Markram', 'South Africa', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Aiden+Markram', {'matches': 33, 'runs': 775, 'avg': 29.81, 'wickets': 2}),
        ('Devdutt Padikkal', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Devdutt+Padikkal', {'matches': 57, 'runs': 1525, 'avg': 26.75, 'wickets': 0}),
        ('Rahul Tripathi', 'India', 'BAT', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Rahul+Tripathi', {'matches': 76, 'runs': 1798, 'avg': 25.68, 'wickets': 0}),
        ('David Warner', 'Australia', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=David+Warner', {'matches': 176, 'runs': 6565, 'avg': 41.54, 'wickets': 0}),
        ('Ravichandaran Ashwin', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Ravichandaran+Ashwin', {'matches': 197, 'runs': 714, 'avg': 15.53, 'wickets': 171}),
        ('Venkatesh Iyer', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Venkatesh+Iyer', {'matches': 36, 'runs': 956, 'avg': 28.11, 'wickets': 3}),
        ('Mitchell Marsh', 'Australia', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Mitchell+Marsh', {'matches': 38, 'runs': 665, 'avg': 23.75, 'wickets': 36}),
        ('Glenn Maxwell', 'Australia', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Glenn+Maxwell', {'matches': 124, 'runs': 2719, 'avg': 25.65, 'wickets': 31}),
        ('Harshal Patel', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Harshal+Patel', {'matches': 91, 'runs': 243, 'avg': 8.1, 'wickets': 111}),
        ('Rachin Ravindra', 'New Zealand', 'AR', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Rachin+Ravindra', {'matches': 10, 'runs': 222, 'avg': 22.2, 'wickets': 0}),
        ('Marcus Stoinis', 'Australia', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Marcus+Stoinis', {'matches': 82, 'runs': 1504, 'avg': 26.84, 'wickets': 39}),
        ('Jonny Bairstow', 'England', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Jonny+Bairstow', {'matches': 39, 'runs': 1291, 'avg': 35.86, 'wickets': 0}),
        ('Quinton De Kock', 'South Africa', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Quinton+De+Kock', {'matches': 96, 'runs': 2907, 'avg': 32.66, 'wickets': 0}),
        ('Rahmanullah Gurbaz', 'Afghanistan', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rahmanullah+Gurbaz', {'matches': 13, 'runs': 227, 'avg': 20.63, 'wickets': 0}),
        ('Ishan Kishan', 'India', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Ishan+Kishan', {'matches': 91, 'runs': 2324, 'avg': 29.05, 'wickets': 0}),
        ('Phil Salt', 'England', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Phil+Salt', {'matches': 9, 'runs': 435, 'avg': 48.33, 'wickets': 0}),
        ('Jitesh Sharma', 'India', 'WK', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Jitesh+Sharma', {'matches': 26, 'runs': 543, 'avg': 23.61, 'wickets': 0}),
        ('Syed Khaleel Ahmed', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Syed+Khaleel+Ahmed', {'matches': 10, 'wickets': 9, 'economy': 9.15, 'runs': 13}),
        ('Trent Boult', 'New Zealand', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Trent+Boult', {'matches': 88, 'wickets': 105, 'economy': 8.26, 'runs': 197}),
        ('Josh Hazlewood', 'Australia', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Josh+Hazlewood', {'matches': 27, 'wickets': 35, 'economy': 8.06, 'runs': 36}),
        ('Avesh Khan', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Avesh+Khan', {'matches': 47, 'wickets': 55, 'economy': 8.92, 'runs': 109}),
        ('Prasidh Krishna', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Prasidh+Krishna', {'matches': 17, 'wickets': 19, 'economy': 9.83, 'runs': 19}),
        ('T. Natarajan', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=T.+Natarajan', {'matches': 48, 'wickets': 56, 'economy': 8.62, 'runs': 38}),
        ('Anrich Nortje', 'South Africa', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Anrich+Nortje', {'matches': 40, 'wickets': 53, 'economy': 8.4, 'runs': 91}),
        ('Noor Ahmad', 'Afghanistan', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Noor+Ahmad', {'matches': 13, 'wickets': 14, 'economy': 7.5, 'runs': 15}),
        ('Rahul Chahar', 'India', 'BOWL', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Rahul+Chahar', {'matches': 69, 'wickets': 65, 'economy': 7.52, 'runs': 79}),
        ('Wanindu Hasaranga', 'Sri Lanka', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Wanindu+Hasaranga', {'matches': 26, 'wickets': 35, 'economy': 8.76, 'runs': 259}),
        ('Waqar Salamkheil', 'Afghanistan', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Waqar+Salamkheil', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Maheesh Theekshana', 'Sri Lanka', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Maheesh+Theekshana', {'matches': 27, 'wickets': 25, 'economy': 7.52, 'runs': 65}),
        ('Adam Zampa', 'Australia', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Adam+Zampa', {'matches': 20, 'wickets': 23, 'economy': 7.98, 'runs': 29}),
        ('Yash Dhull', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Yash+Dhull', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Abhinav Manohar', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abhinav+Manohar', {'matches': 8, 'runs': 108, 'avg': 18, 'wickets': 0}),
        ('Karun Nair', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Karun+Nair', {'matches': 76, 'runs': 1480, 'avg': 23.49, 'wickets': 0}),
        ('Angkrish Raghuvanshi', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Angkrish+Raghuvanshi', {'matches': 2, 'runs': 54, 'avg': 27, 'wickets': 0}),
        ('Anmolpreet Singh', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Anmolpreet+Singh', {'matches': 9, 'runs': 105, 'avg': 15, 'wickets': 0}),
        ('Atharva Taide', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Atharva+Taide', {'matches': 7, 'runs': 186, 'avg': 26.57, 'wickets': 0}),
        ('Nehal Wadhera', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Nehal+Wadhera', {'matches': 14, 'runs': 241, 'avg': 21.91, 'wickets': 0}),
        ('Harpreet Brar', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Harpreet+Brar', {'matches': 30, 'runs': 130, 'avg': 16.25, 'wickets': 20}),
        ('Naman Dhir', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Naman+Dhir', {'matches': 7, 'runs': 140, 'avg': 20, 'wickets': 0}),
        ('Mahipal Lomror', 'India', 'AR', 'Uncapped', 0.5, 'https://via.placeholder.com/200?text=Mahipal+Lomror', {'matches': 43, 'runs': 580, 'avg': 18.71, 'wickets': 1}),
        ('Sameer Rizvi', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Sameer+Rizvi', {'matches': 8, 'runs': 51, 'avg': 10.2, 'wickets': 0}),
        ('Abdul Samad', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abdul+Samad', {'matches': 34, 'runs': 391, 'avg': 21.72, 'wickets': 2}),
        ('Vijay Shankar', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vijay+Shankar', {'matches': 64, 'runs': 1034, 'avg': 22.98, 'wickets': 9}),
        ('Ashutosh Sharma', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ashutosh+Sharma', {'matches': 11, 'runs': 189, 'avg': 27, 'wickets': 0}),
        ('Nishant Sindhu', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Nishant+Sindhu', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Utkarsh Singh', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Utkarsh+Singh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Aryan Juyal', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Aryan+Juyal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Kumar Kushagra', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Kumar+Kushagra', {'matches': 5, 'runs': 3, 'avg': 3, 'wickets': 0}),
        ('Robin Minz', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Robin+Minz', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Anuj Rawat', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Anuj+Rawat', {'matches': 22, 'runs': 291, 'avg': 16.17, 'wickets': 0}),
        ('Luvnith Sisodia', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Luvnith+Sisodia', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Vishnu Vinod', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vishnu+Vinod', {'matches': 3, 'runs': 19, 'avg': 9.5, 'wickets': 0}),
        ('Upendra Singh Yadav', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Upendra+Singh+Yadav', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Vaibhav Arora', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vaibhav+Arora', {'matches': 19, 'wickets': 21, 'economy': 9.17, 'runs': 10}),
        ('Rasikh Dar', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Rasikh+Dar', {'matches': 5, 'wickets': 3, 'economy': 10.5, 'runs': 5}),
        ('Akash Madhwal', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Akash+Madhwal', {'matches': 13, 'wickets': 19, 'economy': 9.36, 'runs': 3}),
        ('Mohit Sharma', 'India', 'BOWL', 'Uncapped', 0.5, 'https://via.placeholder.com/200?text=Mohit+Sharma', {'matches': 100, 'wickets': 119, 'economy': 8.54, 'runs': 213}),
        ('Simarjeet Singh', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Simarjeet+Singh', {'matches': 10, 'wickets': 9, 'economy': 8.5, 'runs': 0}),
        ('Yash Thakur', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Yash+Thakur', {'matches': 9, 'wickets': 13, 'economy': 9.08, 'runs': 5}),
        ('Kartik Tyagi', 'India', 'BOWL', 'Uncapped', 0.4, 'https://via.placeholder.com/200?text=Kartik+Tyagi', {'matches': 19, 'wickets': 13, 'economy': 9.9, 'runs': 5}),
        ('Vyshak Vijaykumar', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vyshak+Vijaykumar', {'matches': 7, 'wickets': 9, 'economy': 10.5, 'runs': 1}),
        ('Piyush Chawla', 'India', 'BOWL', 'Uncapped', 0.5, 'https://via.placeholder.com/200?text=Piyush+Chawla', {'matches': 181, 'wickets': 179, 'economy': 7.91, 'runs': 311}),
        ('Shreyas Gopal', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shreyas+Gopal', {'matches': 49, 'wickets': 49, 'economy': 8.11, 'runs': 103}),
        ('Mayank Markande', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mayank+Markande', {'matches': 33, 'wickets': 37, 'economy': 8.4, 'runs': 31}),
        ('Suyash Sharma', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Suyash+Sharma', {'matches': 11, 'wickets': 10, 'economy': 8.23, 'runs': 0}),
        ('Yudhvir Charak', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Yudhvir+Charak', {'matches': 3, 'runs': 23, 'avg': 23, 'wickets': 3}),
        ('Rishi Dhawan', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Rishi+Dhawan', {'matches': 32, 'runs': 190, 'avg': 15.83, 'wickets': 24}),
        ('Rajvardhan Hangargekar', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Rajvardhan+Hangargekar', {'matches': 2, 'runs': 15, 'avg': 15, 'wickets': 3}),
        ('Tanush Kotian', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Tanush+Kotian', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Arshin Kulkarni', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Arshin+Kulkarni', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Shams Mulani', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shams+Mulani', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Shivam Singh', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shivam+Singh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Lalit Yadav', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Lalit+Yadav', {'matches': 25, 'runs': 229, 'avg': 19.08, 'wickets': 10}),
        ('Mohammed Azharuddeen', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mohammed+Azharuddeen', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('L.R Chethan', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=L.R+Chethan', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Aryaman Singh Dhaliwal', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Aryaman+Singh+Dhaliwal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Urvil Patel', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Urvil+Patel', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Sanskar Rawat', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Sanskar+Rawat', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Bipin Saurabh', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Bipin+Saurabh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Tanay Thyagarajann', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Tanay+Thyagarajann', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Money Grewal', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Money+Grewal', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Ashwani Kumar', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ashwani+Kumar', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Ishan Porel', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ishan+Porel', {'matches': 1, 'wickets': 1, 'economy': 7, 'runs': 0}),
        ('Abhilash Shetty', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abhilash+Shetty', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Akash Singh', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Akash+Singh', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Gurjapneet Singh', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Gurjapneet+Singh', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Basil Thampi', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Basil+Thampi', {'matches': 24, 'wickets': 22, 'economy': 9.54, 'runs': 13}),
        ('Murugan Ashwin', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Murugan+Ashwin', {'matches': 44, 'wickets': 35, 'economy': 8.19, 'runs': 45}),
        ('Shreyas Chavan', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shreyas+Chavan', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Chintal Gandhi', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Chintal+Gandhi', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Raghav Goyal', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Raghav+Goyal', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Jagadeesha Suchith', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Jagadeesha+Suchith', {'matches': 22, 'wickets': 19, 'economy': 8.62, 'runs': 57}),
        ('Roshan Waghsare', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Roshan+Waghsare', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Bailapudi Yeswanth', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Bailapudi+Yeswanth', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Sediqullah Atal', 'Afghanistan', 'BAT', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Sediqullah+Atal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Matthew Breetzke', 'South Africa', 'BAT', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Matthew+Breetzke', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Mark Chapman', 'New Zealand', 'BAT', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Mark+Chapman', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Brandon King', 'West Indies', 'BAT', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Brandon+King', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Evin Lewis', 'West Indies', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Evin+Lewis', {'matches': 53, 'runs': 1515, 'avg': 32.23, 'wickets': 0}),
        ('Pathum Nissanka', 'Sri Lanka', 'BAT', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Pathum+Nissanka', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Bhanuka Rajapaksa', 'Sri Lanka', 'BAT', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Bhanuka+Rajapaksa', {'matches': 11, 'runs': 206, 'avg': 22.89, 'wickets': 0}),
        ('Steve Smith', 'Australia', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Steve+Smith', {'matches': 51, 'runs': 1311, 'avg': 34.5, 'wickets': 0}),
        ('Gus Atkinson', 'England', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Gus+Atkinson', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Tom Curran', 'England', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Tom+Curran', {'matches': 30, 'runs': 127, 'avg': 9.07, 'wickets': 31}),
        ('Krishnappa Gowtham', 'India', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Krishnappa+Gowtham', {'matches': 28, 'runs': 108, 'avg': 9.82, 'wickets': 13}),
        ('Mohammad Nabi', 'Afghanistan', 'AR', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Mohammad+Nabi', {'matches': 17, 'runs': 180, 'avg': 22.5, 'wickets': 13}),
        ('Gulbadin Naib', 'Afghanistan', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Gulbadin+Naib', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Sikandar Raza', 'Zimbabwe', 'AR', 'Capped', 1.25, 'https://via.placeholder.com/200?text=Sikandar+Raza', {'matches': 7, 'runs': 182, 'avg': 36.4, 'wickets': 3}),
        ('Mitchell Santner', 'New Zealand', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Mitchell+Santner', {'matches': 15, 'runs': 56, 'avg': 9.33, 'wickets': 13}),
        ('Jayant Yadav', 'India', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Jayant+Yadav', {'matches': 10, 'runs': 4, 'avg': 2, 'wickets': 8}),
        ('Johnson Charles', 'West Indies', 'WK', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Johnson+Charles', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Litton Das', 'Bangladesh', 'WK', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Litton+Das', {'matches': 1, 'runs': 10, 'avg': 10, 'wickets': 0}),
        ('Andre Fletcher', 'West Indies', 'WK', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Andre+Fletcher', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Tom Latham', 'New Zealand', 'WK', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Tom+Latham', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ollie Pope', 'England', 'WK', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Ollie+Pope', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Kyle Verreynne', 'South Africa', 'WK', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Kyle+Verreynne', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Fazalhaq Farooqi', 'Afghanistan', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Fazalhaq+Farooqi', {'matches': 3, 'wickets': 2, 'economy': 9.5, 'runs': 0}),
        ('Richard Gleeson', 'England', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Richard+Gleeson', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Matt Henry', 'New Zealand', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Matt+Henry', {'matches': 13, 'wickets': 15, 'economy': 9.38, 'runs': 21}),
        ('Alzarri Joseph', 'West Indies', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Alzarri+Joseph', {'matches': 19, 'wickets': 26, 'economy': 9.08, 'runs': 13}),
        ('Kwena Maphaka', 'South Africa', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Kwena+Maphaka', {'matches': 2, 'wickets': 1, 'economy': 15.75, 'runs': 0}),
        ('Kuldeep Sen', 'India', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Kuldeep+Sen', {'matches': 9, 'wickets': 14, 'economy': 8.8, 'runs': 0}),
        ('Reece Topley', 'England', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Reece+Topley', {'matches': 6, 'wickets': 4, 'economy': 9.2, 'runs': 1}),
        ('Lizaad Williams', 'South Africa', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Lizaad+Williams', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Luke Wood', 'England', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Luke+Wood', {'matches': 5, 'wickets': 8, 'economy': 8.38, 'runs': 0}),
        ('Sachin Dhas', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Sachin+Dhas', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Leus Du Plooy', 'England', 'BAT', 'Uncapped', 0.5, 'https://via.placeholder.com/200?text=Leus+Du+Plooy', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ashwin Hebbar', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ashwin+Hebbar', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Rohan Kunnummal', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Rohan+Kunnummal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ayush Pandey', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ayush+Pandey', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Akshat Raghuwanshi', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Akshat+Raghuwanshi', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Shoun Roger', 'India', 'BAT', 'Uncapped', 0.4, 'https://via.placeholder.com/200?text=Shoun+Roger', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Virat Singh', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Virat+Singh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Priyansh Arya', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Priyansh+Arya', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Manoj Bhandage', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Manoj+Bhandage', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Pravin Dubey', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Pravin+Dubey', {'matches': 3, 'runs': 7, 'avg': 7, 'wickets': 0}),
        ('Ajay Mandal', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ajay+Mandal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Prerak Mankad', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Prerak+Mankad', {'matches': 6, 'runs': 97, 'avg': 19.4, 'wickets': 0}),
        ('Vipraj Nigam', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vipraj+Nigam', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Vicky Ostwal', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vicky+Ostwal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Shivalik Sharma', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shivalik+Sharma', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Salil Arora', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Salil+Arora', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Dinesh Bana', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Dinesh+Bana', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ajitesh Guruswamy', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ajitesh+Guruswamy', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Abhinandan Singh', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abhinandan+Singh', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Cooper Connolly', 'Australia', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Cooper+Connolly', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Dushan Hemantha', 'Sri Lanka', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Dushan+Hemantha', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Jason Holder', 'West Indies', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Jason+Holder', {'matches': 38, 'runs': 247, 'avg': 16.47, 'wickets': 49}),
        ('Karim Janat', 'Afghanistan', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Karim+Janat', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Jimmy Neesham', 'New Zealand', 'AR', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Jimmy+Neesham', {'matches': 12, 'runs': 90, 'avg': 15, 'wickets': 8}),
        ('Daniel Sams', 'Australia', 'AR', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Daniel+Sams', {'matches': 16, 'runs': 38, 'avg': 5.43, 'wickets': 13}),
        ('William Sutherland', 'Australia', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=William+Sutherland', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Taskin Ahmed', 'Bangladesh', 'BOWL', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Taskin+Ahmed', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Ben Dwarshuis', 'Australia', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Ben+Dwarshuis', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Obed McCoy', 'West Indies', 'BOWL', 'Capped', 1.25, 'https://via.placeholder.com/200?text=Obed+McCoy', {'matches': 8, 'wickets': 11, 'economy': 8.18, 'runs': 0}),
        ('Riley Meredith', 'Australia', 'BOWL', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Riley+Meredith', {'matches': 18, 'wickets': 20, 'economy': 8.57, 'runs': 8}),
        ('Lance Morris', 'Australia', 'BOWL', 'Capped', 1.25, 'https://via.placeholder.com/200?text=Lance+Morris', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Olly Stone', 'England', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Olly+Stone', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Daniel Worrall', 'England', 'BOWL', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Daniel+Worrall', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Pyla Avinash', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Pyla+Avinash', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Kiran Chormale', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Kiran+Chormale', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ashish Dahariya', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ashish+Dahariya', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Tushar Raheja', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Tushar+Raheja', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Sarthak Ranjan', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Sarthak+Ranjan', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Abhijeet Tomar', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abhijeet+Tomar', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Krish Bhagat', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Krish+Bhagat', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Sohraab Dhaliwal', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Sohraab+Dhaliwal', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Harsh Dubey', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Harsh+Dubey', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ramakrishna Ghosh', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ramakrishna+Ghosh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Raj Limbani', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Raj+Limbani', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Ninad Rathva', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ninad+Rathva', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Vivrant Sharma', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vivrant+Sharma', {'matches': 3, 'runs': 69, 'avg': 34.5, 'wickets': 0}),
        ('Shiva Singh', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shiva+Singh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Sayed Irfan Aftab', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Sayed+Irfan+Aftab', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Anirudh Chowdhary', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Anirudh+Chowdhary', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Anshuman Hooda', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Anshuman+Hooda', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Siddharth Kaul', 'India', 'BOWL', 'Uncapped', 0.4, 'https://via.placeholder.com/200?text=Siddharth+Kaul', {'matches': 38, 'wickets': 42, 'economy': 8.56, 'runs': 19}),
        ('Prashant Sai Painkra', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Prashant+Sai+Painkra', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Venkata Satyanarayana Penmetsa', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Venkata+Satyanarayana+Penmetsa', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Yeddala Reddy', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Yeddala+Reddy', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Zak Foulkes', 'New Zealand', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Zak+Foulkes', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Chris Green', 'Australia', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Chris+Green', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Shakib Al Hasan', 'Bangladesh', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Shakib+Al+Hasan', {'matches': 71, 'runs': 1401, 'avg': 23.35, 'wickets': 140}),
        ('Mehidy Hasan Miraz', 'Bangladesh', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Mehidy+Hasan+Miraz', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Wiaan Mulder', 'South Africa', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Wiaan+Mulder', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Dwaine Pretorius', 'South Africa', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Dwaine+Pretorius', {'matches': 1, 'runs': 0, 'avg': 0, 'wickets': 1}),
        ('Dasun Shanaka', 'Sri Lanka', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Dasun+Shanaka', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Shoriful Islam', 'Bangladesh', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Shoriful+Islam', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Blessing Muzarabani', 'Zimbabwe', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Blessing+Muzarabani', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Matthew Potts', 'England', 'BOWL', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Matthew+Potts', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Tanzim Hasan Sakib', 'Bangladesh', 'BOWL', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Tanzim+Hasan+Sakib', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Benjamin Sears', 'New Zealand', 'BOWL', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Benjamin+Sears', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Tim Southee', 'New Zealand', 'BOWL', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Tim+Southee', {'matches': 44, 'wickets': 43, 'economy': 8.4, 'runs': 64}),
        ('John Turner', 'England', 'BOWL', 'Capped', 1.5, 'https://via.placeholder.com/200?text=John+Turner', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Joshua Brown', 'Australia', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Joshua+Brown', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Oliver Davies', 'Australia', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Oliver+Davies', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Bevan John Jacobs', 'New Zealand', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Bevan+John+Jacobs', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Atharva Kale', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Atharva+Kale', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Abhishek Nair', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abhishek+Nair', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Vishwanath Pratap Singh', 'India', 'BAT', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vishwanath+Pratap+Singh', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Nasir Lone', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Nasir+Lone', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Brandon McMullen', 'Scotland', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Brandon+McMullen', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('S. Midhun', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=S.+Midhun', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Abid Mushtaq', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abid+Mushtaq', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Mahesh Pithiya', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mahesh+Pithiya', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Maramreddy Reddy', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Maramreddy+Reddy', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Atit Sheth', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Atit+Sheth', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Jonty Sidhu', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Jonty+Sidhu', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Mohit Avasthi', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mohit+Avasthi', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Faridoon Dawoodzai', 'Afghanistan', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Faridoon+Dawoodzai', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Praful Hinge', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Praful+Hinge', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Pankaj Jaswal', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Pankaj+Jaswal', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Vijay Kumar', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Vijay+Kumar', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Ashok Sharma', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ashok+Sharma', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Mujtaba Yousuf', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mujtaba+Yousuf', {'matches': 0, 'wickets': 0, 'economy': 0, 'runs': 0}),
        ('Ashton Agar', 'Australia', 'AR', 'Capped', 1.25, 'https://via.placeholder.com/200?text=Ashton+Agar', {'matches': 5, 'runs': 22, 'avg': 7.33, 'wickets': 4}),
        ('Roston Chase', 'West Indies', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Roston+Chase', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Junior Dala', 'South Africa', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Junior+Dala', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Mahedi Hasan', 'Bangladesh', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Mahedi+Hasan', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Nangeyalia Kharote', 'Afghanistan', 'AR', 'Capped', 0.75, 'https://via.placeholder.com/200?text=Nangeyalia+Kharote', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Dan Lawrence', 'England', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Dan+Lawrence', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('Nathan Smith', 'New Zealand', 'AR', 'Capped', 1.0, 'https://via.placeholder.com/200?text=Nathan+Smith', {'matches': 0, 'runs': 0, 'avg': 0, 'wickets': 0}),
        ('James Anderson', 'England', 'BOWL', 'Capped', 1.25, 'https://via.placeholder.com/200?text=James+Anderson', {'matches': 1, 'wickets': 0, 'economy': 6.0, 'runs': 0}),
        ('Kyle Jamieson', 'New Zealand', 'BOWL', 'Capped', 1.5, 'https://via.placeholder.com/200?text=Kyle+Jamieson', {'matches': 9, 'wickets': 11, 'economy': 8.0, 'runs': 12}),
        ('Ruturaj Gaikwad', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Ruturaj+Gaikwad', {'matches': 52, 'runs': 1797, 'avg': 39.93, 'wickets': 0}),
        ('Matheesha Pathirana', 'Sri Lanka', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Matheesha+Pathirana', {'matches': 18, 'wickets': 32, 'economy': 7.88, 'runs': 1}),
        ('Shivam Dube', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Shivam+Dube', {'matches': 42, 'runs': 1002, 'avg': 28.63, 'wickets': 4}),
        ('Ravindra Jadeja', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Ravindra+Jadeja', {'matches': 226, 'runs': 2693, 'avg': 29.27, 'wickets': 152}),
        ('MS Dhoni', 'India', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=MS+Dhoni', {'matches': 250, 'runs': 5082, 'avg': 38.79, 'wickets': 0}),
        ('Axar Patel', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Axar+Patel', {'matches': 87, 'runs': 944, 'avg': 18.88, 'wickets': 84}),
        ('Kuldeep Yadav', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Kuldeep+Yadav', {'matches': 78, 'wickets': 102, 'economy': 8.27, 'runs': 87}),
        ('Tristan Stubbs', 'South Africa', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Tristan+Stubbs', {'matches': 6, 'runs': 71, 'avg': 14.2, 'wickets': 0}),
        ('Abhishek Porel', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Abhishek+Porel', {'matches': 5, 'runs': 86, 'avg': 28.67, 'wickets': 0}),
        ('Rashid Khan', 'Afghanistan', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rashid+Khan', {'matches': 109, 'wickets': 139, 'economy': 6.69, 'runs': 421}),
        ('Shubman Gill', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Shubman+Gill', {'matches': 36, 'runs': 1376, 'avg': 42.99, 'wickets': 0}),
        ('Sai Sudharsan', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Sai+Sudharsan', {'matches': 19, 'runs': 661, 'avg': 41.31, 'wickets': 0}),
        ('Rahul Tewatia', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rahul+Tewatia', {'matches': 60, 'runs': 730, 'avg': 20.28, 'wickets': 32}),
        ('Shahrukh Khan', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shahrukh+Khan', {'matches': 12, 'runs': 132, 'avg': 16.5, 'wickets': 0}),
        ('Rinku Singh', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rinku+Singh', {'matches': 23, 'runs': 474, 'avg': 59.25, 'wickets': 0}),
        ('Varun Chakaravarthy', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Varun+Chakaravarthy', {'matches': 47, 'wickets': 49, 'economy': 7.3, 'runs': 19}),
        ('Sunil Narine', 'West Indies', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Sunil+Narine', {'matches': 177, 'runs': 1029, 'avg': 16.33, 'wickets': 183}),
        ('Andre Russell', 'West Indies', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Andre+Russell', {'matches': 112, 'runs': 2262, 'avg': 29.12, 'wickets': 99}),
        ('Harshit Rana', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Harshit+Rana', {'matches': 7, 'wickets': 11, 'economy': 9.09, 'runs': 0}),
        ('Ramandeep Singh', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ramandeep+Singh', {'matches': 7, 'runs': 125, 'avg': 41.67, 'wickets': 0}),
        ('Nicholas Pooran', 'West Indies', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Nicholas+Pooran', {'matches': 62, 'runs': 1465, 'avg': 36.62, 'wickets': 0}),
        ('Ravi Bishnoi', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Ravi+Bishnoi', {'matches': 50, 'wickets': 53, 'economy': 7.75, 'runs': 43}),
        ('Mayank Yadav', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mayank+Yadav', {'matches': 4, 'wickets': 7, 'economy': 6.99, 'runs': 0}),
        ('Mohsin Khan', 'India', 'BOWL', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Mohsin+Khan', {'matches': 25, 'wickets': 24, 'economy': 9.44, 'runs': 8}),
        ('Ayush Badoni', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Ayush+Badoni', {'matches': 24, 'runs': 437, 'avg': 29.13, 'wickets': 0}),
        ('Jasprit Bumrah', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Jasprit+Bumrah', {'matches': 133, 'wickets': 165, 'economy': 7.39, 'runs': 83}),
        ('Suryakumar Yadav', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Suryakumar+Yadav', {'matches': 139, 'runs': 3597, 'avg': 32.4, 'wickets': 0}),
        ('Hardik Pandya', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Hardik+Pandya', {'matches': 123, 'runs': 2418, 'avg': 26.57, 'wickets': 53}),
        ('Rohit Sharma', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rohit+Sharma', {'matches': 257, 'runs': 6628, 'avg': 29.84, 'wickets': 15}),
        ('Tilak Varma', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Tilak+Varma', {'matches': 32, 'runs': 1005, 'avg': 37.22, 'wickets': 0}),
        ('Shashank Singh', 'India', 'AR', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Shashank+Singh', {'matches': 14, 'runs': 354, 'avg': 44.25, 'wickets': 0}),
        ('Prabhsimran Singh', 'India', 'WK', 'Uncapped', 0.3, 'https://via.placeholder.com/200?text=Prabhsimran+Singh', {'matches': 23, 'runs': 664, 'avg': 30.18, 'wickets': 0}),
        ('Sanju Samson', 'India', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Sanju+Samson', {'matches': 152, 'runs': 3876, 'avg': 29.81, 'wickets': 0}),
        ('Yashasvi Jaiswal', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Yashasvi+Jaiswal', {'matches': 37, 'runs': 1342, 'avg': 39.47, 'wickets': 0}),
        ('Riyan Parag', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Riyan+Parag', {'matches': 33, 'runs': 609, 'avg': 25.38, 'wickets': 3}),
        ('Dhruv Jurel', 'India', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Dhruv+Jurel', {'matches': 8, 'runs': 195, 'avg': 48.75, 'wickets': 0}),
        ('Shimron Hetmyer', 'West Indies', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Shimron+Hetmyer', {'matches': 59, 'runs': 1104, 'avg': 29.84, 'wickets': 0}),
        ('Sandeep Sharma', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Sandeep+Sharma', {'matches': 109, 'wickets': 106, 'economy': 7.81, 'runs': 34}),
        ('Virat Kohli', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Virat+Kohli', {'matches': 252, 'runs': 8004, 'avg': 38.67, 'wickets': 4}),
        ('Rajat Patidar', 'India', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Rajat+Patidar', {'matches': 20, 'runs': 799, 'avg': 47, 'wickets': 0}),
        ('Yash Dayal', 'India', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Yash+Dayal', {'matches': 17, 'wickets': 17, 'economy': 9.33, 'runs': 3}),
        ('Heinrich Klaasen', 'South Africa', 'WK', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Heinrich+Klaasen', {'matches': 28, 'runs': 1047, 'avg': 41.88, 'wickets': 0}),
        ('Pat Cummins', 'Australia', 'BOWL', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Pat+Cummins', {'matches': 42, 'wickets': 46, 'economy': 9.28, 'runs': 120}),
        ('Travis Head', 'Australia', 'BAT', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Travis+Head', {'matches': 15, 'runs': 567, 'avg': 43.62, 'wickets': 1}),
        ('Abhishek Sharma', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Abhishek+Sharma', {'matches': 31, 'runs': 484, 'avg': 17.93, 'wickets': 8}),
        ('Nitish Kumar Reddy', 'India', 'AR', 'Capped', 2.0, 'https://via.placeholder.com/200?text=Nitish+Kumar+Reddy', {'matches': 13, 'runs': 303, 'avg': 33.67, 'wickets': 3}),
    ]
    players = []
    for name, country, role, capped, base, photo, stats in data:
        bat = random.randint(70, 99) if role in ['BAT', 'WK'] else random.randint(40, 80)
        bowl = random.randint(70, 99) if role in ['BOWL', 'AR'] else random.randint(20, 50)
        field = random.randint(60, 95)
        players.append({
            'name': name,
            'country': country,
            'role': role,
            'base_price': base,
            'bat_skill': bat,
            'bowl_skill': bowl,
            'field_skill': field,
            'photo': photo,
            'stats': stats
        })
    random.shuffle(players)
    return players

players = load_players()

class Team:
    def __init__(self, name):
        self.name = name
        self.purse = 130.0
        self.squad = []
        self.overseas = 0
        self.points = 0
        self.nrr = 0.0
        self.role_needs = {'BAT': 6, 'AR': 4, 'WK': 2, 'BOWL': 6}
        self.tournament_stats = {'runs': 0, 'wickets': 0, 'matches': 0}

    def update_needs(self):
        roles = {'BAT': 0, 'AR': 0, 'BOWL': 0, 'WK': 0}
        for p in self.squad:
            roles[p['role']] += 1
        for r in self.role_needs:
            self.role_needs[r] = max(0, self.role_needs[r] - roles.get(r, 0))

    def interested_in(self, player):
        if self.role_needs.get(player['role'], 0) > 0 and len(self.squad) < 20:
            ov_ok = player['country'] == 'India' or self.overseas < 8
            value = (player['bat_skill'] + player['bowl_skill']) / 2
            if value > 60 and self.purse > player['base_price'] * 1.2:
                return ov_ok
        return False

    def can_buy(self, player, price):
        if self.purse < price or len(self.squad) >= 20:
            return False
        if player['country'] != 'India' and self.overseas >= 8:
            return False
        return True

    def buy(self, player, price):
        self.squad.append(player)
        self.purse -= price
        if player['country'] != 'India':
            self.overseas += 1
        self.update_needs()

    def update_tournament_stats(self, runs, wickets):
        self.tournament_stats['runs'] += runs
        self.tournament_stats['wickets'] += wickets
        self.tournament_stats['matches'] += 1

# AI teams
ai_teams = [Team(name) for name in ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'PBKS', 'RR', 'GT', 'LSG']]

# Session state
if 'phase' not in st.session_state:
    st.session_state.phase = 'team_select'
if 'user_team' not in st.session_state:
    st.session_state.user_team = None
if 'auction_index' not in st.session_state:
    st.session_state.auction_index = 0
if 'current_bid' not in st.session_state:
    st.session_state.current_bid = 0.0
if 'current_bidder' not in st.session_state:
    st.session_state.current_bidder = 'Auctioneer'
if 'trade_done' not in st.session_state:
    st.session_state.trade_done = 0
if 'match_index' not in st.session_state:
    st.session_state.match_index = 0
if 'innings' not in st.session_state:
    st.session_state.innings = None
if 'bid_time' not in st.session_state:
    st.session_state.bid_time = 0
if 'auction_results' not in st.session_state:
    st.session_state.auction_results = []
if 'ai_bid_done' not in st.session_state:
    st.session_state.ai_bid_done = False
# Part 2: Auction Phase (with active bidding from all teams, user can bid, pass, or let AI handle)

# Team selection
if st.session_state.phase == 'team_select':
    st.title("Choose Your IPL Team")
    team_options = ['CSK', 'MI', 'RCB', 'KKR', 'SRH', 'DC', 'PBKS', 'RR', 'GT', 'LSG']
    selected_team = st.selectbox("Select Team", team_options)
    if st.button("Start Auction"):
        st.session_state.user_team = Team(selected_team)
        st.session_state.phase = 'auction'
        st.rerun()

# Auction phase
if st.session_state.phase == 'auction':
    st.title("IPL Mega Auction")
    col_main, col_side = st.columns([3,1])
    with col_side:
        st.subheader("Auction Results")
        for result in st.session_state.auction_results:
            st.write(result)
        st.subheader("Other Teams")
        for team in ai_teams:
            with st.expander(team.name):
                st.write(f"Purse: {team.purse:.1f} Cr")
                squad_df = pd.DataFrame(team.squad)
                if not squad_df.empty:
                    st.dataframe(squad_df[['name', 'role']])
    with col_main:
        if st.session_state.auction_index < len(players):
            player = players[st.session_state.auction_index]
            st.markdown(f"<div class='auctioneer'>Auctioneer: Bidding starts for {player['name']} at {player['base_price']} Cr! Going once...</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.image(player['photo'], width=200)
            with col2:
                st.write(f"Name: {player['name']}")
                st.write(f"Country: {player['country']}")
                st.write(f"Role: {player['role']}")
                st.write(f"Base Price: {player['base_price']} Cr")
                st.write(f"Bat: {player['bat_skill']}, Bowl: {player['bowl_skill']}, Field: {player['field_skill']}")
                st.subheader("Stats")
                st.json(player['stats'])

            if st.session_state.current_bid == 0.0:
                st.session_state.current_bid = player['base_price']
                st.session_state.bid_time = time.time()
                st.session_state.ai_bid_done = False
            if 'user_passed' not in st.session_state:
                 st.session_state.user_passed = False
           

           # Display current bid status
st.write(f"Current Bid: {st.session_state.current_bid:.1f} Cr by {st.session_state.current_bidder}")

# AI bidding simulation (unchanged)
if not st.session_state.ai_bid_done:
    if st.session_state.auction_index < len(players):
    player = players[st.session_state.auction_index]
    # ... display player info ...

    # AI bidding — put the line here
    bidding_teams = [t for t in ai_teams 
                     if t.interested_in(player) 
                     and t.can_buy(player, st.session_state.current_bid + 0.1)]
    if bidding_teams:
        bidding_team = random.choice(bidding_teams)
        max_bid = min(st.session_state.current_bid + random.uniform(0.1, 1.0), player['base_price'] * random.uniform(1.1, 3.0))
        max_bid = min(max_bid, bidding_team.purse * 0.15)
        if max_bid > st.session_state.current_bid:
            inc = random.uniform(0.1, min(1.0, max_bid - st.session_state.current_bid))
            st.session_state.current_bid += inc
            st.session_state.current_bid = round(st.session_state.current_bid, 1)
            st.session_state.current_bidder = bidding_team.name
            st.write(f"{bidding_team.name} bids {st.session_state.current_bid:.1f} Cr!")
            st.session_state.bid_time = time.time()
            st.rerun()
    else:
        st.session_state.ai_bid_done = True

# User bidding options only if not passed
if not st.session_state.user_passed:
    col_bid1, col_bid2, col_pass = st.columns(3)
    with col_bid1:
        if st.button(f"Bid {st.session_state.current_bid + 0.1:.1f} Cr") and st.session_state.user_team.can_buy(player, st.session_state.current_bid + 0.1):
            st.session_state.current_bid += 0.1
            st.session_state.current_bidder = st.session_state.user_team.name
            st.session_state.ai_bid_done = False  # Reset for AI to respond
            st.rerun()
    with col_bid2:
        if st.button(f"Bid {st.session_state.current_bid + 0.5:.1f} Cr") and st.session_state.user_team.can_buy(player, st.session_state.current_bid + 0.5):
            st.session_state.current_bid += 0.5
            st.session_state.current_bidder = st.session_state.user_team.name
            st.session_state.ai_bid_done = False
            st.rerun()
    with col_pass:
        if st.button("Pass"):
            # Pass logic: User opts out, but AI can continue bidding
            st.session_state.user_passed = True
            st.write(f"{st.session_state.user_team.name} has passed on {player['name']}. AI teams may continue bidding.")
            st.session_state.ai_bid_done = False  # Allow AI to bid if interested
            st.rerun()
else:
    st.write("You have passed on this player. Waiting for AI bids or auction end.")

# Timer for auction end (unchanged)
if time.time() - st.session_state.bid_time > 5 and st.session_state.ai_bid_done:  # 5 seconds no bid
    if st.session_state.current_bidder != 'Auctioneer':
        winner = next((t for t in ai_teams + [st.session_state.user_team] if t.name == st.session_state.current_bidder), None)
        if winner:
            winner.buy(player, st.session_state.current_bid)
            result = f"{player['name']} sold to {winner.name} for {st.session_state.current_bid:.1f} Cr!"
            st.session_state.auction_results.append(result)
            st.write(result)
    else:
        st.write(f"{player['name']} unsold!")
        st.session_state.auction_results.append(f"{player['name']} unsold.")
    st.session_state.auction_index += 1
    st.session_state.current_bid = 0.0
    st.session_state.current_bidder = 'Auctioneer'
    st.session_state.ai_bid_done = False
    st.session_state.user_passed = False  # Reset for next player
    st.rerun()
# Timer for auction end (unchanged, but ensure it checks if no bids)
if time.time() - st.session_state.bid_time > 5 and st.session_state.ai_bid_done:  # 5 seconds no bid
    if st.session_state.current_bidder != 'Auctioneer':
        winner = next((t for t in ai_teams + [st.session_state.user_team] if t.name == st.session_state.current_bidder), None)
        if winner:
            winner.buy(player, st.session_state.current_bid)
            result = f"{player['name']} sold to {winner.name} for {st.session_state.current_bid:.1f} Cr!"
            st.session_state.auction_results.append(result)
            st.write(result)
    else:
        st.write(f"{player['name']} unsold!")
    st.session_state.auction_index += 1
    st.session_state.current_bid = 0.0
    st.session_state.current_bidder = 'Auctioneer'
    st.session_state.ai_bid_done = False
    st.rerun()
else:
     st.success("Auction Complete! Proceed to Trades.")
     if st.button("Start Trades"):
         st.session_state.phase = 'trade'
     st.rerun()
     
# Part 3: Trade Phase, Season Phase, Match Simulator (with Impact Player and DLS Rain), Sidebar

# Trade phase
if st.session_state.phase == 'trade':
    st.title("Trade Phase")
    if st.session_state.trade_done < 3:  # Allow up to 3 trades
        st.write("Propose a trade with an AI team.")
        trade_team = st.selectbox("Select Team to Trade With", [t.name for t in ai_teams])
        your_player = st.selectbox("Your Player to Trade", [p['name'] for p in st.session_state.user_team.squad])
        their_player = st.selectbox("Their Player to Get", [p['name'] for p in next(t for t in ai_teams if t.name == trade_team).squad if p['role'] == next(p for p in st.session_state.user_team.squad if p['name'] == your_player)['role']])  # Same role
        if st.button("Propose Trade"):
            ai_team = next(t for t in ai_teams if t.name == trade_team)
            your_p = next(p for p in st.session_state.user_team.squad if p['name'] == your_player)
            their_p = next(p for p in ai_team.squad if p['name'] == their_player)
            if random.random() < 0.5:  # 50% chance AI accepts
                # Swap players
                st.session_state.user_team.squad.remove(your_p)
                ai_team.squad.remove(their_p)
                st.session_state.user_team.squad.append(their_p)
                ai_team.squad.append(your_p)
                # Adjust overseas if necessary
                if your_p['country'] != 'India' and their_p['country'] == 'India':
                    st.session_state.user_team.overseas -= 1
                    ai_team.overseas += 1
                elif your_p['country'] == 'India' and their_p['country'] != 'India':
                    st.session_state.user_team.overseas += 1
                    ai_team.overseas -= 1
                st.write("Trade Accepted!")
            else:
                st.write("Trade Rejected!")
            st.session_state.trade_done += 1
            st.rerun()
    else:
        st.success("Trades Complete! Proceed to Season.")
        if st.button("Start Season"):
            st.session_state.phase = 'season'
            st.rerun()

# Season and Match phase
if st.session_state.phase == 'season':
    st.title("IPL Season")
    opponents = ai_teams.copy()
    random.shuffle(opponents)
    if st.session_state.match_index < len(opponents):
        opp = opponents[st.session_state.match_index]
        st.write(f"Match vs {opp.name}")
        if st.button("Start Match"):
            st.session_state.innings = {'score': 0, 'wickets': 0, 'overs': 0.0, 'target': 0, 'bat_team': st.session_state.user_team, 'bowl_team': opp, 'ball_index': 0, 'rain': False, 'impact_sub': False}
            st.rerun()
    else:
        st.success("Season Complete! Calculate standings.")
        all_teams = ai_teams + [st.session_state.user_team]
        standings = sorted(all_teams, key=lambda t: (-t.points, -t.nrr))
        st.write("Standings:")
        for t in standings:
            st.write(f"{t.name}: {t.points} pts, NRR {t.nrr:.2f}")
        if st.session_state.user_team in standings[:4]:
            st.write("You made playoffs!")

# Ball-by-ball match sim with impact player
if 'innings' in st.session_state and st.session_state.innings:
    innings = st.session_state.innings
    if innings['ball_index'] < 120 and innings['wickets'] < 10:
        if innings['bat_team'] == st.session_state.user_team:
            style = st.selectbox("Batting Style", ['Defensive', 'Normal', 'Aggressive'])
            wicket_prob = 0.05 if style == 'Defensive' else 0.1 if style == 'Normal' else 0.15
        else:
            style = st.selectbox("Bowling Type", ['Pace', 'Spin', 'Swing'])
            wicket_prob = 0.12 if style == 'Swing' else 0.1 if style == 'Spin' else 0.08

        if innings['ball_index'] == 60 and not innings['impact_sub']:  # After 10 overs, allow impact sub
            st.write("Impact Player Substitution Available!")
            sub_options = [p['name'] for p in innings['bat_team'].squad if p['role'] == 'AR' or p['role'] == 'BOWL']  # Example: sub AR or Bowl
            sub_player = st.selectbox("Select Impact Player to Substitute In", sub_options)
            if st.button("Substitute Impact Player"):
                # Simulate sub: boost skills for simplicity
                innings['impact_sub'] = True
                wicket_prob -= 0.02  # Boost defense
                st.write(f"Impact Player {sub_player} substituted! Boost applied.")

        if st.button("Bowl/Bat Ball"):
            run = random.choice([0, 1, 2, 3, 4, 6])
            wicket = random.random() < wicket_prob
            if wicket:
                innings['wickets'] += 1
                st.write("Wicket!")
            else:
                innings['score'] += run
                st.write(f"Runs: {run}")
            innings['ball_index'] += 1
            innings['overs'] = innings['ball_index'] // 6 + (innings['ball_index'] % 6) / 10
            if random.random() < 0.05 and innings['ball_index'] > 60:
                innings['rain'] = True
                overs_left = 20 - innings['overs']
                wk_lost = innings['wickets']
                resource = dls_table[wk_lost][int(overs_left)]
                full = dls_table[0][20]
                if innings['target'] > 0:
                    innings['target'] = int(innings['target'] * (resource / full) + 1)
                    st.write(f"Rain! Target adjusted to {innings['target']}")
            st.write(f"Score: {innings['score']}/{innings['wickets']} in {innings['overs']:.1f} overs")
            innings['bat_team'].update_tournament_stats(run if not wicket else 0, 1 if wicket else 0)
            st.rerun()
    else:
        if innings['target'] == 0:
            innings['target'] = innings['score'] + 1
            st.session_state.innings = {'score': 0, 'wickets': 0, 'overs': 0.0, 'target': innings['target'], 'bat_team': innings['bowl_team'], 'bowl_team': innings['bat_team'], 'ball_index': 0, 'rain': False, 'impact_sub': False}
            st.write("Second Innings Start")
            st.rerun()
        else:
            user = st.session_state.user_team
            opp = innings['bowl_team'] if innings['bat_team'] == user else innings['bat_team']
            if innings['score'] > innings['target'] - 1:
                winner = innings['bat_team']
            elif innings['score'] < innings['target'] - 1:
                winner = innings['bowl_team']
            else:
                winner = None
            runs_scored = innings['score']
            overs_faced = innings['overs'] if innings['overs'] > 0 else 20
            runs_conceded = innings['target'] - 1
            overs_bowled = 20 if innings['wickets'] == 10 else innings['overs']
            nrr = (runs_scored / overs_faced) - (runs_conceded / overs_bowled) if winner else 0
            if winner == user:
                user.points += 2
                user.nrr += nrr
                opp.nrr -= nrr
            elif winner == opp:
                opp.points += 2
                opp.nrr += nrr
                user.nrr -= nrr
            else:
                user.points += 1
                opp.points += 1
            st.write(f"Match Result: {winner.name if winner else 'Tie'} wins!")
            st.session_state.match_index += 1
            st.session_state.innings = None
            st.rerun()

# Sidebar
st.sidebar.title("Your Team")
if st.session_state.user_team:
    squad_df = pd.DataFrame(st.session_state.user_team.squad)
    if not squad_df.empty:
        st.sidebar.dataframe(squad_df[['name', 'role']])
    st.sidebar.write(f"Purse: {st.session_state.user_team.purse:.2f} Cr")
    st.sidebar.write(f"Overseas: {st.session_state.user_team.overseas}/8")
    st.sidebar.write(f"Points: {st.session_state.user_team.points}, NRR: {st.session_state.user_team.nrr:.2f}")
    st.sidebar.subheader("Tournament Stats")
    st.sidebar.json(st.session_state.user_team.tournament_stats)










