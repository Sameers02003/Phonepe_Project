import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import os

# ✅ Verify GeoJSON Exists
geojson_path = "india_state.geojson"
if not os.path.exists(geojson_path):
    st.error("GeoJSON file not found! Ensure it's in the correct directory.")

# ✅ Load Indian GeoJSON File
with open(geojson_path, "r") as file:
    india_geojson = json.load(file)

# ✅ MySQL Connection Function
def get_data(query):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Dijas@19110',
        database='phonepe_insights'
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ✅ Streamlit App Title
st.title("PhonePe Pulse Insights")

# 🔹 Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Business Case Study"])

# 🔹 Home Page - Transaction Visualizations
if page == "Home":
    st.subheader("📊 PhonePe Transaction Insights")
    option = st.sidebar.selectbox("Select Visualization", ["Transaction Overview", "Category Insights", "State-Wise Trends"])

    # 🔹 Transaction Overview
    if option == "Transaction Overview":
        query = "SELECT year, quarter, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY year, quarter"
        df = get_data(query)

        st.subheader("Total Sum of Transaction Amount per Year and Quarter")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="year", y="total_amount", hue="quarter", data=df, ax=ax)
        plt.title("Yearly Transaction Amount (Quarterly Breakdown)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # 🔹 Category Insights
    elif option == "Category Insights":
        query = "SELECT transaction_type, SUM(transaction_amount) AS total_amount FROM aggregated_transaction GROUP BY transaction_type"
        df = get_data(query)

        st.subheader("Transaction Amount by Type")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="transaction_type", y="total_amount", data=df, ax=ax)
        plt.title("Transaction Amount by Type")
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # 🔹 State-Wise Trends WITH Quarter Selection
    elif option == "State-Wise Trends":
        selected_quarter = st.sidebar.selectbox("Choose a Quarter:", [1, 2, 3, 4])

        query = f"""
            SELECT state, SUM(transaction_amount) AS total_amount
            FROM aggregated_transaction
            WHERE quarter={selected_quarter}
            GROUP BY state
        """
        df = get_data(query)

        st.subheader(f"State-Wise Transaction Amount for Quarter {selected_quarter}")
        st.dataframe(df)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="state", y="total_amount", data=df, ax=ax)
        plt.title(f"State-Wise Transaction Amount for Quarter {selected_quarter}")
        plt.xticks(rotation=90)
        st.pyplot(fig)

