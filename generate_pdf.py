from fpdf import FPDF

# Function to generate the PDF report
def generate_pdf(company_name, exchange, interval, stock_data, indicators, insights):
    # Create PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title of the PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt=f"AI-Based Stock Insights for {company_name}", ln=True, align='C')

    # Add a space after the title
    pdf.ln(10)

    # Add introduction
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f"Stock Exchange: {exchange}\nCompany: {company_name}\nTime Interval: {interval}\n\n")
    
    # Section 1: Historical Stock Data
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, 'Historical Stock Data:', ln=True)
    pdf.set_font('Arial', '', 12)
    
    # Add stock data as a table
    pdf.ln(5)

    # Prepare table headers and dynamic column widths
    headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    col_widths = [30, 30, 30, 30, 30, 30]  # Adjust column widths if needed

    # Set fill color for headers (light gray) and text color (black)
    pdf.set_fill_color(220, 220, 220)
    pdf.set_text_color(0, 0, 0)

    # Add table headers
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
    pdf.ln()

    # Reset text color for data rows
    pdf.set_text_color(0, 0, 0)

    # Add stock data rows
    for i, row in stock_data.iterrows():
        pdf.cell(col_widths[0], 10, row.name.strftime("%Y-%m-%d"), border=1, align='C')
        pdf.cell(col_widths[1], 10, f"{row['Open']:.2f}", border=1, align='C')
        pdf.cell(col_widths[2], 10, f"{row['High']:.2f}", border=1, align='C')
        pdf.cell(col_widths[3], 10, f"{row['Low']:.2f}", border=1, align='C')
        pdf.cell(col_widths[4], 10, f"{row['Close']:.2f}", border=1, align='C')
        pdf.cell(col_widths[5], 10, f"{row['Volume']:,}", border=1, align='C')
        pdf.ln()

    # Add technical indicators
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, 'Technical Indicators:', ln=True)
    pdf.set_font('Arial', '', 12)

    # Prepare indicator table headers and dynamic column widths
    pdf.ln(5)
    indicator_headers = indicators.columns.tolist()
    col_widths = [28] * len(indicator_headers)  # Adjust column widths dynamically

    # Set fill color for headers
    pdf.set_fill_color(220, 220, 220)

    # Add technical indicator headers
    for i, header in enumerate(indicator_headers):
        pdf.cell(col_widths[i], 10, header, border=1, align='C', fill=True)
    pdf.ln()

    # Add indicator rows
    for i in range(len(indicators)):
        for value in indicators.iloc[i]:
            pdf.cell(col_widths[i % len(indicator_headers)], 10, f"{value:.2f}", border=1, align='C')
        pdf.ln()

    # Add AI Insights
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, 'AI Insights:', ln=True)
    pdf.set_font('Arial', '', 12)

    # Format AI insights: Replace **text** with bold text
    insights = insights.replace("**", "")  # Temporarily remove ** to simplify parsing
    lines = insights.split('\n')
    for line in lines:
        if line.strip().startswith("*") and line.strip().endswith("*"):
            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 10, line.strip("*"))
            pdf.set_font('Arial', '', 12)
        else:
            pdf.multi_cell(0, 10, line)

    # Save PDF to file and return as bytes
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output
