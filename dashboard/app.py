import streamlit as st
import os
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Weather Insights Hub",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
<style>
    /* Dark Mode Premium Theme */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #ffffff;
    }
    
    /* Metrics Highlighting */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 5% 5% 5% 10%;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    
    label[data-testid="stMetricLabel"] p {
        color: #a0aec0 !important;
        font-size: 1.1rem;
        font-weight: 500;
    }
    div[data-testid="stMetricValue"] {
        color: #63b3ed !important;
        font-weight: bold;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }
    h1 {
        background: -webkit-linear-gradient(45deg, #90cdf4, #63b3ed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    /* Hide top padding */
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data(ttl=600)
def load_data():
    try:
        host = os.environ.get("POSTGRES_HOST", "localhost")
        user = os.environ.get("POSTGRES_USER", "weather_user")
        password = os.environ.get("POSTGRES_PASSWORD", "weather_pass")
        dbname = os.environ.get("POSTGRES_DB", "weather_db")
        
        db_url = f"postgresql://{user}:{password}@{host}:5432/{dbname}"
        engine = create_engine(db_url)
        
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'mart_daily_weather_stats' not in tables:
            st.warning("⚠️ Les données de la table 'mart_daily_weather_stats' ne sont pas encore disponibles. Veuillez exécuter la pipeline Dagster.")
            return None, None
            
        df_daily = pd.read_sql("SELECT * FROM mart_daily_weather_stats ORDER BY date_day", engine)
        
        if 'raw_weather' in tables:
            df_hourly = pd.read_sql("SELECT * FROM raw_weather ORDER BY time", engine)
        else:
            df_hourly = None
            
        return df_daily, df_hourly
    except Exception as e:
        st.error(f"Erreur de connexion à PostgreSQL: {e}")
        return None, None

df_daily, df_hourly = load_data()

# --- HEADER SECTION ---
st.title("🌤️ Weather Insights Hub")
st.markdown("### Analyse avancée et tendance météorologiques")

if df_daily is not None and not df_daily.empty:
    
    # 1. KPIs Section
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    latest_date = df_daily['date_day'].max()
    latest_data = df_daily[df_daily['date_day'] == latest_date].iloc[0]
    
    avg_temp_overall = df_daily['avg_temperature_celsius'].mean()
    
    col1.metric("Date", str(latest_date))
    col2.metric("Temp. Moyenne (J. Actuel)", f"{latest_data['avg_temperature_celsius']:.1f} °C", 
                 f"{latest_data['avg_temperature_celsius'] - avg_temp_overall:.1f} vs Moyenne",
                 delta_color="normal")
    col3.metric("Temp. Max (J. Actuel)", f"{latest_data['max_temperature_celsius']:.1f} °C")
    col4.metric("Temp. Min (J. Actuel)", f"{latest_data['min_temperature_celsius']:.1f} °C")
    
    st.markdown("---")
    
    # 2. Main Visualization Section (Daily Trend)
    st.markdown("### 📈 Tendance Journalière")
    
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=df_daily['date_day'], y=df_daily['max_temperature_celsius'],
        mode='lines+markers', name='Max Temp',
        line=dict(color='#fc8181', width=3),
        marker=dict(size=8, color='#fc8181')
    ))
    fig_daily.add_trace(go.Scatter(
        x=df_daily['date_day'], y=df_daily['avg_temperature_celsius'],
        mode='lines+markers', name='Avg Temp',
        line=dict(color='#63b3ed', width=4),
        marker=dict(size=10, color='#63b3ed')
    ))
    fig_daily.add_trace(go.Scatter(
        x=df_daily['date_day'], y=df_daily['min_temperature_celsius'],
        mode='lines+markers', name='Min Temp',
        line=dict(color='#81e6d9', width=3),
        marker=dict(size=8, color='#81e6d9')
    ))
    
    fig_daily.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title="Évolution des Températures (°C)",
        hovermode="x unified",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Température (°C)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # 3. Detailed Hourly Data (if available)
    if df_hourly is not None and not df_hourly.empty:
        st.markdown("### 🕒 Détails Horaires")
        
        # Convert time to datetime if it's not already
        df_hourly['time'] = pd.to_datetime(df_hourly['time'])
        
        fig_hourly = px.area(
            df_hourly, x='time', y='temperature_2m', 
            color_discrete_sequence=['#9f7aea'],
            title="Température Horaire Historique"
        )
        
        fig_hourly.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, title="Heure"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Température (°C)")
        )
        
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Dataframe preview
    with st.expander("Voir les données brutes"):
        st.dataframe(df_daily.style.background_gradient(cmap='Blues'), use_container_width=True)
else:
    st.info("Lancez votre workflow Dagster pour importer et transformer les données depuis l'API Open-Meteo, afin qu'elles s'affichent ici.")
