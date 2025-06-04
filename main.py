from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import subprocess
import tempfile
import os

app = FastAPI()

@app.post("/render-pdf/")
async def render_pdf(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as md_file:
        md_path = md_file.name
        md_content = await file.read()
        md_file.write(md_content)

    pdf_path = md_path.replace(".md", ".pdf")
    subprocess.run(["marp", md_path, "-o", pdf_path])

    response = FileResponse(pdf_path, filename="presentation.pdf")

    @response.call_on_close
    def cleanup():
        try:
            os.remove(md_path)
            os.remove(pdf_path)
        except Exception:
            pass

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
