import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

# ================= CSS =================
st.markdown("""
<style>
body {background-color:#050a08;}
.block-container {padding-top:2rem;}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding:10px;
    border-radius:12px;
    text-align:center;
    color:white;
    border:1px solid rgba(255,255,255,0.1);
    margin:5px;
}

html, body, [class*="css"] {
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD =================
ball_df = pd.read_csv("ipl_ball_by_ball.csv")
ball_df["season"] = ball_df["season"].astype(str).str[:4].astype(int)

# ================= TITLE =================
st.title("🏏 IPL Player Performance Dashboard")

# ================= YEAR FILTER =================
year_range = st.slider("Select Year Range", 2008, 2025, (2008, 2025))

filtered_df = ball_df[
    (ball_df["season"] >= year_range[0]) &
    (ball_df["season"] <= year_range[1])
]

# ================= TOP 15 RUN SCORERS =================
col1, col2 = st.columns(2)

top15 = (
    filtered_df
    .groupby("batter")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    top15,
    x="batsman_runs",
    y="batter",
    orientation="h",
    color="batsman_runs",
    color_continuous_scale="YlOrRd",
    text="batsman_runs"
)

fig.update_traces(
    hovertemplate="<b>%{y}</b><br>Runs: %{x}<extra></extra>"
)

fig.update_layout(
    template="plotly_dark",
    height=600,
    yaxis={'categoryorder':'total ascending'}
)

col1.plotly_chart(fig, use_container_width=True)

# ================= DONUT =================
top_wk = filtered_df[filtered_df["is_wicket"] == 1]["bowler"].value_counts().head(6)

fig2, ax2 = plt.subplots(figsize=(6,4))
wedges, texts, autotexts = ax2.pie(
    top_wk.values,
    labels=top_wk.index,
    autopct="%1.0f%%",
    startangle=90,
    wedgeprops=dict(width=0.4)
)

ax2.text(0, 0, f"{top_wk.sum()}\nWickets",
         ha="center", va="center",
         fontsize=12, color="white", weight="bold")

ax2.set_title("Top Wicket Takers", color="white")
ax2.set_facecolor("#050a08")

for t in texts + autotexts:
    t.set_color("white")

col2.pyplot(fig2)

# ================= PLAYER ANALYSIS =================
st.subheader("Player Analysis")

col1, col2, col3 = st.columns([1,2,1])
player_name = col2.selectbox("Select Player", filtered_df["batter"].unique())

p = filtered_df[filtered_df["batter"] == player_name]

runs = p["batsman_runs"].sum()
balls = len(p)
dismissals = p["is_wicket"].sum()

sr = (runs / balls * 100) if balls else 0
avg = (runs / dismissals) if dismissals else runs

# boundary
fours = (p["batsman_runs"] == 4).sum()
sixes = (p["batsman_runs"] == 6).sum()
boundary_runs = (fours * 4) + (sixes * 6)
boundary_percent = (boundary_runs / runs * 100) if runs else 0

# dot balls
dot_balls = (p["batsman_runs"] == 0).sum()
dot_percent = (dot_balls / balls * 100) if balls else 0

# additional stats (restored)
singles = (p["batsman_runs"] == 1).sum()
doubles = (p["batsman_runs"] == 2).sum()
triples = (p["batsman_runs"] == 3).sum()

# consistency (simple proxy)
consistency = sr * (1 - (dot_percent / 100))

# ================= METRICS =================
metrics = [
    ("Runs", runs),
    ("Balls", balls),
    ("Strike Rate", round(sr,2)),
    ("Average", round(avg,2)),
    ("4s", fours),
    ("6s", sixes),
    ("Boundary %", f"{round(boundary_percent,2)}%"),
    ("Dot %", f"{round(dot_percent,2)}%"),
    ("Singles", singles),
    ("Doubles", doubles),
    ("Triples", triples),
    ("Dismissals", dismissals),
    ("Consistency", round(consistency,2))
]

# layout (3 rows × 4 cols)
cols = st.columns(4)
for i,(k,v) in enumerate(metrics):
    cols[i%4].markdown(
        f"<div class='metric-card'>{k}<br><b>{v}</b></div>",
        unsafe_allow_html=True
    )

# ================= COMPARISON =================
st.subheader("Player Comparison")

col1, col2 = st.columns(2)

p1_name = col1.selectbox("Player 1", filtered_df["batter"].unique())
p2_name = col2.selectbox("Player 2", filtered_df["batter"].unique())

def compute(player):
    d = filtered_df[filtered_df["batter"] == player]
    runs = d["batsman_runs"].sum()
    balls = len(d)
    dismissals = d["is_wicket"].sum()

    sr = (runs/balls*100) if balls else 0
    avg = (runs/dismissals) if dismissals else runs

    return runs, sr, avg

p1_runs, p1_sr, p1_avg = compute(p1_name)
p2_runs, p2_sr, p2_avg = compute(p2_name)

metrics_list = [
    ("Runs", p1_runs, p2_runs),
    ("Strike Rate", p1_sr, p2_sr),
    ("Average", p1_avg, p2_avg)
]

for i in range(0, len(metrics_list), 3):
    cols = st.columns(3)
    for j in range(3):
        if i+j < len(metrics_list):
            title, v1, v2 = metrics_list[i+j]

            fig, ax = plt.subplots(figsize=(5,3))
            ax.barh([p1_name, p2_name], [v1, v2],
                    color=["#ff4b4b","#00ffcc"])

            ax.set_title(title, color="white")
            ax.set_facecolor("#050a08")
            ax.tick_params(colors='white')
            ax.spines[:].set_visible(False)

            cols[j].pyplot(fig)

# ================= MATCHUP =================
st.subheader("Batter vs Bowler")

col1, col2 = st.columns(2)

batter = col1.selectbox("Batter", filtered_df["batter"].unique())
bowler = col2.selectbox("Bowler", filtered_df["bowler"].unique())

m = filtered_df[
    (filtered_df["batter"] == batter) &
    (filtered_df["bowler"] == bowler)
]

def capsule(label, value):
    return f"""
    <div class='metric-card'>
        {label}<br><b>{value}</b>
    </div>
    """

if len(m) > 0:
    runs = m["batsman_runs"].sum()
    balls = len(m)
    outs = m["is_wicket"].sum()
    sr = (runs/balls)*100 if balls else 0

    cols = st.columns(4)
    cols[0].markdown(capsule("Runs", runs), unsafe_allow_html=True)
    cols[1].markdown(capsule("Balls", balls), unsafe_allow_html=True)
    cols[2].markdown(capsule("Outs", outs), unsafe_allow_html=True)
    cols[3].markdown(capsule("SR", round(sr,2)), unsafe_allow_html=True)
else:
    st.warning("No matchup data found")