from runner import *
from data_downloader import *


def greet_user():
    """
    Display a welcome message to the user.
    """
    print("Hello! Welcome to the Data Analysis CLI.")


def get_custom_data_path():
    """
    Prompt the user to choose a custom dataset and return the dataset name.

    Returns:
    str: The chosen custom dataset name.
    """
    print("Available datasets:")
    print("1. parulpandey/us-international-air-traffic-data")
    response = input("Would you like to use a custom dataset? (yes/no): ").lower()
    if response == "yes":
        return input("Please enter the dataset name (e.g., 'pastureland/us-international-air-traffic-data'): ")


def get_report_types():
    """
    Prompt the user to choose the type of report to generate and return the selected report types.

    Returns:
    list: A list of report types to generate. Possible values: ["pdf_visu"], ["pdf_summary"], ["pdf_visu", "pdf_summary"], or [].
    """
    print("Which type of report would you like to generate?")
    response = input("Enter 'pdf_visu', 'pdf_summary', or 'both': ").lower()
    if response == "pdf_visu":
        return ["pdf_visu"]
    elif response == "pdf_summary":
        return ["pdf_summary"]
    elif response == "both":
        return ["pdf_visu", "pdf_summary"]
    else:
        return []


if __name__ == '__main__':
    greet_user()
    custom_data_path = get_custom_data_path()
    if custom_data_path is None:
        df, name = download_example()
    else:
        df, name = read_file_to_dataframe(custom_data_path)  # Update this if your data is in a different format

    report_types = get_report_types()

    if not report_types:
        print("No valid report types selected. Exiting.")
        exit()

    for report_type in report_types:
        if report_type == "pdf_visu":
            run_example_pdf_visu(df, name)
        elif report_type == "pdf_summary":
            run_example_pdf_summary(df, name)

    print("Reports generated successfully.")

    remove_directories()
