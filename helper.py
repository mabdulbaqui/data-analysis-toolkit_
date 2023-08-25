import os
import re

import pandas as pd


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")
    else:
        print(f"Directory '{path}' already exists.")


class DataPreprocessor:
    """
    Data preprocessor class to preprocess DataFrame columns.
    """

    def __init__(self, df, info=True):
        self._preprocess_data(df)
        if info:
            self._print_column_info()
        create_directory("Report")

    def _preprocess_data(self, df):
        """
        Preprocess data to identify numerical, categorical, and datetime columns.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        """
        convert_object_columns_to_datetime(df)
        convert_date_columns_to_datetime(df)
        self.numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        self.categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        self.datetime_columns = df.select_dtypes(include=['datetime64']).columns.tolist()

    def _print_column_info(self):
        """
        Print information about the column types.
        """
        print("Numerical Columns:", self.numerical_columns)
        print("Categorical Columns:", self.categorical_columns)
        print("Datetime Columns:", self.datetime_columns)


def convert_object_columns_to_datetime(df):
    """
    Convert object columns with date-like strings to datetime.

    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    dict: Dictionary of unmatched cells in columns.
    """
    date_patterns = [
        re.compile(r'\d{4}-\d{2}-\d{2}'),
        re.compile(r'\d{4}/\d{2}/\d{2}'),
        re.compile(r'\d{2}/\d{2}/\d{4}'),
        re.compile(r'\d{2}-\d{2}-\d{4}')
    ]
    unmatched = {}

    for column in df.columns:
        if df[column].dtype == 'object':
            unmatched_cells_column = []
            match_all = True
            semi_match = False
            for index, value in df[column].iloc[:1000].items():
                if pd.isna(value) or not any(pattern.match(value) for pattern in date_patterns):
                    match_all = False
                    unmatched_cells_column.append(index)
                else:
                    semi_match = True

            if match_all:
                try:
                    df[column] = pd.to_datetime(df[column])
                except (ValueError, TypeError):
                    pass
            if semi_match and not match_all:
                unmatched[column] = unmatched_cells_column

    return unmatched


def convert_date_columns_to_datetime(df):
    """
    Convert columns containing date-related keywords to datetime.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    """
    date_keywords = ['year', 'month', 'day']

    for column in df.columns:
        if any(keyword in column.lower() for keyword in date_keywords):
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce')
            except (ValueError, TypeError):
                pass


def binary_cols(df):
    """
    Identify and convert binary columns to categorical data type.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    """
    binary_columns = []
    for column in df.columns:
        unique_values = df[column].unique()
        if len(unique_values) == 2 and (0 in unique_values and 1 in unique_values) or (
                "0" in unique_values and "1" in unique_values):
            binary_columns.append(column)

    # Convert binary columns to categorical data type
    df[binary_columns] = df[binary_columns].astype('category')
