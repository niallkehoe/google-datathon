import pandas as pd
from typing import List

def get_drugs_dfs(drug_names: List[str]) -> pd.DataFrame:
    merged_df = None  # Initialize the merged DataFrame

    for i, drug_name in enumerate(drug_names):
        # Read the CSV for the current drug
        df_drug = pd.read_csv(f"data/drugs/{drug_name}.csv")

        # Rename the columns that start with specific prefixes
        df_drug.rename(
            columns={
                col: "Value" if col.startswith("Value:") else
                     "Date" if col.startswith("Date:") else col
                for col in df_drug.columns
            },
            inplace=True
        )

        # Drop the column that starts with "Source:"
        df_drug = df_drug.loc[:, ~df_drug.columns.str.startswith("Source:")]

        # Rename "Value" to the current drug name
        df_drug.rename(columns={"Value": drug_name}, inplace=True)

        # Merge with the previously read data frames
        if merged_df is None:
            merged_df = df_drug
        else:
            merged_df = pd.merge(
                merged_df, 
                df_drug, 
                on=["Date", "placeDcid"], 
                how="outer", 
                suffixes=(None, "_dup"),
            )

            # Drop the duplicate `placeName` column, if it exists
            if "placeName_dup" in merged_df.columns:
                merged_df.drop(columns=["placeName_dup"], inplace=True)

    return merged_df
