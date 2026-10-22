import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import joblib

# --------------------------- Load data ---------------------------

def load_data():
    data_path = Path(__file__).parent / "data" / "cleaned" / "account_data.csv"
    return pd.read_csv(data_path)

# ----------------------------- Theme -----------------------------
def apply_theme():
    st.markdown("""
    <style>

    /* =============== GLOBAL ================ */

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 5%,
                rgba(108, 99, 255, 0.08),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #080b14 0%,
                #0b101c 50%,
                #080c15 100%
            );
        color: #E2E8F0;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }
    #MainMenu,footer {
        visibility: hidden;
    }

    /* ============ SIDEBAR =========== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #090d17 0%,
            #0b101b 100%
        );
        border-right: 1px solid rgba(108, 99, 255, 0.16);
    }
    section[data-testid="stSidebar"] * {
        color: #C8D0E8;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #8A94B2;
    }

    /* ============= SIDEBAR TOGGLE =============== */
    header[data-testid="stHeader"] { background: transparent !important; }
    header [data-testid="stSidebarCollapsedControl"] { color: white !important; }
    header [data-testid="stSidebarCollapsedControl"] svg { fill: white !important; }

    /* ================= GENERAL TEXT ================== */
    h1, h2, h3, h4 { color: #E8ECF5; }
    p {color: #A8B0C4;}
    .stCaption {color: #6F7890;}

    /* ================ TABS ================ */

    .stTabs [data-baseweb="tab-list"] {
    gap: 0.7rem;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
    .stTabs [data-baseweb="tab"] {
    background: transparent;
    border: none;
    color: #858DA3;
    font-size: 1rem;
    font-weight: 500;
    padding: 0.5rem 0.3rem;
}
    .stTabs [data-baseweb="tab"]:hover {
    background: transparent;
    color: #D5D9E5;
}
    .stTabs [data-baseweb="tab-highlight"] {
    background-color: #A78BFA;
}
    .stTabs [data-baseweb="tab-border"] {
    background-color: transparent;
}
    /* =============== FILTERS ==================== */

    div[data-baseweb="select"] > div {
        background: #111722 !important;
        border: 1px solid rgba(108,99,255,0.20) !important;
        border-radius: 8px !important;
        color: #C8D0E8 !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(108,99,255,0.45) !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: rgba(108, 99, 255, 0.22) !important;
        border: 1px solid rgba(108, 99, 255, 0.50) !important;
        border-radius: 6px !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #C7D2FE !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
        fill: #C7D2FE !important;
        color: #C7D2FE !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #111722 !important;
        border-color: rgba(108, 99, 255, 0.35) !important;
    }
    div[data-testid="stRadio"] label {
        color: #A8B0C4 !important;
    }

    /* =========== SECTION HEADER ============ */

    .sec-header {
        display: flex;
        align-items: center;
        gap: 0.7rem;

        margin: 1.8rem 0 1rem;
        padding-bottom: 0.6rem;

        border-bottom: 1px solid rgba(108,99,255,0.14);
    }
    .sec-header .bar {
        width: 4px;
        min-width: 4px;
        height: 24px;

        background: linear-gradient(
            180deg,
            #6C63FF,
            #00D4AA
        );
        border-radius: 4px;
    }
    .sec-header h3 {
        font-size: 1rem;
        font-weight: 700;
        color: #E2E8F0;
        margin: 0;
    }
    .sec-header .badge {
        background: rgba(108,99,255,0.13);
        color: #A78BFA;

        font-size: 0.62rem;
        padding: 2px 8px;

        border-radius: 99px;
        border: 1px solid rgba(108,99,255,0.23);

        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* ================ INSIGHT BOX ================ */

    .insight-box {
        background: linear-gradient(135deg, #171F30, #101622);
        border: 1px solid #30394B;
        border-left: 4px solid #A78BFA;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        margin: 1.2rem 0 1.5rem;
        font-size: 0.88rem;
        line-height: 1.8;
        color: #C8D0E8;
        transition: border-color 0.25s ease, transform 0.25s ease;
    }
    .insight-box:hover {
        transform: translateY(-2px);
        border-color: #A78BFA;
    }
    .insight-box .tag {
        display: inline-block;
        color: #C4B5FD;
        background: rgba(167, 139, 250, 0.12);
        border: 1px solid rgba(167, 139, 250, 0.25);
        border-radius: 6px;
        padding: 3px 9px;
        margin-bottom: 0.65rem;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .insight-box strong { color: #00D4AA; font-weight: 700; }
    .insight-box .critical { color: #FF6B6B; font-weight: 700 }

    /* ============= DATAFRAME , DOWNLOAD BUTTON =============== */
    div[data-testid="stDataFrame"] {
        border: 1px solid #30394B;
        border-radius: 10px;
        overflow: hidden;
    }
    .stDownloadButton button {
        background: #141923;
        color: #E8ECF5;
        border: 1px solid #30394B;
        border-radius: 8px;
    }
    .stDownloadButton button:hover {
        background: #202635;
        color: #FFF;
        border-color: #6C63FF;
    }

    /* ============== MOBILE ========== */
    .model-kpi-row {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 10px;
    }
    @media (max-width: 600px) {
        .model-kpi-row { gap: 4px; }
        .model-kpi-card { padding: 9px 4px !important; }
        .model-kpi-label { font-size: 10px !important; overflow-wrap: anywhere; }
        .model-kpi-value { font-size: 17px !important; }
    }   
    @media (max-width: 900px) {
        .kpi-row { grid-template-columns: repeat(2, 1fr); }
        .rec-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 600px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .kpi-row { grid-template-columns: 1fr; }
    }
    .prediction-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;width:100%}
    .prediction-card{min-width:0;overflow:hidden;box-sizing:border-box;background:linear-gradient(145deg,#171F30,#101622);border:1px solid #30394B;border-top:3px solid var(--accent);border-radius:14px;padding:20px}
    .prediction-label,.prediction-subtitle{color:#8A94B2;font-size:12px;overflow-wrap:anywhere}
    .prediction-label{font-weight:700;text-transform:uppercase;letter-spacing:.7px}
    .prediction-value{color:var(--accent);font-size:clamp(11px,2vw,27px);font-weight:800;margin:12px 0 7px;overflow-wrap:anywhere}
    @media(max-width:768px){.prediction-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.prediction-card{padding:10px 5px}.prediction-label,.prediction-subtitle{font-size:9px}.prediction-value{font-size:clamp(10px,2.8vw,16px);margin:8px 0 5px}}
    </style>
    """, unsafe_allow_html=True)

