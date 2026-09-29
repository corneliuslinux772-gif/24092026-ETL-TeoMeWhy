import great_expectations as gx
import pandas as pd

from gx.config import (
    CURSOS_CHECKPOINT_NAME,
)

from gx.quality.gx_adapter import (
    adapt_gx_result,
)

from gx.quarantine import (
    QuarantineManager,
)


# ============================================================
# CONFIG
# ============================================================

DATASET = "cursos"

SOURCE_FILE = "data/raw/cursos.csv"


# ============================================================
# CONTEXT
# ============================================================

context = gx.get_context(mode="file")


# ============================================================
# LOAD SOURCE DATA
# ============================================================

df = pd.read_csv(
    SOURCE_FILE,
    sep=";",
    encoding="utf-8",
    low_memory=False,
)


# ============================================================
# CHECKPOINT
# ============================================================

checkpoint = context.checkpoints.get(
    CURSOS_CHECKPOINT_NAME
)


# ============================================================
# RUN CHECKPOINT
# ============================================================

result = checkpoint.run()


# ============================================================
# GET VALIDATION RESULT
# ============================================================

validation_results = result.run_results

validation_result = next(
    iter(validation_results.values())
)


# ============================================================
# HEADER
# ============================================================

print("=" * 60)
print("DATA QUALITY VALIDATION")
print("Dataset: cursos")
print("Batch: cursos.csv")
print("=" * 60)


# ============================================================
# STATUS
# ============================================================

success = validation_result.success

print()

if success:
    print("Status: PASS")
else:
    print("Status: FAIL")


# ============================================================
# EXPECTATIONS
# ============================================================

print("\nExpectations:")

for expectation_result in validation_result.results:

    expectation_config = expectation_result.expectation_config

    expectation_type = expectation_config.type

    column = expectation_config.kwargs.get(
        "column"
    )

    expectation_success = expectation_result.success

    if expectation_type == "expect_column_values_to_not_be_null":

        label = f"{column} NOT NULL"

    elif expectation_type == "expect_column_values_to_be_unique":

        label = f"{column} UNIQUE"

    else:

        label = expectation_type

    status = "✓" if expectation_success else "✗"

    print(
        f"  {status} {label}"
    )


# ============================================================
# STATISTICS
# ============================================================

statistics = validation_result.statistics

evaluated = statistics[
    "evaluated_expectations"
]

successful = statistics[
    "successful_expectations"
]

print()

print(
    f"{successful}/{evaluated} expectations passed"
)

print("=" * 60)


# ============================================================
# ADAPT GX → QUALITY CONTRACT
# ============================================================

quality_results = adapt_gx_result(
    validation_result,
    df,
    dataset=DATASET,
)


# ============================================================
# QUARANTINE
# ============================================================

quarantine_manager = QuarantineManager()


print()
print("QUALITY RESULTS:")

for quality_result in quality_results:

    print()
    print(
        f"Check: {quality_result.check_name}"
    )

    print(
        f"Severity: {quality_result.severity}"
    )

    print(
        f"Success: {quality_result.success}"
    )

    if quality_result.invalid_rows is not None:

        print(
            f"Invalid rows: "
            f"{len(quality_result.invalid_rows)}"
        )

    quarantine_result = (
        quarantine_manager.process(
            quality_result,
            source_file=SOURCE_FILE,
            quarantine_reason=(
                quality_result.message
                or "Great Expectations validation failure"
            ),
        )
    )

    if quarantine_result.output_file:

        print(
            f"Quarantine: "
            f"{quarantine_result.output_file}"
        )


# ============================================================
# FINAL PIPELINE STATUS
# ============================================================

print()
print("=" * 60)

if success:

    print(
        "DATA QUALITY: PASS"
    )

else:

    print(
        "DATA QUALITY: FAIL "
        "(invalid rows processed)"
    )

print("=" * 60)