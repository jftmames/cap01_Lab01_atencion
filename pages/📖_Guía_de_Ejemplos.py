# pages/📖_Guía_de_Ejemplos.py

import streamlit as st

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Guía de Ejemplos",
    page_icon="📖",
    layout="wide"
)

# --- Título y Descripción ---
st.title("📖 Guía de Ejemplos para el Visor de Atención")
st.markdown(
    """
    Esta guía proporciona varios ejemplos para probar en el **Visor de Atención**. 
    Cada ejemplo está diseñado para revelar un aspecto diferente de cómo el mecanismo 
    de atención de un Transformer interpreta el lenguaje.
    """
)

# --- Separador ---
st.divider()

# --- Ejemplo 1: Resolución de Pronombres ---
st.subheader("1. Resolución de Pronombres", anchor=False)
st.markdown(
    """
    Esta prueba muestra si el modelo puede vincular correctamente un pronombre (como 'it', 'he', 'she') 
    al sustantivo al que se refiere.
    """
)
st.code("The robot picked up the ball because it was heavy.", language="text")
st.info(
    """
    **Qué esperar:** Busca la fila del token **`it`**. Deberías ver un color muy brillante 
    en la columna del token **`ball`**. Esto demuestra que el modelo entiende que "it" se refiere 
    a "the ball", y no a "the robot".
    """
)

# --- Ejemplo 2: Relación Sujeto-Verbo-Objeto ---
st.subheader("2. Relación Sujeto-Verbo-Objeto", anchor=False)
st.markdown(
    """
    Esta prueba revela cómo la acción principal (el verbo) se conecta con quien la realiza (sujeto) 
    y quien la recibe (objeto).
    """
)
st.code("The programmer wrote the code.", language="text")
st.info(
    """
    **Qué esperar:** En la fila del verbo **`wrote`**, deberías ver puntuaciones de atención altas 
    (colores brillantes) tanto para **`programmer`** (el sujeto) como para **`code`** (el objeto). 
    Esto muestra cómo la atención mapea la estructura gramatical.
    """
)

# --- Ejemplo 3: Dependencias a Larga Distancia ---
st.subheader("3. Dependencias a Larga Distancia", anchor=False)
st.markdown(
    """
    Los Transformers destacan por su capacidad para conectar palabras que están muy separadas en una oración. 
    Este ejemplo prueba esa capacidad.
    """
)
st.code("The dog that chased the cat across the yard finally took a nap.", language="text")
st.info(
    """
    **Qué esperar:** Busca la fila del verbo final, **`nap`** (o `took`). Debería mostrar una puntuación 
    de atención sorprendentemente alta para el sujeto principal, **`dog`**, a pesar de la distancia.
    """
)

# --- Ejemplo 4: Resolución de Ambigüedad ---
st.subheader("4. Resolución de Ambigüedad", anchor=False)
st.markdown(
    """
    Esta prueba muestra cómo el contexto cambia el significado de una palabra y, por lo tanto, 
    sus patrones de atención.
    """
)
st.code("The bank of the river is steep.\nHe deposited money in the bank.", language="text")
st.info(
    """
    **Qué esperar:** En la primera frase, **`bank`** prestará fuerte atención a **`river`**. 
    En la segunda, **`bank`** prestará atención a **`money`** y **`deposited`**. Esto prueba que la atención 
    es dinámica y depende del contexto.
    """
)

# --- Ejemplo 5: Puntuación y Tokens Especiales ---
st.subheader("5. Puntuación y Tokens Especiales", anchor=False)
st.markdown(
    """
    Esto te ayuda a ver cómo el modelo trata los tokens que no son palabras, como la puntuación 
    o los tokens de control que usa internamente.
    """
)
st.code("Apples are sweet.", language="text")
st.info(
    """
    **Qué esperar:** El punto final (`.`) probablemente prestará atención a la última palabra, **`sweet`**. 
    También verás tokens especiales como `[CLS]` y `[SEP]`. El token `[CLS]` a menudo agrega 
    el significado de toda la oración, por lo que podría prestar atención a muchos tokens a la vez.
    """
)
