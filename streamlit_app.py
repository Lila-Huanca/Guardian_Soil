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
    
    # Definición de los requisitos de cada cultivo
    cultivos = {
        "naranjas": {"phosphorus_min": 20, "potassium_min": 15, "temp_min": 20, "temp_max": 30, "humidity_min": 50},
        "uvas": {"phosphorus_min": 25, "potassium_min": 20, "temp_min": 15, "temp_max": 25, "humidity_min": 40},
        "plátanos": {"phosphorus_min": 30, "potassium_min": 25, "temp_min": 25, "temp_max": 35, "humidity_min": 60},
        "maíz": {"phosphorus_min": 20, "potassium_min": 20, "temp_min": 18, "temp_max": 30, "humidity_min": 50},
        "trigo": {"phosphorus_min": 15, "potassium_min": 10, "temp_min": 10, "temp_max": 25, "humidity_min": 40}
    }
    
    # Evaluación de las condiciones del suelo para cada cultivo
    recomendaciones = []
    for cultivo, requisitos in cultivos.items():
        if (phosphorus >= requisitos["phosphorus_min"] and
            potassium >= requisitos["potassium_min"] and
            requisitos["temp_min"] <= temperature <= requisitos["temp_max"] and
            humidity >= requisitos["humidity_min"]):
            recomendaciones.append(cultivo)
    
    if recomendaciones:
        return f"Recomendamos sembrar: {', '.join(recomendaciones)}."
    else:
        return "Las condiciones del suelo no son adecuadas para los cultivos disponibles. Por favor, consulte las recomendaciones específicas."

# Interfaz de usuario con Streamlit
st.title("Guardian_Soil: Recomendador de Cultivos")

# Botón para obtener datos del suelo
if st.button("Obtener datos del suelo"):
    soil_data = get_ubidots_data()
    st.write("Datos del suelo obtenidos:")
    st.write(soil_data)

    user_input = st.text_input("Ingrese el cultivo que desea sembrar (por ejemplo, 'uva'):")

    if user_input:
        st.write(f"Ha ingresado: {user_input}")
        
        recommendation = recommend_crop(soil_data)
        st.write("Recomendación:")
        st.write(recommendation)
        
        st.write("Recomendaciones detalladas de cultivos:")
        recommendations = get_cultivos_recommendations()
        st.write(recommendations)
else:
    st.write("Presiona el botón para obtener los datos del suelo.")
