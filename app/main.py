import numpy as np 
import joblib
from fastapi import FastAPI
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware


app =  FastAPI()
from pydantic import BaseModel

from pydantic import BaseModel

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # sab origins allow (development ke liye)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


model = joblib.load("MODELS/loan_model.pkl")

@app.get("/")
def home():
    return {"message": "Loan Model API is running"}


@app.post("/predict")
def predict(data: LoanInput):
    df = pd.DataFrame([data.dict()])

    proba = model.predict_proba(df)[0]   # [No, Yes]
    prediction = model.predict(df)[0]    # 'Y' or 'N'

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


