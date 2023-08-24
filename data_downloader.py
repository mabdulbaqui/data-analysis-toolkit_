import os
import kaggle
import pandas as pd
import sqlite3
import os
from helper import create_directory


def download_dataset(pattern="international", dataset_name="parulpandey/us-international-air-traffic-data",
                     destination_directory="./Data"):
    """
    Download a dataset from Kaggle.

    Parameters:
    pattern (str): A pattern to check for existing files.
    dataset_name (str): The name of the Kaggle dataset.
    destination_directory (str): The directory to save the downloaded dataset.

    Returns:
    None
    """
    create_directory(destination_directory)
    files_with_pattern = [file for file in os.listdir(destination_directory) if pattern in file.lower()]

    if files_with_pattern:
        print(f"File with '{pattern}' in its name already exists.")
    else:
        try:
            # Download the dataset using Kaggle API
            kaggle.api.dataset_download_files(dataset_name, path=destination_directory, unzip=True)
            print("Dataset downloaded successfully.")

            # Get the name of the downloaded zip file
            zip_file_name = [file for file in os.listdir(destination_directory) if file.endswith('.zip')][0]

            # Unzip the downloaded file
            os.system(f'unzip {os.path.join(destination_directory, zip_file_name)} -d {destination_directory}')

            # Remove the zipped file
            os.remove(os.path.join(destination_directory, zip_file_name))
            print("Zipped file removed.")
        except Exception as e:
            print(f"Error occurred while downloading and processing the dataset: {e}")


def extract_source_type(string):
    """
    Extract the source type from a given string.

    Parameters:
    string (str): The input string to check for source type patterns.

    Returns:
    str or None: The detected source type or None if not recognized.
    """
    source_type_patterns = {
        'csv': r'\b(csv)\b',
        'excel': r'\b(excel|xlsx)\b',
        'db': r'\b(db|sqlite|dbf)\b'
        # Add more patterns for other source types if needed
    }

    for source_type, pattern in source_type_patterns.items():
        if source_type in string.lower():
            return source_type

    return None


def read_file_to_dataframe(file_path):
    """
    Read a file into a pandas DataFrame based on its source type.

    Parameters:
    file_path (str): The path of the file to be read.

    Returns:
    pandas.DataFrame or None: The DataFrame containing the file's data or None if an error occurred.
    """
    # Extract the source type from the file path
    source_type = extract_source_type(file_path)

    if source_type is None:
        print("Unknown file format. Cannot read the file.")
        return None

    # Read the file into a data frame based on the source type
    if source_type == 'csv':
        df = pd.read_csv(file_path)
    elif source_type == 'excel':
        df = pd.read_excel(file_path)
    elif source_type == 'db':
        # Replace the database connection details below with your database connection
        conn = sqlite3.connect(file_path)
        query = "SELECT * FROM your_table_name;"
        df = pd.read_sql_query(query, conn)
        conn.close()
    else:
        print("Unknown source type. Cannot read the file.")
        return None

    return df, os.path.basename(file_path)


def download_example():
    """
    Download a dataset, find a CSV file, and read it into a DataFrame.

    Returns:
    pandas.DataFrame or None: The DataFrame containing data from the CSV file or None if an error occurred.
    """
    # Download the dataset
    download_dataset()

    # Get the list of all files in the current directory
    files_in_current_directory = [file for file in os.listdir() if os.path.isfile(file)]

    # Find the CSV file in the current directory
    csv_files = [file for file in files_in_current_directory if file.lower().endswith('.csv')]

    if not csv_files:
        print("No CSV file found in the current directory.")
        return None

    # Read the first CSV file into a DataFrame
    df, name = read_file_to_dataframe(csv_files[0])
    return df, name


def read_example_files(destination_directory="./Data"):
    """
    Download a dataset, find a CSV file, and read it into a DataFrame.

    Returns:
    list of pandas.DataFrame or None: List of DataFrames containing data from the CSV files or None if an error occurred.
    """
    # Download the dataset
    download_dataset()

    # Get the list of all files in the destination directory
    files_in_destination_directory = [file for file in os.listdir(destination_directory) if
                                      os.path.isfile(os.path.join(destination_directory, file))]

    # Find the CSV files in the destination directory
    csv_files = [file for file in files_in_destination_directory if file.lower().endswith('.csv')]

    return[os.path.join(destination_directory, csv_file) for csv_file in csv_files]


