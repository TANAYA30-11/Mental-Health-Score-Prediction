from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "Mental_Health_Model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load ML model: {e}")


app = FastAPI(
    title="Mental Health Score Predictor API",
    description="API to predict a student's mental health score using a trained ML model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentData(BaseModel):

    age: int = Field(..., ge=10, le=100)

    gender: Literal["Male", "Female"]

    country: str = Field(..., min_length=1)

    academic_level: Literal[
        "Undergraduate",
        "Graduate",
        "High School"
    ]

    most_used_platform: Literal[
        "Facebook",
        "LinkedIn",
        "Instagram",
        "Snapchat",
        "Twitter",
        "YouTube",
        "TikTok",
        "LINE",
        "KakaoTalk",
        "VKontakte",
        "WhatsApp",
        "WeChat"
    ]

    purpose_of_use: Literal[
        "Networking",
        "Education",
        "Entertainment",
        "News"
    ]

    avg_daily_usage_hours: float = Field(..., ge=0, le=24)

    daily_unlocks: int = Field(..., ge=0)

    study_hours: float = Field(..., ge=0, le=24)

    physical_activity_hours: float = Field(..., ge=0, le=24)

    sleep_hours_per_night: float = Field(..., ge=0, le=24)

    stress_level: Literal[
        "Medium",
        "Low",
        "Very High",
        "High"
    ]
class PredictionResponse(BaseModel):

    predicted_mental_health_score: float

TOP_COUNTRIES = [
    "India",
    "USA",
    "Canada",
    "Australia",
    "UK",
    "Germany",
    "Mexico",
    "Turkey",
    "France"
]

@app.get("/")
def home():
    return {
        "message": "Welcome to Mental Health Score Predictor API",
        "status": "Running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"]
)
def predict(data: StudentData):

    try:
        country_group = (
            data.country
            if data.country in TOP_COUNTRIES
            else "other"
        )

        input_row = pd.DataFrame([{
            "Age": data.age,
            "Gender": data.gender,
            "Country": data.country,
            "Academic_Level": data.academic_level,
            "Most_Used_Platform": data.most_used_platform,
            "Purpose_Of_Use": data.purpose_of_use,
            "Avg_Daily_Usage_Hours": data.avg_daily_usage_hours,
            "Daily_Unlocks": data.daily_unlocks,
            "Study_Hours": data.study_hours,
            "Physical_Activity_Hours": data.physical_activity_hours,
            "Sleep_Hours_Per_Night": data.sleep_hours_per_night,
            "Stress_Level": data.stress_level,
            "Grouped_Country": country_group
        }])

        prediction = model.predict(input_row)[0]

        return PredictionResponse(
            predicted_mental_health_score=round(
                float(prediction), 2
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )