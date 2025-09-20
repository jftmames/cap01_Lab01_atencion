# app.py (Versión "Todo en Uno")

# --- Importaciones Esenciales ---
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Visor de Atención",
    page_icon="🧠",
    layout="wide"
)

# --- Carga del Modelo (con Caché) ---
@st.cache_resource
def load_model():
    """Carga el modelo y el tokenizer de Hugging Face."""
    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    model = AutoModel.from_pretrained('bert-base-uncased', output_attentions=True)
    return tokenizer, model

# --- Título Principal ---
st.title("🔬 Visor del Mecanismo de Atención y Guía")

# --- Creación de las Pestañas ---
# st.tabs crea un contenedor con pestañas. Cada bloque 'with' corresponde a una pestaña.
tab1, tab2 = st.tabs(["Visor de Atención", "📖 Guía de Ejemplos"])


# --- Contenido de la Pestaña 1: Visor de Atención ---
with tab1:
    st.header("Visualizador Interactivo de Atención")
    st.write(
        "Esta aplicación te permite ver cómo funciona el mecanismo de 'atención' dentro de un modelo Transformer (BERT). "
        "Introduce una frase y observa qué palabras le 'prestan atención' a otras para construir su significado contextual."
    )

    with st.spinner("Cargando modelo pre-entrenado..."):
        tokenizer, model = load_model()

    st.subheader("Introduce tu frase")
    user_input = st.text_area(
        "Texto a analizar:",
        "The quick brown fox jumps over the lazy dog.",
        height=100,
        key="main_input" # Se añade una 'key' para diferenciarlo de otros text_area
    )

    col1, col2 = st.columns(2)
    layer_to_visualize = col1.slider("Capa de Atención a Visualizar", 0, 11, 6)
    head_to_visualize = col2.slider("Cabeza de Atención a Visualizar", 0, 11, 0)

    if st.button("Visualizar Atención"):
        if user_input:
            inputs = tokenizer(user_input, return_tensors='pt', add_special_tokens=True)
            token_list = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])

            with torch.no_grad():
                outputs = model(**inputs)

            attention_matrix = outputs.attentions[layer_to_visualize][0, head_to_visualize].numpy()

            st.subheader(f"Mapa de Calor de Atención (Capa {layer_to_visualize}, Cabeza {head_to_visualize})")
            st.write(
                "Este mapa muestra la puntuación de atención de cada palabra (eje Y) hacia cada otra palabra (eje X). "
                "Un color más brillante significa una puntuación de atención más alta."
            )

            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(attention_matrix, xticklabels=token_list, yticklabels=token_list, cmap='viridis', ax=ax)
            plt.xticks(rotation=45)
            ax.set_xlabel("Palabra a la que se 'presta atención' (Key)")
            ax.set_ylabel("Palabra que 'presta atención' (Query)")

            st.pyplot(fig)
        else:
            st.warning("Por favor, introduce una frase para analizar.")


# --- Contenido de la Pestaña 2: Guía de Ejemplos ---
with tab2:
    st.header("Guía de Ejemplos para el Visor de Atención")
    st.markdown(
        """
        Esta guía proporciona varios ejemplos para probar en el **Visor de Atención**. 
        Cada ejemplo está diseñado para revelar un aspecto diferente de cómo el mecanismo 
        de atención de un Transformer interpreta el lenguaje.
        """
    )
    st.divider()

    st.subheader("1. Resolución de Pronombres", anchor=False)
    st.markdown("Muestra si el modelo vincula un pronombre (como 'it') al sustantivo al que se refiere.")
    st.code("The robot picked up the ball because it was heavy.", language="text")
    st.info("**Qué esperar:** En la fila de `it`, busca un color brillante en la columna de `ball`.")

    st.subheader("2. Relación Sujeto-Verbo-Objeto", anchor=False)
    st.markdown("Revela cómo la acción (verbo) se conecta con quien la realiza (sujeto) y quien la recibe (objeto).")
    st.code("The programmer wrote the code.", language="text")
    st.info("**Qué esperar:** En la fila de `wrote`, busca colores brillantes en las columnas de `programmer` y `code`.")
    
    st.subheader("3. Dependencias a Larga Distancia", anchor=False)
    st.markdown("Prueba la capacidad del Transformer para conectar palabras que están muy separadas.")
    st.code("The dog that chased the cat across the yard finally took a nap.", language="text")
    st.info("**Qué esperar:** En la fila de `nap` (o `took`), busca un color brillante en la columna de `dog`.")
