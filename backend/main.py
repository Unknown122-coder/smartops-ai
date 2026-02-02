from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd

from backend.preprocessing import clean_data
from backend.model import train_and_predict
from backend.report import generate_pdf, REPORT_PATH

from database import get_db
from fastapi import Form

app = FastAPI()


@app.get("/")
def home():
    return {"message": "SmartOps AI Backend Running"}


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    model_choice: str = Form("random_forest")):

    # Read CSV
    df = pd.read_csv(file.file)

    # Clean data
    clean_df = clean_data(df)

    # Train model & get results
    results = train_and_predict(clean_df)

    # Generate PDF report (saved at project root /reports)
    generate_pdf(results)

    return {
        "columns": list(df.columns),
        "rows": len(df),
        "model_result": results
    }


@app.get("/download-report/")
def download_report():
    return FileResponse(
        path=REPORT_PATH,
        media_type="application/pdf",
        filename="SmartOps_Report.pdf"
    )

@app.post("/register/")
def register(email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )
        conn.commit()
        return {"message": "User registered"}
    except:
        return {"error": "User already exists"}

@app.post("/login/")
def login(email: str = Form(...), password: str = Form(...)):
    conn = get_db()
    cur = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    if user:
        return {"success": True}
    return {"success": False}