from pathlib import Path

import pandas as pd


def write_quarantine(
    df: pd.DataFrame,
    output_file: Path,
    *,
    quarantine_reason: str,
    constraint_name: str,
    source_file: str,
    severity: str,
) -> Path:
    """
    Escreve registros inválidos na área de quarantine.

    O DataFrame recebido é copiado e o raw nunca é alterado.
    """

    quarantine_df = df.copy()

    quarantine_df["quarantine_reason"] = (
        quarantine_reason
    )

    quarantine_df["constraint_name"] = (
        constraint_name
    )

    quarantine_df["source_file"] = (
        source_file
    )

    quarantine_df["severity"] = (
        severity
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    quarantine_df.to_csv(
        output_file,
        sep=";",
        index=False,
    )

    return output_file