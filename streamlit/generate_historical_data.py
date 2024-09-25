import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Função para gerar dados históricos de exemplo (substitua com dados reais)
def generate_historical_data():
    now = datetime.now()
    data = {
        "Run Timestamp": [now - timedelta(days=i) for i in range(10)],
        "Status": ["Success", "Success", "Failed", "Success", "Success", "Failed", "Success", "Success", "Success", "Success"],
        "Errors": [None, None, "Timeout", None, None, "Connection Error", None, None, None, None],
        "Scraping Time (min)": [10, 9, 12, 8, 7, 10, 9, 8, 7, 6],
        "Loading Time (min)": [5, 6, 7, 5, 4, 6, 5, 5, 4, 3],
        "Data Volume (records)": [15000, 16000, 12000, 17000, 18000, 14000, 17500, 18000, 18500, 19000],
    }
    return pd.DataFrame(data)

# Função para mostrar o histórico de execuções
def show_run_history(df):
    st.subheader("📅 Run History")
    st.dataframe(df[['Run Timestamp', 'Status', 'Errors']])

# Função para mostrar tendências de desempenho
def show_performance_trends(df):
    st.subheader("📈 Performance Trends")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Run Timestamp"], df["Scraping Time (min)"], marker='o', label="Scraping Time (min)")
    ax.plot(df["Run Timestamp"], df["Loading Time (min)"], marker='o', label="Loading Time (min)")
    ax.set_xlabel("Run Timestamp")
    ax.set_ylabel("Time (minutes)")
    ax.set_title("Performance Trends Over Time")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Função para mostrar tendências de volume de dados
def show_data_volume_trends(df):
    st.subheader("📊 Data Volume Trends")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["Run Timestamp"], df["Data Volume (records)"], marker='o', color='green', label="Data Volume (records)")
    ax.set_xlabel("Run Timestamp")
    ax.set_ylabel("Data Volume (records)")
    ax.set_title("Data Volume Trends Over Time")
    ax.grid(True)
    st.pyplot(fig)

# Função principal para a página de dados históricos
def show_historical_data():
    st.title("📜 Historical Data")

    # Gerar dados históricos (substitua com a coleta de dados reais)
    df = generate_historical_data()

    # Exibir o histórico de execuções
    show_run_history(df)

    # Exibir tendências de desempenho
    show_performance_trends(df)

    # Exibir tendências de volume de dados
    show_data_volume_trends(df)

# Função principal para controle de navegação entre páginas
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Historical Data"])

    if page == "Historical Data":
        show_historical_data()

# Executar o app
if __name__ == "__main__":
    main()
