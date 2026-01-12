from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import qrcode
from io import BytesIO
from datetime import datetime
from decimal import Decimal


class CertificateGenerator:
    """Generiert  Investitionszertifikate"""
    
    # Design-Konstanten
    PRIMARY_COLOR = colors.HexColor('#061022')  
    ACCENT_COLOR = colors.HexColor('#5eead4')   
    ACCENT_2_COLOR = colors.HexColor('#60a5fa')  
    TEXT_COLOR = colors.HexColor('#333333')     
    LIGHT_GRAY = colors.HexColor('#f3f4f6')
    HEADER_COLOR = colors.HexColor('#0b1320')   
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):        
        # Titelstil
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=self.PRIMARY_COLOR,
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=20
        )
        
        # Untertitelstil
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            textColor=self.TEXT_COLOR,
            alignment=TA_CENTER,
            spaceAfter=24
        )
        
        # Textstil
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=self.TEXT_COLOR,
            alignment=TA_LEFT,
            spaceAfter=6
        )
        
        #Fußzeilenstil
        self.footer_style = ParagraphStyle(
            'CustomFooter',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor('#9fb0c8'),  
            alignment=TA_LEFT,
            leading=10
        )
    
    def _generate_qr_code(self, transaction_id):
        """QR-Code für Transaktionsverifizierung"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(f"INVESTIFY-TX-{transaction_id}")
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # In BytesIO konvertieren
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer
    
    def _draw_header(self, canvas_obj, doc):
        """Kopfzeile mit Logo und Transaktionsinformationen"""
        canvas_obj.saveState()
        
        
        canvas_obj.setFillColor(self.ACCENT_COLOR)
        canvas_obj.roundRect(40*mm, 268*mm, 10*mm, 10*mm, 2*mm, fill=1, stroke=0)
        
        # Logo-Text "iv" in Box
        canvas_obj.setFont('Helvetica-Bold', 16)
        canvas_obj.setFillColor(self.PRIMARY_COLOR)
        canvas_obj.drawCentredString(45*mm, 271*mm, 'iv')
        
        # Firmenname neben Logo
        canvas_obj.setFont('Helvetica-Bold', 18)
        canvas_obj.setFillColor(self.PRIMARY_COLOR)
        canvas_obj.drawString(52*mm, 271*mm, 'investify')
        
        canvas_obj.setFont('Helvetica', 9)
        canvas_obj.setFillColor(self.TEXT_COLOR)
        canvas_obj.drawRightString(170*mm, 275*mm, f"Datum: {datetime.now().strftime('%d.%m.%Y')}")
        
        canvas_obj.restoreState()
    
    def _draw_divider(self, canvas_obj, y_position):
        canvas_obj.saveState()
        canvas_obj.setStrokeColor(self.ACCENT_COLOR)
        canvas_obj.setLineWidth(2)
        canvas_obj.line(40*mm, y_position, 170*mm, y_position)
        canvas_obj.restoreState()
    
    def generate_certificate(self, investment_data, output_path=None):
        """
        Args:
            investment_data (dict): Dictionary enthält:
                - investor_name: Name des Investors
                - investor_address: Adresse (optional)
                - startup_name: Name des Startups
                - investment_amount: Betrag in EUR
                - share_count: Anzahl der Anteile
                - transaction_date: Transaktionsdatum
                - transaction_id: Eindeutige Transaktions-ID
                - equity_percentage: Eigenkapitalanteil in Prozent
            output_path (str): Pfad zum Speichern des PDFs. Falls None, gibt BytesIO zurück.
        
        Returns:
            BytesIO oder Pfad zum generierten PDF
        """
        
        # Puffer erstellen
        if output_path is None:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                   leftMargin=40*mm, rightMargin=40*mm,
                                   topMargin=50*mm, bottomMargin=30*mm)
        else:
            doc = SimpleDocTemplate(output_path, pagesize=A4,
                                   leftMargin=40*mm, rightMargin=40*mm,
                                   topMargin=50*mm, bottomMargin=30*mm)
        
        # Inhaltselemente
        story = []
        
        # Titel
        title = Paragraph('Zeichnungsschein & Investmentbestätigung', self.title_style)
        story.append(title)
        
        # Untertitel mit dynamischen Daten
        investor_name = investment_data.get('investor_name', 'N/A')
        startup_name = investment_data.get('startup_name', 'N/A')
        subtitle_text = f'Hiermit bestätigen wir, dass {investor_name} Anteile an {startup_name} erworben hat.'
        subtitle = Paragraph(subtitle_text, self.subtitle_style)
        story.append(subtitle)
        
        story.append(Spacer(1, 12))
        
        # Transaktions-ID Zeile
        transaction_id = investment_data.get('transaction_id', 'N/A')
        trans_text = f'<b>Transaktions-ID:</b> {transaction_id}'
        trans_para = Paragraph(trans_text, self.body_style)
        story.append(trans_para)
        
        story.append(Spacer(1, 20))
        
        # Hauptdatenblock (Tabelle mit hellgrauem Hintergrund)
        investment_amount = investment_data.get('investment_amount', Decimal('0'))
        share_count = investment_data.get('share_count', 0)
        equity_percentage = investment_data.get('equity_percentage', Decimal('0'))
        investor_address = investment_data.get('investor_address', 'Keine Adresse hinterlegt')
        transaction_date = investment_data.get('transaction_date', datetime.now())
        
        # Datum formatieren
        if isinstance(transaction_date, str):
            try:
                transaction_date = datetime.fromisoformat(transaction_date.replace('Z', '+00:00'))
            except:
                transaction_date = datetime.now()
        
        date_str = transaction_date.strftime('%d.%m.%Y')
        
        data = [
            ['Investitionsobjekt:', startup_name],
            ['Investor:', investor_name],
            ['Adresse:', investor_address],
            ['Anzahl Anteile:', f'{share_count} Stück'],
            ['Equity-Anteil:', f'{equity_percentage}%'],
            ['Investitionssumme:', f'{investment_amount:,.2f} EUR'],
            ['Transaktionsdatum:', date_str],
        ]
        
        table = Table(data, colWidths=[60*mm, 70*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.LIGHT_GRAY),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.TEXT_COLOR),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 14),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, -1), 16),
            ('RIGHTPADDING', (1, 0), (1, -1), 16),
            # Wichtige Datenzeilen hervorheben
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (1, 0), 12),
            ('TEXTCOLOR', (1, 0), (1, 0), self.ACCENT_COLOR),
            # Investitionssumme hervorheben
            ('FONTNAME', (0, 5), (1, 5), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 5), (1, 5), 14),
            ('TEXTCOLOR', (1, 5), (1, 5), self.ACCENT_COLOR),
            ('BACKGROUND', (0, 5), (1, 5), colors.HexColor('#e0f7f4')),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 50))
        
        # Signaturbereich
        signature_style = ParagraphStyle(
            'Signature',
            parent=self.body_style,
            alignment=TA_RIGHT,
            fontSize=10
        )
        
        story.append(Spacer(1, 20))
        sig_text = '<b>Digitale Signatur</b><br/>Lukas Nießen<br/>CEO, Investify GmbH'
        signature = Paragraph(sig_text, signature_style)
        story.append(signature)
        story.append(Spacer(1, 30))
        
        # Fußzeilen
        disclaimer_text = """
        <b>Hinweis:</b> Dieses Dokument wurde maschinell erstellt und dient als Bestätigung für die 
        Simulation auf der Plattform. Es begründet keine realen rechtlichen Ansprüche.
        """
        disclaimer = Paragraph(disclaimer_text, self.footer_style)
        story.append(disclaimer)
        
        # PDF mit benutzerdefinierter Seitenvorlage erstellen
        def add_page_decorations(canvas_obj, doc):
            self._draw_header(canvas_obj, doc)
            self._draw_divider(canvas_obj, 265*mm)
        
        doc.build(story, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)
        
        if output_path is None:
            buffer.seek(0)
            return buffer
        
        return output_path


def generate_investment_certificate(investment):
    """
    Hilfsfunktion
    Args:
        investment: Investment-Modellinstanz
    Returns:
        BytesIO-Puffer mit dem PDF
    """
    
    # Berechne Anzahl der Anteile 1 Anteil pro 100 EUR
    share_count = int(investment.amount / 100)
    
    # Investitionsdaten vorbereiten
    investment_data = {
        'investor_name': f"{investment.investor.first_name} {investment.investor.last_name}" if investment.investor.first_name else investment.investor.username,
        'investor_address': getattr(investment.investor, 'address', 'Landgrabenweg 149, 53227 Bonn'),
        'startup_name': investment.pitch.title,
        'investment_amount': investment.amount,
        'share_count': share_count,
        'equity_percentage': investment.equity_percentage or Decimal('0'),
        'transaction_date': investment.investment_date,
        'transaction_id': str(investment.id).zfill(8),
    }
    
    generator = CertificateGenerator()
    return generator.generate_certificate(investment_data)
