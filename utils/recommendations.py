def generate_recommendations(df):
    """
    Generate automated business recommendations.
    """

    recommendations = []

    # 1. Category revenue recommendation
    category_revenue = (
        df.groupby("Category")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_category = category_revenue.index[0]
    best_category_revenue = category_revenue.iloc[0]

    recommendations.append(
        f"💡 Focus on {best_category} because it generates "
        f"the highest category revenue of "
        f"₹{best_category_revenue:,.2f}. "
        f"Consider maintaining inventory availability and "
        f"promoting high-performing {best_category.lower()} products."
    )

    # 2. Profit margin recommendation
    category_data = (
        df.groupby("Category")
        .agg(
            Revenue=("Net_Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    category_data["Profit_Margin"] = (
        category_data["Profit"]
        / category_data["Revenue"]
        * 100
    )

    best_margin_category = category_data[
        "Profit_Margin"
    ].idxmax()

    best_margin = category_data.loc[
        best_margin_category,
        "Profit_Margin"
    ]

    recommendations.append(
        f"📈 {best_margin_category} has the highest profit margin "
        f"of {best_margin:.2f}%. "
        f"Consider increasing its visibility and testing "
        f"bundles or upselling opportunities."
    )

    # 3. City recommendation
    city_revenue = (
        df.groupby("City")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_city = city_revenue.index[0]

    recommendations.append(
        f"🏙️ {best_city} is the highest-revenue city. "
        f"Consider prioritizing marketing campaigns and "
        f"inventory availability in this market."
    )

    # 4. Channel recommendation
    channel_revenue = (
        df.groupby("Order_Channel")["Net_Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    best_channel = channel_revenue.index[0]

    recommendations.append(
        f"📱 {best_channel} is the strongest revenue channel. "
        f"Consider optimizing the customer experience and "
        f"promotions on this channel."
    )

    # 5. Customer retention recommendation
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

        if returning_percentage > 50:

            recommendations.append(
                f"👥 Returning customers contribute "
                f"{returning_percentage:.2f}% of revenue. "
                f"Prioritize customer retention through "
                f"loyalty programs, personalized offers, "
                f"and repeat-purchase campaigns."
            )

    return recommendations