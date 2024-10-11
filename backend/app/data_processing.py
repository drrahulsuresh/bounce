import pandas as pd

def clean_sustainability_data(df):
    # Step 1: Forward fill merged cells in the first row (to fill out columns like "Demographics")
    df.iloc[0].fillna(method='ffill', inplace=True)

    # Step 2: Concatenate first two rows to create composite column headers
    df.columns = [
        f"{str(df.iloc[0, i]).strip()}_{str(df.iloc[1, i]).strip()}" if pd.notna(df.iloc[1, i]) else str(df.iloc[0, i]).strip()
        for i in range(df.shape[1])
    ]

    # Step 3: Drop the first two rows after they've been used to create headers
    df_cleaned = df.drop([0, 1])

    # Reset index for clean row numbering
    df_cleaned.reset_index(drop=True, inplace=True)

    print(f"Columns after cleaning: {df_cleaned.columns}")
    return df_cleaned

def clean_christmas_data(df):
    # Step 1: Forward fill merged cells in the first row (to fill out columns like "Demographics")
    df.iloc[0].fillna(method='ffill', inplace=True)

    # Step 2: Concatenate first two rows to create composite column headers
    df.columns = [
        f"{str(df.iloc[0, i]).strip()}_{str(df.iloc[1, i]).strip()}" if pd.notna(df.iloc[1, i]) else str(df.iloc[0, i]).strip()
        for i in range(df.shape[1])
    ]

    # Step 3: Drop the first two rows after they've been used to create headers
    df_cleaned = df.drop([0, 1])

    # Reset index for clean row numbering
    df_cleaned.reset_index(drop=True, inplace=True)

    print(f"Columns after cleaning: {df_cleaned.columns}")
    return df_cleaned

def load_and_save_datasets():
    # Load both datasets
    sustainability_df = pd.read_excel("Dataset 1 (Sustainability Research Results).xlsx")
    christmas_df = pd.read_excel("Dataset 2 (Christmas Research Results).xlsx")

    # Clean the datasets using the custom cleanin function
    sustainability_cleaned = clean_sustainability_data(sustainability_df)
    christmas_cleaned = clean_christmas_data(christmas_df)

    # Save cleaned datasets as CSV for verification
    sustainability_cleaned.to_csv("cleaned_sustainability.csv", index=False)
    christmas_cleaned.to_csv("cleaned_christmas.csv", index=False)

    print("Cleaned datasets saved as CSV files.")
    return sustainability_cleaned, christmas_cleaned
