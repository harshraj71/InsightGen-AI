
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load cleaned dataset
df = pd.read_csv("data/sales_cleaned.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Create output folder
output_dir = Path("reports")
output_dir.mkdir(exist_ok=True)

# 1. Monthly sales trend
monthly_sales = (
    df.groupby(df["Order_Date"].dt.to_period("M"))["Net_Sales"]
    .sum()
)
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(10, 5))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title("Monthly Net Sales - 2025")
plt.xlabel("Month")
plt.ylabel("Net Sales (Rs.)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(output_dir / "monthly_sales.png", dpi=150)
plt.close()

# 2. Category-wise revenue
category_sales = (
    df.groupby("Category")["Net_Sales"]
    .sum()
    .sort_values()
)

plt.figure(figsize=(10, 5))
category_sales.plot(kind="barh")
plt.title("Revenue by Product Category")
plt.xlabel("Net Sales (Rs.)")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(output_dir / "category_sales.png", dpi=150)
plt.close()

# 3. Region-wise revenue
region_sales = (
    df.groupby("Region")["Net_Sales"]
    .sum()
    .sort_values()
)

plt.figure(figsize=(8, 5))
region_sales.plot(kind="bar")
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Net Sales (Rs.)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(output_dir / "region_sales.png", dpi=150)
plt.close()

print("All three charts saved in the reports folder!")
