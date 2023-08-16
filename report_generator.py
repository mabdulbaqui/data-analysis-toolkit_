from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak


class ReportGenerator:
    def __init__(self, output_file):
        """
        Initialize the ReportGenerator instance.

        Parameters:
        output_file (str): The name of the output PDF file.
        """
        self.output_file = output_file
        self.data = []

    def add_description(self, text):
        """
        Add a descriptive text paragraph to the report.

        Parameters:
        text (str): The description text to add.
        """
        self.data.append(Paragraph(text, getSampleStyleSheet()["Normal"]))
        self.data.append(Table([("",)]))  # Add an empty table as a separator

    def add_table(self, headers, rows):
        """
        Add a table to the report.

        Parameters:
        headers (list): List of header strings for the table.
        rows (list of lists): List of row data for the table.
        """
        table_data = [headers] + rows
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        self.data.append(table)
        self.data.append(Table([("----------",)]))  # Add an empty table as a separator

    def generate_pdf(self):
        """
        Generate the PDF report using the collected data.

        Returns:
        None
        """
        doc = SimpleDocTemplate(self.output_file, pagesize=letter)
        doc.build(self.data)

    def add_page_break(self):
        """
        Add a page break to the report.

        Returns:
        None
        """
        self.data.append(PageBreak())