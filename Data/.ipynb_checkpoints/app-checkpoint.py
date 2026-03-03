import streamlit as st
import pickle as pkl
import pandas as pd

# Wide layout
st.set_page_config(layout="wide")

# Title and Subheader
st.title("🏏 IPL Win Predictor")
st.markdown("Predict the winning probability of your favorite IPL team in real time.")

# Load resources
teams = pkl.load(open('team.pkl', "rb"))
cities = pkl.load(open('city.pkl', 'rb'))
model = pkl.load(open('model.pkl', 'rb'))

# --- Inputs ---
st.subheader("📝 Match Setup")
col1, col2, col3 = st.columns(3)
with col1:
    batting_team = st.selectbox('🏏 Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('🎯 Bowling Team', sorted(teams))
with col3:
    selected_city = st.selectbox('📍 Match City', sorted(cities))

st.subheader("🎯 Match Situation")
target = st.number_input('🎯 Target Score', min_value=0, max_value=720, step=1)

col4, col5, col6 = st.columns(3)
with col4:
    score = st.number_input('💯 Current Score', min_value=0, max_value=720, step=1)
with col5:
    overs = st.number_input('⏱ Overs Completed', min_value=0.0, max_value=20.0, step=0.1, format="%.1f")
with col6:
    wickets = st.number_input('❌ Wickets Lost', min_value=0, max_value=10, step=1)

# --- Prediction ---
if st.button('🚀 Predict Win Probability'):
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'Score': [score],
        'Wickets': [wickets_left],
        'Remaining Balls': [balls_left],
        'target_left': [runs_left],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = model.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    # --- Results Display ---
    st.subheader("📊 Win Probability")
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"🏆 {batting_team}: **{round(win*100)}%** chance to win")
    with col2:
        st.error(f"🎯 {bowling_team}: **{round(loss*100)}%** chance to win")
