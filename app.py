import streamlit as st
import pickle
import pandas as pd

pipe = pickle.load(open('pipe.pkl', 'rb'))

st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    h1 {
        text-align: center;
        color: #38bdf8;
    }
    .stButton>button {
        background-color: #38bdf8;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px;
        width: 100%;
    }
    .result-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e293b;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏏 IPL Win Predictor")
st.markdown("### Predict live match winning probability")

teams = [
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Daredevils'
]

cities = ['Mumbai', 'Kolkata', 'Delhi', 'Chennai', 'Bangalore', 'Hyderabad', 'Jaipur']

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("🏏 Batting Team", teams)
    city = st.selectbox("📍 City", cities)
    current_score = st.number_input("📊 Current Score", min_value=0)

with col2:
    bowling_team = st.selectbox("🎯 Bowling Team", teams)
    target = st.number_input("🎯 Target Score", min_value=0)
    wickets_left = st.number_input("❌ Wickets Left", min_value=0, max_value=10)

overs = st.slider("⏱ Overs Completed", 0.0, 20.0, step=0.1)

if st.button("🚀 Predict Win Probability"):

    balls_left = 120 - (overs * 6)
    runs_left = target - current_score

    crr = current_score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)

    loss = result[0][0]
    win = result[0][1]

    st.markdown("## 📈 Match Prediction")

    st.markdown(f"""
    <div class="result-box">
        <h3>🏆 Winning Chance: {round(win*100, 2)}%</h3>
        <h3>❌ Losing Chance: {round(loss*100, 2)}%</h3>
    </div>
    """, unsafe_allow_html=True)