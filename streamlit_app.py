import streamlit as st
import requests
import random

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

def recommend_crop(data, user_input):
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

    alternativas = ["manzana", "lechuga", "betarraga", "espárrago", "zanahoria"]
    
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
        mensajes_aliento = [
            "No puedes sembrar ahora limón, pero podrías sembrar: " + ', '.join(alternativas) + ". No te preocupes, que estamos aquí para orientarte y que puedas tener un mejor cultivo.",
            "No puedes sembrar ahora limón, pero podrías sembrar: " + ', '.join(alternativas) + ". No te preocupes que estamos aquí para ayudarte.",
            "No puedes sembrar ahora limón, pero podrías sembrar: " + ', '.join(alternativas) + ". No te preocupes que estamos aquí para apoyarte y que podamos escoger la mejor cosecha de este año y todos los años que falten."
        ]
        mensaje = random.choice(mensajes_aliento)
        return mensaje

# Interfaz de usuario con Streamlit
st.title("Guardian_Soil: Recomendador de Cultivos")

# Inicialización del estado de la sesión
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

# Entrada del usuario para el cultivo
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

# Botón para borrar resultados y hacer otra consulta
if st.button("Borrar resultados y consultar de nuevo"):
    clear_state()
