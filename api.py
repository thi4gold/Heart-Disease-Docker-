from pathlib import Path
import json
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "heart_model.joblib"
META_PATH = BASE_DIR / "models" / "metadata.json"

model = joblib.load(MODEL_PATH)

with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

app = FastAPI(
    title="ML III - Heart Disease API",
    description="API simples para demonstrar como um modelo de ML vira um serviço.",
    version="1.0"
)

class PatientData(BaseModel):
    age: int = Field(54, description="Idade")
    sex: int = Field(1, description="Sexo: 1 = masculino, 0 = feminino")
    cp: int = Field(0, description="Tipo de dor no peito")
    trestbps: int = Field(130, description="Pressão arterial em repouso")
    chol: int = Field(246, description="Colesterol sérico")
    fbs: int = Field(0, description="Glicemia em jejum > 120 mg/dl")
    restecg: int = Field(1, description="Resultado eletrocardiográfico em repouso")
    thalach: int = Field(150, description="Frequência cardíaca máxima")
    exang: int = Field(0, description="Angina induzida por exercício")
    oldpeak: float = Field(1.0, description="Depressão ST")
    slope: int = Field(1, description="Inclinação do segmento ST")
    ca: int = Field(0, description="Número de vasos principais")
    thal: int = Field(2, description="Resultado thal")

@app.get("/")
def home():
    return {
        "mensagem": "API funcionando!",
        "objetivo": "Transformar um modelo de ML em uma aplicação utilizável.",
        "endpoint_principal": "/predict",
        "documentacao": "/docs"
    }

@app.post("/predict")
def predict(data: PatientData):
    input_df = pd.DataFrame([data.model_dump()])
    input_df = input_df[metadata["features"]]

    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    return {
        "classe_prevista": prediction,
        "probabilidade_doenca": round(probability, 4),
        "interpretacao": metadata["classes"][str(prediction)]
    }