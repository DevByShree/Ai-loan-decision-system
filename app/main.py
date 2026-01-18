import os
import numpy as np
import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

#  APP INIT 
app = FastAPI()

#  CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  STATIC FRONTEND 
# BASE DIR = project root (LOAD_API)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app.mount(
    "/frontend",
    StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True),
    name="frontend"
)

#  INPUT SCHEMA 
class LoanInput(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str

#  LOAD MODEL 
model = joblib.load(os.path.join(BASE_DIR, "MODELS", "loan_model.pkl"))

#  ROUTES 
@app.get("/")
def home():
    return {"message": "Loan Model API is running"}

@app.post("/predict")
def predict(data: LoanInput):
    df = pd.DataFrame([data.dict()])

    proba = model.predict_proba(df)[0]
    prediction = model.predict(df)[0]

    decision = "APPROVED" if prediction == "Y" else "REJECTED"

    return {
        "decision": decision,
        "yes_probability": float(round(proba[1], 3)),
        "no_probability": float(round(proba[0], 3)),
        "explanation": [
            "Credit history played a major role",
            "Income and loan amount were evaluated"
        ]
    }
