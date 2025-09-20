## **Guía Completa del Laboratorio: Interpretando la Atención**

Este laboratorio está diseñado para darte una intuición visual de cómo un modelo Transformer "piensa". No es una caja negra; es un sistema de ponderaciones y relaciones que podemos observar. Sigue estos pasos para cada ejemplo y aprende a leer los "pensamientos" del modelo.

### **Configuraciones Generales**

* **Texto a Introducir:** El campo donde pegas la frase que quieres analizar.
* **Capa de Atención (Layer):** Un Transformer está compuesto por múltiples capas apiladas (BERT-base tiene 12). Las primeras capas (0-3) tienden a capturar relaciones sintácticas y de bajo nivel. Las capas intermedias (4-8) capturan relaciones semánticas más complejas. Las últimas capas (9-11) refinan la representación para la tarea final. **Para nuestros ejemplos, la capa 6 es un buen punto de partida.**
* **Cabeza de Atención (Head):** Dentro de cada capa, hay múltiples "cabezas" (BERT-base tiene 12). Cada cabeza es un mecanismo de atención independiente que se especializa en detectar un tipo diferente de relación. Una cabeza puede especializarse en pronombres, otra en relaciones de causalidad, etc. **Puedes empezar con la cabeza 0 y luego experimentar.**

---

### **Paso a Paso 1: Resolución de Pronombres**

* **Objetivo:** Ver si el modelo puede identificar correctamente a qué sustantivo se refiere un pronombre.

1.  **Configuración:**
    * **Texto a Introducir:** Pega la siguiente frase:
        `The robot picked up the ball because it was heavy.`
    * **Capa a Visualizar:** Selecciona la `6`.
    * **Cabeza a Visualizar:** Selecciona la `0` (o prueba con otras como la 2 o la 6).

2.  **Ejecución y Análisis:**
    * Haz clic en el botón **"Visualizar Atención"**.
    * Aparecerá el mapa de calor. Busca en el eje Y (Palabra que 'presta atención') la fila correspondiente al token **`it`**.
    * Sigue esa fila con la vista hacia la derecha y busca la celda más brillante (la de color más cercano al amarillo).
    * **Resultado esperado:** Verás que la celda más brillante en la fila de `it` se alinea con la columna de **`ball`**. Esto confirma que el modelo ha conectado correctamente el pronombre con el sustantivo.

3.  **Experimentación:**
    * Cambia `ball` por `trophy`. ¿Sigue funcionando?
    * Cambia la frase a `... because he was tired.` ¿A quién presta atención `he`? (Debería ser a `robot`).

---

### **Paso a Paso 2: Relación Sujeto-Verbo-Objeto**

* **Objetivo:** Observar cómo el verbo de la oración se conecta con el sujeto y el objeto.

1.  **Configuración:**
    * **Texto a Introducir:** Pega la siguiente frase:
        `The programmer wrote the code.`
    * **Capa a Visualizar:** Selecciona la `7`.
    * **Cabeza a Visualizar:** Selecciona la `8`.

2.  **Ejecución y Análisis:**
    * Haz clic en **"Visualizar Atención"**.
    * Busca la fila del verbo **`wrote`**.
    * **Resultado esperado:** Notarás que en esta fila hay dos puntos relativamente brillantes: uno en la columna de **`programmer`** (el sujeto que ejecuta la acción) y otro en la de **`code`** (el objeto que recibe la acción). La atención del verbo se distribuye entre los actores principales de la frase.

3.  **Experimentación:**
    * Prueba con otras cabezas. ¿Hay alguna que se centre más en el sujeto que en el objeto, o viceversa?

---

### **Paso a Paso 3: Dependencias a Larga Distancia**

* **Objetivo:** Comprobar la capacidad del modelo para relacionar palabras que están muy separadas.

1.  **Configuración:**
    * **Texto a Introducir:** Pega la siguiente frase larga:
        `The dog that chased the cat across the yard finally took a nap.`
    * **Capa a Visualizar:** Selecciona la `8`.
    * **Cabeza a Visualizar:** Selecciona la `4`.

2.  **Ejecución y Análisis:**
    * Haz clic en **"Visualizar Atención"**.
    * Busca la fila del verbo principal, **`took`** (o `nap`).
    * **Resultado esperado:** A pesar de la distancia y las cláusulas intermedias, verás una puntuación de atención significativamente alta en la columna del sujeto principal, **`dog`**. Esto es algo que los modelos más antiguos no podían hacer de forma fiable.

---

### **Paso a Paso 4: Resolución de Ambigüedad**

* **Objetivo:** Demostrar que la atención es contextual y cambia según el significado de la frase.

1.  **Configuración (Prueba A):**
    * **Texto a Introducir:** `The bank of the river is steep.`
    * **Capa y Cabeza:** Usa `6` y `0`.

2.  **Ejecución y Análisis (Prueba A):**
    * Visualiza la atención.
    * **Resultado esperado:** En la fila de **`bank`**, la atención más alta estará en **`river`**, porque el contexto indica que se trata de una orilla.

3.  **Configuración (Prueba B):**
    * **Texto a Introducir:** `He deposited money in the bank.`
    * **Capa y Cabeza:** Usa las mismas, `6` y `0`.

4.  **Ejecución y Análisis (Prueba B):**
    * Visualiza la atención.
    * **Resultado esperado:** Ahora, en la fila de **`bank`**, la atención se dirigirá a **`money`** y **`deposited`**. El mismo token (`bank`) genera patrones de atención completamente diferentes gracias al contexto.

---

