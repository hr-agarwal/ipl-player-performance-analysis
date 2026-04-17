import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="IPL Player Performance Dashboard",
    layout="wide"
)

# ================= MYSQL CONNECTION =================
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harsh@425",   # <-- CHANGE
    database="ipl"
)

# ================= LOAD DATA =================
batting = pd.read_sql("SELECT * FROM batting_stats", conn)
ball_df = pd.read_sql("SELECT * FROM ball_by_ball", conn)

# ================= FORMAT BEST FIGURES =================
batting["best_batting_display"] = (
    batting["best_batting_runs"].astype(int).astype(str)
    + "/"
    + batting["best_batting_balls"].astype(int).astype(str)
)

batting["best_bowling_display"] = (
    batting["best_bowling_wickets"].astype(int).astype(str)
    + "/"
    + batting["best_bowling_runs"].astype(int).astype(str)
)

# ================= TITLE =================
st.title("🏏 IPL Player Performance Analytics Dashboard")

# =========================================================
# TOP 10 RUN SCORERS (NOW SQL OPTIMIZED)
# =========================================================
st.subheader("Top 10 IPL Run Scorers")

top10 = pd.read_sql("""
    SELECT batter, total_runs
    FROM batting_stats
    ORDER BY total_runs DESC
    LIMIT 10
""", conn)

fig1 = px.bar(
    top10,
    x="batter",
    y="total_runs",
    color="total_runs",
    text_auto=True,
    title="Top 10 Run Scorers"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# PLAYER SEARCH + METRICS (NO CHANGE IN LOGIC)
# =========================================================
st.subheader("Search Player Performance")

player_name = st.selectbox(
    "Search Player Name",
    batting["batter"].unique()
)

player_data = batting[
    batting["batter"] == player_name
].iloc[0]

st.subheader(f"Performance Metrics: {player_name}")

# ROW 1
row1 = st.columns(5)

with row1[0]:
    st.metric("Total Runs", int(player_data["total_runs"]))

with row1[1]:
    st.metric("Balls Played", int(player_data["balls_played"]))

with row1[2]:
    st.metric("Innings", int(player_data["innings"]))

with row1[3]:
    st.metric("Strike Rate", round(player_data["strike_rate"], 2))

with row1[4]:
    st.metric("Average", round(player_data["average"], 2))

# ROW 2
row2 = st.columns(5)

with row2[0]:
    st.metric("50s", int(player_data["total_50s"]))

with row2[1]:
    st.metric("100s", int(player_data["total_100s"]))

with row2[2]:
    st.metric("Boundary %", str(round(player_data["boundary_percent"], 2)) + "%")

with row2[3]:
    st.metric("Dot Ball %", str(round(player_data["dot_ball_percent"], 2)) + "%")

with row2[4]:
    st.metric("Consistency", round(player_data["consistency_score"], 2))

# ROW 3
row3 = st.columns(5)

with row3[0]:
    st.metric("Boundary Runs", int(player_data["boundary_runs"]))

with row3[1]:
    st.metric("Dismissals", int(player_data["dismissals"]))

with row3[2]:
    st.metric("Wickets", int(player_data["total_wickets"]))

with row3[3]:
    st.metric("Best Batting", player_data["best_batting_display"])

with row3[4]:
    st.metric("Best Bowling", player_data["best_bowling_display"])

# =========================================================
# PLAYER PERFORMANCE GRAPH (NO CHANGE)
# =========================================================
st.subheader(f"{player_name} Performance Overview")

performance_df = pd.DataFrame({
    "Metric": [
        "Strike Rate",
        "Average",
        "Boundary %",
        "Dot Ball %",
        "Consistency"
    ],
    "Value": [
        player_data["strike_rate"],
        player_data["average"],
        player_data["boundary_percent"],
        player_data["dot_ball_percent"],
        player_data["consistency_score"]
    ]
})

fig2 = px.line(
    performance_df,
    x="Metric",
    y="Value",
    markers=True,
    title=f"{player_name} Performance Analysis"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# PLAYER COMPARISON (NO CHANGE)
# =========================================================
st.subheader("Compare Two Players")

c1, c2 = st.columns(2)

with c1:
    player1 = st.selectbox(
        "Select First Player",
        batting["batter"].unique(),
        key="compare1"
    )

with c2:
    player2 = st.selectbox(
        "Select Second Player",
        batting["batter"].unique(),
        key="compare2"
    )

p1 = batting[batting["batter"] == player1].iloc[0]
p2 = batting[batting["batter"] == player2].iloc[0]

metrics_list = [
    ("Total Runs", "total_runs"),
    ("Strike Rate", "strike_rate"),
    ("Average", "average"),
    ("50s", "total_50s"),
    ("100s", "total_100s"),
    ("Wickets", "total_wickets")
]

for i in range(0, len(metrics_list), 3):

    col1, col2, col3 = st.columns(3)

    for j, col in enumerate([col1, col2, col3]):
        if i + j < len(metrics_list):
            title, col_name = metrics_list[i + j]

            compare_df = pd.DataFrame({
                "Player": [player1, player2],
                "Value": [p1[col_name], p2[col_name]]
            })

            fig = px.bar(
                compare_df,
                x="Player",
                y="Value",
                color="Player",
                text_auto=True,
                title=title
            )

            with col:
                st.plotly_chart(fig, use_container_width=True)

# =========================================================
# MATCHUP (NO CHANGE)
# =========================================================
st.subheader("Bowler vs Batter Matchup Analysis")

m1, m2 = st.columns(2)

with m1:
    batter_selected = st.selectbox(
        "Select Batter",
        ball_df["batter"].unique(),
        key="batter_match"
    )

with m2:
    bowler_selected = st.selectbox(
        "Select Bowler",
        ball_df["bowler"].unique(),
        key="bowler_match"
    )

matchup = ball_df[
    (ball_df["batter"] == batter_selected) &
    (ball_df["bowler"] == bowler_selected)
]

if len(matchup) > 0:

    total_runs = matchup["batsman_runs"].sum()
    balls = len(matchup)
    dismissals = matchup["is_wicket"].sum()
    strike_rate = (total_runs / balls) * 100 if balls > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Runs Scored", int(total_runs))
    c2.metric("Balls Faced", int(balls))
    c3.metric("Times Out", int(dismissals))
    c4.metric("Strike Rate", round(strike_rate, 2))

    dismissals_df = matchup[matchup["dismissal_kind"] != ""]

    if len(dismissals_df) > 0:
        counts = dismissals_df["dismissal_kind"].value_counts()

        fig = px.pie(
            names=counts.index,
            values=counts.values,
            title="Dismissal Types"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Overall Matchup Analysis")

    if strike_rate >= 150:
        verdict = "Dominating"
    elif strike_rate >= 120:
        verdict = "Competitive"
    elif strike_rate >= 100:
        verdict = "Balanced"
    else:
        verdict = "Bowler Dominating"

    st.success(
        f"""
        **Analysis Summary:**  
        {batter_selected} has scored **{total_runs} runs** off **{balls} balls**
        against **{bowler_selected}** at a strike rate of **{round(strike_rate,2)}**  
        and has been dismissed **{dismissals} times**.  
        Overall matchup verdict: **{verdict}**
        """
        )

else:
    st.warning("No matchup data found.")


   