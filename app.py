import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
        print("Successfully loaded CSV files.")
        return d1, d2
    except FileNotFoundError:
        print("CSV files not found. Using empty dataframes.")
        return pd.DataFrame(), pd.DataFrame()

data1, data2 = load_data()

def get_entity_column(df):
    for col in ["Entity", "Country", "Organization", "Company"]:
        if col in df.columns:
            return col
    return df.columns[0]

# =====================================================
# 2. App Config – Improved Palette
# =====================================================
NEON_BLUE   = "#00d4ff"
NEON_RED    = "#ff4d6d"
NEON_GREEN  = "#39ff14"
NEON_YELLOW = "#ffe600"
NEON_PURPLE = "#bf5fff"

CARD_BG     = "rgba(14, 17, 28, 0.85)"
PANEL_BG    = "#0a0d1a"
GLOW_BLUE   = f"0 0 18px rgba(0,212,255,0.35)"
GLOW_RED    = f"0 0 18px rgba(255,77,109,0.35)"
GLOW_GREEN  = f"0 0 18px rgba(57,255,20,0.35)"
GLOW_YELLOW = f"0 0 18px rgba(255,230,0,0.35)"

# Google Font: Orbitron (techy), Rajdhani (body)
EXTERNAL_SCRIPTS = ["https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600&display=swap"]

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG] + EXTERNAL_SCRIPTS,
    title="Cyber Intelligence Dashboard",
    suppress_callback_exceptions=True,
)
server = app.server   # ← Required for Hugging Face / Gunicorn

# ── Shared Plotly layout ──────────────────────────────
LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#ccd6f6", family="Rajdhani, sans-serif", size=13),
    margin=dict(t=35, l=12, r=12, b=12),
    hoverlabel=dict(bgcolor="#0a0d1a", bordercolor=NEON_BLUE, font_color=NEON_BLUE),
)

# ── Helper card builder ────────────────────────────────
def kpi_card(label, elem_id, color, glow):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.P(label, className="text-muted mb-1",
                       style={"fontSize": "0.72rem", "letterSpacing": "2px", "fontFamily": "Orbitron, monospace"}),
                html.H2(id=elem_id, style={
                    "color": color,
                    "fontWeight": "900",
                    "fontFamily": "Orbitron, monospace",
                    "textShadow": f"0 0 12px {color}",
                    "marginBottom": 0,
                }),
            ], className="text-center py-3"),
            style={
                "backgroundColor": CARD_BG,
                "border": f"1px solid {color}",
                "borderRadius": "12px",
                "boxShadow": glow,
                "backdropFilter": "blur(6px)",
            }
        ),
        width=3, className="mb-3"
    )

def chart_card(title, subtitle, elem_id, height=480):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, style={
                "textAlign": "center",
                "color": NEON_BLUE,
                "fontFamily": "Orbitron, monospace",
                "fontWeight": "700",
                "letterSpacing": "2px",
                "textTransform": "uppercase",
                "borderBottom": f"1px solid rgba(0,212,255,0.3)",
                "paddingBottom": "8px",
                "marginBottom": "4px",
                "textShadow": f"0 0 8px {NEON_BLUE}",
            }),
            html.Small(subtitle, className="d-block text-center text-muted mb-2",
                       style={"letterSpacing": "1px", "fontSize": "0.72rem"}),
            dcc.Graph(id=elem_id, style={"height": f"{height}px"}, config={"responsive": True}),
        ]),
        style={
            "backgroundColor": CARD_BG,
            "border": "1px solid rgba(0,212,255,0.2)",
            "borderRadius": "14px",
            "boxShadow": GLOW_BLUE,
            "backdropFilter": "blur(6px)",
        }
    )

