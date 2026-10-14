import streamlit as st
import pandas as pd
from utils.data_cleaner import clean_dataset
from utils.insights import generate_business_insights
from utils.recommendations import generate_recommendations

from dashboard.charts import (
    calculate_kpis,
    calculate_monthly_revenue,
    create_monthly_revenue_chart,
    calculate_top_products,
    create_top_products_chart,
    calculate_category_revenue,
    create_category_revenue_chart,
    calculate_city_revenue,
    create_city_revenue_chart,
    calculate_channel_revenue,
    create_channel_revenue_chart,
    calculate_payment_revenue,
    create_payment_revenue_chart,
    calculate_customer_revenue,
    create_customer_revenue_chart,
    calculate_profit_by_category,
    create_profit_by_category_chart,
    calculate_category_profit_margin,
    create_profit_margin_chart
)

st.set_page_config(
    page_title="InsightGen AI",
    page_icon="🤖",
    layout="wide"
)

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None

if "cleaning_report" not in st.session_state:
    st.session_state.cleaning_report = None

st.title("🤖 InsightGen AI")
st.subheader("Agentic Business Intelligence Assistant")

st.write(
    "Upload your business dataset and let AI analyze it, "
    "generate insights, and provide recommendations."
)

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset uploaded successfully!")

    # Dataset Overview
    st.write("## 📊 Dataset Overview")

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Rows", f"{total_rows:,}")

    with col2:
        st.metric("Total Columns", total_columns)

    with col3:
        st.metric("Missing Values", f"{missing_values:,}")

    with col4:
        st.metric("Duplicate Rows", duplicate_rows)

    # Dataset Preview
    st.write("## 🔍 Dataset Preview")
    st.dataframe(df, use_container_width=True)

    # Data Types
    st.write("## 🧾 Data Types")

    data_types = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        data_types,
        use_container_width=True
    )

    # Statistical Summary
    st.write("## 📈 Statistical Summary")

    st.dataframe(
        df.describe(include="all").T,
        use_container_width=True
    )

        # Data Cleaning
    st.write("## 🧹 Data Cleaning")

    if st.button("Clean Dataset"):
        cleaned_df, cleaning_report = clean_dataset(df)

        st.session_state.cleaned_df = cleaned_df
        st.session_state.cleaning_report = cleaning_report

        st.success("Dataset cleaned successfully!")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Original Rows",
                cleaning_report["Original Rows"]
            )

        with col2:
            st.metric(
                "Duplicates Removed",
                cleaning_report["Duplicate Rows Removed"]
            )

        with col3:
            st.metric(
                "Final Rows",
                cleaning_report["Final Rows"]
            )

        with col4:
            st.metric(
                "Missing Values Remaining",
                cleaning_report["Missing Values Remaining"]
            )

        st.write("### 🧹 Cleaned Dataset")

        st.dataframe(
            cleaned_df,
            use_container_width=True
        )

        st.write("### 🔄 Before vs After Cleaning")

        comparison_data = pd.DataFrame({
            "Metric": [
                "Rows",
                "Missing Values",
                "Duplicate Rows"
            ],
            "Before Cleaning": [
                len(df),
                int(df.isnull().sum().sum()),
                int(df.duplicated().sum())
            ],
            "After Cleaning": [
                len(cleaned_df),
                int(cleaned_df.isnull().sum().sum()),
                int(cleaned_df.duplicated().sum())
            ]
            
        })

        st.dataframe(
            comparison_data,
            use_container_width=True,
            hide_index=True
        )
        
                # Business KPIs
        st.write("## 💰 Business KPIs")

        kpis = calculate_kpis(cleaned_df)

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Total Revenue",
                f"₹{kpis['Total Revenue']:,.2f}"
            )

        with col2:
            st.metric(
                "Total Profit",
                f"₹{kpis['Total Profit']:,.2f}"
            )

        with col3:
            st.metric(
                "Total Orders",
                f"{kpis['Total Orders']:,}"
            )

        with col4:
            st.metric(
                "Average Order Value",
                f"₹{kpis['Average Order Value']:,.2f}"
            )

        with col5:
            st.metric(
                "Profit Margin",
                f"{kpis['Profit Margin']:.2f}%"
            )
            
                # Monthly Revenue Trend
        st.write("## 📈 Monthly Revenue Trend")

        monthly_revenue = calculate_monthly_revenue(cleaned_df)

        monthly_revenue_chart = create_monthly_revenue_chart(
            monthly_revenue
        )

        st.plotly_chart(
            monthly_revenue_chart,
            use_container_width=True
        )
        
                # Top Products by Revenue
        st.write("## 🍗 Top 10 Products by Revenue")

        top_products = calculate_top_products(cleaned_df)

        top_products_chart = create_top_products_chart(
            top_products
        )

        st.plotly_chart(
            top_products_chart,
            use_container_width=True
        )
        
                # City Revenue Analysis
        st.write("## 🏙️ Top Cities by Revenue")

        city_revenue = calculate_city_revenue(cleaned_df)

        city_chart = create_city_revenue_chart(
            city_revenue
        )

        st.plotly_chart(
            city_chart,
            use_container_width=True
        )
        
            # Order Channel Revenue Analysis
        st.write("## 📱 Revenue by Order Channel")

        channel_revenue = calculate_channel_revenue(cleaned_df)

        channel_chart = create_channel_revenue_chart(
        channel_revenue
        )

        st.plotly_chart(
        channel_chart,
        use_container_width=True
        )
        
                # Payment Method Revenue Analysis
        st.write("## 💳 Revenue by Payment Method")

        payment_revenue = calculate_payment_revenue(cleaned_df)

        payment_chart = create_payment_revenue_chart(
            payment_revenue
        )

        st.plotly_chart(
            payment_chart,
            use_container_width=True
        )
        
                # Customer Type Revenue Analysis
        st.write("## 👥 Revenue by Customer Type")

        customer_revenue = calculate_customer_revenue(
            cleaned_df
        )

        customer_chart = create_customer_revenue_chart(
            customer_revenue
        )

        st.plotly_chart(
            customer_chart,
            use_container_width=True
        )
        
                # Profit by Category Analysis
        st.write("## 💰 Profit by Category")

        profit_by_category = calculate_profit_by_category(
            cleaned_df
        )

        profit_chart = create_profit_by_category_chart(
            profit_by_category
        )

        st.plotly_chart(
            profit_chart,
            use_container_width=True
        )
        
                # Profit Margin Analysis
        st.write("## 📊 Profit Margin by Category")

        category_profit_margin = calculate_category_profit_margin(
            cleaned_df
        )

        margin_chart = create_profit_margin_chart(
            category_profit_margin
        )

        st.plotly_chart(
            margin_chart,
            use_container_width=True
        )
        
                # Automated Business Insights
        st.write("## 🤖 Automated Business Insights")

        insights = generate_business_insights(cleaned_df)

        for insight in insights:
            st.info(insight)
            
                # Automated Business Recommendations
        st.write("## 💡 Business Recommendations")

        recommendations = generate_recommendations(
            cleaned_df
        )

        for recommendation in recommendations:
            st.success(recommendation)