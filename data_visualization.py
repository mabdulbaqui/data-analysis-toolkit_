import os

import matplotlib.pyplot as plt
import seaborn as sns
from helper import *
import datetime

directory_name = None


def make_dir():
    """
    Create a directory with a formatted timestamp.
    """
    global directory_name
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    directory_name = f'directory_{formatted_datetime}'
    os.makedirs(directory_name)
    current_time = datetime.datetime.now().time()
    formatted_time = current_time.strftime('%H-%M-%S')


def save_img(title: str, fig, fig_ax=None):
    """
    Save the given figure and optionally axis to an image file.
    """
    if directory_name is None:
        make_dir()

    if fig_ax is None:
        title = title.lower().replace(" ", "_")
        img_path = f"{directory_name}/{title}.jpg"
        fig.savefig(img_path)
        return img_path
    else:
        return fig_ax


class DataVisualization:
    """
    Class for generating various data visualizations from a DataFrame.
    """
    _instance = None

    def __new__(cls, df):
        """
        Create a new instance of DataVisualization if it doesn't exist.

        Parameters:
        df (pd.DataFrame): Input DataFrame.

        Returns:
        DataVisualization instance.
        """
        if cls._instance is None:
            cls._instance = super(DataVisualization, cls).__new__(cls)
            cls._instance.preprocessor = DataPreprocessor(df)  # Instantiate DataPreprocessor

            cls._instance.numerical_columns = cls._instance.preprocessor.numerical_columns
            cls._instance.categorical_columns = cls._instance.preprocessor.categorical_columns
            cls._instance.datetime_columns = cls._instance.preprocessor.datetime_columns

            cls._instance.initialized = True
        return cls._instance

    def __init__(self, df):
        """
        Initialize the DataVisualization instance with a DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        """
        if hasattr(self, 'initialized'):
            return

    @staticmethod
    def plot_boxplot(df, column, save=False, fig_ax=False):
        """
        Plot a box plot for the given column in the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name.
        save (bool): Whether to save the plot as an image.
        fig_ax: Optional axis to save for further customization.

        Returns:
        str or Axes: Image path if saved, else axis object.
        """
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(data=df, y=column, ax=ax)
        ax.set_title(f'Box Plot of {column}')
        ax.set_ylabel(column)
        plt.tight_layout()
        ret = None
        if save:
            ret = save_img(ax.get_title(), fig)
        elif fig_ax:
            ret = save_img(ax.get_title(), (fig, ax))
        else:
            plt.show()
            plt.close(fig)

        plt.close(fig)
        return ret

    @staticmethod
    def plot_density(df, column, save=False, fig_ax=False):
        """
        Plot a density plot for the given column in the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name.
        save (bool): Whether to save the plot as an image.
        fig_ax: Optional axis to save for further customization.

        Returns:
        str or Axes: Image path if saved, else axis object.
        """
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.kdeplot(df[column], fill=True, ax=ax)
        ax.set_title(f'Density Plot of {column}')
        ret = None
        if save:
            ret = save_img(ax.get_title(), fig)
        elif fig_ax:
            ret = save_img(ax.get_title(), (fig, ax))
        else:
            plt.show()
            plt.close(fig)

        plt.close(fig)
        return ret

    @staticmethod
    def plot_skewness_kurtosis(df, column, save=False, fig_ax=False
                               ):
        """
        Plot a histogram with skewness and kurtosis information for the given column in the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name.
        save (bool): Whether to save the plot as an image.
        fig_ax: Optional axis to save for further customization.

        Returns:
        str or Axes: Image path if saved, else axis object.
        """
        skewness = df[column].skew()
        kurt = df[column].kurtosis()

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df, x=column, bins=10, kde=True, fill=True, ax=ax)
        ax.set_title(f'Histogram of {column}\nSkewness: {skewness:.2f}, Kurtosis: {kurt:.2f}')

        ret = None
        if save:
            ret = save_img(ax.get_title(), fig)
        elif fig_ax:
            ret = save_img(ax.get_title(), (fig, ax))
        else:
            plt.show()
            plt.close(fig)

        plt.close(fig)
        return ret

    @staticmethod
    def plot_categorical_count(df, column, save=False, fig_ax=False
                               ):
        """
        Plot a count plot for the given categorical column in the DataFrame.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name.
        save (bool): Whether to save the plot as an image.
        fig_ax: Optional axis to save for further customization.

        Returns:
        str or Axes: Image path if saved, else axis object.
        """
        fig, ax = plt.subplots(figsize=(8, 5))

        # Get the top 10 categories by count
        top_categories = df[column].value_counts().head(10).index

        # Filter the DataFrame to include only the top 10 categories
        df_filtered = df[df[column].isin(top_categories)]

        sns.countplot(data=df_filtered, x=column, ax=ax)
        ax.set_title(f'Count Plot of {column} (Top 10)')
        plt.xticks(rotation=45)

        ret = None
        if save:
            ret = save_img(ax.get_title(), fig)
        elif fig_ax:
            ret = save_img(ax.get_title(), (fig, ax))
        else:
            plt.show()
            plt.close(fig)

        plt.close(fig)
        return ret

    def plot_categorical_columns(self, df, save=False, fig_ax=False
                         ):
        """
        Generate and save count plots for all categorical columns.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        save (bool): Whether to save the plots as images.
        fig_ax: Optional axis to save for further customization.

        Returns:
        list: List of image paths if saved, else an empty list.
        """

        imgs_dir = []
        for column in self.categorical_columns:
            x = self.plot_categorical_count(df, column, save, fig_ax)
            imgs_dir.append(x)

        return imgs_dir

    @staticmethod
    def plot_correlation_matrix(df, columns=None, save=False, fig_ax=False
                                ):
        """
        Generate and save a correlation matrix plot for the given columns.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        columns (list or None): Columns for which to generate the correlation matrix.
        save (bool): Whether to save the plot as an image.
        fig_ax: Optional axis to save for further customization.

        Returns:
        str or Axes: Image path if saved, else axis object.
        """
        if columns is not None:
            df = df[columns]
        fig, ax = plt.subplots(figsize=(8, 5))

        corr_matrix = df.corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title("Correlation Matrix")

        ret = None
        if save:
            ret = save_img(ax.get_title(), fig)
        elif fig_ax:
            ret = save_img(ax.get_title(), (fig, ax))
        else:
            plt.show()
            plt.close(fig)

        plt.close(fig)
        return ret

    def plot_numerical_columns(self, df, save=False, fig_ax=False
                               ):
        """
        Generate and save various visualizations for numerical columns.

        Parameters:
        df (pd.DataFrame): Input DataFrame.
        save (bool): Whether to save the plots as images.
        fig_ax: Optional axis to save for further customization.

        Returns:
        list: List of image paths if saved, else an empty list.
        """

        imgs_dir = []
        for column in self.numerical_columns:
            x = self.plot_boxplot(df, column, save, fig_ax)
            y = self.plot_density(df, column, save, fig_ax)
            z = self.plot_skewness_kurtosis(df, column, save, fig_ax)
            if save:
                imgs_dir.append(x)
                imgs_dir.append(y)
                imgs_dir.append(z)
        x = self.plot_correlation_matrix(df, self.numerical_columns, save, fig_ax)
        imgs_dir.append(x)
        return imgs_dir
