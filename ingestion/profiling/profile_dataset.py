from pathlib import Path
import pandas as pd

DATA_DIR = Path("data/raw")

def load_profile_dataset(file_path: Path) -> None:
    """Load the profile dataset from the raw data directory."""
    print("\n" + "=" * 80)
    print(f"File: {file_path.name}")
    print("=" * 80)
    
    df = pd.read_csv(
        file_path,
        encoding="utf-8",
        sep=";"
    )
    
    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    
    print("\n--- Columns ---")
    for col in df.columns:
        dtype = df[col].dtype
        nulls = df[col].isna().sum()
        null_pct = (nulls / len(df)) * 100
        unique = df[col].nunique(dropna=True)
        print(
            f"{col:<30} dtype={str(dtype):<12} "
            f"nulls={nulls:<8} - %={null_pct:>6.2f}% "
            f"unique={unique:,}"
        )
        
    print("\n--- Duplicated rows ---")
    duplicated = df.duplicated().sum()
    print(f"Duplicates: {duplicated:,}")
    
    print("\n--- Sample ---")
    print(df.head(5).to_string(index=False))

def main():
    files = sorted(DATA_DIR.glob("*.csv"))
    if not files:
        print(f"No CSV files found in: {DATA_DIR}")
        return
    
    print(f"Found {len(files)} CSV file(s).")
    for file_path in files:
        load_profile_dataset(file_path)

if __name__ == "__main__":
    main()
