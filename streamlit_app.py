import streamlit as st
import requests
import pandas as pd
import random

UBIDOTS_URL = "https://stem.ubidots.com/app/dashboards/public/dashboard/DSqu9x3MSr7Z_MTANddWfZWKBbaYMdlDv_tVhA3NkE0"
CULTIVOS_DOC_URL = "https://docs.google.com/document/d/1VCnEJqoRa-Da7MbDzPzBmKkkyGTqtzIW/export?format=txt"

def get_ubidots_data():
    response = requests.get(UBIDOTS_URL)
    data = {
        "phosphorus": 30,
        "potassium": 20,
        "temperature": 25,
        "humidity": 60
    }
    return data

def recommend_crop(data, user_input):
    phosphorus = data["phosphorus"]
    potassium = data["potassium"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    
    cultivos = {
        "naranjas": {"phosphorus_min": 20, "potassium_min": 15, "temp_min": 20, "temp_max": 30, "humidity_min": 50},
        "uvas": {"phosphorus_min": 25, "potassium_min": 20, "temp_min": 15, "temp_max": 25, "humidity_min": 40},
        "plátanos": {"phosphorus_min": 30, "potassium_min": 25, "temp_min": 25, "temp_max": 35, "humidity_min": 60},
        "maíz": {"phosphorus_min": 20, "potassium_min": 20, "temp_min": 18, "temp_max": 30, "humidity_min": 50},
        "trigo": {"phosphorus_min": 15, "potassium_min": 10, "temp_min": 10, "temp_max": 25, "humidity_min": 40}
    }
    
    recomendaciones = []
    for cultivo, requisitos in cultivos.items():
        if (phosphorus >= requisitos["phosphorus_min"] and
            potassium >= requisitos["potassium_min"] and
            requisitos["temp_min"] <= temperature <= requisitos["temp_max"] and
            humidity >= requisitos["humidity_min"]):
            recomendaciones.append(cultivo)
    
    if user_input in recomendaciones:
        return f"Recomendamos sembrar: {user_input}."
    else:
        alternative_crops = [crop for crop in recomendaciones if crop != user_input]
        random.shuffle(alternative_crops)
        alternative_crops = ', '.join(alternative_crops[:5])
        responses = [
            f"No puedes sembrar ahora {user_input} pero podrías sembrar: {alternative_crops}. No te preocupes, que estamos aquí para orientarte y que puedas tener un mejor cultivo.",
            f"No puedes sembrar ahora {user_input} pero podrías sembrar: {alternative_crops}. No te preocupes que estamos aquí para ayudarte.",
            f"No puedes sembrar ahora {user_input} pero podrías sembrar: {alternative_crops}. No te preocupes que estamos aquí para apoyarte y que podamos escoger la mejor cosecha de este año y todos los años que falten."
        ]
        return random.choice(responses)

st.title("Guardian_Soil: Recomendador de Cultivos")

if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "soil_data" not in st.session_state:
    st.session_state.soil_data = None
if "recommendation" not in st.session_state:
    st.session_state.recommendation = ""

def clear_state():
    st.session_state.user_input = ""
    st.session_state.soil_data = None
    st.session_state.recommendation = ""

st.session_state.user_input = st.text_input("Ingrese el cultivo que desea sembrar (por ejemplo, 'uva'):", st.session_state.user_input)

if st.session_state.user_input:
    st.write(f"Ha ingresado: {st.session_state.user_input}")
    if st.button("Obtener recomendación"):
        st.session_state.soil_data = get_ubidots_data()
        st.write("Datos del suelo obtenidos:")
        st.write(st.session_state.soil_data)

        st.session_state.recommendation = recommend_crop(st.session_state.soil_data, st.session_state.user_input)
        st.write("Recomendación:")
        st.write(st.session_state.recommendation)

if st.button("Borrar resultados y consultar de nuevo"):
    clear_state()
