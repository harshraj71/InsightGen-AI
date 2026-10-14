import pandas as pd


def generate_business_insights(df):
    """
    Generate automated business insights from cleaned sales data.
    """

    insights = []

    # 1. Highest revenue category
    category_revenue = (
        df.groupby("Category")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = category_revenue.index[0]
    best_category_revenue = category_revenue.iloc[0]

    insights.append(
        f"🏆 {best_category} generated the highest category revenue "
        f"of ₹{best_category_revenue:,.2f}."
    )

    # 2. Highest profit category
    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    best_profit_category = category_profit.index[0]
    best_profit = category_profit.iloc[0]

    insights.append(
        f"💰 {best_profit_category} generated the highest total profit "
        f"of ₹{best_profit:,.2f}."
    )

    # 3. Highest profit margin category
    category_margin = (
        df.groupby("Category")
        .agg(
            Revenue=("Net_Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    category_margin["Profit_Margin"] = (
        category_margin["Profit"]
        / category_margin["Revenue"]
        * 100
    )

    best_margin_category = category_margin["Profit_Margin"].idxmax()
    best_margin = category_margin.loc[
        best_margin_category,
        "Profit_Margin"
    ]

    insights.append(
        f"📈 {best_margin_category} had the highest profit margin "
        f"of {best_margin:.2f}%."
    )

    # 4. Best performing city
    city_revenue = (
        df.groupby("City")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_city = city_revenue.index[0]
    best_city_revenue = city_revenue.iloc[0]

    insights.append(
        f"🏙️ {best_city} generated the highest city revenue "
        f"of ₹{best_city_revenue:,.2f}."
    )

    # 5. Best order channel
    channel_revenue = (
        df.groupby("Order_Channel")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_channel = channel_revenue.index[0]
    best_channel_revenue = channel_revenue.iloc[0]

    insights.append(
        f"📱 {best_channel} was the highest-revenue order channel "
        f"with ₹{best_channel_revenue:,.2f}."
    )

    # 6. Best payment method
    payment_revenue = (
        df.groupby("Payment_Method")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_payment = payment_revenue.index[0]
    best_payment_revenue = payment_revenue.iloc[0]

    insights.append(
        f"💳 {best_payment} generated the highest payment-method revenue "
        f"of ₹{best_payment_revenue:,.2f}."
    )

    # 7. Customer type contribution
    customer_revenue = (
        df.groupby("Customer_Type")["Net_Sales"]
        .sum()
    )

    total_revenue = customer_revenue.sum()

    if "Returning" in customer_revenue.index:
        returning_revenue = customer_revenue["Returning"]

        returning_percentage = (
            returning_revenue / total_revenue
        ) * 100

        insights.append(
            f"👥 Returning customers contributed "
            f"{returning_percentage:.2f}% of total revenue."
        )

    return insights