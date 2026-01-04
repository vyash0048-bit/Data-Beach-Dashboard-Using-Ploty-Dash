import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
import os

# =====================================================
# 1. Load Data
# =====================================================
def load_data():
    try:
        d1 = pd.read_csv("data1_country_wise_breaches.csv")
        d2 = pd.read_csv("data2_company_wise_breaches.csv")
        print("✅ Successfully loaded CSV files.")
        return d1, d2
    except FileNotFoundError:
        print("❌ CSV files not found. Using empty dataframes.")
        return pd.DataFrame(), pd.DataFrame()

data1, data2 = load_data()

def get_entity_column(df):
    for col in ["Entity", "Country", "Organization", "Company"]: 
        if col in df.columns:
            return col
    return df.columns[0]

# =====================================================
# 2. App Config (Cyborg Theme)
# =====================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# --- Custom Styles ---
card_style = {
    "backgroundColor": "rgba(20, 20, 20, 0.6)",
    "border": "1px solid #444",
    "borderRadius": "8px",
    "boxShadow": "0 0 15px rgba(0, 212, 255, 0.05)"
}

title_style = {
    'textAlign': 'center',
    'color': '#00d4ff', 
    'fontWeight': 'bold',
    'letterSpacing': '2px',
    'textTransform': 'uppercase',
    'borderBottom': '1px solid rgba(0, 212, 255, 0.3)',
    'paddingBottom': '10px',
    'marginBottom': '15px',
    'textShadow': '0 0 5px rgba(0, 212, 255, 0.6)'
}

# New Stylish Dropdown Style
dropdown_style = {
    'backgroundColor': 'rgba(0, 0, 0, 0.5)', # Semi-transparent dark
    'color': '#00d4ff',                       # Neon Text
    'border': '1px solid #00d4ff',            # Neon Border
    'borderRadius': '5px',
    'fontWeight': 'bold',
    'boxShadow': '0 0 10px rgba(0, 212, 255, 0.2)', # Blue Glow
    'cursor': 'pointer'
}

# =====================================================
# 3. Layout
# =====================================================
app.layout = dbc.Container(fluid=True, style={'padding': '25px', 'fontFamily': 'Roboto, sans-serif'}, children=[

    # Store for Filter State
    dcc.Store(id='sector_filter_store', data=None),

    # --- Header ---
    html.H1("CYBER INTELLIGENCE DASHBOARD", className="text-center mb-5", 
            style={'color': '#00d4ff', 'fontWeight': '900', 'letterSpacing': '4px', 'textShadow': '0 0 20px #00d4ff'}),

    # --- KPI Cards ---
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("TOTAL BREACHES", className="text-muted", style={'fontSize': '0.8rem'}),
            html.H2(id="total_breaches", style={'color': '#ff4d4d', 'fontWeight': 'bold', 'textShadow': '0 0 15px #ff4d4d'})
        ], className="text-center")], style=card_style), width=3),
        
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("ATTACK VECTORS", className="text-muted", style={'fontSize': '0.8rem'}),
            html.H2(id="total_methods", style={'color': '#00d4ff', 'fontWeight': 'bold', 'textShadow': '0 0 15px #00d4ff'})
        ], className="text-center")], style=card_style), width=3),
        
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("VULNERABLE SECTORS", className="text-muted", style={'fontSize': '0.8rem'}),
            html.H2(id="total_org_types", style={'color': '#ffea00', 'fontWeight': 'bold', 'textShadow': '0 0 15px #ffea00'})
        ], className="text-center")], style=card_style), width=3),
        
        dbc.Col(dbc.Card([dbc.CardBody([
            html.H6("YEARS ACTIVE", className="text-muted", style={'fontSize': '0.8rem'}),
            html.H2(id="years_covered", style={'color': '#00ff88', 'fontWeight': 'bold', 'textShadow': '0 0 15px #00ff88'})
        ], className="text-center")], style=card_style), width=3),
    ], className="mb-4"),

    # --- Controls ---
    dbc.Row([
        dbc.Col([
            html.Label("📂 DATA SOURCE VIEW", className="text-info", style={'fontWeight': 'bold', 'letterSpacing': '1px'}),
            # STYLISH DROPDOWN (dbc.Select)
            dbc.Select(
                id="dataset_picker",
                options=[
                    {"label": "🏢 COMPANY DATA", "value": "company"},
                    {"label": "🌍 COUNTRY DATA", "value": "country"}
                ],
                value="company",
                style=dropdown_style
            )
        ], width=4),
        
        # Action Area (Filter Message + Reset Button)
        dbc.Col([
             html.Div([
                 html.Span(id="filter_message", style={'marginRight': '15px', 'fontWeight': 'bold', 'color': '#00d4ff'}),
                 dbc.Button("✕ RESET FILTER", id="reset_btn", color="danger", outline=True, size="sm", 
                            style={'display': 'none', 'boxShadow': '0 0 10px #dc3545', 'fontWeight': 'bold'})
             ], className="d-flex align-items-center h-100 mt-4")
        ], width=8)
    ], className="mb-4"),

    # --- Row 1 ---
    dbc.Row([
        # Chart 1: Entities
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Top Targets", style=title_style),
                dcc.Graph(id="top_entity_chart", style={'height': '450px'}, config={'responsive': True})
            ])
        ], style=card_style), width=6),

        # Chart 2: Methods (TreeMap)
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Attack Heatmap", style=title_style),
                dcc.Graph(id="method_chart", style={'height': '450px'}, config={'responsive': True})
            ])
        ], style=card_style), width=6),
    ], className="mb-4"),

    # --- Row 2 ---
    dbc.Row([
        # Chart 3: Sunburst
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Sector Distribution", style=title_style),
                html.Small("Click inner rings to filter dashboard", className="text-muted d-block text-center mb-2"),
                dcc.Graph(id="orgtype_chart", style={'height': '500px'}, config={'responsive': True})
            ])
        ], style=card_style), width=6),

        # Chart 4: Timeline
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Breach Timeline", style=title_style),
                dcc.Graph(id="year_chart", style={'height': '500px'}, config={'responsive': True})
            ])
        ], style=card_style), width=6),
    ]),

])

