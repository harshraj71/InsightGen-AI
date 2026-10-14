
import pandas as pd

# Load our sales dataset
file_path = "data/kfc_style_sales_dataset(1).csv"
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

# STEP 3: DATA QUALITY CHECKS

print("\n--- DATA QUALITY REPORT ---")

# 1. Check missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# 2. Check duplicate rows
print("\nTotal duplicate rows:")
print(df.duplicated().sum())

# 3. Check data types
print("\nColumn data types:")
print(df.dtypes)

# 4. Check date format
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

print("\nInvalid order dates:")
print(df["Order_Date"].isnull().sum())

# 5. Check basic statistics
print("\nNumerical summary:")
print(df.describe())

# STEP 4: DATA CLEANING

print("\n--- STARTING DATA CLEANING ---")

# Keep a copy of the original data
clean_df = df.copy()

# 1. Remove exact duplicate rows
before = len(clean_df)
clean_df = clean_df.drop_duplicates()
print("Duplicate rows removed:", before - len(clean_df))

# 2. Fill missing city and payment method
clean_df["City"] = clean_df["City"].fillna("Unknown")
clean_df["Payment_Method"] = clean_df["Payment_Method"].fillna("Unknown")

# 3. Handle missing discount values carefully
# Do not assume a missing discount means zero.
# Keep missing values until the business rule is verified.

# 4. Convert dates to datetime
clean_df["Order_Date"] = pd.to_datetime(
    clean_df["Order_Date"], errors="coerce"
)

# 5. Check the cleaning result
print("\nRows before cleaning:", len(df))
print("Rows after removing duplicates:", len(clean_df))

print("\nRemaining missing values:")
print(clean_df.isnull().sum()[clean_df.isnull().sum() > 0])

print("\nData types after cleaning:")
print(clean_df.dtypes)

# 6. Save cleaned data separately
clean_df.to_csv("data/sales_cleaned.csv", index=False)

print("\nCleaned dataset saved to data/sales_cleaned.csv")

# STEP 5: SALES ANALYSIS

print("\n--- SALES PERFORMANCE ANALYSIS ---")

# Load the cleaned dataset
sales_df = pd.read_csv("data/sales_cleaned.csv")

# Total revenue
total_revenue = sales_df["Net_Sales"].sum()

# Total profit
total_profit = sales_df["Profit"].sum()

# Total unique orders
total_orders = sales_df["Order_ID"].nunique()

# Average order value
average_order_value = total_revenue / total_orders if total_orders else 0

# Profit margin
profit_margin = (
    (total_profit / total_revenue) * 100
    if total_revenue else 0
)

print(f"Total Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Profit: Rs. {total_profit:,.2f}")
print(f"Total Unique Orders: {total_orders:,}")
print(f"Average Order Value: Rs. {average_order_value:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")

# Top 5 products by revenue
print("\n--- TOP 5 PRODUCTS BY REVENUE ---")

top_products = (
    sales_df.groupby("Product")["Net_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_products)

# STEP 6: MONTHLY SALES TREND

import matplotlib.pyplot as plt

# Group sales by month
sales_df["Order_Date"] = pd.to_datetime(sales_df["Order_Date"])

monthly_sales = (
    sales_df.groupby(sales_df["Order_Date"].dt.to_period("M"))["Net_Sales"]
    .sum()
)

# Convert month labels to strings for plotting
monthly_sales.index = monthly_sales.index.astype(str)

print("\n--- MONTHLY SALES ---")
print(monthly_sales.round(2))

# Create line chart
plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)

plt.title("Monthly Net Sales - 2025")
plt.xlabel("Month")
plt.ylabel("Net Sales (Rs.)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save chart
plt.savefig("data/monthly_sales_trend.png", dpi=150)

# Display chart
plt.show()

print("\nChart saved to data/monthly_sales_trend.png")

# STEP 7: CATEGORY AND REGION ANALYSIS

print("\n--- CATEGORY-WISE PERFORMANCE ---")

category_analysis = (
    sales_df.groupby("Category")
    .agg(
        Total_Sales=("Net_Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
    .sort_values("Total_Sales", ascending=False)
)

print(category_analysis.round(2))

print("\n--- REGION-WISE PERFORMANCE ---")

region_analysis = (
    sales_df.groupby("Region")
    .agg(
        Total_Sales=("Net_Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique")
    )
    .sort_values("Total_Sales", ascending=False)
)

print(region_analysis.round(2))

print("\n--- TOP 5 CITIES BY SALES ---")

city_analysis = (
    sales_df.groupby("City")["Net_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(city_analysis.round(2))

# Save analysis results
category_analysis.to_csv("data/category_analysis.csv")
region_analysis.to_csv("data/region_analysis.csv")

print("\nCategory and region reports saved successfully!")
