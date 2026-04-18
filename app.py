import streamlit as st
import pandas as pd
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="IPL Player Performance Dashboard",
    layout="wide"
)

# ================= DATA LOADING =================
batting = pd.read_csv("advanced_batting_stats.csv")
ball_df = pd.read_csv("ipl_ball_by_ball.csv")

top10 = batting.sort_values(by="total_runs", ascending=False).head(10)

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
# TOP 10 RUN SCORERS
# =========================================================
st.subheader("Top 10 IPL Run Scorers")

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
# PLAYER SEARCH + METRICS
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
row1[0].metric("Total Runs", int(player_data["total_runs"]))
row1[1].metric("Balls Played", int(player_data["balls_played"]))
row1[2].metric("Innings", int(player_data["innings"]))
row1[3].metric("Strike Rate", round(player_data["strike_rate"], 2))
row1[4].metric("Average", round(player_data["average"], 2))

# ROW 2
row2 = st.columns(5)
row2[0].metric("50s", int(player_data["total_50s"]))
row2[1].metric("100s", int(player_data["total_100s"]))
row2[2].metric("Boundary %", str(round(player_data["boundary_percent"], 2)) + "%")
row2[3].metric("Dot Ball %", str(round(player_data["dot_ball_percent"], 2)) + "%")
row2[4].metric("Consistency", round(player_data["consistency_score"], 2))

# ROW 3
row3 = st.columns(5)
row3[0].metric("Boundary Runs", int(player_data["boundary_runs"]))
row3[1].metric("Dismissals", int(player_data["dismissals"]))
row3[2].metric("Wickets", int(player_data["total_wickets"]))
row3[3].metric("Best Batting", player_data["best_batting_display"])
row3[4].metric("Best Bowling", player_data["best_bowling_display"])

# =========================================================
# PERFORMANCE GRAPH
# =========================================================
st.subheader(f"{player_name} Performance Overview")

performance_df = pd.DataFrame({
    "Metric": [
        "Strike Rate", "Average", "Boundary %", "Dot Ball %", "Consistency"
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
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# PLAYER COMPARISON
# =========================================================
st.subheader("Compare Two Players")

c1, c2 = st.columns(2)

player1 = c1.selectbox("Player 1", batting["batter"].unique(), key="p1")
player2 = c2.selectbox("Player 2", batting["batter"].unique(), key="p2")

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

            fig = px.bar(compare_df, x="Player", y="Value", color="Player", title=title)

            col.plotly_chart(fig, use_container_width=True)

# =========================================================
# MATCHUP ANALYSIS
# =========================================================
st.subheader("Bowler vs Batter Matchup Analysis")

batter_selected = st.selectbox("Select Batter", ball_df["batter"].unique())
bowler_selected = st.selectbox("Select Bowler", ball_df["bowler"].unique())

matchup = ball_df[
    (ball_df["batter"] == batter_selected) &
    (ball_df["bowler"] == bowler_selected)
]

if len(matchup) > 0:
    total_runs = matchup["batsman_runs"].sum()
    balls = len(matchup)
    dismissals = matchup["is_wicket"].sum()
    strike_rate = (total_runs / balls) * 100 if balls else 0

    cols = st.columns(4)
    cols[0].metric("Runs", total_runs)
    cols[1].metric("Balls", balls)
    cols[2].metric("Outs", dismissals)
    cols[3].metric("SR", round(strike_rate, 2))

    if strike_rate >= 150:
        verdict = "Dominating"
    elif strike_rate >= 120:
        verdict = "Competitive"
    elif strike_rate >= 100:
        verdict = "Balanced"
    else:
        verdict = "Bowler Dominating"

    st.success(f"{batter_selected} vs {bowler_selected}: {verdict}")

else:
    st.warning("No matchup data found.")