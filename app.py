
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# PAGE CONFIGURATION
# ==========================================
BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Bloom | Customer Intelligence",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <div style="
        padding: 22px 26px;
        border-radius: 16px;
        background: linear-gradient(120deg, #E8F3EC, #F7FAF8);
        border: 1px solid #D5E7DA;
        margin-bottom: 24px;
    ">
        <h1 style="
            color: #216E49;
            margin: 0;
            font-size: 30px;
        ">🌿 Bloom Customer Intelligence</h1>
        <p style="
            color: #52665A;
            margin: 8px 0 0 0;
            font-size: 15px;
        ">
            Understand customers. Predict churn. Improve retention.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# PASTEL PINK + PISTA GREEN DESIGN
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --pink: #C97891;
    --pink-light: #FCE8EE;
    --pink-dark: #794657;
    --pista: #EAF2E5;
    --green: #709579;
    --green-dark: #42674B;
}

.stApp {
    background: linear-gradient(135deg, #FFF7F8, #FFFCFA 55%, #F0F5EC);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F9E4EA, #F2E9ED 65%, #EAF2E5);
    border-right: 1px solid #EAD5DE;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
h1, h2, h3 {
    color: #794657;
    font-family: 'Playfair Display', serif;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid #EEDCE2;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 5px 20px rgba(121,70,87,0.05);
}

[data-testid="stMetricLabel"] {
    color: #896B78;
}

[data-testid="stMetricValue"] {
    color: #794657;
    font-weight: 700;
}

div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.86);
    border: 1px solid #E6EBDD;
    border-radius: 18px;
    padding: 10px;
}

.stButton > button, .stDownloadButton > button {
    background: #C97891;
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    background: #A85F78;
    color: white;
    border: none;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E7DCE1;
    border-radius: 14px;
}

.hero {
    background: linear-gradient(120deg, #F8E1E8, #EEF5E8);
    padding: 28px 30px;
    border: 1px solid #EADCE0;
    border-radius: 22px;
    margin-bottom: 22px;
}

.hero h1 {
    margin: 4px 0;
    font-size: 2.2rem;
}

.hero p {
    color: #806A75;
    margin-bottom: 0;
}

.eyebrow {
    color: #A65E79;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #EADBE0;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():
    sales_file = BASE_DIR / "data" / "processed" / "online_retail_cleaned.csv"
    segments_file = BASE_DIR / "data" / "processed" / "customer_segments.csv"
    forecast_file = BASE_DIR / "data" / "processed" / "sales_forecast.csv"

    # Load sales data
    sales = pd.read_csv(
        sales_file,
        encoding="latin1",
        low_memory=False
    )
    sales["InvoiceDate"] = pd.to_datetime(
        sales["InvoiceDate"], errors="coerce"
    )
    sales["TotalSales"] = pd.to_numeric(
        sales["TotalSales"], errors="coerce"
    )
    sales = sales.dropna(subset=["InvoiceDate", "TotalSales"])

    # Load customer segments
    segments = pd.read_csv(segments_file, low_memory=False)
    segments.columns = segments.columns.str.strip()

    if "Cluster" in segments.columns:
        segments["Cluster"] = segments["Cluster"].astype(str)
    elif "cluster" in segments.columns:
        segments["cluster"] = segments["cluster"].astype(str)
    else:
        st.warning("Cluster column not found in customer_segments.csv")

    # Load sales forecast
    forecast = pd.read_csv(forecast_file)
    forecast["Date"] = pd.to_datetime(
        forecast["Date"], errors="coerce"
    )
    forecast["ForecastSales"] = pd.to_numeric(
        forecast["ForecastSales"], errors="coerce"
    )

    return sales, segments, forecast


try:
    sales, segments, forecast = load_data()
except FileNotFoundError as error:
    st.error(f"Cannot find a required data file: {error.filename}")
    st.markdown("""
    **Check these files in your project:**
    - `data/processed/online_retail_cleaned.csv`
    - `data/processed/customer_segments.csv`
    - `data/processed/sales_forecast.csv`

    Run your segmentation and forecasting scripts first if the output files
    have not yet been created.
    """)
    st.stop()
except Exception as error:
    st.error(f"Unable to load the project data: {error}")
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("# 🌸 Bloom")
    st.caption("CUSTOMER INTELLIGENCE")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Sales Analytics",
            "Customer Segments",
            "Sales Forecast",
            "Customer Churn Prediction",
            "Explore Data"
        ]
    )

    st.markdown("---")
    st.caption("Made with Python & Streamlit")
    st.caption("Pastel Analytics Edition 🌿")