# ── Custom CSS injected via index_string ───────────────
app.index_string = """<!DOCTYPE html>
<html>
<head>
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
<style>
  body { background: #060810 !important; }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0d1a; }
  ::-webkit-scrollbar-thumb { background: #00d4ff44; border-radius: 3px; }
  .Select-control, .Select-menu-outer { background: #0a0d1a !important; color: #00d4ff !important; }
  /* Scanline overlay */
  body::after {
    content: "";
    position: fixed; inset: 0;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,212,255,0.012) 2px, rgba(0,212,255,0.012) 4px);
    pointer-events: none; z-index: 9999;
  }
</style>
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>"""

# ── Layout ─────────────────────────────────────────────
app.layout = dbc.Container(fluid=True, style={"padding": "28px", "minHeight": "100vh"}, children=[

    dcc.Store(id="sector_filter_store", data=None),

    # ── Header ──
    html.Div([
        html.H1("⚠ CYBER INTELLIGENCE DASHBOARD", style={
            "color": NEON_BLUE,
            "fontFamily": "Orbitron, monospace",
            "fontWeight": "900",
            "letterSpacing": "5px",
            "textAlign": "center",
            "textShadow": f"0 0 30px {NEON_BLUE}, 0 0 60px rgba(0,212,255,0.2)",
            "marginBottom": "4px",
        }),
        html.P("Global Data Breach Intelligence Platform", className="text-center text-muted mb-4",
               style={"letterSpacing": "3px", "fontSize": "0.78rem", "fontFamily": "Rajdhani, sans-serif"}),
    ]),

    # ── KPI Row ──
    dbc.Row([
        kpi_card("TOTAL BREACHES",     "total_breaches",  NEON_RED,    GLOW_RED),
        kpi_card("ATTACK VECTORS",     "total_methods",   NEON_BLUE,   GLOW_BLUE),
        kpi_card("VULNERABLE SECTORS", "total_org_types", NEON_YELLOW, GLOW_YELLOW),
        kpi_card("YEARS ACTIVE",       "years_covered",   NEON_GREEN,  GLOW_GREEN),
    ], className="mb-4"),

    # ── Controls ──
    dbc.Row([
        dbc.Col([
            html.Label("📂 DATA SOURCE VIEW", style={
                "color": NEON_BLUE, "fontWeight": "600",
                "letterSpacing": "2px", "fontFamily": "Orbitron, monospace", "fontSize": "0.72rem"
            }),
            dbc.Select(
                id="dataset_picker",
                options=[
                    {"label": "🏢  COMPANY DATA", "value": "company"},
                    {"label": "🌍  COUNTRY DATA", "value": "country"},
                ],
                value="company",
                style={
                    "backgroundColor": "#0a0d1a",
                    "color": NEON_BLUE,
                    "border": f"1px solid {NEON_BLUE}",
                    "borderRadius": "8px",
                    "fontWeight": "600",
                    "boxShadow": GLOW_BLUE,
                    "fontFamily": "Rajdhani, sans-serif",
                }
            ),
        ], width=4),
        dbc.Col([
            html.Div([
                html.Span(id="filter_message", style={
                    "marginRight": "14px", "fontWeight": "600",
                    "color": NEON_YELLOW, "fontFamily": "Rajdhani, sans-serif",
                    "letterSpacing": "1px",
                }),
                dbc.Button("✕ RESET FILTER", id="reset_btn", color="danger", outline=True, size="sm",
                           style={"display": "none", "boxShadow": GLOW_RED,
                                  "fontWeight": "700", "fontFamily": "Orbitron, monospace",
                                  "fontSize": "0.7rem", "borderRadius": "6px"}),
            ], className="d-flex align-items-center h-100 mt-4")
        ], width=8),
    ], className="mb-4"),

    # ── Row 1: Top Targets + Attack Heatmap ──
    dbc.Row([
        dbc.Col(chart_card("Top Targets", "Most affected entities by breach count", "top_entity_chart", 460), width=6),
        dbc.Col(chart_card("Attack Heatmap", "Breakdown of breach methods", "method_chart", 460), width=6),
    ], className="mb-4"),

    # ── Row 2: Sector Sunburst + Timeline ──
    dbc.Row([
        dbc.Col(chart_card("Sector Distribution", "Click a segment to filter entire dashboard", "orgtype_chart", 510), width=6),
        dbc.Col(chart_card("Breach Timeline", "Drag the slider to zoom into a time range", "year_chart", 510), width=6),
    ]),

    # ── Footer ──
    html.Hr(style={"borderColor": "rgba(0,212,255,0.15)", "marginTop": "36px"}),
    html.P("Cyber Intelligence Dashboard · Data Breach Analytics · Built with Dash + Plotly",
           className="text-center text-muted", style={"fontSize": "0.7rem", "letterSpacing": "2px"}),
])

