import pandas as pd

def clean_filename_column(df, source_col='FileName', new_col='FileNameClean', to_lower=False, to_title=True):
    """
    Membersihkan nama file dari karakter asing, simbol, dan spasi berlebih.
    """
    series = df[source_col].astype(str)

    # Bersihkan karakter asing: kurung, tanda baca, simbol
    series = series.str.replace(r'[\[\]\(\)\{\}_\-]', ' ', regex=True)
    series = series.str.replace(r'[^\w\s]', '', regex=True)
    series = series.str.replace(r'\s+', ' ', regex=True)
    series = series.str.strip()

    # Format huruf
    if to_lower:
        series = series.str.lower()
    elif to_title:
        series = series.str.title()

    df[new_col] = series
    return df