# 🔹 Business Case Study Section
elif page == "Business Case Study":
    st.subheader("📌 Business Case Study Solutions")

    case_option = st.sidebar.selectbox("Select Case Study", [
        "Decoding Transactions",
        "Device & User Analysis",
        "Insurance & Growth Analysis",
        "Market Transaction Analysis",
        "User & Growth Strategies"
    ])

    query_options = {
        "Decoding Transactions": [
            "SELECT state, SUM(Transaction_amount) AS Total_transaction_value FROM aggregated_transaction GROUP BY state ORDER BY Total_transaction_value DESC;",
            "SELECT state, SUM(Transaction_count) AS Total_transactions FROM aggregated_transaction GROUP BY state ORDER BY Total_transactions DESC;",
            "SELECT year, state, SUM(Transaction_amount) AS Yearly_transaction_value FROM aggregated_transaction GROUP BY year, state ORDER BY year, Yearly_transaction_value DESC;",
            "SELECT quarter, state, SUM(Transaction_amount) AS Quarterly_transaction_value FROM aggregated_transaction GROUP BY quarter, state ORDER BY quarter, Quarterly_transaction_value DESC;",
            "SELECT state, SUM(Transaction_amount) AS Total_transaction_value FROM aggregated_transaction GROUP BY state ORDER BY Total_transaction_value DESC LIMIT 5;"
        ],
        "Device & User Analysis": [
            "SELECT User_Brand, SUM(User_percentage) AS TotalUsers FROM aggregated_user GROUP BY User_Brand ORDER BY TotalUsers DESC;",
            "SELECT User_Brand, SUM(User_Count) AS TotalAppOpens FROM aggregated_user GROUP BY User_Brand ORDER BY TotalAppOpens DESC;",
            "SELECT User_Brand, SUM(User_Count) / SUM(User_percentage) AS AvgAppOpensPerUser FROM aggregated_user GROUP BY User_Brand ORDER BY AvgAppOpensPerUser DESC;",
            "SELECT State, SUM(User_Count) AS TotalAppOpens FROM aggregated_user GROUP BY State ORDER BY TotalAppOpens DESC;",
            "SELECT User_Brand, SUM(User_Count) / SUM(User_percentage) AS EngagementRate FROM aggregated_user GROUP BY User_Brand ORDER BY EngagementRate DESC LIMIT 5;"
        ],
        "Insurance & Growth Analysis": [
            "SELECT State, SUM(Insurance_Count) AS TotalPolicies FROM aggregated_insurance GROUP BY State ORDER BY TotalPolicies DESC;",
            "SELECT State, SUM(Insurance_Amount) AS TotalInsuranceValue FROM aggregated_insurance GROUP BY State ORDER BY TotalInsuranceValue DESC;",
            "SELECT State, SUM(Insurance_Amount) / SUM(Insurance_Count) AS AvgPolicyValue FROM aggregated_insurance GROUP BY State ORDER BY AvgPolicyValue DESC;",
            "SELECT Year, state, SUM(Insurance_Count) AS YearlyPoliciesSold FROM aggregated_insurance GROUP BY Year, State ORDER BY Year, YearlyPoliciesSold DESC;",
            "SELECT State, SUM(Insurance_Count) AS TotalPolicies FROM aggregated_insurance GROUP BY State ORDER BY TotalPolicies DESC LIMIT 5;"
        ],
        "Market Transaction Analysis": [
            "SELECT State, SUM(Transaction_count) AS TotalTransactions FROM map_transaction GROUP BY State ORDER BY TotalTransactions DESC;",
            "SELECT State, SUM(Transaction_amount) AS TotalTransactionValue FROM map_transaction GROUP BY State ORDER BY TotalTransactionValue DESC;",
            "SELECT Quarter, State, SUM(Transaction_amount) AS QuarterlyTransactionValue FROM map_transaction GROUP BY Quarter, State ORDER BY Quarter, QuarterlyTransactionValue DESC;",
            "SELECT Year, State, SUM(Transaction_amount) AS YearlyTransactionValue FROM map_transaction GROUP BY Year, State ORDER BY Year, YearlyTransactionValue DESC;",
            "SELECT State, SUM(Transaction_amount) AS TotalTransactionValue FROM map_transaction GROUP BY State ORDER BY TotalTransactionValue DESC LIMIT 5;"
        ],
        "User & Growth Strategies": [
            "SELECT State, SUM(Users_registeredUsers) AS TotalUsers FROM map_user GROUP BY State ORDER BY TotalUsers DESC;",
            "SELECT State, SUM(Users_appOpens) AS TotalAppOpens FROM map_user GROUP BY State ORDER BY TotalAppOpens DESC;",
            "SELECT State, SUM(Users_appOpens) / SUM(Users_registeredUsers) AS AvgAppOpenFrequency FROM map_user GROUP BY State ORDER BY AvgAppOpenFrequency DESC;",
            "SELECT State, SUM(Users_appOpens) AS TotalAppOpens FROM map_user GROUP BY State ORDER BY TotalAppOpens DESC;",
            "SELECT State, SUM(Users_appOpens) / SUM(Users_registeredUsers) AS EngagementRate FROM map_user GROUP BY State ORDER BY EngagementRate DESC LIMIT 5;"
        ]
    }

    selected_query = st.sidebar.selectbox("Choose Query", ["Query 1", "Query 2", "Query 3", "Query 4", "Query 5"])
    query_str = query_options[case_option][int(selected_query[-1]) - 1]
    df_case_study = get_data(query_str)

    st.subheader(f"📍 {case_option} - {selected_query}")
    st.dataframe(df_case_study)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=df_case_study.columns[0], y=df_case_study.columns[-1], data=df_case_study, ax=ax)
    plt.title(f"{case_option} - Detailed Analysis")
    plt.xticks(rotation=90)
    st.pyplot(fig)
