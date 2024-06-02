import markdown
from fpdf import FPDF
from django.contrib.staticfiles import finders
from django.http import HttpResponse

class PDF(FPDF):
    def header(self):
        logo_path = finders.find('images/codeia-pro-2.png')
        self.image(logo_path, x=10, y=10, w=70, h=25)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

def response_pdf(pdf_bytes, name, version):
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}-{}.pdf"'.format(name, version)
    response['Content-Encoding'] = 'binary'
    return response

def parse_markdown(pdf, text):
    lines = text.splitlines()
    parsed_text = []
    in_code_block = False
    for line in lines:
        if line.startswith('#'):
            level = line.count('#')
            if level == 1:
                pdf.set_font('Arial', 'B', 16)
            elif level == 2:
                pdf.set_font('Arial', 'B', 14)
            elif level == 3:
                pdf.set_font('Arial', 'B', 12)
            parsed_text.append(line.lstrip('#').strip())
            pdf.multi_cell(0, 10, line.lstrip('#').strip(), 0, 'L')
        elif line.startswith('```python'):
            pdf.set_font('Courier', '', 10)
            in_code_block = True
            code_block = []
        elif line.startswith('```') and in_code_block:
            parsed_text.extend(code_block)
            pdf.multi_cell(0, 5, '\n'.join(code_block), 0, 'L')
            pdf.set_font('Arial', '', 12)
            in_code_block = False
        elif in_code_block:
            code_block.append(line)
        else:
            parsed_text.append(line)
            pdf.multi_cell(0, 10, line, 0, 'L')
        pdf.ln(5)
    return '\n'.join(parsed_text)

def replace_special_characters(text):
    replacements = {
        '\u2019': "'",
        # Añadir más reemplazos si es necesario
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

def generate_pdf(*, html_content, version, name):
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()  # Agregar página antes de escribir contenido
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.compress = False
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    cleaned_content = replace_special_characters(html_content)
    text = parse_markdown(pdf, cleaned_content)
    pdf.multi_cell(190, 10, text, border=0)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    return response_pdf(pdf_bytes, name, version)