import great_expectations as gx

from great_expectations import expectations as gxe
from gx.config import CURSOS_EPISODIOS_SUITE_NAME

context = gx.get_context(mode="file")


# ---------------------------------------------------------
# Expectation Suite
# ---------------------------------------------------------

try:
    suite = context.suites.get(CURSOS_EPISODIOS_SUITE_NAME)
    print(f"Excepectation Suite já existe: {CURSOS_EPISODIOS_SUITE_NAME}")

except Exception:
    suite = gx.ExpectationSuite(
        name=CURSOS_EPISODIOS_SUITE_NAME
    )

    suite = context.suites.add(suite)

    print(f"Expectation Suite criada: {CURSOS_EPISODIOS_SUITE_NAME}")


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

# Simulando a lista de slugs válidos obtidos do dataset 'cursos':
# slugs_validos = ["python-basico", "machine-learning", "sql-avancado"] 

expectations = [
    # gxe.ExpectColumnValuesToBeInSet(
    #    column="descSlugCurso",
    #    value_set=slugs_validos
    #),

    gxe.ExpectColumnValuesToNotBeNull(
        column="descSlugCurso",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="nrEp",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="descEpisodio",
    ),

    gxe.ExpectColumnValuesToBeUnique(
        column="descEpisodio",
    ),

    gxe.ExpectColumnValuesToNotBeNull(
        column="descYoutubeID",
    ),

    gxe.ExpectColumnValuesToBeUnique(
        column="descYoutubeID",
    ),

    gxe.ExpectCompoundColumnsToBeUnique(
        column_list=["descSlugCurso", "nrEp"],
    ),
]

for expectation in expectations:
    add_if_missing(
        suite=suite,
        expectation=expectation,
    )


# ---------------------------------------------------------
# Persist
# ---------------------------------------------------------

context.suites.add_or_update(suite)


print("\nExpectation Suite:")
print(suite)