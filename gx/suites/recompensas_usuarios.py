import great_expectations as gx
from great_expectations import expectations as gxe
from gx.config import RECOMPENSAS_SUITE_NAME


context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Expectation Suite
# ---------------------------------------------------------

try:
    suite = context.suites.get(RECOMPENSAS_SUITE_NAME)
    print(f"Expectation Suite já existe: {RECOMPENSAS_SUITE_NAME}")

except Exception:
    suite = gx.ExpectationSuite(
        name=RECOMPENSAS_SUITE_NAME
    )

    suite = context.suites.add(suite)

    print(f"Expectation Suite criada: {RECOMPENSAS_SUITE_NAME}")


# ---------------------------------------------------------
# Helper: Idempotência
# ---------------------------------------------------------

def add_if_missing(suite, expectation):

    for existing in suite.expectations:

        if existing == expectation:
            return

    suite.add_expectation(expectation)



# ---------------------------------------------------------
# Expectations
# ---------------------------------------------------------

expectations = [
    gxe.ExpectColumnValuesToNotBeNull(
        column="idUsuario",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="idRecompensa",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="dtRecompensa",
    ),
]


for expectation in expectations:
    add_if_missing(
        suite,
        expectation,
    )


# ---------------------------------------------------------
# Persist
# ---------------------------------------------------------

context.suites.add_or_update(suite)


print("\nExpectation Suite:")
print(suite)