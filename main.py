from io import BytesIO
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from PyPDF2 import PdfMerger
import requests

app = FastAPI()

class MergeRequest(BaseModel):
    pdf_urls: list[str] = Field(min_length=2, description="List of public PDF URLs to merge")


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/merge")
def merge_pdfs(req: MergeRequest):
    merger = PdfMerger()
    input_streams = []
    output_stream = BytesIO()

    try:
        for url in req.pdf_urls:
            try:
                r = requests.get(url, timeout=20)
                r.raise_for_status()
            except requests.RequestException as exc:
                raise HTTPException(status_code=400, detail=f"Unable to download PDF: {url}") from exc

            stream = BytesIO(r.content)
            input_streams.append(stream)
            try:
                merger.append(stream)
            except Exception as exc:
                raise HTTPException(status_code=400, detail=f"Invalid or corrupted PDF: {url}") from exc

        merger.write(output_stream)
        output_stream.seek(0)

        return StreamingResponse(
            output_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=merged.pdf"},
        )
    finally:
        merger.close()
        for stream in input_streams:
            try:
                stream.close()
            except Exception:
                pass