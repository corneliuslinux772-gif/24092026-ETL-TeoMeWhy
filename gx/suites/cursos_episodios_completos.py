import great_expectations as gx
from great_expectations import expectations as gxe
from gx.config import CURSOS_EPISODIOS_COMPLETOS_SUITE_NAME


context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Expectation Suite
# ---------------------------------------------------------

try:
    suite = context.suites.get(CURSOS_EPISODIOS_COMPLETOS_SUITE_NAME)
    print(f"Expectation Suite já existe: {CURSOS_EPISODIOS_COMPLETOS_SUITE_NAME}")

except Exception:
    suite = gx.ExpectationSuite(
        name=CURSOS_EPISODIOS_COMPLETOS_SUITE_NAME
    )

    suite = context.suites.add(suite)

    print(f"Expectation Suite criada: {CURSOS_EPISODIOS_COMPLETOS_SUITE_NAME}")


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

# descSlugCurso;descSlugCursoEpisodio;dtCriacao

expectations = [
    gxe.ExpectColumnValuesToNotBeNull(
        column="idCursoEpisodioCompleto",
    ),

    gxe.ExpectColumnValuesToBeUnique(
        column="idCursoEpisodioCompleto",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="idUsuario",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="descSlugCurso",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="descSlugCursoEpisodio",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="dtCriacao",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="nrAno",
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