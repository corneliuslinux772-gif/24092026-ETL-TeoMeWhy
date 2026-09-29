from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import pandas as pd


class Severity(StrEnum):
    PASS = "PASS"
    CRITICAL = "CRITICAL"
    SEVERE = "SEVERE"


@dataclass
class QualityCheckResult:
    """
    Resultado normalizado de uma validação de qualidade.
    """

    check_name: str
    dataset: str
    severity: Severity
    success: bool
    invalid_rows: pd.DataFrame | None = None
    message: str | None = None


@dataclass
class QuarantineResult:
    """
    Resultado da operação de quarantine.
    """

    check_name: str
    dataset: str
    severity: Severity
    quarantined_rows: int
    output_file: Path | None
    success: bool