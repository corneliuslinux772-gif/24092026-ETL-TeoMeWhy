from pathlib import Path

import pandas as pd


DATA_DIR = Path("data/raw")


def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Carrega um CSV tentando detectar automaticamente
    alguns problemas comuns de encoding.
    """

    encodings = ["utf-8", "utf-8-sig", "latin1"]

    for encoding in encodings:
        try:
            return pd.read_csv(
                file_path,
                encoding=encoding,
                low_memory=False,
                sep=";"
            )
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Não foi possível ler: {file_path}")


def profile_basic(df: pd.DataFrame, file_name: str):
    print("\n" + "=" * 100)
    print(f"FILE: {file_name}")
    print("=" * 100)

    print(f"\nRows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\n--- DATA TYPES ---")

    for column in df.columns:
        print(f"{column:<35} {str(df[column].dtype)}")

    print("\n--- NULLS ---")

    nulls = df.isna().sum()

    for column, value in nulls.items():
        pct = value / len(df) * 100

        print(
            f"{column:<35} "
            f"nulls={value:<8,} "
            f"null%={pct:>7.2f}%"
        )

    print("\n--- DUPLICATES ---")

    print(
        f"Duplicated rows: "
        f"{df.duplicated().sum():,}"
    )


def profile_cardinality(df: pd.DataFrame):

    print("\n--- CARDINALITY ---")

    for column in df.columns:

        unique = df[column].nunique(
            dropna=False
        )

        unique_non_null = df[column].nunique(
            dropna=True
        )

        print(
            f"{column:<35} "
            f"unique={unique_non_null:<8,} "
            f"unique_with_null={unique:<8,}"
        )


def profile_unique_values(df: pd.DataFrame):

    print("\n--- UNIQUE VALUES ---")

    for column in df.columns:

        unique = df[column].nunique(
            dropna=True
        )

        # Só mostramos valores distintos
        # quando a cardinalidade for pequena.
        if unique <= 30:

            values = (
                df[column]
                .dropna()
                .unique()
                .tolist()
            )

            print(f"\n{column}")
            print("-" * len(column))

            for value in values:
                print(f"  {value}")


def profile_numeric(df: pd.DataFrame):

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numeric_columns) == 0:
        return

    print("\n--- NUMERIC PROFILE ---")

    for column in numeric_columns:

        series = df[column]

        print(f"\n{column}")

        print(
            f"  min:    {series.min()}"
        )

        print(
            f"  max:    {series.max()}"
        )

        print(
            f"  mean:   {series.mean():.2f}"
        )

        print(
            f"  median: {series.median():.2f}"
        )


def profile_dates(df: pd.DataFrame):

    print("\n--- POSSIBLE DATE COLUMNS ---")

    for column in df.columns:

        if df[column].dtype != "object":
            continue

        sample = df[column].dropna()

        if len(sample) == 0:
            continue

        parsed = pd.to_datetime(
            sample,
            errors="coerce"
        )

        success_rate = parsed.notna().mean()

        if success_rate >= 0.90:

            print(f"\n{column}")

            print(
                f"  parse success: "
                f"{success_rate * 100:.2f}%"
            )

            print(
                f"  min: {parsed.min()}"
            )

            print(
                f"  max: {parsed.max()}"
            )


def profile_candidate_keys(df: pd.DataFrame):

    print("\n--- POSSIBLE PRIMARY KEYS ---")

    for column in df.columns:

        if df[column].isna().any():
            continue

        if df[column].is_unique:

            print(
                f"✓ {column}"
                " -> candidate primary key"
            )


def profile_composite_keys(df: pd.DataFrame):

    print(
        "\n--- POSSIBLE COMPOSITE KEYS ---"
    )

    columns = list(df.columns)

    # Testa combinações de duas colunas.
    for i in range(len(columns)):

        for j in range(i + 1, len(columns)):

            col1 = columns[i]
            col2 = columns[j]

            duplicated = df.duplicated(
                subset=[col1, col2]
            ).sum()

            if duplicated == 0:

                print(
                    f"✓ ({col1}, {col2})"
                    " -> candidate composite key"
                )


def profile_file(file_path: Path):

    df = load_csv(file_path)

    profile_basic(
        df,
        file_path.name
    )

    profile_cardinality(df)

    profile_unique_values(df)

    profile_numeric(df)

    profile_dates(df)

    profile_candidate_keys(df)

    profile_composite_keys(df)


def main():

    files = sorted(
        DATA_DIR.glob("*.csv")
    )

    if not files:

        print(
            f"Nenhum CSV encontrado em "
            f"{DATA_DIR}"
        )

        return

    print(
        f"Encontrados "
        f"{len(files)} arquivos CSV."
    )

    for file_path in files:

        profile_file(file_path)


if __name__ == "__main__":
    main()