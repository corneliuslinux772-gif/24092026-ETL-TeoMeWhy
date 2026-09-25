import great_expectations as gx
from great_expectations import expectations as gxe
from config import CURSOS_SUITE_NAME


context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Expectation Suite
# ---------------------------------------------------------

try:
    suite = context.suites.get(CURSOS_SUITE_NAME)
    print(f"Expectation Suite já existe: {CURSOS_SUITE_NAME}")

except Exception:
    suite = gx.ExpectationSuite(
        name=CURSOS_SUITE_NAME
    )

    suite = context.suites.add(suite)

    print(f"Expectation Suite criada: {CURSOS_SUITE_NAME}")


# ---------------------------------------------------------
# Expectations
# ---------------------------------------------------------

expectations = [
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="descSlugCurso",
    ),

    gx.expectations.ExpectColumnValuesToBeUnique(
        column="descSlugCurso",
    ),

    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="descCurso",
    ),

    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="descDescricao",
    ),

    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="nrAno",
    ),
]


for expectation in expectations:
    suite.add_expectation(expectation)


# ---------------------------------------------------------
# Persist
# ---------------------------------------------------------

context.suites.add_or_update(suite)


print("\nExpectation Suite:")
print(suite)