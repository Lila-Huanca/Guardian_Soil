import streamlit as st
import requests
import pandas as pd
import random

# Constants
UBIDOTS_URL = "https://stem.ubidots.com/app/dashboards/public/dashboard/DSqu9x3MSr7Z_MTANddWfZWKBbaYMdlDv_tVhA3NkE0"

# Function to fetch data from Ubidots
def get_ubidots_data():
    response = requests.get(UBIDOTS_URL)
    data = {
        "phosphorus": 30,
        "potassium": 20,
        "temperature": 25,
        "humidity": 60
    }
    return data

# Function to recommend crops based on soil data
def recommend_crop(data, user_input):
    phosphorus = data["phosphorus"]
    potassium = data["potassium"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    
    # Crop requirements
    cultivos = {
        "naranjas": {"phosphorus_min": 20, "potassium_min": 15, "temp_min": 20, "temp_max": 30, "humidity_min": 50},
        "uvas": {"phosphorus_min": 25, "potassium_min": 20, "temp_min": 15, "temp_max": 25, "humidity_min": 40},
        "plátanos": {"phosphorus_min": 30, "potassium_min": 25, "temp_min": 25, "temp_max": 35, "humidity_min": 60},
        "maíz": {"phosphorus_min": 20, "potassium_min": 20, "temp_min": 18, "temp_max": 30, "humidity_min": 50},
        "trigo": {"phosphorus_min": 15, "potassium_min": 10, "temp_min": 10, "temp_max": 25, "humidity_min": 40}
    }
    
    # Recommendations based on the soil data
    recomendaciones = []
    for cultivo, requisitos in cultivos.items():
        if (phosphorus >= requisitos["phosphorus_min"] and
            potassium >= requisitos["potassium_min"] and
            requisitos["temp_min"] <= temperature <= requisitos["temp_max"] and
            humidity >= requisitos["humidity_min"]):
            recomendaciones.append(cultivo.capitalize())
    
    if user_input.capitalize() in recomendaciones:
        return f"Recomendamos sembrar: {user_input.capitalize()}. Puedes sembrar {user_input.capitalize()} porque cuentas con los estándares aptos para esta siembra. ¡Buena suerte! Este es tu año."
    else:
        alternative_crops = [crop for crop in recomendaciones if crop != user_input.capitalize()]
        random.shuffle(alternative_crops)
        alternative_crops = ', '.join(alternative_crops[:5])
        responses = [
            f"No puedes sembrar ahora {user_input.capitalize()} pero podrías sembrar: {alternative_crops}. No te preocupes, que estamos aquí para orientarte y que puedas tener un mejor cultivo.",
            f"No puedes sembrar ahora {user_input.capitalize()} pero podrías sembrar: {alternative_crops}. No te preocupes que estamos aquí para ayudarte.",
            f"No puedes sembrar ahora {user_input.capitalize()} pero podrías sembrar: {alternative_crops}. No te preocupes que estamos aquí para apoyarte y que podamos escoger la mejor cosecha de este año y todos los años que falten."
        ]
        return random.choice(responses)

# Streamlit App
st.title("Guardian_Soil: Recomendador de Cultivos")

# Introduction
st.markdown("""
# Guardian Soil
### Monitoreo remoto en tiempo real de la calidad del suelo
¡BIENVENIDOS A GUARDIAN SOIL!

¡Bienvenidos a todos! Este es la aplicación del grupo 3 del curso de fundamentos de diseño. Por aquí podrán ver y analizar todo el trabajo realizado sobre nuestro equipo. Somos un grupo de estudiantes con las ganas de aportar nuestro granito de arena en el mundo, buscamos desarrollar e implementar soluciones innovadoras y creativas. ¡BIENVENIDOS A GUARDIAN SOIL!

¿Para quienes está dirigida la aplicación? 
Guardian Soil está especialmente dirigida a la población agrícola de La Oroya, Junín, en la Sierra Central del Perú. No obstante, también puede implementarse en otros lugares con el tiempo.
""")

# Ubidots Data
st.markdown(f"### [Monitoreo en tiempo real](https://stem.ubidots.com/app/dashboards/public/dashboard/DSqu9x3MSr7Z_MTANddWfZWKBbaYMdlDv_tVhA3NkE0)")
st.write("")

# Comparativa Table
st.markdown(f"### [Tabla Comparativa](https://docs.google.com/document/d/1VCnEJqoRa-Da7MbDzPzBmKkkyGTqtzIW/edit?usp=drive_link&ouid=113185433440571333811&rtpof=true&sd=true)")
st.write("")

# Pie Chart
st.markdown(f"### [Gráfico Circular](https://docs.google.com/document/d/1Lb9cVvxqfVCjV_8zK9EclqNE06AopXWlpOAt_ES80Jg/edit?usp=drive_link)")
st.write("")

# Initialize session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "soil_data" not in st.session_state:
    st.session_state.soil_data = None
if "recommendation" not in st.session_state:
    st.session_state.recommendation = ""

# Clear session state
def clear_state():
    st.session_state.user_input = ""
    st.session_state.soil_data = None
    st.session_state.recommendation = ""

# User input
st.session_state.user_input = st.text_input("Ingrese el cultivo que desea sembrar (por ejemplo, 'uva'):", st.session_state.user_input)

# Process input
if st.session_state.user_input:
    st.write(f"Ha ingresado: {st.session_state.user_input.capitalize()}")
    if st.button("Obtener recomendación"):
        st.session_state.soil_data = get_ubidots_data()
        st.write("Datos del suelo obtenidos:")
        st.write(st.session_state.soil_data)

        st.session_state.recommendation = recommend_crop(st.session_state.soil_data, st.session_state.user_input)
        st.write("Recomendación:")
        st.write(st.session_state.recommendation)

# Clear results
if st.button("Borrar resultados y consultar de nuevo"):
    clear_state()

# Contact Information
st.markdown("""
### Soporte técnico
Estamos disponible para cualquier duda o consulta, no dudes en mandarnos un mensaje.

Correo electrónico:                                        
- lila.huanca@upch.pe
- brenda.sanchez@upch.pe
- bertil.rodriguez@upch.pe 
- anjhy.zamora@upch.pe 
- maycol.condor@upch.pe 
""")
