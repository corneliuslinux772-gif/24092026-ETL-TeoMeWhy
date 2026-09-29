from gx.quarantine.models import Severity


class PipelineStopError(RuntimeError):
    """
    Indica que uma validação SEVERE deve interromper o pipeline.
    """


def apply_severity_policy(severity: Severity) -> str:
    """
    Decide o comportamento do pipeline de acordo com a severidade.
    """

    if severity == Severity.PASS:
        return "CONTINUE"

    if severity == Severity.CRITICAL:
        return "QUARANTINE"

    if severity == Severity.SEVERE:
        raise PipelineStopError(
            "A validation returned SEVERE. "
            "Pipeline execution must stop."
        )

    raise ValueError(
        f"Unknown severity: {severity}"
    )