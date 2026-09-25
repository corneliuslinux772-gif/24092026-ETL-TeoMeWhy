import great_expectations as gx

from gx.config import (
    CURSOS_CHECKPOINT_NAME,
)


context = gx.get_context(mode="file")


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
# GET VALIDATION RESULTS
# ============================================================

validation_results = result.run_results

validation_result = next(
    iter(validation_results.values())
)


# ============================================================
# HEADER
# ============================================================

print("=" * 50)
print("DATA QUALITY VALIDATION")
print("Dataset: cursos")
print("Batch: cursos.csv")
print("=" * 50)


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

    column = expectation_config.kwargs.get("column")

    expectation_success = expectation_result.success

    # --------------------------------------------------------
    # Human-readable label
    # --------------------------------------------------------

    if expectation_type == "expect_column_values_to_not_be_null":
        label = f"{column} NOT NULL"

    elif expectation_type == "expect_column_values_to_be_unique":
        label = f"{column} UNIQUE"

    else:
        label = expectation_type

    status = "✓" if expectation_success else "✗"

    print(f"  {status} {label}")


# ============================================================
# STATISTICS
# ============================================================

statistics = validation_result.statistics

evaluated = statistics["evaluated_expectations"]

successful = statistics["successful_expectations"]

print()

print(
    f"{successful}/{evaluated} expectations passed"
)

print("=" * 50)


# ============================================================
# PIPELINE STATUS
# ============================================================

if not success:
    raise RuntimeError(
        "Data quality validation failed."
    )