# ==========================================
# HELPER: HERO HEADER
# ==========================================
def show_hero(eyebrow, title, subtitle):
    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# OVERVIEW
# ==========================================
if page == "Overview":

    show_hero(
        "YOUR BUSINESS, UNDERSTOOD",
        "Customer Intelligence 🌸",
        "Discover sales patterns, understand customers, and make data-informed decisions."
    )

    total_sales = sales["TotalSales"].sum()
    total_orders = sales["InvoiceNo"].nunique()
    total_customers = sales["CustomerID"].nunique()
    total_products = sales["StockCode"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"£{total_sales:,.0f}")
    c2.metric("Orders", f"{total_orders:,}")
    c3.metric("Customers", f"{total_customers:,}")
    c4.metric("Products", f"{total_products:,}")

    st.markdown("### 🌷 Sales at a glance")

    monthly = (
        sales.set_index("InvoiceDate")["TotalSales"]
        .resample("MS").sum()
        .reset_index()
    )

    fig = px.area(
        monthly,
        x="InvoiceDate",
        y="TotalSales",
        markers=True,
        title="Monthly Revenue Trend",
        color_discrete_sequence=["#C97891"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#794657",
        xaxis_title="Month",
        yaxis_title="Revenue (£)",
        margin=dict(l=20, r=20, t=55, b=20)
    )
    st.plotly_chart(fig, width="stretch")

    left, right = st.columns(2)

    with left:
        st.markdown("### 🌿 Sales by country")
        country_sales = (
            sales.groupby("Country")["TotalSales"]
            .sum()
            .nlargest(8)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            country_sales,
            x="TotalSales",
            y="Country",
            orientation="h",
            color_discrete_sequence=["#86A98B"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#794657",
            xaxis_title="Revenue (£)",
            yaxis_title=""
        )
        st.plotly_chart(fig, width="stretch")

    with right:
        st.markdown("### 🌸 Customer cluster sizes")

        if "Cluster" in segments.columns:
            counts = (
                segments["Cluster"].astype(str)
                .value_counts()
                .rename_axis("Cluster")
                .reset_index(name="Customers")
            )

            fig = px.pie(
                counts,
                names="Cluster",
                values="Customers",
                hole=0.55,
                color_discrete_sequence=[
                    "#C97891", "#91B79A", "#EBC4D0",
                    "#A8C6A5", "#DDA5B6", "#D6E6CD"
                ]
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#794657"
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Run the segmentation script to create Cluster labels.")

# ==========================================
# SALES ANALYTICS
# ==========================================
elif page == "Sales Analytics":

    show_hero(
        "REVENUE & PERFORMANCE",
        "Sales Analytics 📈",
        "Explore revenue across countries, products, and time."
    )

    countries = sorted(sales["Country"].dropna().unique().tolist())
    selected_country = st.selectbox(
        "Choose a country",
        ["All Countries"] + countries
    )

    filtered = sales.copy()
    if selected_country != "All Countries":
        filtered = filtered[filtered["Country"] == selected_country]

    col1, col2 = st.columns(2)
    col1.metric("Revenue", f"£{filtered['TotalSales'].sum():,.2f}")
    col2.metric("Unique Orders", f"{filtered['InvoiceNo'].nunique():,}")

    monthly = (
        filtered.set_index("InvoiceDate")["TotalSales"]
        .resample("MS").sum()
        .reset_index()
    )

    fig = px.bar(
        monthly,
        x="InvoiceDate",
        y="TotalSales",
        title="Monthly Sales",
        color_discrete_sequence=["#91B79A"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#794657"
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Best-selling products")
    products = (
        filtered.groupby("Description")["TotalSales"]
        .sum()
        .nlargest(10)
        .sort_values()
        .reset_index()
    )

    fig = px.bar(
        products,
        x="TotalSales",
        y="Description",
        orientation="h",
        color_discrete_sequence=["#C97891"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#794657",
        yaxis_title="",
        xaxis_title="Revenue (£)"
    )
    st.plotly_chart(fig, width="stretch")

# ==========================================
# CUSTOMER SEGMENTS
# ==========================================
elif page == "Customer Segments":

    show_hero(
        "KNOW YOUR CUSTOMERS",
        "Customer Segments 👥",
        "Explore groups created by your K-Means clustering model."
    )

    if "Cluster" not in segments.columns:
        st.warning("The Cluster column is missing. Run src/segmentation.py first.")
        st.stop()

    cluster_counts = (
        segments["Cluster"].astype(str)
        .value_counts()
        .rename_axis("Cluster")
        .reset_index(name="Customers")
    )

    fig = px.bar(
        cluster_counts,
        x="Cluster",
        y="Customers",
        color="Cluster",
        title="Customers per Cluster",
        color_discrete_sequence=[
            "#C97891", "#91B79A", "#EBC4D0",
            "#A8C6A5", "#DDA5B6", "#D6E6CD"
        ]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#794657",
        showlegend=False
    )
    st.plotly_chart(fig, width="stretch")

    metrics = [
        col for col in ["Recency", "Frequency", "Monetary"]
        if col in segments.columns
    ]

    if metrics:
        summary = segments.groupby("Cluster")[metrics].mean().round(2)
        st.markdown("### 🌿 Cluster profiles")
        st.dataframe(summary, width="stretch")

    st.markdown("### Customer records")
    st.dataframe(segments, width="stretch")

    st.download_button(
        "Download customer segments",
        data=segments.to_csv(index=False).encode("utf-8"),
        file_name="customer_segments.csv",
        mime="text/csv"
    )

# ==========================================
# SALES FORECAST
# ==========================================
elif page == "Sales Forecast":

    show_hero(
        "PLAN AHEAD",
        "Sales Forecast 🔮",
        "Explore your baseline model's predicted sales for the next 30 days."
    )

    forecast_clean = forecast.dropna(
        subset=["Date", "ForecastSales"]
    ).sort_values("Date")

    if forecast_clean.empty:
        st.warning("No valid forecast records are available.")
        st.stop()

    c1, c2 = st.columns(2)
    c1.metric(
        "30-day forecast total",
        f"£{forecast_clean['ForecastSales'].sum():,.2f}"
    )
    c2.metric(
        "Average daily forecast",
        f"£{forecast_clean['ForecastSales'].mean():,.2f}"
    )

    fig = px.line(
        forecast_clean,
        x="Date",
        y="ForecastSales",
        markers=True,
        title="Predicted Daily Sales",
        color_discrete_sequence=["#C97891"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#794657",
        xaxis_title="Date",
        yaxis_title="Forecast revenue (£)"
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("### Forecast details")
    st.dataframe(forecast_clean, width="stretch")

    st.download_button(
        "Download forecast CSV",
        data=forecast_clean.to_csv(index=False).encode("utf-8"),
        file_name="sales_forecast.csv",
        mime="text/csv"
    )

    st.caption(
        "Forecasts are estimates from a baseline model and are not guaranteed results."
    )

# ==========================================
# EXPLORE DATA
# ==========================================
elif page == "Explore Data":

    show_hero(
        "YOUR DATASET",
        "Explore the Data 🪴",
        "Inspect transaction records and download data for further analysis."
    )

    st.markdown("### Filter transactions")

    countries = sorted(sales["Country"].dropna().unique().tolist())
    selected_country = st.selectbox("Country filter", ["All Countries"] + countries)

    filtered = sales.copy()
    if selected_country != "All Countries":
        filtered = filtered[filtered["Country"] == selected_country]

    start_date = filtered["InvoiceDate"].min().date()
    end_date = filtered["InvoiceDate"].max().date()

    date_range = st.date_input(
        "Invoice date range",
        value=(start_date, end_date)
    )

    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            filtered["InvoiceDate"].dt.date.between(start, end)
        ]

    st.write(f"**Rows shown:** {len(filtered):,}")
    st.dataframe(filtered, width="stretch")

    st.download_button(
        "Download filtered transactions",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_transactions.csv",
        mime="text/csv"
    )

# ==========================================
# CUSTOMER CHURN PREDICTION
# ==========================================    
elif page == "Customer Churn Prediction":
   
    st.title("Customer Churn Prediction")
    st.success("Step 1: Churn page selected.")

    try:
        from src.churn_dashboard import show_churn_dashboard

        st.success("Step 2: Dashboard imported successfully.")
        show_churn_dashboard()

    except Exception as error:
        st.error("The churn dashboard encountered an error:")
        st.exception(error)



# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#987987;'>"
    "🌸 Bloom Customer Intelligence · Built with Python, "
    "Pandas, Plotly & Streamlit 🌿"
    "</p>",
    unsafe_allow_html=True
)