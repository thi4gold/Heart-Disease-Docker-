import os
import requests
import streamlit as st

# Local: usa a API na própria máquina. Na nuvem: configurar API_URL
# em Streamlit Community Cloud → App settings → Secrets.
try:
    cloud_url = st.secrets.get("API_URL", "")
except (FileNotFoundError, KeyError):
    cloud_url = ""
API_URL = os.getenv("API_URL") or cloud_url or "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="ML III - Demo Heart Disease",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Sistema Inteligente de Predição de Doença Cardíaca")
st.write(
    "Esta é uma demonstração simples de como um modelo treinado em Machine Learning "
    "pode virar uma aplicação utilizável por pessoas reais."
)

st.warning(
    "Demonstração exclusivamente didática; não utilizar para diagnóstico médico."
)

st.subheader("Dados do paciente")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Idade", min_value=20, max_value=100, value=54)
    sex = st.selectbox("Sexo", options=[0, 1], format_func=lambda x: "Feminino" if x == 0 else "Masculino")
    cp = st.selectbox("Tipo de dor no peito (cp)", options=[0, 1, 2, 3])
    trestbps = st.number_input("Pressão arterial em repouso", min_value=80, max_value=220, value=130)
    chol = st.number_input("Colesterol", min_value=100, max_value=600, value=246)
    fbs = st.selectbox("Glicemia em jejum > 120 mg/dl?", options=[0, 1], format_func=lambda x: "Não" if x == 0 else "Sim")
    restecg = st.selectbox("ECG em repouso", options=[0, 1, 2])

with col2:
    thalach = st.number_input("Frequência cardíaca máxima", min_value=60, max_value=230, value=150)
    exang = st.selectbox("Angina induzida por exercício?", options=[0, 1], format_func=lambda x: "Não" if x == 0 else "Sim")
    oldpeak = st.number_input("Oldpeak", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    slope = st.selectbox("Slope", options=[0, 1, 2])
    ca = st.selectbox("Número de vasos principais (ca)", options=[0, 1, 2, 3])
    thal = st.selectbox("Thal", options=[0, 1, 2, 3])

payload = {
    "age": age,
    "sex": sex,
    "cp": cp,
    "trestbps": trestbps,
    "chol": chol,
    "fbs": fbs,
    "restecg": restecg,
    "thalach": thalach,
    "exang": exang,
    "oldpeak": oldpeak,
    "slope": slope,
    "ca": ca,
    "thal": thal
}

if st.button("Realizar previsão"):
    try:
        response = requests.post(API_URL, json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()

        st.subheader("Resultado")
        st.metric("Probabilidade estimada de doença cardíaca", f"{result['probabilidade_doenca']:.1%}")
        st.write(f"**Classe prevista:** {result['classe_prevista']}")
        st.write(f"**Interpretação:** {result['interpretacao']}")

    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar à API. Verifique a URL configurada e se o backend está ativo.")
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
