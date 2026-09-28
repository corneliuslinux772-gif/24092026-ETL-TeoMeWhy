import great_expectations as gx
from great_expectations import expectations as gxe
from gx.config import HABILIDADES_USUARIOS_SUITE_NAME


context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Expectation Suite
# ---------------------------------------------------------

try:
    suite = context.suites.get(HABILIDADES_USUARIOS_SUITE_NAME)
    print(f"Expectation Suite já existe: {HABILIDADES_USUARIOS_SUITE_NAME}")

except Exception:
    suite = gx.ExpectationSuite(
        name=HABILIDADES_USUARIOS_SUITE_NAME
    )

    suite = context.suites.add(suite)

    print(f"Expectation Suite criada: {HABILIDADES_USUARIOS_SUITE_NAME}")


# ---------------------------------------------------------
# Helper: Idempotência
# ---------------------------------------------------------

def add_if_missing(suite, expectation):

    for existing in suite.expectations:

        if existing == expectation:
            return

    suite.add_expectation(expectation)


# ---------------------------------------------------------
# Helper: Remove Expectation
# ---------------------------------------------------------

def removeExpectation(column_name):
    for existing in suite.expectations.copy():

        if (
            type(existing) is gxe.ExpectColumnValuesToNotBeNull
            and existing.column == column_name
        ):
            suite.delete_expectation(existing)


# ---------------------------------------------------------
# Expectations
# ---------------------------------------------------------

expectations = [
    gxe.ExpectColumnValuesToNotBeNull(
        column="idHabilidadeusuario",
    ),

    gxe.ExpectColumnValuesToBeUnique(
        column="idHabilidadeusuario",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="idUsuario",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="descNomeHabilidade",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="dtCriacao",
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