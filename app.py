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

# DLS Resource Table (simplified, expand as needed)
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

# Full player data
@st.cache_data
def load_players():
    data = [
        ('Jos Buttler', 'England', 'WK', 'Capped', 2.0),
        ('Shreyas Iyer', 'India', 'BAT', 'Capped', 2.0),
        ('Rishabh Pant', 'India', 'BAT', 'Capped', 2.0),
        ('Kagiso Rabada', 'South Africa', 'BOWL', 'Capped', 2.0),
        ('Arshdeep Singh', 'India', 'BOWL', 'Capped', 2.0),
        ('Mitchell Starc', 'Australia', 'BOWL', 'Capped', 2.0),
        ('Yuzvendra Chahal', 'India', 'BOWL', 'Capped', 2.0),
        ('Liam Livingstone', 'England', 'AR', 'Capped', 2.0),
        ('David Miller', 'South Africa', 'BAT', 'Capped', 1.5),
        ('KL Rahul', 'India', 'WK', 'Capped', 2.0),
        ('Mohammad Shami', 'India', 'BOWL', 'Capped', 2.0),
        ('Mohammad Siraj', 'India', 'BOWL', 'Capped', 2.0),
        ('Harry Brook', 'England', 'BAT', 'Capped', 2.0),
        ('Devon Conway', 'New Zealand', 'BAT', 'Capped', 2.0),
        ('Jake Fraser-Mcgurk', 'Australia', 'BAT', 'Capped', 2.0),
        ('Aiden Markram', 'South Africa', 'BAT', 'Capped', 2.0),
        ('Devdutt Padikkal', 'India', 'BAT', 'Capped', 2.0),
        ('Rahul Tripathi', 'India', 'BAT', 'Capped', 0.75),
        ('David Warner', 'Australia', 'BAT', 'Capped', 2.0),
        ('Ravichandaran Ashwin', 'India', 'AR', 'Capped', 2.0),
        ('Venkatesh Iyer', 'India', 'AR', 'Capped', 2.0),
        ('Mitchell Marsh', 'Australia', 'AR', 'Capped', 2.0),
        ('Glenn Maxwell', 'Australia', 'AR', 'Capped', 2.0),
        ('Harshal Patel', 'India', 'AR', 'Capped', 2.0),
        ('Rachin Ravindra', 'New Zealand', 'AR', 'Capped', 1.5),
        ('Marcus Stoinis', 'Australia', 'AR', 'Capped', 2.0),
        ('Jonny Bairstow', 'England', 'WK', 'Capped', 2.0),
        ('Quinton De Kock', 'South Africa', 'WK', 'Capped', 2.0),
        ('Rahmanullah Gurbaz', 'Afghanistan', 'WK', 'Capped', 2.0),
        ('Ishan Kishan', 'India', 'WK', 'Capped', 2.0),
        ('Phil Salt', 'England', 'WK', 'Capped', 2.0),
        ('Jitesh Sharma', 'India', 'WK', 'Capped', 1.0),
        ('Syed Khaleel Ahmed', 'India', 'BOWL', 'Capped', 2.0),
        ('Trent Boult', 'New Zealand', 'BOWL', 'Capped', 2.0),
        ('Josh Hazlewood', 'Australia', 'BOWL', 'Capped', 2.0),
        ('Avesh Khan', 'India', 'BOWL', 'Capped', 2.0),
        ('Prasidh Krishna', 'India', 'BOWL', 'Capped', 2.0),
        ('T. Natarajan', 'India', 'BOWL', 'Capped', 2.0),
        ('Anrich Nortje', 'South Africa', 'BOWL', 'Capped', 2.0),
        ('Noor Ahmad', 'Afghanistan', 'BOWL', 'Capped', 2.0),
        ('Rahul Chahar', 'India', 'BOWL', 'Capped', 1.0),
        ('Wanindu Hasaranga', 'Sri Lanka', 'BOWL', 'Capped', 2.0),
        ('Waqar Salamkheil', 'Afghanistan', 'BOWL', 'Capped', 0.75),
        ('Maheesh Theekshana', 'Sri Lanka', 'BOWL', 'Capped', 2.0),
        ('Adam Zampa', 'Australia', 'BOWL', 'Capped', 2.0),
        ('Yash Dhull', 'India', 'BAT', 'Uncapped', 0.3),
        ('Abhinav Manohar', 'India', 'BAT', 'Uncapped', 0.3),
        ('Karun Nair', 'India', 'BAT', 'Uncapped', 0.3),
        ('Angkrish Raghuvanshi', 'India', 'BAT', 'Uncapped', 0.3),
        ('Anmolpreet Singh', 'India', 'BAT', 'Uncapped', 0.3),
        ('Atharva Taide', 'India', 'BAT', 'Uncapped', 0.3),
        ('Nehal Wadhera', 'India', 'BAT', 'Uncapped', 0.3),
        ('Harpreet Brar', 'India', 'AR', 'Uncapped', 0.3),
        ('Naman Dhir', 'India', 'AR', 'Uncapped', 0.3),
        ('Mahipal Lomror', 'India', 'AR', 'Uncapped', 0.5),
        ('Sameer Rizvi', 'India', 'AR', 'Uncapped', 0.3),
        ('Abdul Samad', 'India', 'AR', 'Uncapped', 0.3),
        ('Vijay Shankar', 'India', 'AR', 'Uncapped', 0.3),
        ('Ashutosh Sharma', 'India', 'AR', 'Uncapped', 0.3),
        ('Nishant Sindhu', 'India', 'AR', 'Uncapped', 0.3),
        ('Utkarsh Singh', 'India', 'AR', 'Uncapped', 0.3),
        ('Aryan Juyal', 'India', 'WK', 'Uncapped', 0.3),
        ('Kumar Kushagra', 'India', 'WK', 'Uncapped', 0.3),
        ('Robin Minz', 'India', 'WK', 'Uncapped', 0.3),
        ('Anuj Rawat', 'India', 'WK', 'Uncapped', 0.3),
        ('Luvnith Sisodia', 'India', 'WK', 'Uncapped', 0.3),
        ('Vishnu Vinod', 'India', 'WK', 'Uncapped', 0.3),
        ('Upendra Singh Yadav', 'India', 'WK', 'Uncapped', 0.3),
        ('Vaibhav Arora', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Rasikh Dar', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Akash Madhwal', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Mohit Sharma', 'India', 'BOWL', 'Uncapped', 0.5),
        ('Simarjeet Singh', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Yash Thakur', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Kartik Tyagi', 'India', 'BOWL', 'Uncapped', 0.4),
        ('Vyshak Vijaykumar', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Piyush Chawla', 'India', 'BOWL', 'Uncapped', 0.5),
        ('Shreyas Gopal', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Mayank Markande', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Suyash Sharma', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Yudhvir Charak', 'India', 'AR', 'Uncapped', 0.3),
        ('Rishi Dhawan', 'India', 'AR', 'Uncapped', 0.3),
        ('Rajvardhan Hangargekar', 'India', 'AR', 'Uncapped', 0.3),
        ('Tanush Kotian', 'India', 'AR', 'Uncapped', 0.3),
        ('Arshin Kulkarni', 'India', 'AR', 'Uncapped', 0.3),
        ('Shams Mulani', 'India', 'AR', 'Uncapped', 0.3),
        ('Shivam Singh', 'India', 'AR', 'Uncapped', 0.3),
        ('Lalit Yadav', 'India', 'AR', 'Uncapped', 0.3),
        ('Mohammed Azharuddeen', 'India', 'WK', 'Uncapped', 0.3),
        ('L.R Chethan', 'India', 'WK', 'Uncapped', 0.3),
        ('Aryaman Singh Dhaliwal', 'India', 'WK', 'Uncapped', 0.3),
        ('Urvil Patel', 'India', 'WK', 'Uncapped', 0.3),
        ('Sanskar Rawat', 'India', 'WK', 'Uncapped', 0.3),
        ('Bipin Saurabh', 'India', 'WK', 'Uncapped', 0.3),
        ('Tanay Thyagarajann', 'India', 'WK', 'Uncapped', 0.3),
        ('Money Grewal', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Ashwani Kumar', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Ishan Porel', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Abhilash Shetty', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Akash Singh', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Gurjapneet Singh', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Basil Thampi', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Murugan Ashwin', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Shreyas Chavan', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Chintal Gandhi', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Raghav Goyal', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Jagadeesha Suchith', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Roshan Waghsare', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Bailapudi Yeswanth', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Sediqullah Atal', 'Afghanistan', 'BAT', 'Capped', 0.75),
        ('Matthew Breetzke', 'South Africa', 'BAT', 'Capped', 0.75),
        ('Mark Chapman', 'New Zealand', 'BAT', 'Capped', 1.5),
        ('Brandon King', 'West Indies', 'BAT', 'Capped', 0.75),
        ('Evin Lewis', 'West Indies', 'BAT', 'Capped', 2.0),
        ('Pathum Nissanka', 'Sri Lanka', 'BAT', 'Capped', 0.75),
        ('Bhanuka Rajapaksa', 'Sri Lanka', 'BAT', 'Capped', 0.75),
        ('Steve Smith', 'Australia', 'BAT', 'Capped', 2.0),
        ('Gus Atkinson', 'England', 'AR', 'Capped', 2.0),
        ('Tom Curran', 'England', 'AR', 'Capped', 2.0),
        ('Krishnappa Gowtham', 'India', 'AR', 'Capped', 1.0),
        ('Mohammad Nabi', 'Afghanistan', 'AR', 'Capped', 1.5),
        ('Gulbadin Naib', 'Afghanistan', 'AR', 'Capped', 1.0),
        ('Sikandar Raza', 'Zimbabwe', 'AR', 'Capped', 1.25),
        ('Mitchell Santner', 'New Zealand', 'AR', 'Capped', 2.0),
        ('Jayant Yadav', 'India', 'AR', 'Capped', 0.75),
        ('Johnson Charles', 'West Indies', 'WK', 'Capped', 0.75),
        ('Litton Das', 'Bangladesh', 'WK', 'Capped', 0.75),
        ('Andre Fletcher', 'West Indies', 'WK', 'Capped', 0.75),
        ('Tom Latham', 'New Zealand', 'WK', 'Capped', 1.5),
        ('Ollie Pope', 'England', 'WK', 'Capped', 0.75),
        ('Kyle Verreynne', 'South Africa', 'WK', 'Capped', 0.75),
        ('Fazalhaq Farooqi', 'Afghanistan', 'BOWL', 'Capped', 2.0),
        ('Richard Gleeson', 'England', 'BOWL', 'Capped', 0.75),
        ('Matt Henry', 'New Zealand', 'BOWL', 'Capped', 2.0),
        ('Alzarri Joseph', 'West Indies', 'BOWL', 'Capped', 2.0),
        ('Kwena Maphaka', 'South Africa', 'BOWL', 'Capped', 0.75),
        ('Kuldeep Sen', 'India', 'BOWL', 'Capped', 0.75),
        ('Reece Topley', 'England', 'BOWL', 'Capped', 0.75),
        ('Lizaad Williams', 'South Africa', 'BOWL', 'Capped', 0.75),
        ('Luke Wood', 'England', 'BOWL', 'Capped', 0.75),
        ('Sachin Dhas', 'India', 'BAT', 'Uncapped', 0.3),
        ('Leus Du Plooy', 'England', 'BAT', 'Uncapped', 0.5),
        ('Ashwin Hebbar', 'India', 'BAT', 'Uncapped', 0.3),
        ('Rohan Kunnummal', 'India', 'BAT', 'Uncapped', 0.3),
        ('Ayush Pandey', 'India', 'BAT', 'Uncapped', 0.3),
        ('Akshat Raghuwanshi', 'India', 'BAT', 'Uncapped', 0.3),
        ('Shoun Roger', 'India', 'BAT', 'Uncapped', 0.4),
        ('Virat Singh', 'India', 'BAT', 'Uncapped', 0.3),
        ('Priyansh Arya', 'India', 'AR', 'Uncapped', 0.3),
        ('Manoj Bhandage', 'India', 'AR', 'Uncapped', 0.3),
        ('Pravin Dubey', 'India', 'AR', 'Uncapped', 0.3),
        ('Ajay Mandal', 'India', 'AR', 'Uncapped', 0.3),
        ('Prerak Mankad', 'India', 'AR', 'Uncapped', 0.3),
        ('Vipraj Nigam', 'India', 'AR', 'Uncapped', 0.3),
        ('Vicky Ostwal', 'India', 'AR', 'Uncapped', 0.3),
        ('Shivalik Sharma', 'India', 'AR', 'Uncapped', 0.3),
        ('Salil Arora', 'India', 'WK', 'Uncapped', 0.3),
        ('Dinesh Bana', 'India', 'WK', 'Uncapped', 0.3),
        ('Ajitesh Guruswamy', 'India', 'WK', 'Uncapped', 0.3),
        ('Abhinandan Singh', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Cooper Connolly', 'Australia', 'AR', 'Capped', 0.75),
        ('Dushan Hemantha', 'Sri Lanka', 'AR', 'Capped', 0.75),
        ('Jason Holder', 'West Indies', 'AR', 'Capped', 2.0),
        ('Karim Janat', 'Afghanistan', 'AR', 'Capped', 0.75),
        ('Jimmy Neesham', 'New Zealand', 'AR', 'Capped', 1.5),
        ('Daniel Sams', 'Australia', 'AR', 'Capped', 1.5),
        ('William Sutherland', 'Australia', 'AR', 'Capped', 0.75),
        ('Taskin Ahmed', 'Bangladesh', 'BOWL', 'Capped', 1.0),
        ('Ben Dwarshuis', 'Australia', 'BOWL', 'Capped', 0.75),
        ('Obed McCoy', 'West Indies', 'BOWL', 'Capped', 1.25),
        ('Riley Meredith', 'Australia', 'BOWL', 'Capped', 1.5),
        ('Lance Morris', 'Australia', 'BOWL', 'Capped', 1.25),
        ('Olly Stone', 'England', 'BOWL', 'Capped', 0.75),
        ('Daniel Worrall', 'England', 'BOWL', 'Capped', 1.5),
        ('Pyla Avinash', 'India', 'BAT', 'Uncapped', 0.3),
        ('Kiran Chormale', 'India', 'BAT', 'Uncapped', 0.3),
        ('Ashish Dahariya', 'India', 'BAT', 'Uncapped', 0.3),
        ('Tushar Raheja', 'India', 'BAT', 'Uncapped', 0.3),
        ('Sarthak Ranjan', 'India', 'BAT', 'Uncapped', 0.3),
        ('Abhijeet Tomar', 'India', 'BAT', 'Uncapped', 0.3),
        ('Krish Bhagat', 'India', 'AR', 'Uncapped', 0.3),
        ('Sohraab Dhaliwal', 'India', 'AR', 'Uncapped', 0.3),
        ('Harsh Dubey', 'India', 'AR', 'Uncapped', 0.3),
        ('Ramakrishna Ghosh', 'India', 'AR', 'Uncapped', 0.3),
        ('Raj Limbani', 'India', 'AR', 'Uncapped', 0.3),
        ('Ninad Rathva', 'India', 'AR', 'Uncapped', 0.3),
        ('Vivrant Sharma', 'India', 'AR', 'Uncapped', 0.3),
        ('Shiva Singh', 'India', 'AR', 'Uncapped', 0.3),
        ('Sayed Irfan Aftab', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Anirudh Chowdhary', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Anshuman Hooda', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Siddharth Kaul', 'India', 'BOWL', 'Uncapped', 0.4),
        ('Prashant Sai Painkra', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Venkata Satyanarayana Penmetsa', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Yeddala Reddy', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Zak Foulkes', 'New Zealand', 'AR', 'Capped', 0.75),
        ('Chris Green', 'Australia', 'AR', 'Capped', 1.0),
        ('Shakib Al Hasan', 'Bangladesh', 'AR', 'Capped', 1.0),
        ('Mehidy Hasan Miraz', 'Bangladesh', 'AR', 'Capped', 1.0),
        ('Wiaan Mulder', 'South Africa', 'AR', 'Capped', 0.75),
        ('Dwaine Pretorius', 'South Africa', 'AR', 'Capped', 0.75),
        ('Dasun Shanaka', 'Sri Lanka', 'AR', 'Capped', 0.75),
        ('Shoriful Islam', 'Bangladesh', 'BOWL', 'Capped', 0.75),
        ('Blessing Muzarabani', 'Zimbabwe', 'BOWL', 'Capped', 0.75),
        ('Matthew Potts', 'England', 'BOWL', 'Capped', 1.5),
        ('Tanzim Hasan Sakib', 'Bangladesh', 'BOWL', 'Capped', 0.75),
        ('Benjamin Sears', 'New Zealand', 'BOWL', 'Capped', 1.0),
        ('Tim Southee', 'New Zealand', 'BOWL', 'Capped', 1.5),
        ('John Turner', 'England', 'BOWL', 'Capped', 1.5),
        ('Joshua Brown', 'Australia', 'BAT', 'Uncapped', 0.3),
        ('Oliver Davies', 'Australia', 'BAT', 'Uncapped', 0.3),
        ('Bevan John Jacobs', 'New Zealand', 'BAT', 'Uncapped', 0.3),
        ('Atharva Kale', 'India', 'BAT', 'Uncapped', 0.3),
        ('Abhishek Nair', 'India', 'BAT', 'Uncapped', 0.3),
        ('Vishwanath Pratap Singh', 'India', 'BAT', 'Uncapped', 0.3),
        ('Nasir Lone', 'India', 'AR', 'Uncapped', 0.3),
        ('Brandon McMullen', 'Scotland', 'AR', 'Uncapped', 0.3),
        ('S. Midhun', 'India', 'AR', 'Uncapped', 0.3),
        ('Abid Mushtaq', 'India', 'AR', 'Uncapped', 0.3),
        ('Mahesh Pithiya', 'India', 'AR', 'Uncapped', 0.3),
        ('Maramreddy Reddy', 'India', 'AR', 'Uncapped', 0.3),
        ('Atit Sheth', 'India', 'AR', 'Uncapped', 0.3),
        ('Jonty Sidhu', 'India', 'AR', 'Uncapped', 0.3),
        ('Mohit Avasthi', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Faridoon Dawoodzai', 'Afghanistan', 'BOWL', 'Uncapped', 0.3),
        ('Praful Hinge', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Pankaj Jaswal', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Vijay Kumar', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Ashok Sharma', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Mujtaba Yousuf', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Ashton Agar', 'Australia', 'AR', 'Capped', 1.25),
        ('Roston Chase', 'West Indies', 'AR', 'Capped', 0.75),
        ('Junior Dala', 'South Africa', 'AR', 'Capped', 0.75),
        ('Mahedi Hasan', 'Bangladesh', 'AR', 'Capped', 0.75),
        ('Nangeyalia Kharote', 'Afghanistan', 'AR', 'Capped', 0.75),
        ('Dan Lawrence', 'England', 'AR', 'Capped', 1.0),
        ('Nathan Smith', 'New Zealand', 'AR', 'Capped', 1.0),
        ('James Anderson', 'England', 'BOWL', 'Capped', 1.25),
        ('Kyle Jamieson', 'New Zealand', 'BOWL', 'Capped', 1.5),
        # Retained players
        ('Ruturaj Gaikwad', 'India', 'BAT', 'Capped', 2.0),
        ('Matheesha Pathirana', 'Sri Lanka', 'BOWL', 'Capped', 2.0),
        ('Shivam Dube', 'India', 'AR', 'Capped', 2.0),
        ('Ravindra Jadeja', 'India', 'AR', 'Capped', 2.0),
        ('MS Dhoni', 'India', 'WK', 'Capped', 2.0),
        ('Axar Patel', 'India', 'AR', 'Capped', 2.0),
        ('Kuldeep Yadav', 'India', 'BOWL', 'Capped', 2.0),
        ('Tristan Stubbs', 'South Africa', 'BAT', 'Capped', 2.0),
        ('Abhishek Porel', 'India', 'WK', 'Uncapped', 0.3),
        ('Rashid Khan', 'Afghanistan', 'BOWL', 'Capped', 2.0),
        ('Shubman Gill', 'India', 'BAT', 'Capped', 2.0),
        ('Sai Sudharsan', 'India', 'BAT', 'Capped', 2.0),
        ('Rahul Tewatia', 'India', 'AR', 'Capped', 2.0),
        ('Shahrukh Khan', 'India', 'AR', 'Uncapped', 0.3),
        ('Rinku Singh', 'India', 'BAT', 'Capped', 2.0),
        ('Varun Chakaravarthy', 'India', 'BOWL', 'Capped', 2.0),
        ('Sunil Narine', 'West Indies', 'AR', 'Capped', 2.0),
        ('Andre Russell', 'West Indies', 'AR', 'Capped', 2.0),
        ('Harshit Rana', 'India', 'BOWL', 'Capped', 2.0),
        ('Ramandeep Singh', 'India', 'AR', 'Uncapped', 0.3),
        ('Nicholas Pooran', 'West Indies', 'WK', 'Capped', 2.0),
        ('Ravi Bishnoi', 'India', 'BOWL', 'Capped', 2.0),
        ('Mayank Yadav', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Mohsin Khan', 'India', 'BOWL', 'Uncapped', 0.3),
        ('Ayush Badoni', 'India', 'AR', 'Uncapped', 0.3),
        ('Jasprit Bumrah', 'India', 'BOWL', 'Capped', 2.0),
        ('Suryakumar Yadav', 'India', 'BAT', 'Capped', 2.0),
        ('Hardik Pandya', 'India', 'AR', 'Capped', 2.0),
        ('Rohit Sharma', 'India', 'BAT', 'Capped', 2.0),
        ('Tilak Varma', 'India', 'BAT', 'Capped', 2.0),
        ('Shashank Singh', 'India', 'AR', 'Uncapped', 0.3),
        ('Prabhsimran Singh', 'India', 'WK', 'Uncapped', 0.3),
        ('Sanju Samson', 'India', 'WK', 'Capped', 2.0),
        ('Yashasvi Jaiswal', 'India', 'BAT', 'Capped', 2.0),
        ('Riyan Parag', 'India', 'AR', 'Capped', 2.0),
        ('Dhruv Jurel', 'India', 'WK', 'Capped', 2.0),
        ('Shimron Hetmyer', 'West Indies', 'BAT', 'Capped', 2.0),
        ('Sandeep Sharma', 'India', 'BOWL', 'Capped', 2.0),
        ('Virat Kohli', 'India', 'BAT', 'Capped', 2.0),
        ('Rajat Patidar', 'India', 'BAT', 'Capped', 2.0),
        ('Yash Dayal', 'India', 'BOWL', 'Capped', 2.0),
        ('Heinrich Klaasen', 'South Africa', 'WK', 'Capped', 2.0),
        ('Pat Cummins', 'Australia', 'BOWL', 'Capped', 2.0),
        ('Travis Head', 'Australia', 'BAT', 'Capped', 2.0),
        ('Abhishek Sharma', 'India', 'AR', 'Capped', 2.0),
        ('Nitish Kumar Reddy', 'India', 'AR', 'Capped', 2.0),
    ]
    players = []
    for name, country, role, capped, base in data:
        is_capped = capped == 'Capped'
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
            'photo': f"https://via.placeholder.com/200x200?text={name.replace(' ', '+')}"  # Placeholder
        })
    random.shuffle(players)
    return players

players = load_players()

class Team:
    def __init__(self, name):
        self.name = name
        self.purse = 120.0
        self.squad = []
        self.overseas = 0
        self.points = 0
        self.nrr = 0.0
        self.role_needs = {'BAT': 6, 'AR': 4, 'WK': 2, 'BOWL': 6}

    def update_needs(self):
        roles = {'BAT': 0, 'AR': 0, 'BOWL': 0, 'WK': 0}
        for p in self.squad:
            roles[p['role']] += 1
        for r in self.role_needs:
            self.role_needs[r] = max(0, self.role_needs[r] - roles.get(r, 0))

    def interested_in(self, player):
        if self.role_needs.get(player['role'], 0) > 0 and len(self.squad) < 24:
            ov_ok = player['country'] == 'India' or self.overseas < 8
            value = (player['bat_skill'] + player['bowl_skill']) / 2
            if value > 60 and self.purse > player['base_price'] * 1.2:
                return ov_ok
        return False

    def can_buy(self, player, price):
        if self.purse < price or len(self.squad) >= 25:
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

        if st.session_state.current_bid == 0.0:
            st.session_state.current_bid = player['base_price']
            st.session_state.bid_time = time.time()

        # AI bidding simulation
        if 'ai_bid_done' not in st.session_state:
            st.session_state.ai_bid_done = False
        if not st.session_state.ai_bid_done:
            time.sleep(1)  # Simulate delay
            for team in ai_teams:
                if team.interested_in(player) and team.can_buy(player, st.session_state.current_bid + 0.1):
                    inc = random.uniform(0.1, 0.5) if st.session_state.current_bid < 10 else random.uniform(0.5, 1.0)
                    if st.session_state.current_bid + inc < team.purse * 0.5:  # Realistic cap
                        st.session_state.current_bid += inc
                        st.session_state.current_bid = round(st.session_state.current_bid, 1)
                        st.session_state.current_bidder = team.name
                        st.write(f"{team.name} bids {st.session_state.current_bid:.1f} Cr!")
                        st.session_state.bid_time = time.time()
                        break
            st.session_state.ai_bid_done = True
            st.rerun()

        st.write(f"Current Bid: {st.session_state.current_bid:.1f} Cr by {st.session_state.current_bidder}")

        col_bid1, col_bid2, col_bid3, col_pass = st.columns(4)
        with col_bid1:
            if st.button("+0.1 Cr", key="bid01"):
                new_bid = st.session_state.current_bid + 0.1
                if st.session_state.user_team.can_buy(player, new_bid):
                    st.session_state.current_bid = new_bid
                    st.session_state.current_bidder = st.session_state.user_team.name
                    st.session_state.ai_bid_done = False
                    st.session_state.bid_time = time.time()
                    st.rerun()
        with col_bid2:
            if st.button("+0.5 Cr", key="bid05"):
                new_bid = st.session_state.current_bid + 0.5
                if st.session_state.user_team.can_buy(player, new_bid):
                    st.session_state.current_bid = new_bid
                    st.session_state.current_bidder = st.session_state.user_team.name
                    st.session_state.ai_bid_done = False
                    st.session_state.bid_time = time.time()
                    st.rerun()
        with col_bid3:
            if st.button("+1 Cr", key="bid1"):
                new_bid = st.session_state.current_bid + 1.0
                if st.session_state.user_team.can_buy(player, new_bid):
                    st.session_state.current_bid = new_bid
                    st.session_state.current_bidder = st.session_state.user_team.name
                    st.session_state.ai_bid_done = False
                    st.session_state.bid_time = time.time()
                    st.rerun()
        with col_pass:
            if st.button("Pass", key="pass"):
                if st.session_state.current_bidder == st.session_state.user_team.name:
                    st.session_state.user_team.buy(player, st.session_state.current_bid)
                    st.success(f"You bought {player['name']} for {st.session_state.current_bid:.1f} Cr!")
                elif st.session_state.current_bidder != 'Auctioneer':
                    winner = next(t for t in ai_teams if t.name == st.session_state.current_bidder)
                    winner.buy(player, st.session_state.current_bid)
                    st.info(f"Sold to {winner.name} for {st.session_state.current_bid:.1f} Cr!")
                else:
                    st.info("Unsold!")
                st.session_state.auction_index += 1
                st.session_state.current_bid = 0.0
                st.session_state.current_bidder = 'Auctioneer'
                st.session_state.ai_bid_done = False
                st.session_state.bid_time = 0
                st.rerun()
        # Countdown for auto-sell
        if st.session_state.current_bidder != 'Auctioneer':
            elapsed = time.time() - st.session_state.bid_time
            if elapsed > 5:
                winner = st.session_state.user_team if st.session_state.current_bidder == st.session_state.user_team.name else next(t for t in ai_teams if t.name == st.session_state.current_bidder)
                winner.buy(player, st.session_state.current_bid)
                st.success(f"Sold to {winner.name} for {st.session_state.current_bid:.1f} Cr after countdown!")
                st.session_state.auction_index += 1
                st.session_state.current_bid = 0.0
                st.session_state.current_bidder = 'Auctioneer'
                st.session_state.ai_bid_done = False
                st.session_state.bid_time = 0
                st.rerun()
            else:
                remaining = 5 - int(elapsed)
                st.write(f"Going twice... Sold in {remaining} seconds!")
                time.sleep(1)
                st.rerun()
    else:
        st.success("Auction Complete!")
        if st.button("Proceed to Trades"):
            st.session_state.phase = 'trade'
            st.rerun()

# Trade phase
if st.session_state.phase == 'trade':
    st.title("Trade Phase (Up to 3 Trades)")
    if st.session_state.trade_done < 3:
        st.write("Your Squad:")
        user_squad = pd.DataFrame(st.session_state.user_team.squad)
        st.dataframe(user_squad[['name', 'role', 'bat_skill', 'bowl_skill', 'field_skill']])
        out_player = st.selectbox("Select player to trade out", user_squad['name'])

        ai_team_name = st.selectbox("Select AI team", [t.name for t in ai_teams])
        ai_team = next(t for t in ai_teams if t.name == ai_team_name)
        ai_squad = pd.DataFrame(ai_team.squad)
        st.write(f"{ai_team_name} Squad:")
        st.dataframe(ai_squad[['name', 'role', 'bat_skill', 'bowl_skill', 'field_skill']])
        in_player = st.selectbox("Select player to trade in", ai_squad['name'])

        if st.button("Propose Trade"):
            out_p = next(p for p in st.session_state.user_team.squad if p['name'] == out_player)
            in_p = next(p for p in ai_team.squad if p['name'] == in_player)
            # Simple value check
            out_val = out_p['bat_skill'] + out_p['bowl_skill']
            in_val = in_p['bat_skill'] + in_p['bowl_skill']
            if random.random() < 0.5 or out_val > in_val:  # 50% chance or better deal
                st.session_state.user_team.squad.remove(out_p)
                ai_team.squad.remove(in_p)
                st.session_state.user_team.squad.append(in_p)
                ai_team.squad.append(out_p)
                st.session_state.user_team.update_needs()
                ai_team.update_needs()
                st.success("Trade Accepted!")
                st.session_state.trade_done += 1
            else:
                st.error("Trade Rejected!")
            st.rerun()
    else:
        st.success("Trades Complete!")
        if st.button("Proceed to Season"):
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
            st.session_state.innings = {'score': 0, 'wickets': 0, 'overs': 0.0, 'target': 0, 'bat_team': st.session_state.user_team, 'bowl_team': opp, 'ball_index': 0, 'rain': False}
            st.rerun()
    else:
        st.success("Season Complete! Calculate standings.")
        # Simple standings
        all_teams = ai_teams + [st.session_state.user_team]
        standings = sorted(all_teams, key=lambda t: -t.points)
        st.write("Standings:")
        for t in standings:
            st.write(f"{t.name}: {t.points} pts, NRR {t.nrr:.2f}")
        if st.session_state.user_team in standings[:4]:
            st.write("You made playoffs!")

# Ball-by-ball match sim
if 'innings' in st.session_state and st.session_state.innings:
    innings = st.session_state.innings
    if innings['ball_index'] < 120 and innings['wickets'] < 10:
        # User choice for bat or bowl
        if innings['bat_team'] == st.session_state.user_team:
            style = st.selectbox("Batting Style", ['Defensive', 'Normal', 'Aggressive'])
            bat_eff = 1.0 if style == 'Normal' else 0.8 if style == 'Defensive' else 1.2
            wicket_prob = 0.05 if style == 'Defensive' else 0.1 if style == 'Normal' else 0.15
        else:
            style = st.selectbox("Bowling Type", ['Pace', 'Spin', 'Swing'])
            bowl_eff = 1.0  # Simplify
            wicket_prob = 0.12 if style == 'Swing' else 0.1 if style == 'Spin' else 0.08

        if st.button("Bowl/Bat Ball"):
            # Sim ball
            run = random.choice([0, 1, 2, 3, 4, 6])
            if random.random() < wicket_prob:
                innings['wickets'] += 1
                st.write("Wicket!")
            else:
                innings['score'] += run
                st.write(f"Runs: {run}")
            innings['ball_index'] += 1
            innings['overs'] = innings['ball_index'] / 6
            # Rain check
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
            st.rerun()
    else:
        if innings['target'] == 0:
            innings['target'] = innings['score'] + 1
            st.session_state.innings = {'score': 0, 'wickets': 0, 'overs': 0.0, 'target': innings['target'], 'bat_team': innings['bowl_team'], 'bowl_team': innings['bat_team'], 'ball_index': 0, 'rain': False}
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
            nrr = (innings['score'] / innings['overs'] - (innings['target'] - 1) / 20) if winner else 0
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
if st.session_state.user_team and st.session_state.user_team.squad:
    squad_df = pd.DataFrame(st.session_state.user_team.squad)
    st.sidebar.dataframe(squad_df[['name', 'role']])
    st.sidebar.write(f"Purse: {st.session_state.user_team.purse:.2f} Cr")
    st.sidebar.write(f"Overseas: {st.session_state.user_team.overseas}/8")
    st.sidebar.write(f"Points: {st.session_state.user_team.points}, NRR: {st.session_state.user_team.nrr:.2f}")
