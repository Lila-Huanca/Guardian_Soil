import streamlit as st
import requests
import pandas as pd

# URL del dashboard de Ubidots
UBIDOTS_URL = "https://stem.ubidots.com/app/dashboards/public/dashboard/DSqu9x3MSr7Z_MTANddWfZWKBbaYMdlDv_tVhA3NkE0"
# URL del documento de Google con las recomendaciones de cultivos
CULTIVOS_DOC_URL = "https://docs.google.com/document/d/1VCnEJqoRa-Da7MbDzPzBmKkkyGTqtzIW/export?format=txt"

def get_ubidots_data():
    # Aquí deberías hacer la petición a la API de Ubidots para obtener los datos del suelo
    # Por simplicidad, se asume que ya tienes los datos en un formato legible
    response = requests.get(UBIDOTS_URL)
    # Simulación de datos obtenidos
    data = {
        "phosphorus": 30,
        "potassium": 20,
        "temperature": 25,
        "humidity": 60
    }
    return data

def get_cultivos_recommendations():
    response = requests.get(CULTIVOS_DOC_URL)
    recommendations = response.text
    return recommendations

def recommend_crop(data):
    phosphorus = data["phosphorus"]
    potassium = data["potassium"]
    temperature = data["temperature"]
    humidity = data["humidity"]

    # Lógica simple para recomendaciones de cultivos
    if phosphorus > 20 and potassium > 15 and 20 <= temperature <= 30 and humidity > 50:
        return "Recomendamos sembrar naranjas."
    else:
        return "Las condiciones del suelo no son adecuadas para el cultivo de naranjas. Por favor, consulte las recomendaciones específicas."

# Interfaz de usuario con Streamlit
st.title("Guardian_Soil: Recomendador de Cultivos")

user_input = st.text_input("Ingrese el cultivo que desea sembrar (por ejemplo, 'uva'):")

if user_input:
    st.write(f"Ha ingresado: {user_input}")
    soil_data = get_ubidots_data()
    st.write("Datos del suelo obtenidos:")
    st.write(soil_data)
    
    recommendation = recommend_crop(soil_data)
    st.write("Recomendación:")
    st.write(recommendation)
    
    st.write("Recomendaciones detalladas de cultivos:")
    recommendations = get_cultivos_recommendations()
    st.write(recommendations)
