from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime  # Import datetime module

def generateT_pdf(df, filename="tables.pdf"):
    """Generate a PDF from a DataFrame with borders, total row, and multipage support."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4  # Use A4 page size
    margin = 25
    line_height = 20
    col_width = 180
    num_cols = len(df.columns)

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    def draw_headers(c, x, y):
        """Draw column headers with red background and white text."""
        c.setFont("Helvetica-Bold", 10)
        headers = df.columns.tolist()
        for header in headers:
            c.setFillColor(colors.red)
            c.rect(x, y, col_width, line_height, stroke=1, fill=1)  # Red background with border
            c.setFillColor(colors.white)
            c.drawString(x + 5, y + 5, header)  # White text
            x += col_width

    def draw_row(c, x, y, row):
        """Draw a single row of data."""
        c.setFont("Helvetica", 8)
        for value in row:
            c.setFillColor(colors.black)
            c.rect(x, y, col_width, line_height, stroke=1, fill=0)  # Draw cell border without fill
            c.drawString(x + 5, y + 5, str(value))
            x += col_width

    def new_page(c, x, y):
        """Handle adding a new page if content exceeds current page."""
        c.showPage()
        y = height - margin - line_height - 40  # Add padding for subsequent pages
        draw_headers(c, margin, y)
        return y - line_height

    # Title with current date
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, height - margin, f"Rapport - {current_date}")

    # Start drawing content with extra padding below the title
    y = height - margin - line_height - 40  # 40 units of padding between title and table
    draw_headers(c, margin, y)
    y -= line_height

    for i, row in df.iterrows():
        if y < margin:  # Check if new page is needed
            y = new_page(c, margin, y)
        draw_row(c, margin, y, row)
        y -= line_height

    c.save()
    buffer.seek(0)
    return buffer