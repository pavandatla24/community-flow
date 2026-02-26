from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import io

from backend.utils.report_builder import build_report_data
from backend.utils.pdf_service import generate_weekly_report_pdf

router = APIRouter()


@router.get("/report-pdf")
def download_weekly_report_pdf():
    report_data = build_report_data(limit=10, sort="date_desc")
    pdf_bytes = generate_weekly_report_pdf(report_data)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=community_flow_weekly_report.pdf"
        }
    )
