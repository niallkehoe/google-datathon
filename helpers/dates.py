import pandas as pd


@pd.api.extensions.register_dataframe_accessor("generate_year")
class StateColumnGenerator:
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def __call__(self, date_column="Date"):
        # Apply the mapping function to the specified column
        self._obj['Year'] = self._obj[date_column].str.split("-").str[0]
        return self._obj
