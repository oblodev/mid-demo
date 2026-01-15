"""
PDF-Generator für Pflegeberichte
Erstellt professionelle PDF-Dokumente für Klienten-Dokumentation.
"""
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


def generate_client_report(client, entries):
    """
    Generiert einen PDF-Bericht für einen Klienten.

    Args:
        client: Client-Objekt mit allen Daten
        entries: Liste der CareEntry-Objekte

    Returns:
        BytesIO: PDF als Byte-Stream
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='MIDTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E8B8B'),
        spaceAfter=20,
        alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        name='MIDSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.grey,
        alignment=TA_CENTER,
        spaceAfter=30
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2E8B8B'),
        spaceBefore=20,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='EntryText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14
    ))

    # Content
    story = []

    # Header
    story.append(Paragraph("MID Pflegedokumentation", styles['MIDTitle']))
    story.append(Paragraph("Meine Intensivpflege Daheim", styles['MIDSubtitle']))

    # Klienten-Info Box
    story.append(Paragraph("Klientendaten", styles['SectionHeader']))

    client_data = [
        ['Name:', client.name],
        ['Geburtsdatum:', client.birth_date.strftime('%d.%m.%Y') if client.birth_date else '-'],
        ['Alter:', f'{client.age} Jahre' if client.age else '-'],
        ['Pflegegrad:', f'Pflegegrad {client.care_level}' if client.care_level else '-'],
        ['Adresse:', client.address or '-'],
    ]

    client_table = Table(client_data, colWidths=[4*cm, 12*cm])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E0F2F1')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2E8B8B')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2E8B8B')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(client_table)

    # Notizen
    if client.notes:
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Notizen:</b> {client.notes}", styles['EntryText']))

    story.append(Spacer(1, 20))

    # Pflegeeinträge
    story.append(Paragraph(f"Pflegeeinträge ({len(entries)} Einträge)", styles['SectionHeader']))

    if entries:
        # Kategorien-Mapping für deutsche Namen
        category_names = {
            'grundpflege': 'Grundpflege',
            'medikamente': 'Medikamente',
            'vitalzeichen': 'Vitalzeichen',
            'ernaehrung': 'Ernährung',
            'mobilisation': 'Mobilisation',
            'besonderheiten': 'Besonderheiten',
        }

        for entry in entries:
            # Entry Header
            entry_date = entry.recorded_at.strftime('%d.%m.%Y %H:%M')
            category = category_names.get(entry.category, entry.category)

            entry_header = f"<b>{entry_date}</b> | <font color='#2E8B8B'>{category}</font> | Erfasst von: {entry.recorded_by}"
            story.append(Paragraph(entry_header, styles['EntryText']))

            # Entry Content
            story.append(Paragraph(entry.description, styles['EntryText']))
            story.append(Spacer(1, 10))

            # Trennlinie
            line_data = [['─' * 80]]
            line_table = Table(line_data, colWidths=[16*cm])
            line_table.setStyle(TableStyle([
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.lightgrey),
                ('FONTSIZE', (0, 0), (-1, -1), 6),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ]))
            story.append(line_table)
            story.append(Spacer(1, 5))
    else:
        story.append(Paragraph("Keine Pflegeeinträge vorhanden.", styles['EntryText']))

    # Footer
    story.append(Spacer(1, 30))
    footer_text = f"Erstellt am {datetime.now().strftime('%d.%m.%Y um %H:%M Uhr')} | MID Pflegedokumentation"
    story.append(Paragraph(footer_text, ParagraphStyle(
        name='Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
