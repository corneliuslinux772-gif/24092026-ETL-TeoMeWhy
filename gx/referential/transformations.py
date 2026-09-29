import pandas as pd


def extract_nr_ep(series: pd.Series) -> pd.Series:
    """
    Extrai o número do episódio de valores no formato 'ep-XX'.

    Exemplos:
        ep-00 -> 0
        ep-01 -> 1
        ep-12 -> 12
        ep-35 -> 35
    """

    return (
        series
        .str.extract(r"ep-(\d+)", expand=False)
        .astype("Int64")
    )