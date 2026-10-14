import pandas as pd
import plotly.express as px



def calculate_kpis(df):
    """
    Calculate important business KPIs from the cleaned dataset.
    """

    total_revenue = df["Net_Sales"].sum()

    total_profit = df["Profit"].sum()

    total_orders = df["Order_ID"].nunique()

    average_order_value = total_revenue / total_orders

    profit_margin = (total_profit / total_revenue) * 100

    kpis = {
        "Total Revenue": total_revenue,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Average Order Value": average_order_value,
        "Profit Margin": profit_margin
    }

    return kpis

def calculate_monthly_revenue(df):
    """
    Calculate total revenue for each month.
    """

    monthly_revenue = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Net_Sales"]
        .sum()
        .reset_index()
    )

    monthly_revenue["Order_Date"] = (
        monthly_revenue["Order_Date"]
        .dt.strftime("%b %Y")
    )

    monthly_revenue = monthly_revenue.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return monthly_revenue

def create_monthly_revenue_chart(monthly_revenue):
    """
    Create an interactive monthly revenue line chart.
    """

    fig = px.line(
        monthly_revenue,
        x="Order_Date",
        y="Revenue",
        markers=True,
        title="Monthly Revenue Trend"
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        hovermode="x unified"
    )

    fig.update_traces(
        hovertemplate="Month: %{x}<br>Revenue: ₹%{y:,.2f}<extra></extra>"
    )

    return fig

def calculate_top_products(df, top_n=10):
    """
    Calculate top products by total revenue.
    """

    top_products = (
        df.groupby("Product")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Net_Sales",
            ascending=False
        )
        .head(top_n)
    )

    top_products = top_products.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return top_products

def create_top_products_chart(top_products):
    """
    Create a horizontal bar chart for top products by revenue.
    """

    fig = px.bar(
        top_products.sort_values("Revenue"),
        x="Revenue",
        y="Product",
        orientation="h",
        title="Top 10 Products by Revenue",
        text="Revenue"
    )

    fig.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Product",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Product: %{y}<br>"
            "Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_category_revenue(df):
    """
    Calculate total revenue for each product category.
    """

    category_revenue = (
        df.groupby("Category")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Net_Sales",
            ascending=False
        )
    )

    category_revenue = category_revenue.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return category_revenue

def create_category_revenue_chart(category_revenue):
    """
    Create a bar chart for revenue by product category.
    """

    fig = px.bar(
        category_revenue.sort_values("Revenue"),
        x="Revenue",
        y="Category",
        orientation="h",
        title="Revenue by Category",
        text="Revenue"
    )

    fig.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Category",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Category: %{y}<br>"
            "Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_city_revenue(df, top_n=10):
    """
    Calculate top cities by total revenue.
    """

    city_revenue = (
        df.groupby("City")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Net_Sales",
            ascending=False
        )
        .head(top_n)
    )

    city_revenue = city_revenue.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return city_revenue

def create_city_revenue_chart(city_revenue):
    """
    Create a horizontal bar chart for revenue by city.
    """

    fig = px.bar(
        city_revenue.sort_values("Revenue"),
        x="Revenue",
        y="City",
        orientation="h",
        title="Top Cities by Revenue",
        text="Revenue"
    )

    fig.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="City",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "City: %{y}<br>"
            "Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_channel_revenue(df):
    """
    Calculate total revenue for each order channel.
    """

    channel_revenue = (
        df.groupby("Order_Channel")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Net_Sales",
            ascending=False
        )
    )

    channel_revenue = channel_revenue.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return channel_revenue

def create_channel_revenue_chart(channel_revenue):
    """
    Create a bar chart for revenue by order channel.
    """

    fig = px.bar(
        channel_revenue.sort_values("Revenue"),
        x="Revenue",
        y="Order_Channel",
        orientation="h",
        title="Revenue by Order Channel",
        text="Revenue"
    )

    fig.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Order Channel",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Channel: %{y}<br>"
            "Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_payment_revenue(df):
    """
    Calculate total revenue for each payment method.
    """

    payment_revenue = (
        df.groupby("Payment_Method")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Net_Sales",
            ascending=False
        )
    )

    payment_revenue = payment_revenue.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return payment_revenue

def create_payment_revenue_chart(payment_revenue):
    """
    Create a horizontal bar chart for revenue by payment method.
    """

    fig = px.bar(
        payment_revenue.sort_values("Revenue"),
        x="Revenue",
        y="Payment_Method",
        orientation="h",
        title="Revenue by Payment Method",
        text="Revenue"
    )

    fig.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Payment Method",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Payment Method: %{y}<br>"
            "Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_customer_revenue(df):
    """
    Calculate total revenue for each customer type.
    """

    customer_revenue = (
        df.groupby("Customer_Type")["Net_Sales"]
        .sum()
        .reset_index()
        .sort_values(
            by="Net_Sales",
            ascending=False
        )
    )

    customer_revenue = customer_revenue.rename(
        columns={
            "Net_Sales": "Revenue"
        }
    )

    return customer_revenue

def create_customer_revenue_chart(customer_revenue):
    """
    Create a horizontal bar chart for revenue by customer type.
    """

    fig = px.bar(
        customer_revenue.sort_values("Revenue"),
        x="Revenue",
        y="Customer_Type",
        orientation="h",
        title="Revenue by Customer Type",
        text="Revenue"
    )

    fig.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Customer Type",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Customer Type: %{y}<br>"
            "Revenue: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_profit_by_category(df):
    """
    Calculate total profit for each product category.
    """

    profit_by_category = (
        df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
        .sort_values(
            by="Profit",
            ascending=False
        )
    )

    return profit_by_category

def create_profit_by_category_chart(profit_by_category):
    """
    Create a horizontal bar chart for profit by category.
    """

    fig = px.bar(
        profit_by_category.sort_values("Profit"),
        x="Profit",
        y="Category",
        orientation="h",
        title="Profit by Category",
        text="Profit"
    )

    fig.update_layout(
        xaxis_title="Profit (₹)",
        yaxis_title="Category",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="₹%{text:,.0f}",
        textposition="outside",
        hovertemplate=(
            "Category: %{y}<br>"
            "Profit: ₹%{x:,.2f}"
            "<extra></extra>"
        )
    )

    return fig

def calculate_category_profit_margin(df):
    """
    Calculate profit margin for each product category.
    """

    category_profit_margin = (
        df.groupby("Category")
        .agg(
            Revenue=("Net_Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    category_profit_margin["Profit_Margin"] = (
        category_profit_margin["Profit"]
        / category_profit_margin["Revenue"]
        * 100
    )

    category_profit_margin = category_profit_margin.sort_values(
        by="Profit_Margin",
        ascending=False
    )

    return category_profit_margin

def create_profit_margin_chart(category_profit_margin):
    """
    Create a horizontal bar chart for profit margin by category.
    """

    fig = px.bar(
        category_profit_margin.sort_values("Profit_Margin"),
        x="Profit_Margin",
        y="Category",
        orientation="h",
        title="Profit Margin by Category",
        text="Profit_Margin"
    )

    fig.update_layout(
        xaxis_title="Profit Margin (%)",
        yaxis_title="Category",
        hovermode="y"
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        hovertemplate=(
            "Category: %{y}<br>"
            "Profit Margin: %{x:.2f}%"
            "<extra></extra>"
        )
    )

    return fig