def sh(title, badge=""):
    st.markdown(
        f"""
        <div class="sec-header">
            <span class="bar"></span><h3>{title}</h3>
            {f'<span class="badge">{badge}</span>' if badge else ''}
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------- PLOTLY THEME -------------------------

PAL = {
    "blue":       "#818CF8",  "red":        "#FF6B6B",  
    "green":      "#00D4AA",  "gold":       "#F4C95D",  
    "orange":     "#F08A4B",  "purple":     "#A78BFA",  
    "cyan":       "#45C4D9",  "pink":       "#E879A9",  
    "lime":       "#A3BE5B",  "slate":      "#94A3B8"   
}

churn_labels = {0: "Retained", 1: "Churned"}
country_short = {
    "Australia": "AU", "Canada": "CA", "France": "FR",
    "Germany": "DE", "India": "IN", "United Kingdom": "UK",
    "United States": "US"
}

def style_chart(fig, x_title="", y_title="", marg=None, height=380):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#E2E8F0", size=12),
        margin=marg or dict(t=50, b=40, l=40, r=60),
        height=height,
        title_font=dict(size=16, color="#E2E8F0"),
        legend_font=dict(size=11, color="#8A94B2"),
        xaxis_title=x_title,
        yaxis_title=y_title
    )
    fig.update_xaxes(showgrid=False, zeroline=False, color="#8A94B2", automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False, color="#8A94B2", automargin=True)
    return fig


def style_bar(fig, x_title="", y_title="", pos="outside", template=None,scale=False,
                legend=False, radius=6, marg=None, height=380, legend_layout=None):
    
    fig = style_chart(fig, x_title, y_title, marg=marg, height=height)
    fig.update_layout(coloraxis_showscale=scale, showlegend=legend)
    
    if legend_layout is not None:   
        fig.update_layout(legend=legend_layout)
    
    fig.update_traces(textposition=pos, cliponaxis=False, marker=dict(cornerradius=radius))
    
    if template is not None:    
        fig.update_traces(texttemplate=template)
    
    return fig

# ------------------------- Header -------------------------

def render_header():
    st.html("""
    <div class="app-header">
        <div class="header-top">
            <span class="header-tag">
                <i></i> AI / CUSTOMER INTELLIGENCE
            </span>
            <span class="header-badge">ML POWERED</span>
        </div>
        <div class="header-title">
            SaaS Subscription <span>Churn Prediction</span>
        </div>
        <div class="header-subtitle">
            Predictive analytics for smarter retention decisions.
        </div>
    </div>
    <style>
    .app-header{padding:10px 0 24px;border-bottom:1px solid #272D3B;margin-bottom:24px}
    .header-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:22px}
    .header-tag{font-size:.61rem;letter-spacing:1px;color:#8B95AD}
    .header-tag i{display:inline-block;width:7px;height:7px;border-radius:50%;background:#00D4AA;box-shadow:0 0 9px #00D4AA;margin-right:7px}
    .header-badge{font-size:.62rem;font-weight:750;letter-spacing:.8px;color:#00D4AA;background:#00D4AA12;border:1px solid #00D4AA35;border-radius:6px;padding:6px 9px}
    .header-title{font-size:clamp(1.8rem,4vw,2.7rem);font-weight:850;line-height:1.15;color:#E8ECF5;letter-spacing:-1px}
    .header-title span{color:#8B80FF}
    .header-subtitle{font-size:.84rem;color:#8B95AD;margin-top:13px}
    </style>
    """)

# ------------------------- Sidebar -------------------------

def render_sidebar(df):
    st.sidebar.title("🔍 Dashboard Filters")

    country = st.sidebar.multiselect(
        "Country",
        options=sorted(df["country"].dropna().unique().tolist()),
        default=sorted(df["country"].dropna().unique().tolist()),
    )

    plan_tier = st.sidebar.multiselect(
        "Plan Tier",
        options=sorted(df["plan_tier"].dropna().unique().tolist()),
        default=sorted(df["plan_tier"].dropna().unique().tolist()),
    )

    industry = st.sidebar.multiselect(
        "Industry",
        options=sorted(df["industry"].dropna().unique().tolist()),
        default=sorted(df["industry"].dropna().unique().tolist()),
    )

    return {
        "country": country,
        "plan_tier": plan_tier,
        "industry": industry,
    }

def apply_filters(df, filters):
    dff = df.copy()

    if filters.get("country"):
        dff = dff[dff["country"].isin(filters["country"])]

    if filters.get("plan_tier"):
        dff = dff[dff["plan_tier"].isin(filters["plan_tier"])]

    if filters.get("industry"):
        dff = dff[dff["industry"].isin(filters["industry"])]

    return dff

def render_kpis(dff):
    total = dff["account_id"].nunique()
    churned = dff.loc[dff["churn_flag"] == 1, "account_id"].nunique()
    rate = churned / total * 100 if total else 0
    mrr = dff["avg_mrr"].mean()

    cards = [
        ("👥", "Total Customers", f"{total:,}", f"{churned:,} churned customers", "Dataset Loaded", "ok", "blue"),
        ("📉", "Churned Customers", f"{churned:,}", "Customers lost", "High Risk", "danger", "red"),
        ("📊", "Churn Rate", f"{rate:.1f}%", "Share of customers who churned", "Churn Overview", "warning", "amber"),
        ("💰", "Average MRR", f"${mrr:,.2f}" if pd.notna(mrr) else "N/A", "Average monthly revenue", "Revenue Metric", "ok", "green")
    ]

    html = """
    <style>
    .kpi-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;align-items:stretch;font-family:'Inter',sans-serif;}
    .kpi-card{--accent:#818CF8;--glow:rgba(129,140,248,.15);position:relative;isolation:isolate;min-width:0;min-height:205px;padding:22px 21px 20px;display:flex;flex-direction:column;overflow:hidden;border-radius:17px;background:radial-gradient(ellipse at 95% 0%,var(--glow),transparent 48%),linear-gradient(145deg,#192235 0%,#111827 58%,#0D1421 100%);border:1px solid rgba(148,163,184,.15);box-shadow:0 8px 24px rgba(0,0,0,.18),inset 0 1px 0 rgba(255,255,255,.035);transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;}
    .kpi-card.blue{--accent:#818CF8;--glow:rgba(129,140,248,.17);}
    .kpi-card.red{--accent:#FF6B6B;--glow:rgba(255,107,107,.16);}
    .kpi-card.amber{--accent:#FFB347;--glow:rgba(255,179,71,.15);}
    .kpi-card.green{--accent:#00D4AA;--glow:rgba(0,212,170,.15);}
    .kpi-card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,transparent,var(--accent),transparent);opacity:.9;}
    .kpi-card::after{content:"";position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);box-shadow:0 0 13px var(--accent);opacity:.65;transition:opacity .25s ease,height .25s ease;}
    .kpi-card:hover{transform:translateY(-5px);border-color:var(--accent);box-shadow:0 13px 30px rgba(0,0,0,.26),0 0 22px var(--glow),inset 0 1px 0 rgba(255,255,255,.045);}
    .kpi-card:hover::after{opacity:1;height:3px;}
    .kpi-icon{display:flex;align-items:center;justify-content:center;width:43px;height:43px;flex-shrink:0;border-radius:12px;font-size:22px;background:var(--glow);border:1px solid color-mix(in srgb,var(--accent) 25%,transparent);box-shadow:0 0 18px var(--glow);}
    .kpi-top{display:flex;align-items:center;justify-content:flex-start;gap:12px;margin-bottom:17px;}
    .kpi-label{color:#A8B3C9;font-size:.70rem;font-weight:700;text-transform:uppercase;letter-spacing:.095em;line-height:1.5;}
    .kpi-value{color:var(--accent);font-size:clamp(1.85rem,2.25vw,2.45rem);font-weight:800;letter-spacing:-.055em;line-height:1.15;margin:0 0 9px;overflow-wrap:anywhere;text-shadow:0 0 22px var(--glow);font-variant-numeric:tabular-nums;}
    .kpi-sub{color:#929DB4;font-size:.76rem;line-height:1.5;margin-bottom:15px;}
    .kpi-badge{display:inline-flex;align-items:center;align-self:flex-start;gap:6px;margin-top:auto;padding:5px 10px;border-radius:99px;font-size:.65rem;font-weight:700;letter-spacing:.025em;line-height:1.3;border:1px solid transparent;}
    .kpi-badge::before{content:"";width:6px;height:6px;flex-shrink:0;border-radius:50%;background:currentColor;box-shadow:0 0 7px currentColor;}
    .kpi-badge.ok{color:#00D4AA;background:rgba(0,212,170,.09);border-color:rgba(0,212,170,.23);}
    .kpi-badge.danger{color:#FF7777;background:rgba(255,107,107,.09);border-color:rgba(255,107,107,.23);}
    .kpi-badge.warning{color:#FFB347;background:rgba(255,179,71,.09);border-color:rgba(255,179,71,.23);}
    @media(max-width:1000px){.kpi-row{grid-template-columns:repeat(2,minmax(0,1fr));gap:13px;}.kpi-value{font-size:2rem;}}
    @media(max-width:480px){.kpi-row{gap:9px;}.kpi-card{padding:15px 12px;min-height:185px;border-radius:14px;}.kpi-top{margin-bottom:14px;align-items:flex-start;flex-direction:column;gap:9px;}.kpi-icon{width:35px;height:35px;font-size:19px;border-radius:10px;}.kpi-label{font-size:.63rem;letter-spacing:.055em;}.kpi-value{font-size:1.65rem;margin-bottom:8px;}.kpi-sub{font-size:.68rem;margin-bottom:12px;}.kpi-badge{font-size:.59rem;padding:4px 7px;}}
    @media(prefers-reduced-motion:reduce){.kpi-card,.kpi-card::after{transition:none;}.kpi-card:hover{transform:none;}}
    </style>
    <div class="kpi-row">
    """

    for icon, label, value, sub, badge, badge_type, color in cards:
        html += (
            f'<div class="kpi-card {color}">'
            f'<div class="kpi-top"><div class="kpi-icon">{icon}</div>'
            f'<div class="kpi-label">{label}</div></div>'
            f'<div class="kpi-value">{value}</div>'
            f'<div class="kpi-sub">{sub}</div>'
            f'<span class="kpi-badge {badge_type}">{badge}</span>'
            f'</div>'
        )

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

def recommendation_card():

    sh("🎯 Data-Driven Recommendations", "Key Findings & Actions")    

    html = """
    <style>
    .rec-grid{ display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    .rec-card{background:#141923;border:1px solid #2A3040;border-radius:12px;padding:16px 14px;position:relative;overflow:hidden;min-width:0}
    .rec-card:before{content:"";position:absolute;top:0;left:0;width:100%;height:3px;background:var(--accent)}
    .rec-top{display:flex;justify-content:space-between;align-items:center;gap:5px;margin-bottom:13px}
    .rec-num{font-size:.68rem;font-weight:800;color:var(--accent)}
    .rec-priority{font-size:.55rem;font-weight:750;color:var(--accent);background:#202635;border:1px solid #343B4C;border-radius:12px;padding:4px 6px}
    .rec-tag{font-size:.58rem;font-weight:700;letter-spacing:.7px;color:#8B95AD;margin-bottom:6px}
    .rec-title{font-size:.94rem;font-weight:750;color:#E8ECF5;margin-bottom:12px;overflow-wrap:anywhere}
    .rec-label{font-size:.62rem;font-weight:750;letter-spacing:.5px;color:#8B95AD;margin-bottom:5px}
    .rec-finding{font-size:.76rem;line-height:1.55;color:#D1D8E6;margin:0 0 12px;overflow-wrap:anywhere}
    .rec-divider{height:1px;background:#272D3B;margin-bottom:11px}
    .rec-action{font-size:.73rem;line-height:1.6;color:#AAB4C8;margin:0;overflow-wrap:anywhere}
    </style>
    """

    cards = [
        ("01", "DevTools Segment", "SEGMENT ANALYSIS", "INVESTIGATE", "#FF6B6B",
         "DevTools has a 31.0% churn rate, with 35 of 113 customers leaving. This segment shows a notable retention concern.",
         "Compare feature adoption, support activity, and subscription patterns to identify behaviors linked to customer churn."),

        ("02", "Refund Patterns", "CHURN SIGNAL", "INVESTIGATE", "#00D4AA",
         "Churned customers have average refunds of 20.63, compared with 16.37 for retained customers. This difference warrants further investigation.",
         "Analyze refund frequency, amounts, and timing relative to cancellation to determine whether refund activity is associated with churn."),

        ("03", "Trial Conversion", "BEHAVIOR ANALYSIS", "REVIEW", "#8B80FF",
         "Trial customers have a 25.8% churn rate, compared with 21.1% for non-trial customers. This difference warrants further investigation, not a causal conclusion.",
         "Compare trial-to-paid conversion, onboarding engagement, and subsequent retention to identify potential improvements."),

        ("04", "Acquisition Quality", "CHANNEL ANALYSIS", "INVESTIGATE", "#FFB347",
         "Event-referred customers have a 30.2% churn rate, with 29 of 96 customers leaving. Acquisition source may be worth investigating.",
         "Compare churn rates and customer retention across referral sources to identify channels associated with longer-lasting subscriptions.")
    ]

    html = html + """<div class="rec-grid">"""

    for num, title, tag, priority, color, finding, action in cards:
        html += f"""
        <div class="rec-card" style="--accent:{color}">
            <div class="rec-top">
                <span class="rec-num">{num} / 04</span>
                <span class="rec-priority">{priority}</span>
            </div>
            <div class="rec-tag">{tag}</div>
            <div class="rec-title">{title}</div>
            <div class="rec-label">📊 FINDING</div>
            <p class="rec-finding">{finding}</p>
            <div class="rec-divider"></div>
            <div class="rec-label">↗ NEXT STEP</div>
            <p class="rec-action">{action}</p>
        </div>
        """
    html += "</div>"
    st.html(html)

def section_overview(dff):
    sh("Churn Overview","CUSTOMER RETENTION ANALYSIS")

    col1, col2 = st.columns(2)

    with col1:
        # ---------------- Chart 1: Customer Churn Distribution ----------------
        churn_data = (
            dff["churn_flag"].map(churn_labels)
            .value_counts()
            .rename_axis("churn_status")
            .reset_index(name="customer_count")
        )
        fig = px.pie(
            churn_data,
            names="churn_status",
            values="customer_count",
            hole=0.55,
            color_discrete_map={"Retained": PAL["green"], "Churned": PAL["red"]},
            title="Customer Churn Distribution"
        )

        fig = style_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # ---------------- Chart 2: Churn Rate by Plan Tier ----------------
        plan_data = (
            dff.groupby("plan_tier", as_index=False)
            .agg(
                customers=("account_id", "nunique"),
                churned=("churn_flag", "sum")
            ))

        plan_data["churn_rate"] = (
            plan_data["churned"] /
            plan_data["customers"] * 100
        )
        fig = px.bar(
            plan_data.sort_values("churn_rate"),
            x="churn_rate",
            y="plan_tier",
            orientation="h",
            title="Churn Rate by Plan Tier",
            color="plan_tier",
            color_discrete_map={"Basic": PAL["cyan"],"Pro": PAL["gold"],"Enterprise": PAL["pink"]},         
            labels={
                "churn_rate": "Churn Rate (%)",
                "plan_tier": "Plan Tier"
            },
            text="churn_rate",
        )
        fig = style_bar(fig, "Plan Tier", "Churn Rate (%)",template="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    <div class="insight-box">
        <div class="tag">🌀 Churn Overview</div><br>
        Churn is consistent across plans at <span class="critical">~22%</span> (21.91%–22.08%), suggesting plan tier alone is not a key differentiator. Analyze customer behavior and engagement to identify stronger churn predictors.
    </div>
    """, unsafe_allow_html=True)
    
# =================== Tab 2:Geographic Churn Analysis ========================

def section_geography(dff):
    sh("🌍 Geographic Churn Analysis", "COUNTRY INSIGHTS") 
    
    if dff.empty or "country" not in dff.columns or "churn_flag" not in dff.columns: 
        st.info("No geographic data available for the selected filters.") 
        return 
    
    country_data = ( dff.groupby("country", as_index=False) .agg( customers=("account_id", "nunique"), churned=("churn_flag", "sum"), churn_rate=("churn_flag", "mean") ) ) 
    
    country_data["churn_rate"] *= 100 
    country_data = country_data.sort_values("customers", ascending=False)
    
    # ---------------- Chart 3: Customer Distribution by Country ----------------

    status_data = dff[["country", "churn_flag"]].assign(
        Status=dff["churn_flag"].map(churn_labels),
        country_short=dff["country"].map(country_short).fillna(dff["country"])
    )
    fig1 = px.histogram(
        status_data,
        x="country_short",
        color="Status",
        barmode="stack",
        title="Customer Distribution by Country",
        category_orders={
            "country_short": country_data["country"].map(country_short).fillna(country_data["country"]).tolist()
        },        
        color_discrete_map={"Retained": PAL["purple"],"Churned": PAL["gold"]},    
        labels={"country_short": "Country", "count": "Customers", "Status": "Customer Status"},
    )
    fig1.update_traces(
        customdata=status_data[["country"]].to_numpy(),
        hovertemplate="Country=%{customdata[0]}<br>Status=%{fullData.name}<br>Customers=%{y}<extra></extra>"
    )
    fig1 = style_chart(fig1,y_title="Number of Customers",x_title="")
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- Chart 4: Churn rate by country ----------------

    churn_sorted = country_data.sort_values("churn_rate", ascending=True).copy()
    churn_sorted["country_short"] = churn_sorted["country"].map(country_short).fillna(churn_sorted["country"])
    
    fig2 = px.bar(
        churn_sorted,
        x="churn_rate",
        y="country_short",
        custom_data=["country"],
        orientation="h",
        title="Churn Rate (%) by Country",
        color="churn_rate",
        text=churn_sorted["churn_rate"].map(lambda x: f"{x:.1f}%"),
        labels={
            "churn_rate": "Churn Rate (%)",
            "country_short": "Country"
        },
        template="plotly_dark"
    )
    bar_colors = []

    for rate in churn_sorted["churn_rate"]:
        if rate < 20:
            bar_colors.append(PAL["cyan"])
        elif rate < 30:
            bar_colors.append(PAL["gold"])
        else:
            bar_colors.append(PAL["red"])

    fig2.update_traces(marker_color=bar_colors,
        hovertemplate="Country=%{y}<br>Churn Rate (%)=%{x:.1f}%<extra></extra>"
    )
    fig2 = style_bar(fig2, "Churn Rate (%)", "", template="%{text}")
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- Chart 5: Country × Plan Tier churn heatmap ----------------
    if "plan_tier" in dff.columns:

        heat_data = (
            dff.groupby(["country", "plan_tier"], as_index=False)
            .agg(churn_rate=("churn_flag", "mean"))
        )
        heat_data["Churn Rate (%)"] = heat_data["churn_rate"] * 100

        heatmap = heat_data.assign(
            country_short=heat_data["country"].map(country_short).fillna(heat_data["country"])
        ).pivot(
            index="country_short",
            columns="plan_tier",
            values="Churn Rate (%)"
        )

        fig3 = px.imshow(
            heatmap,
            text_auto=".1f",
            color_continuous_scale=[[0, "#0c1220"],[0.4, PAL["purple"]],[1, PAL["red"]]],
            title="Churn by Country & Plan",
            labels={
                "x": "" ,"y": "" ,"color": "Churn Rate (%)"
            },
            aspect="auto",
            template="plotly_dark"
        )

        fig3.update_layout(coloraxis_showscale=False)
        fig3 = style_chart(fig3,marg=dict(t=48, b=30, l=35, r=10),height=425)
        st.plotly_chart(fig3, use_container_width=True)

    
    st.markdown("""
    <div class="insight-box">
        <div class="tag">🌍 Geographic Insight</div><br>
        Germany has the highest churn rate at <span class="critical">32% (8/25)</span>, while the US records <span class="critical">68 churned customers</span>. Investigate Germany's high churn rate and prioritize US retention efforts because of its larger number of churned customers.
    </div>
    """, unsafe_allow_html=True)

def section_tenure_engagement(dff):
    sh("Tenure & Engagement Analysis", "CUSTOMER LIFECYCLE")

    if dff.empty:
        st.info("No data available for the selected filters.")
        return

    # Prepare tenure order without modifying dff
    tenure_order = ["0–6 Months", "6–12 Months", "1–2 Years", "1+ Years"]
    existing_groups = dff["tenure_group"].dropna().astype(str).unique().tolist()
    ordered_groups = [g for g in tenure_order if g in existing_groups]
    ordered_groups += [g for g in existing_groups if g not in ordered_groups]

    # Chart 5: Churn Rate by Tenure Group
    tenure_data = (
        dff.groupby("tenure_group", observed=True)
        .agg(
            customers=("account_id", "nunique"),
            churned=("churn_flag", "sum"),
            churn_rate=("churn_flag", "mean")
        )
        .reset_index()
    )
    tenure_data["churn_rate"] *= 100

    fig1 = px.bar(
        tenure_data,
        x="tenure_group" ,
        y="churn_rate" ,
        color="churn_rate",
        category_orders={"tenure_group": ordered_groups},
        color_continuous_scale=["#45C4D9", "#A78BFA", "#FF6B6B"],
        text=tenure_data["churn_rate"].map(lambda x: f"{x:.1f}%"),
        title="Churn Rate by Tenure Group",
        labels={
            "tenure_group": "Tenure Group",
            "churn_rate": "Churn Rate (%)"
        }
    )
    fig1.update_traces(hovertemplate="Tenure Group=%{x}<br>Churn Rate (%)=%{y:.1f}%<extra></extra>")
    
    fig1 = style_bar(fig1,"Tenure Group","Churn Rate (%)")
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- Chart 6: Customer Behavior vs Churn ----------------
    metric_options = {
        "Beta Feature Usage (Count)": "beta_feature_usage",
        "Usage Duration (Minutes)": "total_usage_duration",
        "Support Satisfaction (Score)": "avg_satisfaction"
    }
    selected_metric = st.radio(
        "Select behavior metric",
        list(metric_options.keys()),
        horizontal=True,
        key="engagement_metric"
    )

    metric_column = metric_options[selected_metric]

    behavior_data = (
        dff.groupby("churn_flag")
        .agg(average_value=(metric_column, "mean"))
        .reset_index()
    )
    behavior_data["churn_status"] = behavior_data["churn_flag"].map(churn_labels)

    # Set units and format values
    if metric_column == "total_usage_duration":
        behavior_data["average_value"] /= 60
        y_axis_title = "Average Usage Duration (Minutes)"
    elif metric_column == "avg_satisfaction":
        y_axis_title = "Average Satisfaction Score"
    else:   y_axis_title = "Average Beta Feature Uses (Count)"

    behavior_data["average_value"] = behavior_data["average_value"].round(2)

    fig2 = px.bar(
        behavior_data,
        x="churn_status",
        y="average_value",
        color="churn_status",
        color_discrete_map={
            "Retained": PAL["green"],
            "Churned": PAL["red"]
        },
        text="average_value",
        title=f"{selected_metric} vs Churn",
        labels={
            "churn_status": "Churn Status",
            "average_value": y_axis_title
        },
        category_orders={"churn_status": ["Retained", "Churned"]}
    )
    if metric_column == "avg_satisfaction":
        fig2.update_yaxes(range=[0, 5], dtick=1)

    fig2 = style_bar(fig2,"Churn Status",y_axis_title)
    st.plotly_chart(fig2, use_container_width=True)

    # ----------------- Chart 7: Country × Tenure Churn Heatmap -----------------
    heatmap_data = (
        dff.groupby(["country", "tenure_group"], observed=True)
        .agg(churn_rate=("churn_flag", "mean"))
        .reset_index()
    )
    heatmap_data["churn_rate"] *= 100

    heatmap_data["country_short"] = heatmap_data["country"].map(country_short).fillna(heatmap_data["country"])
    
    heatmap_pivot = (
        heatmap_data.pivot(
            index="country_short",
            columns="tenure_group",
            values="churn_rate"
        )
        .reindex(columns=ordered_groups)
    )
    fig3 = px.imshow(
        heatmap_pivot,
        color_continuous_scale=["#101622", "#6C63FF", "#FF6B6B"],
        text_auto=".1f" ,aspect="auto",
        labels={
            "x": "Tenure Group",
            "y": "Country",
            "color": "Churn Rate (%)"
        },
        title="Churn Rate by Country and Tenure"
    )
    fig3.update_layout(coloraxis_showscale=False)
    fig3 = style_chart(fig3, x_title="Tenure Group", y_title="Country",marg=dict(t=48, b=35, l=45, r=10),height=425)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="tag">⏳ Tenure & Engagement Insight</div><br>
        Customers with <span class="critical">1+ years of tenure (31.2% churn rate)</span> are more likely to leave than newer customers, whose churn rate is <strong>18.7%</strong>. This suggests that even long-term customers may need better engagement and retention support.
    </div>
    """, unsafe_allow_html=True)

def section_subscription_behavior(dff):
    sh("Subscription & Behavior", "SUBSCRIPTION INSIGHTS")

    if dff.empty:
        st.info("No data available for the selected filters.")
        return

    # ---------------- Chart 8: Average MRR by Churn Status ----------------
    mrr_data = (
        dff.groupby("churn_flag")
        .agg(
            avg_mrr=("avg_mrr", "mean"),
            customer_count=("account_id", "nunique"),
            total_recorded_mrr=("avg_mrr", "sum")
        )
        .reset_index()
    )
    mrr_data["churn_status"] = mrr_data["churn_flag"].map(churn_labels)
    mrr_data["avg_mrr"] = mrr_data["avg_mrr"].round(2)

    fig1 = px.bar(
        mrr_data,
        x="churn_status",
        y="avg_mrr",
        color="churn_status",
        color_discrete_map={
            "Retained": PAL["green"],
            "Churned": PAL["red"]
        },
        text="avg_mrr",
        custom_data=["customer_count", "total_recorded_mrr"],
        title="Monthly Recurring Revenue by Churn Status",
        labels={
            "churn_status": "Churn Status",
            "avg_mrr": "Average MRR ($)"
        },
        category_orders={"churn_status": ["Retained", "Churned"]}
    )
    fig1.update_traces(
        hovertemplate=(
        "Churn Status = %{x}<br>""Average MRR = $%{y:,.2f}<br>""Customer Count = %{customdata[0]:,.0f}<br>"
        "Total Recorded MRR = $%{customdata[1]:,.2f}""<extra></extra>")
    )   
    fig1 = style_bar(fig1,"Churn Status","Average MRR ($)",template="$%{y:,.2f}")
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- Chart 9: Subscription Changes by Churn Status ----------------
    changes_data = (
        dff.groupby("churn_flag")
        .agg(
            avg_upgrades=("upgrade_count", "mean") ,avg_downgrades=("downgrade_count", "mean")
        )
        .reset_index()
    )
    changes_data["churn_status"] = changes_data["churn_flag"].map(churn_labels)

    changes_long = changes_data.melt(
        id_vars="churn_status",
        value_vars=["avg_upgrades", "avg_downgrades"],
        var_name="change_type",
        value_name="average_changes"
    )
    changes_long["change_type"] = changes_long["change_type"].map({
        "avg_upgrades": "Upgrades" ,"avg_downgrades": "Downgrades"
    })
    changes_long["average_changes"] = changes_long["average_changes"].round(2)

    fig2 = px.bar(
        changes_long,
        x="churn_status",
        y="average_changes",
        color="change_type",
        barmode="group",
        color_discrete_map={
            "Upgrades": PAL["cyan"] ,"Downgrades": PAL["orange"]
        },
        text="average_changes",
        title="Subscription Changes by Churn Status",
        labels={
            "churn_status": "Churn Status",
            "average_changes": "Average Number of Changes",
            "change_type": "Subscription Change"
        },
        category_orders={
            "churn_status": ["Retained", "Churned"] ,"change_type": ["Upgrades", "Downgrades"]
        }
    )
    fig2 = style_bar(fig2,"Churn Status","Average Number of Changes")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="tag">💳 Subscription Behavior Insight</div><br>
        Churned customers average <span class="critical">$2,082.92 MRR</span>, compared with <strong>$2,315.30</strong> for retained customers—a <strong>$232.38 higher MRR</strong> among retained customers. Investigate whether subscription value and customer engagement influence churn.
    </div>
    """, unsafe_allow_html=True)

# ============================ Tab 5: Classification Model ============================
MODEL_RESULTS = {
    "Logistic Regression": {"Accuracy": 0.650,"Precision": 0.303,"Recall": 0.455,"F1": 0.364,"ROC-AUC": 0.646},
    "Random Forest":       {"Accuracy": 0.850,"Precision": 0.818,"Recall": 0.409,"F1": 0.545,"ROC-AUC": 0.810},
    "Gradient Boosting":   {"Accuracy": 0.900,"Precision": 0.929,"Recall": 0.591,"F1": 0.722,"ROC-AUC": 0.805}
}
@st.cache_resource
def load_model_artifacts():
    project_dir = Path(__file__).parent
    model_dir = project_dir / "models"
    output_dir = project_dir / "outputs"

    model = joblib.load(model_dir / "churn_model.pkl")
    threshold = joblib.load(model_dir / "churn_threshold.pkl")
    feature_importance = pd.read_csv(output_dir / "feature_importance.csv")
    confusion_matrix_df = pd.read_csv(
        output_dir / "confusion_matrix.csv", index_col=0
    )

    return model, threshold, feature_importance, confusion_matrix_df

def section_classification():
    sh("Classification Model", "MACHINE LEARNING")
    
    try:
        model, threshold, feature_importance, cm_df = load_model_artifacts()
    except Exception as e:
        st.error(f"Unable to load classification artifacts: {e}")
        st.info(
            "Check that churn_model.pkl, churn_threshold.pkl, "
            "feature_importance.csv and confusion_matrix.csv exist ""in the expected project folders."
        )
        return

    # Extract the threshold
    if isinstance(threshold, dict):
        threshold = next(iter(threshold.values()))

    threshold = float(threshold)

    # Final test metrics
    metrics = {
        "Accuracy": 0.900,"Precision": 0.800,"Recall": 0.727,"F1 Score": 0.762,"ROC-AUC": 0.876
    }
    metric_colors = [
        PAL["blue"], PAL["green"], PAL["gold"],PAL["purple"], PAL["cyan"]
    ]
    cards = []

    for (label, value), color in zip(metrics.items(), metric_colors):
        cards.append(
            f'<div class="model-kpi-card" style="'
            f'background:linear-gradient(145deg,#171C2B,#111522);'
            f'border:1px solid #2A3043;'
            f'border-top:3px solid {color};'
            f'border-radius:12px;'
            f'padding:15px 10px;'
            f'min-width:0;box-sizing:border-box;">'
            f'<div class="model-kpi-label" '
            f'style="font-size:12px;color:#A5AEC4;">'
            f'{label}</div>'
            f'<div class="model-kpi-value" style="'
            f'font-size:25px;font-weight:700;'
            f'color:#F1F5F9;margin-top:9px;">'
            f'{value:.1%}</div>'
            f'</div>'
        )
    html = (
        '<div class="model-kpi-row">'
        + "".join(cards)
        + '</div>'
    )
    st.markdown(html, unsafe_allow_html=True)
    st.markdown(
        "<div style='height:20px;'></div>",
        unsafe_allow_html=True
    )

    # ---------------- Chart 10 — Model Performance Comparison ----------------
    comparison_df = (
        pd.DataFrame.from_dict(MODEL_RESULTS, orient="index")
        .rename_axis("Model")
        .reset_index()
        .melt(id_vars="Model", var_name="Metric", value_name="Score")
    )
    comparison_df["Score"] *= 100

    fig = px.bar(
        comparison_df,
        x="Model", y="Score", title=" ",
        color="Metric", barmode="group",
        text=comparison_df["Score"].round(1),
        color_discrete_map={
            "Accuracy": PAL["blue"], "Precision": PAL["green"],
            "Recall": PAL["gold"], "F1": PAL["purple"],
            "ROC-AUC": PAL["cyan"]
        }
    )
    fig = style_bar(
        fig, x_title="Model", y_title="Score (%)", template="%{text:.1f}%",
        legend=True, radius=0, height=480,
        marg=dict(t=100, b=55, l=8, r=8),
        legend_layout=dict(
            orientation="h", x=0.5, xanchor="center",
            y=1.08, yanchor="bottom",
            font=dict(size=10)
        )
    )
    fig.update_layout(
        bargap=0.10,
        bargroupgap=0.04,
        uniformtext_minsize=8,
        uniformtext_mode="hide"
    )
    fig.update_xaxes(
        automargin=True,
        tickangle=0,
        tickfont=dict(size=10)
    )
    fig.update_yaxes(
        range=[0, 115],
        ticksuffix="%",
        tickfont=dict(size=10)
    )
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "Model=%{x}<br>"
            "Metric=%{fullData.name}<br>"
            "Score=%{y:.1f}%<extra></extra>"
        )
    )

    st.markdown("#### Classification Model Performance")
    st.markdown(
        '<div style="color:#929DB4;font-size:0.82rem;margin:-8px 0 12px 2px;">Comparison of candidate models using previously recorded validation results.</div>',
        unsafe_allow_html=True
    )
    st.plotly_chart(fig, use_container_width=True, config={"responsive": True})

    # ---------------- Chart 11 — Confusion Matrix ----------------
    expected_rows = ["Actual Retained", "Actual Churned"] 
    expected_cols = ["Predicted Retained", "Predicted Churned"]
    cm_df = cm_df.loc[expected_rows, expected_cols].astype(int)

    cm_df.index = ["Retained", "Churned"]
    cm_df.columns = ["Retained", "Churned"]

    fig_cm = px.imshow(
        cm_df,
        text_auto=True,
        title="Confusion Matrix — Final Model",
        color_continuous_scale=[[0, "#171C2B"],[0.5, "#5654A5"],[1, "#00D4AA"]],
        aspect="auto",
        labels={
            "x": "Predicted Status",
            "y": "Actual Status",
            "color": "Customers"
        }
    )
    fig_cm.update_traces(
        texttemplate="%{z}",textfont=dict(size=16),
        hovertemplate=("Actual: %{y}<br>""Predicted: %{x}<br>""Customers: %{z}<extra></extra>")
    )
    fig_cm.update_layout(
        xaxis=dict(title="Predicted Status",side="bottom",automargin=True,tickfont=dict(size=11)),
        yaxis=dict(title="Actual Status",automargin=True,tickfont=dict(size=11)),
        coloraxis_showscale=False
    )
    st.plotly_chart(
        style_chart(fig_cm,"Predicted Status","Actual Status",
            marg=dict(t=55, b=55, l=12, r=12),height=400
        ),
        use_container_width=True,config={"responsive": True}
    )
    
    # ---------------- Chart 12: Feature Importance ----------------
    feature_col = next((c for c in ["feature", "Feature", "feature_name"] if c in feature_importance.columns), None)
    importance_col = next((c for c in ["importance", "Importance", "feature_importance"] if c in feature_importance.columns), None)

    if feature_col and importance_col:
        top_features = feature_importance.nlargest(10, importance_col).sort_values(importance_col).copy()
        feature_names = dict(zip(["Avg Mrr", "Auto Renew Count", "Tenure Months", "Total Usage Duration", "Total Errors", "Upgrade Count", "Seats", "Total Tickets", "Avg Response Minutes", "Total Usage"], 
            ["AVG MRR", "Auto Renew", "Tenure Months", "Usage Duration", "Total Errors", "Upgrade Count", "Seats", "Total Tickets", "Response Minutes", "Total Usage"]))
        top_features["feature_label"] = top_features[feature_col].replace(feature_names)        
        
        fig_imp = px.bar(
            top_features, x=importance_col, y="feature_label", orientation="h",
            text=top_features[importance_col].round(3), color=importance_col,
            color_continuous_scale=["#5654A5", "#00D4AA"],
            title="Top Features Influencing Churn",
            labels={importance_col: "Importance", "feature_label": "Feature"},
            custom_data=[feature_col]
        )
        fig_imp.update_traces(
            textposition="outside", cliponaxis=False,
            hovertemplate="Feature=%{customdata[0]}<br>Importance=%{x:.3f}<extra></extra>"
        )
        fig_imp.update_layout(coloraxis_showscale=False,bargap=0.25,)
        fig_imp.update_yaxes(automargin=False, ticklabelstandoff=3)

        st.plotly_chart(style_chart(fig_imp, "Importance", "Feature", height=420,
            marg=dict(l=5, r=29, t=50, b=35)),use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
        <div class="tag">🤖 Model Performance Insight</div><br>
        Selected model: <strong>Gradient Boosting</strong> &nbsp;|&nbsp; Decision threshold: <strong>{threshold:.2f}</strong><br>
        <strong>Average MRR</strong> is the most influential churn predictor, contributing <strong>52.8%</strong> of total feature importance, followed by <strong>Auto Renew Count (15.2%)</strong> and <strong>Tenure Months (14.6%)</strong>. Together, these three features account for <strong>82.0%</strong> of total feature importance.
    </div>
    """, unsafe_allow_html=True)

# ============================ Tab 6: Prediction & Risk ============================
def risk_level(probability):
    if probability >= 0.60:     return "HIGH", PAL["red"], "🔴"
    elif probability >= 0.30:   return "MEDIUM", PAL["gold"], "🟡"
    return "LOW", PAL["green"], "🟢"


def prediction_card(label, value, color, subtitle=""):
    return f"""
        <div class="prediction-card" style="--accent:{color}">
            <div class="prediction-label">{label}</div>
            <div class="prediction-value">{value}</div>
            <div class="prediction-subtitle">{subtitle}</div>
        </div>
    """

def prediction_cards(cards):
    html = '<div class="prediction-grid">'
    html += "".join(prediction_card(*card) for card in cards)
    html += '</div>'
    st.html(html)


def section_prediction(df):
    sh("Customer Churn Risk Prediction", "PREDICTION ENGINE")

    try:
        model, threshold, _, _ = load_model_artifacts()
        threshold = float(
            next(iter(threshold.values()))
            if isinstance(threshold, dict) else threshold
        )
    except Exception as e:
        st.error(f"Unable to load prediction model: {e}")
        return

    if df.empty:
        st.warning("No customer records are available for the current filters.")
        return

    customer_ids = sorted(
        df["account_id"].dropna().astype(str).unique().tolist()
    )

    selected_id = st.selectbox(
        "Customer Account",
        options=customer_ids,
        index=None,
        placeholder="Search by customer ID...",
        key="prediction_customer"
    )

    if selected_id is not None:
        customer = df.loc[
            df["account_id"].astype(str) == selected_id
        ].iloc[0]

        sh("Customer Profile", "SELECTED ACCOUNT")

        st.dataframe(
            customer.to_frame().T,
            use_container_width=True,
            hide_index=True
        )

        sh("Churn Prediction", "MODEL ANALYSIS")

        features = list(getattr(model, "feature_names_in_", []))

        try:
            customer_features = customer[features].to_frame().T
            probabilities = model.predict_proba(customer_features)[0]
            classes = list(model.classes_)

            probability = float(probabilities[classes.index(1)])
            prediction = probability >= threshold
            risk, color, emoji = risk_level(probability)

            
            prediction_cards([
                ("Churn Probability", f"{probability:.1%}", PAL["blue"], "Estimated probability of churn"),
                ("Risk Category", f"{emoji} {risk}", color, "Based on churn probability"),
                ("Model Prediction", "Likely to Churn" if prediction else "Likely to Stay",
                PAL["orange"] if prediction else PAL["cyan"], f"Decision threshold: {threshold:.1%}")
            ])
              
            # Dynamic Customer Risk Insight
            if risk == "HIGH":
                insight = (
                    f'This customer has a '
                    f'<span class="risk">{probability:.1%} predicted churn probability</span>. '
                    f'Prioritise immediate retention outreach and investigate possible reasons for leaving.'
                        )
            elif risk == "MEDIUM":
                insight = (
                    f'This customer has a '
                    f'<span class="highlight">{probability:.1%} predicted churn probability</span>. '
                    f'Monitor engagement and consider proactive retention outreach before the risk increases.'
                )
            else:
                insight = (
                    f'This customer has a '
                    f'<span class="positive">{probability:.1%} predicted churn probability</span>. '
                    f'Continue regular engagement and monitor for changes in churn risk.'
                )

            st.markdown(f"""
            <div class="insight-box">
                <div class="tag">🎯 Customer Risk Insight</div><br>
                {insight}
                <div style="height:12px"></div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Unable to generate churn prediction: {e}")

    sh("Cleaned Customer Dataset", "FILTERED DATA EXPORT")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    csv_data = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 Download Cleaned Customer Data (CSV)",
        data=csv_data,
        file_name="saas_cleaned_customer_data.csv",
        mime="text/csv",
        use_container_width=True,key="download_customer_data"
    )

# ----------------------------- Main -----------------------------

def main():
    st.set_page_config(
        page_title="ChurnSight | SaaS Subscription Prediction",
        page_icon="🧩",
        layout="wide"
    )
    df = load_data()

    apply_theme()

    filters = render_sidebar(df)
    dff = apply_filters(df, filters)

    render_header()
    render_kpis(dff)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🌀 Churn Overview",
        "🌍 Geography",
        "⏳ Tenure & Engagement",
        "💳 Subscription & Behavior",
        "🤖 Classification Model",
        "🎯 Prediction & Risk"
    ])

    with tab1:
        section_overview(dff)
    with tab2:
        section_geography(dff)
    with tab3:
        section_tenure_engagement(dff)
    with tab4:
        section_subscription_behavior(dff)
    with tab5:
        section_classification()
    with tab6:
        section_prediction(dff)

    recommendation_card()


if __name__ == "__main__":
    main()