# =====================================================
# 4. Callbacks
# =====================================================

# Callback 1: Manage Filter State
@app.callback(
    Output("sector_filter_store", "data"),
    [
        Input("dataset_picker", "value"),
        Input("reset_btn", "n_clicks"),
        Input("orgtype_chart", "clickData")
    ],
    State("sector_filter_store", "data")
)
def update_filter_store(dataset_view, reset_clicks, click_data, current_filter):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Reset if dataset changes or reset button clicked
    if trigger_id == "dataset_picker" or trigger_id == "reset_btn":
        return None
    
    # Set filter if chart clicked
    if trigger_id == "orgtype_chart" and click_data:
        try:
            point = click_data['points'][0]
            selected_org = point.get('label') or point.get('id') or point.get('theta')
            return selected_org
        except:
            return current_filter
    return current_filter

# Callback 2: Update Dashboard
@app.callback(
    [
        Output("total_breaches", "children"),
        Output("total_methods", "children"),
        Output("total_org_types", "children"),
        Output("years_covered", "children"),
        Output("top_entity_chart", "figure"),
        Output("method_chart", "figure"),
        Output("orgtype_chart", "figure"),
        Output("year_chart", "figure"),
        Output("filter_message", "children"),
        Output("reset_btn", "style"),
    ],
    [
        Input("dataset_picker", "value"),
        Input("sector_filter_store", "data")
    ]
)
def update_dashboard(view, active_filter):
    
    if view == "country":
        df = data1.copy()
        entity_col = "Country"
    else:
        df = data2.copy()
        entity_col = get_entity_column(df)

    # Filter Data
    if active_filter and "Organization type" in df.columns:
        df = df[df["Organization type"] == active_filter]
        msg = f"FILTER ACTIVE: {active_filter}"
        btn_style = {'display': 'block', 'boxShadow': '0 0 10px #dc3545', 'fontWeight': 'bold'}
    else:
        msg = ""
        btn_style = {'display': 'none'}

    # KPIs
    total_breaches = f"{len(df):,}"
    total_methods = df["Method"].nunique() if "Method" in df.columns else 0
    total_org_types = df["Organization type"].nunique() if "Organization type" in df.columns else 0
    years_covered = df["Year"].nunique() if "Year" in df.columns else 0

    # Layout Settings
    layout_settings = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0'),
        margin=dict(t=30, l=10, r=10, b=10)
    )

    # Chart 1: Entities
    df_entity = df[entity_col].value_counts().head(10).reset_index()
    df_entity.columns = [entity_col, "Count"]
    fig_entity = px.bar(
        df_entity, y=entity_col, x="Count", orientation='h',
        template="plotly_dark", color="Count", color_continuous_scale="Turbo"
    )
    fig_entity.update_layout(**layout_settings, yaxis=dict(autorange="reversed"))
    fig_entity.update_coloraxes(showscale=False)

    # Chart 2: Methods (TreeMap)
    if "Method" in df.columns:
        df_method = df["Method"].value_counts().reset_index()
        df_method.columns = ["Method", "Count"]
        fig_method = px.treemap(
            df_method, path=['Method'], values='Count',
            color='Count', color_continuous_scale='Viridis', template="plotly_dark"
        )
        fig_method.update_layout(**layout_settings)
        fig_method.update_traces(marker=dict(cornerradius=5))
    else:
        fig_method = px.bar(title="No Data", template="plotly_dark")

    # Chart 3: Sunburst
    if "Organization type" in df.columns:
        df_org = df["Organization type"].value_counts().reset_index()
        df_org.columns = ["Organization type", "Count"]
        fig_org = px.sunburst(
            df_org, path=["Organization type"], values="Count",
            color="Count", color_continuous_scale="Plasma", template="plotly_dark"
        )
        fig_org.update_layout(**layout_settings)
        fig_org.update_traces(insidetextorientation='radial')
    else:
        fig_org = px.bar(title="No Data", template="plotly_dark")

    # Chart 4: Timeline
    if "Year" in df.columns:
        df_year = df.groupby("Year").size().reset_index(name="Count")
        fig_year = px.area(
            df_year, x="Year", y="Count", template="plotly_dark", markers=True
        )
        fig_year.update_layout(
            **layout_settings,
            xaxis=dict(rangeslider=dict(visible=True), showgrid=False, showspikes=True, spikemode='across', spikesnap='cursor'),
            yaxis=dict(showgrid=True, gridcolor='#333'),
            hovermode="x unified"
        )
        fig_year.update_traces(line_color='#00ffcc', fillcolor='rgba(0, 255, 204, 0.1)')
    else:
        fig_year = px.line(title="No Data", template="plotly_dark")

    return (
        total_breaches, total_methods, total_org_types, years_covered,
        fig_entity, fig_method, fig_org, fig_year,
        msg, btn_style
    )

if __name__ == "__main__":
    app.run(debug=True)