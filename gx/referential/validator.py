from pathlib import Path

import pandas as pd

# ============================================================
# VALIDATE FK SIMPLES
# ============================================================

def validate_foreign_key(
    child_file: Path,
    child_column: str,
    parent_file: Path,
    parent_column: str,
) -> dict:
    """
    Valida uma chave estrangeira simples entre dois arquivos CSV.

    Verifica se todos os valores existentes na coluna filha
    também existem na coluna pai.
    """

    child_df = pd.read_csv(
        child_file,
        sep=";",
        low_memory=False,
    )

    parent_df = pd.read_csv(
        parent_file,
        sep=";",
        low_memory=False,
    )

    child_values = child_df[child_column].dropna()
    parent_values = parent_df[parent_column].dropna()

    orphan_values = child_values[
        ~child_values.isin(parent_values)
    ].drop_duplicates()

    return {
        "child_file": child_file.name,
        "child_column": child_column,
        "parent_file": parent_file.name,
        "parent_column": parent_column,
        "child_rows": len(child_df),
        "distinct_child_values": child_values.nunique(),
        "parent_rows": len(parent_df),
        "distinct_parent_values": parent_values.nunique(),
        "orphan_count": len(orphan_values),
        "orphan_values": orphan_values.tolist(),
        "success": len(orphan_values) == 0,
    }


# ============================================================
# VALIDATE FK COMPOUNDED
# ============================================================

def validate_compound_foreign_key(
    child_file: Path,
    child_columns: list[str],
    parent_file: Path,
    parent_columns: list[str],
    transform=None,
) -> dict:
    """
    Valida uma chave estrangeira composta entre dois arquivos CSV.

    Permite transformar uma coluna do filho antes da comparação.
    """

    child_df = pd.read_csv(
        child_file,
        sep=";",
        low_memory=False,
    )

    parent_df = pd.read_csv(
        parent_file,
        sep=";",
        low_memory=False,
    )

    child_df = child_df.copy()
    parent_df = parent_df.copy()

    if transform is not None:
        child_df["nrEp"] = transform(
            child_df["descSlugCursoEpisodio"]
        )

    child_keys = child_df[["descSlugCurso", "nrEp"]].drop_duplicates()

    parent_keys = parent_df[
        ["descSlugCurso", "nrEp"]
    ].drop_duplicates()

    merged = child_keys.merge(
        parent_keys,
        on=["descSlugCurso", "nrEp"],
        how="left",
        indicator=True,
    )

    orphan_keys = merged[
        merged["_merge"] == "left_only"
    ][["descSlugCurso", "nrEp"]]

    return {
        "child_file": child_file.name,
        "child_columns": child_columns,
        "parent_file": parent_file.name,
        "parent_columns": parent_columns,
        "child_rows": len(child_df),
        "distinct_child_keys": len(child_keys),
        "parent_rows": len(parent_df),
        "distinct_parent_keys": len(parent_keys),
        "orphan_count": len(orphan_keys),
        "orphan_values": orphan_keys.to_dict("records"),
        "success": len(orphan_keys) == 0,
    }