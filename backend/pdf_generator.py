from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import os
from datetime import datetime
from reportlab.lib import colors

def generate_pdf(
    image_path,
    prediction,
    confidence,
    severity,
    repair_cost,
    repair_time,
):

    os.makedirs("reports", exist_ok=True)

    filename = f"inspection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join("reports", filename)

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story = []


    header = ParagraphStyle(
        "Header",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=15,
    )

    story.append(Paragraph("AI ROAD INSPECTION REPORT", header))
    story.append(
    Paragraph(
        "<font color='grey'>Surface Crack Detection System</font>",
        styles["Heading2"],
    )
)

    story.append(
        Paragraph(
            "<font color='Black'><b>ACE Bootcamp Team 7</b></font>",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1,20))

    inspection_id = "INS-" + datetime.now().strftime("%Y%m%d-%H%M%S")

    story.append(
        Paragraph(
            f"<b>Inspection ID:</b> {inspection_id}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}",
            styles["BodyText"],
        )
    )

    story.append(Spacer(1,15))


    if os.path.exists(image_path):
        img = Image(image_path, width=4 * inch, height=3 * inch)
        img.hAlign = "CENTER"
        story.append(img)

    story.append(Spacer(1, 20))

    cost_text = repair_cost["display"] if repair_cost else "N/A"
    time_text = repair_time["display"] if repair_time else "N/A"

    table_data = [
        ["Parameter", "Value"],
        ["Prediction", prediction],
        ["Confidence", f"{confidence*100:.2f}%"],
        ["Severity", severity],
        ["Repair Cost", cost_text],
        ["Repair Time", time_text],
    ]

    table = Table(table_data, colWidths=[180, 220])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#374151")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ])
    )

    story.append(table)
    story.append(Spacer(1, 20))


    story.append(
    Paragraph(
        "<b>Maintenance Recommendation</b>",
            styles["Heading2"],
        )
    )

    if prediction == "Potholes":

        recommendation = "Immediate pothole patch repair using cold asphalt."

    elif prediction == "Cracks":

        recommendation = "Seal cracks immediately to prevent water seepage."

    elif prediction == "Patch":

        recommendation = "Surface overlay recommended."

    else:

        recommendation = "Detailed structural inspection recommended."

    story.append(
        Paragraph(recommendation, styles["BodyText"])

    )
    story.append(Spacer(1,20))



    story.append(
    Paragraph(
        "<b>Generated Automatically by Surface Crack Detection AI</b>",
            styles["Italic"],
        )
    )

    story.append(
        Paragraph(
            "ACE Bootcamp Team 7",
            styles["BodyText"],
        )
    )

    story.append(
        Paragraph(
            "This report is AI-generated. Manual verification is recommended before maintenance.",
            styles["Italic"],
        )
    )

    doc.build(story)

    return filepath