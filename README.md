# 🎾 Pipeline de Extracción y Consolidación de Chats de Soporte - Padmi SAC

Este proyecto es una solución integral de ingeniería de datos diseñada para extraer de forma quirúrgica el historial de conversaciones de **WhatsApp Web**, procesar los metadatos ocultos y consolidar la información en un **Dataset Tabular de grado de producción (CSV)**. 

El dataset final está optimizado para análisis de KPI de atención al cliente (SAC) o para el entrenamiento (Fine-Tuning) de modelos de Inteligencia Artificial de P****.

Contenido del archivo `README.md`

```markdown
# 🎾 Pipeline de Extracción y Consolidación de Chats de Soporte - Padmi SAC

Este proyecto es una solución integral de ingeniería de datos diseñada para extraer de forma quirúrgica el historial de conversaciones de **WhatsApp Web**, procesar los metadatos ocultos y consolidar la información en un **Dataset Tabular de grado de producción (CSV)**. 

El dataset final está optimizado para análisis de KPI de atención al cliente (SAC) o para el entrenamiento (Fine-Tuning) de modelos de Inteligencia Artificial de Padmi.

---

## 📂 Estructura del Proyecto

```text
Proyecto_Dataset_SAC/
├── json/                                # Carpeta contenedora de las extracciones crudas
│   ├── +34643520400.json
│   ├── +34639265681.json
│   └── ...
├── Python_DataFrame_to_Dataset.py       # Script maestro de ETL (Extracción, Transformación y Carga)
├── dataset_soporte_padmi.csv            # Dataset final unificado y sanitizado (Auto-generado)
└── README.md                            # Documentación del proyecto (Este archivo)

```

---

## 🛠️ Componentes del Sistema

### 1. Extractor del DOM (JavaScript - Consola del Navegador)

Script de ejecución directa en la consola de Google Chrome (`F12`) con WhatsApp Web abierto.

* **Características:**
* Renderiza emojis nativos desde etiquetas `<img>` a texto plano.
* Filtra jerárquicamente nodos duplicados (sub-listas `<ul>`/`<li>`).
* Extrae marcas de tiempo y emisores reales directamente desde el atributo oculto `data-pre-plain-text`.
* **Barrera Anti-Basura:** Ignora automáticamente elementos flotantes de la UI de WhatsApp ("haz clic aquí...", avisos de sincronización, etc.).
* **Descarga Dinámica:** Detecta el identificador del cliente en el encabezado y descarga el archivo como `+####.json`.



### 2. Pipeline de Consolidación (Python + Pandas)

Script de automatización analítica ejecutado localmente en el entorno virtual.

* **Características:**
* **Unificación:** Agrupa todos los JSONs de la carpeta `./json/` bajo un índice común.
* **Normalización:** Limpia los nombres de archivo eliminando símbolos y sufijos de duplicidad de sistema (ej: ` (1)`).
* **De-duplicación:** Purga mensajes repetidos mediante una clave compuesta de control (`chat_id`, `fecha_hora`, `mensaje`).
* **Indexación:** Re-calcula la secuencia cronológica real de las interacciones (`mensaje_id`) del 1 al N de forma unívoca por chat.



---

## 🚀 Guía de Uso del Pipeline

### Paso 1: Raspado de Datos (Fase de Extracción)

1. Abre **WhatsApp Web** en Google Chrome y selecciona el chat del cliente.
2. Abre la consola de desarrollador (`F12` o clic derecho -> Inspeccionar -> pestaña *Console*).
3. Pega el script de JavaScript desarrollado para el proyecto y presiona `Enter`.
4. El archivo `.json` con el número del cliente se descargará automáticamente. Muévelo a la carpeta `json/` del proyecto.

### Paso 2: Ejecución del Pipeline (Fase ETL)

1. Abre tu terminal en la raíz del proyecto.
2. Asegúrate de tener activado tu entorno virtual (`.venv`).
3. Instala la dependencia de procesamiento de datos si aún no la tienes:
```bash
pip install pandas

```


4. Ejecuta el pipeline de Python:
```bash
python Python_DataFrame_to_Dataset.py

```



---

## 📊 Esquema del Dataset Final (`dataset_soporte_padmi.csv`)

El archivo de salida cuenta con una estructura tabular relacional limpia con codificación `utf-8-sig` (compatible con Excel e IA):

| Columna | Tipo de Dato | Descripción | Ejemplo |
| --- | --- | --- | --- |
| **`chat_id`** | `Int64` / `String` | Identificador único numérico del cliente (Teléfono). | `34643520400` |
| **`mensaje_id`** | `Int` | Índice correlativo cronológico del mensaje dentro de ese chat. | `1`, `2`, `3`... |
| **`fecha_hora`** | `Datetime` | Marca de tiempo estandarizada (AAAA-MM-DD HH:MM:SS). | `2026-06-22 13:22:00` |
| **`rol`** | `String` | Clasificación categórica de la interacción (`Cliente` / `Soporte`). | `Cliente` |
| **`emisor`** | `String` | Identidad textual extraída de WhatsApp. | `Yo (Padmi Soporte)` |
| **`mensaje`** | `String` | Texto íntegro de la conversación, incluyendo emojis y saltos de línea. | `"He jugado en pádel Munda..."` |

---

💻 *Desarrollado para la infraestructura de datos y soporte técnico de Padmi.*



Gemini I: https://gemini.google.com/share/d/1DYcrOQ9TV2Pi6MxpiIfCTZlFO7P29rlW?usp=sharing

Gemini II: https://gemini.google.com/share/d/1rBVJZXwe_q3QzssGlTKR_vgb1GdBQgEE?usp=sharing
