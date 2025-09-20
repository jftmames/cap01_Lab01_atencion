# app.py
# Laboratorio 1: Visualizando el Mecanismo de Atención
# Libro IA LABS

# --- Importaciones Esenciales ---
# Importamos las librerías necesarias.
# streamlit para la interfaz web, transformers para el modelo, torch es el backend,
# y matplotlib/seaborn para la visualización.
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página ---
# Damos un título y un ícono a nuestra página en el navegador.
st.set_page_config(
    page_title="Visor de Atención",
    page_icon="🧠",
    layout="wide"
)

# --- Carga del Modelo (con Caché) ---
# Esta función carga el tokenizer y el modelo.
# Usamos el decorador @st.cache_resource de Streamlit para que esta operación
# (que es muy lenta) solo se ejecute una vez, la primera vez que se carga la app.
# Las siguientes veces, usará la versión en caché, haciendo la app mucho más rápida.
@st.cache_resource
def load_model():
    """Carga el modelo y el tokenizer de Hugging Face."""
    # Usaremos 'bert-base-uncased', un modelo estándar y versátil.
    # 'output_attentions=True' es CRÍTICO. Le dice al modelo que nos devuelva
    # los pesos de atención además de la salida normal.
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    model = AutoModel.from_pretrained('bert-base-uncased', output_attentions=True)
    return tokenizer, model

# --- Título y Descripción de la App ---
st.title("🔬 Visor del Mecanismo de Atención en Transformers")
st.write(
    "Esta aplicación te permite ver cómo funciona el mecanismo de 'atención' dentro de un modelo Transformer (BERT). "
    "Introduce una frase y observa qué palabras le 'prestan atención' a otras para construir su significado contextual."
)

# --- Carga de los modelos ---
# Llamamos a nuestra función para tener el tokenizer y el modelo listos.
# Streamlit mostrará un spinner mientras esta operación se completa.
with st.spinner("Cargando modelo pre-entrenado..."):
    tokenizer, model = load_model()

# --- Interfaz de Usuario ---
st.header("Introduce tu frase")
# Usamos un text_area para que el usuario pueda escribir su texto.
# Le damos una frase de ejemplo para guiarlo.
user_input = st.text_area(
    "Texto a analizar:",
    "The quick brown fox jumps over the lazy dog.",
    height=100
)

# Creamos columnas para poner los selectores de capa y cabeza uno al lado del otro.
col1, col2 = st.columns(2)
# Creamos un slider para que el usuario elija qué capa de atención visualizar.
# BERT-base tiene 12 capas (de 0 a 11).
layer_to_visualize = col1.slider("Capa de Atención a Visualizar", 0, 11, 6)
# Y otro para la cabeza de atención. BERT-base tiene 12 cabezas (de 0 a 11).
head_to_visualize = col2.slider("Cabeza de Atención a Visualizar", 0, 11, 0)

# El botón que iniciará el análisis.
if st.button("Visualizar Atención"):
    if user_input:
        # --- Procesamiento del Modelo ---
        # 1. Tokenización: Convertimos el texto en tokens que el modelo entiende.
        inputs = tokenizer(user_input, return_tensors='pt', add_special_tokens=True)
        token_list = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

        # 2. Inferencia: Pasamos los tokens por el modelo.
        # 'torch.no_grad()' desactiva el cálculo de gradientes, lo que acelera
        # la inferencia ya que no estamos entrenando el modelo.
        with torch.no_grad():
            outputs = model(**inputs)

        # 3. Extracción de Atención:
        # Los pesos de atención están en 'outputs.attentions'.
        # Es una tupla con las matrices de atención de cada capa.
        # Seleccionamos la capa y la cabeza que el usuario eligió.
        attention_matrix = outputs.attentions[layer_to_visualize][0, head_to_visualize].numpy()

        # --- Visualización del Heatmap ---
        st.header(f"Mapa de Calor de Atención (Capa {layer_to_visualize}, Cabeza {head_to_visualize})")
        st.write(
            "Este mapa muestra la puntuación de atención de cada palabra (eje Y) hacia cada otra palabra (eje X). "
            "Un color más brillante significa una puntuación de atención más alta."
        )

        # Usamos matplotlib y seaborn para crear el gráfico.
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(attention_matrix, xticklabels=token_list, yticklabels=token_list, cmap='viridis', ax=ax)
        plt.xticks(rotation=45) # Rotamos las etiquetas para que no se superpongan.
        ax.set_xlabel("Palabra a la que se 'presta atención' (Key)")
        ax.set_ylabel("Palabra que 'presta atención' (Query)")

        # Mostramos el gráfico en Streamlit.
        st.pyplot(fig)
    else:
        st.warning("Por favor, introduce una frase para analizar.")
