import time 
timestr = time.strftime("%d.%m.%Y %H:%M:%S")
from fastapi import FastAPI, File, UploadFile, Request 
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn 
import os
import platform
from EDIFACT_Val_Functions import ProProcessingStep1, ProProcessingStep2, ProProcessingStep3, yarrrmlparser_bash, rmlmapper_bash, yarrrmlparser_batch, rmlmapper_batch, validates
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app = FastAPI() 

origins = [
    'http://localhost:300'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins
)

app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")


@app.get("/", response_class=HTMLResponse)
async def read_item():
     return FileResponse("static/index.html")

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(..., description="The EDIFACT file")):
    filename = file.filename
    contents = await file.read()
    with open(filename, "wb") as f:
        f.write(contents)
    ProProcessingStep1(filename)
    ProProcessingStep2()
    process = ProProcessingStep3()[1]
    if platform.system() == "Windows":
        yarrrmlparser_bash()
        rmlmapper_bash()
        validation_result = validates(process)
    elif platform.system() in {"Darwin", "Linux"}:
        yarrrmlparser_bash()
        rmlmapper_bash()
        validation_result = validates(process)
    else: 
        validation_result = "Unknown system"

    return templates.TemplateResponse("result.html", {"request": request, "filename": filename, "validation_result": validation_result, "validation_time": timestr})

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=800)