# =====================================================
# 3. Callbacks
# =====================================================
@app.callback(
    Output("sector_filter_store", "data"),
    [Input("dataset_picker", "value"),
     Input("reset_btn", "n_clicks"),
     Input("orgtype_chart", "clickData")],
    State("sector_filter_store", "data"),
)
def update_filter_store(dataset_view, reset_clicks, click_data, current_filter):
    ctx = dash.callback_context
    if not ctx.triggered:
        return None
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id in ("dataset_picker", "reset_btn"):
        return None
    if trigger_id == "orgtype_chart" and click_data:
        try:
            point = click_data["points"][0]
            selected_org = point.get("label") or point.get("id") or point.get("theta")
            return selected_org
        except Exception:
            return current_filter
    return current_filter


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
    [Input("dataset_picker", "value"),
     Input("sector_filter_store", "data")],
)
def update_dashboard(view, active_filter):
    if view == "country":
        df = data1.copy()
        entity_col = "Country"
    else:
        df = data2.copy()
        entity_col = get_entity_column(df)

    # Apply filter
    if active_filter and "Organization type" in df.columns:
        df = df[df["Organization type"] == active_filter]
        msg = f"▶ FILTER: {active_filter.upper()}"
        btn_style = {"display": "inline-block", "boxShadow": GLOW_RED,
                     "fontWeight": "700", "fontFamily": "Orbitron, monospace",
                     "fontSize": "0.7rem", "borderRadius": "6px"}
    else:
        msg = ""
        btn_style = {"display": "none"}

    # KPIs
    total_breaches  = f"{len(df):,}"
    total_methods   = df["Method"].nunique()           if "Method"            in df.columns else "—"
    total_org_types = df["Organization type"].nunique() if "Organization type" in df.columns else "—"
    years_covered   = df["Year"].nunique()              if "Year"              in df.columns else "—"

    # ── Chart 1: Horizontal bar – Top Targets ──────────
    df_entity = df[entity_col].value_counts().head(12).reset_index()
    df_entity.columns = [entity_col, "Count"]
    df_entity = df_entity.sort_values("Count")            # ascending for proper left→right glow

    fig_entity = go.Figure(go.Bar(
        x=df_entity["Count"],
        y=df_entity[entity_col],
        orientation="h",
        marker=dict(
            color=df_entity["Count"],
            colorscale=[[0, "#1a0533"], [0.4, NEON_PURPLE], [0.75, NEON_BLUE], [1, "#ffffff"]],
            line=dict(width=0),
        ),
        text=df_entity["Count"],
        textposition="outside",
        textfont=dict(color=NEON_BLUE, size=11),
        hovertemplate=f"<b>%{{y}}</b><br>Breaches: %{{x:,}}<extra></extra>",
    ))
    fig_entity.update_layout(
        **LAYOUT_BASE,
        xaxis=dict(showgrid=True, gridcolor="rgba(0,212,255,0.08)", zeroline=False, showline=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=11)),
        bargap=0.35,
    )

    # ── Chart 2: Treemap – Attack Methods ──────────────
    if "Method" in df.columns:
        df_method = df["Method"].value_counts().reset_index()
        df_method.columns = ["Method", "Count"]
        fig_method = px.treemap(
            df_method, path=["Method"], values="Count",
            color="Count",
            color_continuous_scale=[[0, "#0a0d1a"], [0.3, "#1a0040"],
                                     [0.6, NEON_PURPLE], [1.0, NEON_BLUE]],
            template="plotly_dark",
        )
        fig_method.update_traces(
            textfont=dict(size=14, family="Orbitron, monospace"),
            marker=dict(cornerradius=8, pad=dict(t=20, l=4, r=4, b=4)),
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<extra></extra>",
        )
        fig_method.update_layout(**LAYOUT_BASE, coloraxis_showscale=False)
    else:
        fig_method = go.Figure()
        fig_method.update_layout(**LAYOUT_BASE)

    # ── Chart 3: Sunburst – Sector Distribution ────────
    if "Organization type" in df.columns:
        df_org = df["Organization type"].value_counts().reset_index()
        df_org.columns = ["Organization type", "Count"]
        fig_org = px.sunburst(
            df_org, path=["Organization type"], values="Count",
            color="Count",
            color_continuous_scale=[[0, "#0a0d1a"], [0.3, "#3d0068"],
                                     [0.65, NEON_PURPLE], [1, NEON_BLUE]],
            template="plotly_dark",
        )
        fig_org.update_traces(
            insidetextorientation="radial",
            textfont=dict(size=13, family="Rajdhani, sans-serif"),
            leaf=dict(opacity=0.9),
            marker=dict(line=dict(color="#060810", width=1.5)),
            hovertemplate="<b>%{label}</b><br>Breaches: %{value:,}<extra></extra>",
        )
        fig_org.update_layout(**LAYOUT_BASE, coloraxis_showscale=False)
    else:
        fig_org = go.Figure()
        fig_org.update_layout(**LAYOUT_BASE)

    # ── Chart 4: Area – Breach Timeline ────────────────
    if "Year" in df.columns:
        df_year = df.groupby("Year").size().reset_index(name="Count")
        fig_year = go.Figure()
        # Shaded fill
        fig_year.add_trace(go.Scatter(
            x=df_year["Year"], y=df_year["Count"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(0,212,255,0.07)",
            line=dict(color=NEON_BLUE, width=2.5, shape="spline"),
            marker=dict(size=7, color=NEON_BLUE,
                        line=dict(color="#060810", width=2)),
            hovertemplate="<b>Year: %{x}</b><br>Breaches: %{y:,}<extra></extra>",
        ))
        # Peak highlight
        peak_idx = df_year["Count"].idxmax()
        fig_year.add_trace(go.Scatter(
            x=[df_year.loc[peak_idx, "Year"]],
            y=[df_year.loc[peak_idx, "Count"]],
            mode="markers+text",
            marker=dict(size=14, color=NEON_RED, symbol="star",
                        line=dict(color="white", width=1)),
            text=["PEAK"],
            textposition="top center",
            textfont=dict(color=NEON_RED, size=10, family="Orbitron, monospace"),
            showlegend=False,
            hoverinfo="skip",
        ))
        fig_year.update_layout(
            **LAYOUT_BASE,
            showlegend=False,
            xaxis=dict(
                rangeslider=dict(visible=True, bgcolor="#0a0d1a", bordercolor=NEON_BLUE, thickness=0.08),
                showgrid=False,
                showspikes=True,
                spikecolor=NEON_BLUE,
                spikethickness=1,
                spikedash="dot",
                spikemode="across",
            ),
            yaxis=dict(showgrid=True, gridcolor="rgba(0,212,255,0.07)", zeroline=False),
            hovermode="x unified",
        )
    else:
        fig_year = go.Figure()
        fig_year.update_layout(**LAYOUT_BASE)

    return (
        total_breaches, total_methods, total_org_types, years_covered,
        fig_entity, fig_method, fig_org, fig_year,
        msg, btn_style,
    )


# =====================================================
# 4. Entry Point  ← HuggingFace needs host="0.0.0.0"
# =====================================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))   # HF default port
    app.run(host="0.0.0.0", port=port, debug=False)
    