import streamlit as st
import py3Dmol
import pandas as pd
import os # Importar el módulo os para manejar rutas de archivos

# --- Configuración de la Página ---
st.set_page_config(layout="wide")

st.title("🧬 Visualización 3D del Plegamiento de DNA")

# --- Secuencia de ADN y Métricas ---
dna_sequence = "AACTGCTATCTAACGCCAGC"
st.subheader("Secuencia de ADN:")
st.code(dna_sequence)

st.subheader("Métricas de Simulación (MD = 10ns):")
md_metrics = {
    "RMSD": "X Å",
    "Radio de giro": "Y Å",
    "Energía Potencial": "Z kcal/mol",
    "Densidad": "W g/cm³"
}
st.write("Estas métricas se obtendrían del análisis de su simulación de dinámica molecular.")
st.json(md_metrics)

# --- Visualización 3D ---
st.subheader("Visualización 3D Interactiva:")

# Definir la ruta al archivo PDB
# Usamos os.path.join para construir rutas de manera compatible con diferentes sistemas operativos
PDB_FILE_PATH = os.path.join("data", "dna_structure.pdb")

pdb_data = None # Inicializar pdb_data fuera del try para que siempre esté definido

try:
    with open(PDB_FILE_PATH, "r") as f:
        pdb_data = f.read()
except FileNotFoundError:
    st.error(f"`{PDB_FILE_PATH}` no encontrado. Por favor, asegúrese de tener un archivo PDB en la carpeta 'data'.")
    st.info("Para una prueba rápida, intente descargar el PDB 1BNA (B-DNA) de RCSB PDB y guárdelo como `data/dna_structure.pdb`.")

if pdb_data:
    st.markdown("---")
    st.markdown("### Estructura 3D (estática)")

    view = py3Dmol.view(width=800, height=500)
    view.addModel(pdb_data, 'pdb')
    view.setStyle({'stick':{}})
    view.zoomTo()

    st_3dmol = st.empty()
    with st_3dmol:
        # Aquí se usa view.show() que no devuelve un valor,
        # py3Dmol se encarga de renderizar el visor en el componente Streamlit.
        view.show()
    
    st.info("Puede rotar, hacer zoom y mover la estructura 3D.")

    st.markdown("---")
    st.markdown("### Visualización de Dinámica Molecular (Concepto)")
    st.write("""
    Para visualizar una trayectoria de 10ns MD:

    1.  **Cargue su archivo de trayectoria** (ej., .dcd, .xtc) y el PDB inicial.
    2.  Use librerías como `MDAnalysis` para leer la trayectoria.
    3.  Itere a través de los fotogramas de la trayectoria.
    4.  Actualice la visualización de `py3Dmol` para cada fotograma o genere una animación.
    """)
else:
    st.warning("No se pudo cargar la estructura 3D. La visualización no estará disponible hasta que se proporcione un archivo PDB válido.")

st.markdown("---")
st.write("Desarrollado con Streamlit y py3Dmol.")
