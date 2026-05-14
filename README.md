<p align="center">
  <img src="header.svg" width="800" alt="Cyber Intelligence Header">
</p>

# 🛡️ Cyber Intelligence Dashboard

A high-performance, interactive analytics platform for visualizing global data breach intelligence. This dashboard provides deep insights into attack vectors, vulnerable sectors, and historical trends of cyber security incidents.

## 🚀 Live Demo
<p align="left">
  <img src="loading.svg" width="150" alt="Loading">
</p>

You can view the live dashboard here: [Hugging Face Space](https://huggingface.co/spaces/YashAI07/DataBreach)

## ✨ Features

- **Global Breach Intelligence:** Analyze data across countries and companies.
- **Cyber/Neon UI:** A sleek, dark-mode interface designed with the CYBORG Bootstrap theme and glowing neon accents.
- **Interactive Visualizations:**
  - **Top Targets:** Identify the most frequently attacked entities with gradient bar charts.
  - **Attack Heatmap:** Explore the methods used in breaches using interactive Treemaps.
  - **Sector Distribution:** Deep dive into vulnerable industries with Sunburst charts (click segments to filter).
  - **Breach Timeline:** Track trends over time with an interactive area chart and range slider.
- **Dynamic Filtering:** Click on any sector or switch data sources to instantly update the entire dashboard.
- **Responsive Design:** Fully responsive layout built with `dash-bootstrap-components`.

## 🛠️ Tech Stack

- **Framework:** [Dash](https://dash.plotly.com/) (Python)
- **Visuals:** [Plotly.py](https://plotly.com/python/)
- **Styling:** Dash Bootstrap Components (Cyborg Theme) + Custom CSS
- **Data:** Pandas
- **Deployment:** Hugging Face Spaces (Docker)

## 📦 Local Setup

To run this project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vyash0048-bit/Data-Beach-Dashboard-Using-Ploty-Dash.git
   cd Data-Beach-Dashboard-Using-Ploty-Dash
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```
   The dashboard will be available at `http://127.0.0.1:7860`.

## 📊 Data Sources
The dashboard utilizes two primary datasets:
- `data1_country_wise_breaches.csv`: Global statistics on a per-country basis.
- `data2_company_wise_breaches.csv`: Detailed records of organizational breaches.

---
*Built with ❤️ for Cyber Security Researchers and Data Enthusiasts.*
