import streamlit as st
import pickle as pkl
import pandas as pd

# --- Page config & basic theming ---
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Subtle gradient background */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a 0, #020617 40%, #000000 100%);
        color: #e5e7eb;
    }
    /* Card-like containers */
    .prediction-card {
        padding: 1.25rem 1.5rem;
        border-radius: 0.85rem;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.35);
    }
    .section-title {
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .ipl-logo {
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }
    .ipl-logo-text {
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Static team logo mapping ---
TEAM_LOGOS = {
    # Exact keys match team names inside team.pkl
    "Chennai Super Kings": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2b/Chennai_Super_Kings_Logo.svg/500px-Chennai_Super_Kings_Logo.svg.png",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Mumbai_Indians_Logo.svg/500px-Mumbai_Indians_Logo.svg.png",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Royal_Challengers_Bengaluru_Logo.svg/330px-Royal_Challengers_Bengaluru_Logo.svg.png",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/thumb/4/4c/Kolkata_Knight_Riders_Logo.svg/330px-Kolkata_Knight_Riders_Logo.svg.png",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/thumb/5/5c/This_is_the_logo_for_Rajasthan_Royals%2C_a_cricket_team_playing_in_the_Indian_Premier_League_%28IPL%29.svg/500px-This_is_the_logo_for_Rajasthan_Royals%2C_a_cricket_team_playing_in_the_Indian_Premier_League_%28IPL%29.svg.png",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/thumb/5/51/Sunrisers_Hyderabad_Logo.svg/500px-Sunrisers_Hyderabad_Logo.svg.png",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/Delhi_Capitals.svg/500px-Delhi_Capitals.svg.png",
    "Kings XI Punjab": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Punjab_Kings_Logo.svg/330px-Punjab_Kings_Logo.svg.png",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Gujarat_Titans_Logo.svg/500px-Gujarat_Titans_Logo.svg.png",
}

DEFAULT_TEAM_LOGO = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Cricket_logo.svg/120px-Cricket_logo.svg.png"


def get_team_logo(team_name: str) -> str:
    """Return logo for an exact team name, fallback to generic logo."""
    return TEAM_LOGOS.get(team_name, DEFAULT_TEAM_LOGO)


# --- Header with logo ---
header_col1, header_col2 = st.columns([1, 3])
with header_col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Indian_Premier_League_Official_Logo.svg/500px-Indian_Premier_League_Official_Logo.svg.png",
        width=90,
    )
with header_col2:
    st.markdown(
        """
        <div class="ipl-logo">
            <div>
                <div class="ipl-logo-text">IPL ANALYTICS DESK</div>
                <div style="opacity:0.8; font-size:0.9rem;">
                    Smart win probability insights for every chase.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### 🏏 IPL Win Predictor")
    st.markdown(
        "Use live match details to **instantly estimate** which team has the upper hand."
    )

with st.expander("ℹ️ How to use this app", expanded=False):
    st.markdown(
        """
        1. Select **batting team**, **bowling team** and **venue** from the sidebar.  
        2. Enter **target**, **current score**, **overs** and **wickets**.  
        3. Click **Predict Win Probability** and watch how the chances move ball-by-ball.
        """
    )

# Load resources
teams = pkl.load(open("team.pkl", "rb"))
cities = pkl.load(open("city.pkl", "rb"))
model = pkl.load(open("model.pkl", "rb"))

# --- Layout: sidebar for setup, main for situation & result ---
with st.sidebar:
    st.markdown("### 📝 Match Setup")
    batting_team = st.selectbox("🏏 Batting Team", sorted(teams))
    bowling_team = st.selectbox("🎯 Bowling Team", sorted(teams))
    selected_city = st.selectbox("📍 Match City", sorted(cities))

    batting_logo_url = get_team_logo(batting_team)
    bowling_logo_url = get_team_logo(bowling_team)

    st.markdown("---")
    logo_cols = st.columns(2)
    with logo_cols[0]:
        st.image(batting_logo_url, caption="Batting", width=70)
    with logo_cols[1]:
        st.image(bowling_logo_url, caption="Bowling", width=70)

    st.markdown("---")
    st.caption("Tip: Update values ball-by-ball to track win probability dynamically.")

st.markdown("### 🎯 Match Situation")

top_cols = st.columns(4)
with top_cols[0]:
    target = st.number_input(
        "Target Score", min_value=0, max_value=720, value=160, step=1
    )
with top_cols[1]:
    score = st.number_input(
        "Current Score", min_value=0, max_value=720, value=80, step=1
    )
with top_cols[2]:
    overs = st.number_input(
        "Overs Completed",
        min_value=0.0,
        max_value=20.0,
        value=10.0,
        step=0.1,
        format="%.1f",
    )
with top_cols[3]:
    wickets = st.number_input(
        "Wickets Lost", min_value=0, max_value=10, value=2, step=1
    )

st.markdown("")
predict_clicked = st.button("🚀 Predict Win Probability", use_container_width=True)

# --- Prediction & dynamic display ---
if predict_clicked:
    runs_left = target - score
    balls_left = 120 - int(overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
    rr_diff = crr - rrr if balls_left > 0 and overs > 0 else 0

    input_df = pd.DataFrame(
        {
            "batting_team": [batting_team],
            "bowling_team": [bowling_team],
            "city": [selected_city],
            "Score": [score],
            "Wickets": [wickets_left],
            "Remaining Balls": [balls_left],
            "target_left": [runs_left],
            "crr": [crr],
            "rrr": [rrr],
        }
    )

    result = model.predict_proba(input_df)
    loss = float(result[0][0])
    win = float(result[0][1])

    # Stats & context
    st.markdown("### 📊 Match Snapshot")
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.metric("Target", f"{target}")
    with stat_cols[1]:
        st.metric("Runs Left", f"{max(runs_left, 0)}")
    with stat_cols[2]:
        st.metric("Balls Left", f"{max(balls_left, 0)}")
    with stat_cols[3]:
        st.metric("Required RR", f"{rrr:.2f}" if balls_left > 0 else "—")

    extra_cols = st.columns(3)
    with extra_cols[0]:
        st.metric("Current RR", f"{crr:.2f}" if overs > 0 else "—")
    with extra_cols[1]:
        st.metric(
            "RR vs Required",
            f"{rr_diff:+.2f}" if overs > 0 and balls_left > 0 else "—",
        )
    with extra_cols[2]:
        st.metric("Wickets in Hand", f"{wickets_left}")

    st.markdown("")
    st.markdown("### 🏆 Win Probability")

    prob_cols = st.columns(2)
    with prob_cols[0]:
        st.image(batting_logo_url, width=70)
        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="section-title">Batting: {batting_team}</div>
                <h2 style="margin-top: 0.4rem; color:#4ade80;">
                    {round(win * 100)}%
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(win)

    with prob_cols[1]:
        st.image(bowling_logo_url, width=70)
        st.markdown(
            f"""
            <div class="prediction-card">
                <div class="section-title">Bowling: {bowling_team}</div>
                <h2 style="margin-top: 0.4rem; color:#f97373;">
                    {round(loss * 100)}%
                </h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(loss)

    # Short textual summary
    if win > 0.65:
        verdict = f"**{batting_team}** are in a **dominant position**."
    elif win < 0.35:
        verdict = f"**{bowling_team}** are well on top right now."
    else:
        verdict = "This is a **tight contest** – every ball matters!"

    st.markdown("")
    st.markdown(
        f"#### 🔍 Match Insight\n{verdict} Try changing the score, overs or wickets to see how the probability shifts live."
    )

else:
    st.info("Set the match details and click **Predict Win Probability** to see the chances.")
