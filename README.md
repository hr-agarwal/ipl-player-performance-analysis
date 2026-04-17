# IPL Player Performance Analytics (Data Engineering Project)

## Overview

This project builds an end-to-end data engineering pipeline to analyze IPL player performance using ball-by-ball match data. It includes data ingestion, transformation, storage in MySQL, and an interactive dashboard for visualization.

---

## Features

* Player performance metrics (runs, strike rate, average, 50s, 100s)
* Advanced analytics (boundary %, dot ball %, consistency)
* Best batting (runs/balls) and best bowling (wickets/runs)
* Top 10 run scorers visualization
* Player vs Player comparison
* Bowler vs Batter matchup analysis
* Dismissal type distribution
* Interactive Streamlit dashboard

---

## Tech Stack

* Python (Pandas)
* MySQL (Database)
* Streamlit (Frontend Dashboard)
* Plotly (Visualization)

---

## Data Pipeline

Raw IPL JSON data is processed and transformed into structured format.

JSON → Pandas ETL → CSV → MySQL → Streamlit Dashboard

---

## Database Design (Conceptual ER)

The system follows a simplified schema:

* batting_stats (aggregated player performance)
* ball_by_ball (delivery-level data)

Relationship:
One player → many ball-by-ball records

(Note: In production, player_id would be used instead of player name.)

---

## Project Structure

cricket_project/
│
├── data/                     # Raw JSON files
├── advanced_batting_stats.csv
├── ipl_ball_by_ball.csv
├── 1_data_pipeline.ipynb     # ETL pipeline
├── app.py                    # Streamlit dashboard
└── README.md

---

## Setup Instructions

### 1. Install Dependencies

pip install pandas streamlit plotly mysql-connector-python

---

### 2. Setup MySQL

CREATE DATABASE ipl;

---

### 3. Run Data Pipeline

Run the notebook:
1_data_pipeline.ipynb

This will:

* Process raw data
* Generate CSV files
* Insert data into MySQL

---

### 4. Run Dashboard

streamlit run app.py

---

## Deployment Note

For deployment (Streamlit Cloud), CSV files are used instead of MySQL to avoid external database dependency.

---

## Key Insights

* Identify top-performing players
* Analyze consistency and strike efficiency
* Compare players across multiple metrics
* Evaluate bowler vs batter matchups

---

## Future Improvements

* Add caching for faster queries
* Normalize database schema (player_id, match_id)
* Deploy MySQL on cloud (AWS / GCP)
* Add team-level analytics

---

## Author

Harsh Raj Agarwal
