import streamlit as st
import requests

# Datos de estándares agronómicos
cultivos = {
    "palta": {"npk_min": 5, "npk_max": 15, "temp_min": 16, "temp_max": 25, "hum_min": 60, "hum_max": 80},
    "tomate": {"npk_min": 4, "npk_max": 10, "temp_min": 20, "temp_max": 30, "hum_min": 40, "hum_max": 60},
    # Añadir más cultivos según sea necesario
}

# Función para evaluar datos del usuario
def evaluar_cultivo(cultivo, npk, temp, humedad):
    if cultivo not in cultivos:
        return f"Lo siento, no tengo información sobre {cultivo}."
    
    datos_cultivo = cultivos[cultivo]
    
    if not (datos_cultivo["npk_min"] <= npk <= datos_cultivo["npk_max"]):
        return f"No puedes plantar {cultivo} porque el NPK está fuera del rango permitido."
    if not (datos_cultivo["temp_min"] <= temp <= datos_cultivo["temp_max"]):
        return f"No puedes plantar {cultivo} porque la temperatura está fuera del rango permitido."
    if not (datos_cultivo["hum_min"] <= humedad <= datos_cultivo["hum_max"]):
        return f"No puedes plantar {cultivo} porque la humedad está fuera del rango permitido."
    
    return f"Puedes plantar {cultivo}."

# Función para sugerir un cultivo alternativo
def sugerir_cultivo(npk, temp, humedad):
    for cultivo, datos_cultivo in cultivos.items():
        if (datos_cultivo["npk_min"] <= npk <= datos_cultivo["npk_max"] and
            datos_cultivo["temp_min"] <= temp <= datos_cultivo["temp_max"] and
            datos_cultivo["hum_min"] <= humedad <= datos_cultivo["hum_max"]):
            return f"Puedes plantar {cultivo}."
    return "Lo siento, no encuentro un cultivo adecuado para las condiciones dadas."

# Función para obtener datos de Ubidots
def obtener_datos_ubidots(token, device, variable):
    url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{device}/{variable}/lv"
    headers = {"X-Auth-Token": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error al obtener datos de Ubidots: {response.status_code}")
        return None

# Configuración de la interfaz de usuario con Streamlit
st.title("Asistente de Plantación de Cultivos")

# Token y device de Ubidots
ubidots_token = st.text_input("Ingresa tu token de Ubidots:")
device = st.text_input("Ingresa el nombre del dispositivo:")

if st.button("Obtener Datos y Evaluar"):
    if ubidots_token and device:
        npk_usuario = obtener_datos_ubidots(ubidots_token, device, "npk")
        temp_usuario = obtener_datos_ubidots(ubidots_token, device, "temperature")
        hum_usuario = obtener_datos_ubidots(ubidots_token, device, "humidity")
        
        if npk_usuario is not None and temp_usuario is not None and hum_usuario is not None:
            st.write(f"NPK: {npk_usuario}")
            st.write(f"Temperatura: {temp_usuario}°C")
            st.write(f"Humedad: {hum_usuario}%")
            
            cultivo_deseado = st.selectbox("Selecciona el cultivo deseado:", list(cultivos.keys()))
            resultado = evaluar_cultivo(cultivo_deseado, npk_usuario, temp_usuario, hum_usuario)
            st.write(resultado)

            if "No puedes" in resultado:
                sugerencia = sugerir_cultivo(npk_usuario, temp_usuario, hum_usuario)
                st.write(sugerencia)
        else:
            st.error("No se pudieron obtener todos los datos necesarios de Ubidots.")
    else:
        st.error("Por favor, ingresa el token y el nombre del dispositivo de Ubidots.")
