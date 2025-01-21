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
    
    # Add stock data as table (ensuring it's neat)
    pdf.ln(5)
    col_width = pdf.get_string_width('Date') + 10
    col_width2 = pdf.get_string_width('Close') + 10
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(col_width, 10, 'Date', border=1, align='C')
    pdf.cell(col_width2, 10, 'Close Price', border=1, align='C')
    pdf.ln()

    pdf.set_font('Arial', '', 10)
    for i, row in stock_data.iterrows():
        pdf.cell(col_width, 10, row.name.strftime("%Y-%m-%d"), border=1, align='C')
        pdf.cell(col_width2, 10, f"{row['Close']:.2f}", border=1, align='C')
        pdf.ln()

    # Add technical indicators
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, 'Technical Indicators:', ln=True)
    pdf.set_font('Arial', '', 12)

    # Add technical indicators as table (similar approach)
    pdf.ln(5)
    for col in indicators.columns:
        pdf.cell(col_width, 10, col, border=1, align='C')
    pdf.ln()

    for i in range(len(indicators)):
        pdf.set_font('Arial', '', 10)
        for value in indicators.iloc[i]:
            pdf.cell(col_width, 10, f"{value:.2f}", border=1, align='C')
        pdf.ln()

    # Add AI Insights
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, 'AI Insights:', ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, insights)

    # Save PDF to file
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

