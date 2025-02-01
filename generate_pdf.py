from fpdf import FPDF

class StyledPDF(FPDF):
    def header(self):
        self.set_fill_color(220, 230, 240)
        self.rect(0, 0, 210, 20, 'F')
        self.set_font('Arial', '', 14)  # Regular font, not bold
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, 'AI-Based Stock Insights Report', ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def generate_pdf(company_name, stock_data, indicators, insights,exchange):
    pdf = StyledPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font('Arial', '', 28)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(0, 50, txt=f"{company_name} Stock Insights", ln=True, align='C')

    # Subtitle and Summary
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(34, 34, 34)
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"This report provides AI-generated stock insights for {company_name}. "
                          f"It includes historical stock data, technical indicators, and actionable insights for stakeholders.\n\n")

    pdf.ln(10)

    # Historical Stock Data Section
    pdf.add_page()
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 10, 'Historical Stock Data:', ln=True)

    headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    col_widths = [30, 30, 30, 30, 30, 30]

    pdf.set_font('Arial', '', 12)
    pdf.set_fill_color(200, 200, 255)
    pdf.set_text_color(0, 0, 0)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 12, header, border=1, align='C', fill=True)
    pdf.ln()

    fill = False
    pdf.set_text_color(0, 0, 0)
    for i, row in stock_data.iterrows():
        pdf.set_fill_color(240, 240, 240) if fill else pdf.set_fill_color(255, 255, 255)
        fill = not fill
        pdf.cell(col_widths[0], 12, row.name.strftime("%Y-%m-%d"), border=1, align='C', fill=True)
        pdf.cell(col_widths[1], 12, f"{row['Open']:.2f}", border=1, align='C', fill=True)
        pdf.cell(col_widths[2], 12, f"{row['High']:.2f}", border=1, align='C', fill=True)
        pdf.cell(col_widths[3], 12, f"{row['Low']:.2f}", border=1, align='C', fill=True)
        pdf.cell(col_widths[4], 12, f"{row['Close']:.2f}", border=1, align='C', fill=True)
        pdf.cell(col_widths[5], 12, f"{row['Volume']:,}", border=1, align='C', fill=True)
        pdf.ln()

    # Technical Indicators Section
    pdf.add_page()
    pdf.set_font('Arial', '', 14)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 10, 'Technical Indicators:', ln=True)

    pdf.set_font('Arial', '', 12)
    pdf.set_fill_color(200, 200, 255)
    pdf.set_text_color(0, 0, 0)
    indicator_headers = indicators.columns.tolist()
    col_widths = [28] * len(indicator_headers)
    for i, header in enumerate(indicator_headers):
        pdf.cell(col_widths[i], 12, header, border=1, align='C', fill=True)
    pdf.ln()

    fill = False
    for i in range(len(indicators)):
        pdf.set_fill_color(240, 240, 240) if fill else pdf.set_fill_color(255, 255, 255)
        fill = not fill
        for value in indicators.iloc[i]:
            pdf.cell(col_widths[i % len(indicator_headers)], 12, f"{value:.2f}", border=1, align='C', fill=True)
        pdf.ln()

    # AI Insights Section
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(0, 0, 128)
    pdf.cell(0, 10, 'AI Insights:', ln=True)

    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(34, 34, 34)
    for line in insights.split('\n'):
        if line.strip().startswith("") and line.strip().endswith(""):
            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 10, line.strip("*"))
            pdf.set_font('Arial', '', 12)
        else:
            pdf.multi_cell(0, 10, line)

    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output