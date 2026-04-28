# IPL Player Performance Analytics (Data Engineering Project)

🚀 **Live App:** https://hr-agarwal-ipl-player-performance-analysis-app-5jn9xv.streamlit.app/

---

## Overview

This project builds an end-to-end data engineering pipeline to analyze IPL player performance using ball-by-ball match data. It includes data ingestion, transformation, storage using CSV files, and an interactive dashboard for visualization.

The dashboard dynamically computes player statistics based on filters such as year range, ensuring flexible and real-time analysis.

---

## Demo Preview

![Dashboard Preview](assets/dashboard1.png)
![Dashboard Preview](assets/dashboard2.png)
![Dashboard Preview](assets/dashboard3.png)

---

## Features

- Dynamic player performance metrics (runs, strike rate, average, dismissals)
- Advanced analytics (boundary %, dot ball %, consistency)
- Top 15 run scorers visualization (interactive)
- Player vs Player comparison (multi-metric charts)
- Batter vs Bowler matchup analysis
- Year range filtering (2008–2025)
- Interactive Streamlit dashboard with responsive UI

---

## Tech Stack

- Python (Pandas)
- CSV (Data Storage)
- Streamlit (Frontend Dashboard)
- Plotly & Matplotlib (Visualization)

---

## Data Pipeline

Raw IPL JSON data is processed and transformed into structured format:

JSON → Pandas ETL → CSV → Streamlit Dashboard

---

## Data Design (Conceptual)

The system follows a simplified schema:

- **ball_by_ball** (delivery-level data – primary source)
- **batting_stats** (precomputed, optional reference)

**Relationship:**  
One player → many ball-by-ball records  

Note: All dashboard metrics are dynamically computed from ball-by-ball data to support filtering (e.g., year range).

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

pip install pandas streamlit plotly matplotlib

---

### 2. Run Data Pipeline

Run the notebook:

1_data_pipeline.ipynb

This will:
- Process raw data  
- Generate CSV files  

---

### 3. Run Dashboard

streamlit run app.py

---

## Deployment Note

The project uses CSV files instead of a database to ensure easy deployment on Streamlit Cloud without requiring external database configuration.

---

## Key Insights

- Identify top-performing players across different time ranges  
- Analyze consistency and scoring patterns  
- Compare players across multiple performance metrics  
- Evaluate batter vs bowler matchups dynamically  

---

## Future Improvements

- Add caching for faster performance  
- Introduce normalized schema (player_id, match_id)  
- Integrate cloud database (AWS / GCP)  
- Add team-level and match-level analytics  

---

## Author

Harsh Raj Agarwal