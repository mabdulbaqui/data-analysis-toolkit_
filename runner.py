import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from data_analyzer import DataAnalyzer
from data_visualization import DataVisualization
from report_generator import ReportGenerator


# Generate a PDF with exploratory data analysis visualizations
def run_example_pdf_visu(df=None, name=None):
    data_visualization = DataVisualization(df)

    # Define the PDF filename
    pdf_filename = f"eda_report_graphs_{name}.pdf" if name is not None else "eda_report_graphs.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []

    # Add a title to the PDF
    title_style = getSampleStyleSheet()["Title"]
    title = Paragraph("Exploratory Data Analysis Results", style=title_style)
    elements.append(title)

    # Generate and add categorical column plots to the PDF
    imgs = data_visualization.plot_categorical_columns(df, save=True)
    for i in imgs:
        elements.append(Image(i))

    # Generate and add numerical column plots to the PDF
    imgs = data_visualization.plot_numerical_columns(df, True)
    for i in imgs:
        elements.append(Image(i))

    # Build the PDF
    doc.build(elements)
    print("PDF generated successfully.")


# Generate a summary PDF report
def run_example_pdf_summary(df=None, name=None):
    analyzer = DataAnalyzer(df)

    pdf_filename = f"eda_report_summary_{name}.pdf" if name is not None else "eda_report_summary.pdf"

    report = ReportGenerator(pdf_filename)

    # Add descriptions and tables to the PDF

    # Column Types
    report.add_description("Column Types:")
    numerical_columns = ", ".join(analyzer.numerical_columns)
    categorical_columns = ", ".join(analyzer.categorical_columns)
    datetime_columns = ", ".join(analyzer.datetime_columns)
    report.add_table(["Type", "Column Names"], [
        ("Numerical Columns", numerical_columns),
        ("Categorical Columns", categorical_columns),
        ("Datetime Columns", datetime_columns)
    ])

    # Duplicate Percentage
    report.add_description("Duplicate Percentage:")
    duplicate_percentage, _ = analyzer.duplicates_nulls_percentage(df)
    report.add_table(["Metric", "Percentage"], [("Duplicate Percentage", f"{duplicate_percentage}%")])

    # Null Percentage
    report.add_description("Null Percentage:")
    _, null_percentage = analyzer.duplicates_nulls_percentage(df)
    null_table_data = [["Column Name", "Percentage"]]
    for column_name, percentage in null_percentage.items():
        null_table_data.append([column_name, f"{percentage:.2f}%"])
    report.add_table(null_table_data[0], null_table_data[1:])

    # Outliers
    report.add_description("Outliers:")
    outliers_info = analyzer.remove_outliers(df)
    report.add_table(["Column Name", "Percentage of Outliers", "Number of Outliers"],
                     [(info['Name'], f"{info['Percentage'] * 100:.2f}%", info['Number_Of_Outliers']) for info in
                      outliers_info])

    # Statistics for Numerical Columns
    for num_col in analyzer.numerical_columns:
        report.add_description(f"Statistics for {num_col}:")
        column_stats = df[num_col].describe(percentiles=[0.25, 0.5, 0.75])
        stats_table_data = [["Statistic", "Value"]]
        for stat, value in column_stats.items():
            stats_table_data.append([stat, f"{value:.2f}"])
        report.add_table(stats_table_data[0], stats_table_data[1:])

    # Top 10 Value Counts for Categorical Columns
    for cat_col in analyzer.categorical_columns:
        report.add_description(f"Top 10 Value Counts for {cat_col}:")
        value_counts = df[cat_col].value_counts().reset_index()
        value_counts.columns = ["Category", "Count"]
        top_10_value_counts = value_counts.head(10)
        value_counts_table_data = top_10_value_counts.values.tolist()
        report.add_table(["Category", "Count"], value_counts_table_data)

    # Generate the PDF
    report.generate_pdf()
    analyzer.encode_scale_features(df)
    df.to_csv(f"{name}_scaled.csv", index=False)

    print("PDF summary report generated successfully.")


# Remove directories starting with a specific prefix
def remove_directories(starting_with="directory"):
    current_directory = os.getcwd()
    items = os.listdir(current_directory)

    # Iterate through items in the directory
    for item in items:
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path) and item.startswith(starting_with):
            try:
                shutil.rmtree(item_path)  # Use shutil.rmtree() to remove non-empty directories
                print(f"Removed directory: {item}")
            except Exception as e:
                print(f"Error removing directory {item}: {e}")


# Entry point of the script
if __name__ == '__main__':
    pass
