import io
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_weekly_report_pdf(report_data: Dict[str, Any]) -> bytes:
    """
    Build Community Flow Weekly Wellness PDF from /report-data payload
    """
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()
    story = []

    # ---------- Header ----------
    story.append(Paragraph("COMMUNITY FLOW", styles["Title"]))
    story.append(Paragraph(
        "Weekly Wellness Weather Report — Chicago",
        styles["Heading2"]
    ))
    story.append(Spacer(1, 12))

    generated_date = datetime.now().strftime("%B %d, %Y")
    story.append(Paragraph(f"Generated on: {generated_date}", styles["Normal"]))
    story.append(Spacer(1, 12))

    # ---------- Summary ----------
    story.append(Paragraph("Snapshot Summary", styles["Heading3"]))
    story.append(Paragraph(
        f"Total Articles: {report_data.get('total_articles', 0)}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 12))

    # ---------- Top Themes ----------
    story.append(Paragraph("Top Themes", styles["Heading3"]))

    theme_rows = [["Theme ID", "Article Count"]]
    for theme in report_data.get("theme_distribution", []):
        theme_rows.append([
            str(theme.get("id")),
            str(theme.get("count"))
        ])

    theme_table = Table(theme_rows, colWidths=[2 * inch, 2 * inch])
    theme_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story.append(theme_table)
    story.append(Spacer(1, 12))

    # ---------- Top Clusters ----------
    story.append(Paragraph("Top Topic Clusters", styles["Heading3"]))

    cluster_rows = [["Topic ID", "Article Count"]]
    for cluster in report_data.get("top_clusters", []):
        cluster_rows.append([
            str(cluster.get("topic_id")),
            str(cluster.get("count"))
        ])

    cluster_table = Table(cluster_rows, colWidths=[2 * inch, 2 * inch])
    cluster_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story.append(cluster_table)
    story.append(Spacer(1, 12))

    # ---------- Latest Articles ----------
    story.append(Paragraph("Latest 5 Items", styles["Heading3"]))

    for article in report_data.get("latest_items", [])[:5]:
        story.append(Paragraph(
            f"<b>{article.get('title')}</b>",
            styles["Normal"]
        ))
        story.append(Paragraph(
            f"{article.get('date')} — {article.get('source')}",
            styles["Italic"]
        ))
        story.append(Spacer(1, 6))

    doc.build(story)
    return buffer.getvalue()
