import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datasist.structdata import detect_outliers
from helper import *
from data_downloader import download_example

class DataAnalyzer:
    _instance = None

    def __new__(cls, df):
        """
        Create a new instance of DataAnalyzer if it doesn't exist.

        Parameters:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        DataAnalyzer instance.
        """
        if cls._instance is None:
            cls._instance = super(DataAnalyzer, cls).__new__(cls)
        return cls._instance

    def __init__(self, df):
        """
        Initialize DataAnalyzer instance.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        """
        if hasattr(self, 'initialized'):
            return
        self.preprocessor = DataPreprocessor(df)  # Pass the DataFrame
        pd.set_option('display.max_rows', None)

        self.numerical_columns = self.preprocessor.numerical_columns
        self.categorical_columns = self.preprocessor.categorical_columns
        self.datetime_columns = self.preprocessor.datetime_columns

    @staticmethod
    def duplicates_nulls_percentage(df):
        """
        Calculate the percentage of duplicates and null values in the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        tuple: A tuple containing duplicate percentage and null percentage.
        """
        try:
            duplicate_percentage = (df.duplicated().mean() * 100).round(2)
            null_percentage = (df.isnull().mean() * 100).round(2)
            return duplicate_percentage, null_percentage
        except Exception as e:
            print("Error occurred while calculating duplicate and null percentages.")
            print(f"Error message: {str(e)}")
            return None, None

    @staticmethod
    def remove_duplicates_and_nulls_from_dataframe(df):
        """
        Remove duplicates and null values from the DataFrame in place.

        Parameters:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        None
        """
        try:
            df.drop_duplicates(inplace=True)
            df.dropna(inplace=True)
            df.reset_index(drop=True, inplace=True)
        except Exception as e:
            print("Error occurred while removing duplicates and null values.")
            print(f"Error message: {str(e)}")

    def remove_outliers(self, df, cols=None):
        """
        Detect and remove outliers from the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        cols (list or None): List of column names to analyze. If None, use all numerical columns.

        Returns:
        list: A list of dictionaries containing outlier information.
        """
        try:
            idx = self.numerical_columns if cols is None else cols
            dic = []
            for column_name in idx:
                outliers_indices = detect_outliers(df, 0, [column_name])
                dic.append({'Name': column_name,
                            'Percentage': len(outliers_indices) / len(df[column_name]),
                            'Number_Of_Outliers': len(outliers_indices)
                            })

            # Replace detect_outliers with your outlier detection function
            # df.drop(outliers_indices, inplace=True, axis=0)
            return dic
        except Exception as e:
            print("Error occurred while removing outliers.")
            print(f"Error message: {str(e)}")
            return 0

    @staticmethod
    def dataframe_summary_to_dict(df):
        """
        Generate a summary dictionary from the DataFrame's statistics.

        Parameters:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        dict: A dictionary containing summary statistics.
        """
        summary = df.describe(include='all').to_dict()
        return summary

    def encode_scale_features(self, df):
        """
        Encode and scale features in the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        None
        """
        try:
            numerical_features = self.numerical_columns
            categorical_features = self.categorical_columns

            scaler = StandardScaler()
            label_encoder = LabelEncoder()

            df[numerical_features] = scaler.fit_transform(df[numerical_features])

            for cat_feature in categorical_features:
                df[cat_feature] = label_encoder.fit_transform(df[cat_feature])

            df[categorical_features] = df[categorical_features].astype("category")
        except Exception as e:
            print("Error occurred while encoding features.")
            print(f"Error message: {str(e)}")
