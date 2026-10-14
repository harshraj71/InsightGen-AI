import pandas as pd


def clean_dataset(df):
    df = df.copy()

    original_rows = len(df)

    # Count duplicate rows
    duplicate_rows = df.duplicated().sum()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Convert Order_Date to datetime
    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(
            df["Order_Date"],
            errors="coerce"
        )

    # Handle missing City values
    if "City" in df.columns:
        df["City"] = df["City"].fillna("Unknown")

    # Handle missing Payment_Method values
    if "Payment_Method" in df.columns:
        df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")

    # Handle missing Discount_Percent values
    if "Discount_Percent" in df.columns:
        median_discount = df["Discount_Percent"].median()

        df["Discount_Percent"] = df["Discount_Percent"].fillna(
            median_discount
        )

    # Generate cleaning report
    final_rows = len(df)

    report = {
        "Original Rows": original_rows,
        "Duplicate Rows Removed": duplicate_rows,
        "Final Rows": final_rows,
        "Missing Values Remaining": int(df.isnull().sum().sum())
    }

    return df, report