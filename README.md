## Data Breach Dashboard 🛡️
A high-performance, interactive cyber intelligence dashboard built with Python, Dash, and Plotly. This application visualizes historical data breach records from global companies and countries, providing insights into attack vectors, vulnerable sectors, and trends over time.

![Dashboard Preview](https://github.com/vyash0048-bit/Data-Beach-Dashboard-Using-Ploty-Dash/blob/main/Screenshot%202026-01-04%20190918.png)

## 🚀 Features
- Cyber/Neon UI: A sleek, dark-mode interface designed with the CYBORG Bootstrap theme and glowing neon accents.
- Dual Dataset Support: seamless switching between Company-wise and Country-wise breach data.

- Interactive Analytics:

  - Sunburst Chart: Drill down into sector distributions (click rings to filter the entire dashboard).

  - TreeMap: Visualize the frequency of different attack methods (Hacking, Lost Devices, etc.).

  - Timeline: Analyze breach trends over years with a zoomable area chart and range slider.

  - Top Targets: A gradient bar chart highlighting the most affected entities.

- Cross-Filtering: Clicking on a specific sector in the Sunburst chart automatically filters all other charts to show data for that sector only.

- Responsive Design: Fully responsive layout using dash-bootstrap-components.

## 🛠️ Tech Stack
- Dash: For building the web application framework.

- Plotly Express: For generating high-quality interactive graphs.

- Dash Bootstrap Components: For the responsive grid layout and Cyborg theme.

- Pandas: For data manipulation and analysis.

## 📂 Project Structure
```
Data-Beach-Dashboard-Using-Ploty-Dash/
├── app.py                            # Main application code
├── data1_country_wise_breaches.csv   # Dataset 1 (Country records)
├── data2_company_wise_breaches.csv   # Dataset 2 (Company records)
├── requirements.txt                  # List of dependencies
├── Procfile                          # Configuration for deployment (e.g., Render/Heroku)
└── README.md                         # Project documentation
```
## ⚙️ Installation & Setup
- Clone the repository:
```
git clone https://github.com/vyash0048-bit/Data-Beach-Dashboard-Using-Ploty-Dash.git
cd Data-Beach-Dashboard-Using-Ploty-Dash
```
- Create a virtual environment (optional but recommended):
```
python -m venv venv
```
### Windows
```
venv\Scripts\activate
```
### Mac/Linux
```
source venv/bin/activate
```
- Install dependencies:
```
pip install -r requirements.txt
```
- Run the application:
```
python app.py
```
- View the dashboard: Open your browser and navigate to http://127.0.0.1:8050/.

## 📊 Data Sources
This dashboard utilizes two primary datasets:

- Country-wise Breaches: Aggregated data on government and agency breaches sorted by nation.
- Company-wise Breaches: Detailed records of corporate data breaches, including organization type and records lost.

(Ensure these CSV files are present in the root directory for the app to function correctly.)

## 🚀 Deployment
This app is ready for deployment on platforms like Render, Heroku, or PythonAnywhere.
For Render:
- Push this repo to GitHub.

- Link your GitHub repo to a new "Web Service" on Render.

- Set the Start Command to: gunicorn app:server

## 🤝 Contributing
Contributions are welcome! If you have ideas for new features or better visualizations:

- Fork the repository.

- Create a new branch (```git checkout -b feature/NewFeature```).

- Commit your changes.

- Push to the branch and open a Pull Request.

## 📜 License
This project is open-source and available under the MIT License.
