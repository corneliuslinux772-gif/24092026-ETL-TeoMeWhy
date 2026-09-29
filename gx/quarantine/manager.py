from pathlib import Path

import pandas as pd

from gx.quarantine.config import QUARANTINE_ROOT
from gx.quarantine.models import (
    QualityCheckResult,
    QuarantineResult,
    Severity,
)
from gx.quarantine.policy import (
    apply_severity_policy,
)
from gx.quarantine.writer import (
    write_quarantine,
)


class QuarantineManager:
    """
    Gerencia o destino dos registros após uma validação
    de qualidade.

    PASS:
        segue o pipeline.

    CRITICAL:
        registros inválidos são enviados para quarantine.

    SEVERE:
        interrompe o pipeline.
    """

    def __init__(
        self,
        quarantine_root: Path = QUARANTINE_ROOT,
    ):
        self.quarantine_root = quarantine_root

    def process(
        self,
        result: QualityCheckResult,
        *,
        source_file: str,
        quarantine_reason: str,
    ) -> QuarantineResult:

        action = apply_severity_policy(
            result.severity
        )

        if action == "CONTINUE":
            return QuarantineResult(
                check_name=result.check_name,
                dataset=result.dataset,
                severity=result.severity,
                quarantined_rows=0,
                output_file=None,
                success=True,
            )

        if action == "QUARANTINE":

            if result.invalid_rows is None:
                raise ValueError(
                    f"Validation '{result.check_name}' "
                    "was marked as CRITICAL but did not "
                    "provide invalid rows."
                )

            invalid_rows = result.invalid_rows

            output_file = (
                self.quarantine_root
                / result.dataset
                / f"{result.check_name}.csv"
            )

            write_quarantine(
                df=invalid_rows,
                output_file=output_file,
                quarantine_reason=quarantine_reason,
                constraint_name=result.check_name,
                source_file=source_file,
                severity=result.severity.value,
            )

            return QuarantineResult(
                check_name=result.check_name,
                dataset=result.dataset,
                severity=result.severity,
                quarantined_rows=len(invalid_rows),
                output_file=output_file,
                success=True,
            )

        raise RuntimeError(
            f"Unexpected quarantine action: {action}"
        )