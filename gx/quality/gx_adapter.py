import pandas as pd

from gx.quarantine.models import (
    QualityCheckResult,
    Severity,
)


# ============================================================
# EXPECTATION → CHECK NAME
# ============================================================

def _build_check_name(
    dataset: str,
    expectation_type: str,
    column: str | None,
) -> str:

    suffix_map = {
        "expect_column_values_to_not_be_null": "not_null",
        "expect_column_values_to_be_unique": "unique",
    }

    suffix = suffix_map.get(
        expectation_type,
        expectation_type.replace("expect_", ""),
    )

    if column:
        return f"{dataset}_{column}_{suffix}"

    return f"{dataset}_{suffix}"


# ============================================================
# SEVERITY
# ============================================================

def _resolve_severity(
    expectation_result,
) -> Severity:

    # Uma expectativa que passou não deve ser enviada
    # ao QuarantineManager como CRITICAL.
    if expectation_result.success:
        return Severity.PASS

    expectation_config = expectation_result.expectation_config

    raw_severity = expectation_config.get(
        "severity",
        "critical",
    )

    # Great Expectations pode retornar:
    #
    # <FailureSeverity.CRITICAL: 'critical'>
    #
    # Nesse caso, usamos o valor interno do enum.
    if hasattr(raw_severity, "value"):
        raw_severity = raw_severity.value

    try:
        return Severity(str(raw_severity).upper())

    except ValueError as exc:
        raise ValueError(
            f"Severity inválida na expectativa: "
            f"{raw_severity!r}"
        ) from exc


# ============================================================
# INVALID ROWS
# ============================================================

def _get_invalid_rows(
    expectation_result,
    df: pd.DataFrame,
) -> pd.DataFrame | None:

    if expectation_result.success:
        return None

    result = expectation_result.result

    invalid_indices = result.get(
        "partial_unexpected_index_list",
        [],
    )

    if not invalid_indices:
        return None

    return df.iloc[invalid_indices].copy()


# ============================================================
# ADAPTER
# ============================================================

def adapt_gx_result(
    validation_result,
    df: pd.DataFrame,
    *,
    dataset: str,
) -> list[QualityCheckResult]:

    quality_results: list[QualityCheckResult] = []

    for expectation_result in validation_result.results:

        expectation_config = expectation_result.expectation_config

        expectation_type = expectation_config.type

        column = expectation_config.kwargs.get(
            "column"
        )

        check_name = _build_check_name(
            dataset=dataset,
            expectation_type=expectation_type,
            column=column,
        )

        severity = _resolve_severity(
            expectation_result
        )

        invalid_rows = _get_invalid_rows(
            expectation_result,
            df,
        )

        unexpected_count = expectation_result.result.get(
            "unexpected_count",
            0,
        )

        if expectation_result.success:

            message = (
                f"Expectation '{check_name}' "
                "passed."
            )

        else:

            message = (
                f"Expectation '{check_name}' "
                f"failed with "
                f"{unexpected_count} unexpected values."
            )

        quality_results.append(
            QualityCheckResult(
                check_name=check_name,
                dataset=dataset,
                severity=severity,
                success=expectation_result.success,
                invalid_rows=invalid_rows,
                message=message,
            )
        )

    return quality_results