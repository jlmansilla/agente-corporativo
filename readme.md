# 🤖 Agente IA Corporativo — Challenge Alura ONE

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)

Agente de inteligencia artificial que responde preguntas de colaboradores de una empresa basándose de manera rigurosa y precisa en sus documentos internos institucionales mediante **RAG (Retrieval-Augmented Generation)**.

---

## 📌 Tabla de Contenidos
- [✨ Características](#-características)
- [📁 Formatos Soportados](#-formatos-soportados)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [🏗️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [🧠 Mapa Conceptual](#-mapa-conceptual)
- [🚀 Instalación y Ejecución Local](#-instalación-y-ejecución-local)
- [☁️ Despliegue en Streamlit Cloud](#️-despliegue-en-streamlit-cloud)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚠️ Limitaciones y Próximos Pasos](#️-limitaciones-y-próximos-pasos)

---

## ✨ Características

- 🔍 **Búsqueda Semántica**: Encuentra la información relevante dentro de los documentos utilizando embeddings de alta dimensión.
- 🎯 **Respuestas Fundamentadas**: El LLM responde únicamente basándose en el contexto extraído de los archivos subidos.
- ⚡ **Procesamiento Multiformato**: Carga e indexa una amplia variedad de archivos empresariales.
- 📊 **Citas y Fuentes**: Muestra de forma transparente las partes de los documentos utilizadas para generar cada respuesta.
- 💬 **Interfaz Intuitiva**: Chat interactivo desarrollado en Streamlit con carga diferida y gestión de estado.

---

## 📁 Formatos Soportados

El agente es capaz de extraer y procesar texto de los siguientes formatos:

| Categoría | Extensiones Soportadas |
| :--- | :--- |
| **Documentos de Texto** | PDF (`.pdf`), Word (`.docx`), Texto Plano (`.txt`), Markdown (`.md`) |
| **Hojas de Cálculo** | Excel (`.xlsx`), CSV (`.csv`) |
| **Presentaciones** | PowerPoint (`.pptx`) |
| **Datos Estructurados & Web** | JSON (`.json`), HTML (`.html`) |

---

## 🛠️ Tecnologías Utilizadas

- **Interfaz de Usuario**: [Streamlit](https://streamlit.io/)
- **Orquestador RAG**: [LangChain](https://www.langchain.com/)
- **Embeddings & LLM**: OpenAI (`text-embedding-3-small` / `gpt-4o-mini`)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Extracción de Documentos**: `pypdf`, `python-docx`, `openpyxl`, `python-pptx`, `beautifulsoup4`, `pandas`

---

## 🏗️ Arquitectura del Sistema

```text
Documento → Extracción → Limpieza → Chunking → Embeddings → Vector DB (Chroma)
                                                                   ↓
Pregunta del usuario → Embedding → Búsqueda por similitud → Top-k chunks
                                                                   ↓
                                               LLM + Contexto → Respuesta
```

---

## 🧠 Mapa Conceptual

```text
┌─────────────────────────────────────────────────────────┐
│                    INTERFAZ (app.py)                     │
│  Streamlit: chat, upload de docs, sidebar, fuentes      │
└──────────────────────┬──────────────────────────────────┘
                       │ llama a
                       ▼
┌─────────────────────────────────────────────────────────┐
│               MOTOR RAG (rag_engine.py)                  │
│                                                         │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐    │
│  │Extracción│──▶│ Limpieza │──▶│ Chunking + Meta  │    │
│  │por formato│   │de texto  │   │ datos por chunk  │    │
│  └──────────┘   └──────────┘   └────────┬─────────┘    │
│                                         │              │
│                                         ▼              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  EMBEDDINGS (texto → vector de 1536 dimensiones) │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         ▼                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  VECTOR STORE (ChromaDB)                         │  │
│  │  Almacena vectores + metadatos                   │  │
│  │  Permite búsqueda por similitud coseno           │  │
│  └──────────────────────┬───────────────────────────┘  │
│                         ▼                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │  CONSULTA RAG                                    │  │
│  │  1. Pregunta → embedding                         │  │
│  │  2. Búsqueda top-k en vector store               │  │
│  │  3. Chunks recuperados → contexto del prompt     │  │
│  │  4. LLM genera respuesta fundamentada            │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalación y Ejecución Local

### 1. Requisitos Previos
- Python 3.10 o superior.
- Una clave de API activa de OpenAI (`OPENAI_API_KEY`).

### 2. Clonar el Repositorio e Instalar Dependencias
```bash
git clone <URL_DE_TU_REPOSITORIO>
cd agente-corporativo
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno
Copia el archivo de ejemplo `.env.example` a `.env` y agrega tu clave de OpenAI:
```bash
cp .env.example .env
```
Edita `.env`:
```env
OPENAI_API_KEY=sk-tu-api-key-aqui
```

### 4. Iniciar la Aplicación
```bash
streamlit run app.py
```

---

## ☁️ Despliegue en Streamlit Cloud

1. Sube tu repositorio a **GitHub**.
2. Ingresa a [share.streamlit.io](https://share.streamlit.io) e inicia sesión.
3. Haz clic en **"New app"** y conecta tu repositorio.
4. En la sección **Settings → Secrets**, agrega tu clave de API de OpenAI:
   ```toml
   OPENAI_API_KEY = "sk-tu-key-aqui"
   ```
5. Haz clic en **Deploy**. El despliegue se realizará de forma automática.

---

## 📂 Estructura del Proyecto

```text
agente-corporativo/
├── .streamlit/         # Configuración del tema e interfaz de Streamlit
├── app.py              # Interfaz de usuario (Streamlit Chat & Sidebar)
├── rag_engine.py       # Lógica principal del RAG (ingestión, chunking, ChromaDB, QA)
├── requirements.txt    # Librerías y dependencias de Python
├── .env.example        # Plantilla para variables de entorno
└── readme.md           # Documentación del proyecto
```

---

## ⚠️ Limitaciones y Próximos Pasos

| Limitación Actual | Concepto / Tecnología a Estudiar para Solucionar |
| :--- | :--- |
| **Sin OCR para PDFs escaneados** | Computer Vision, Tesseract OCR, Unstructured |
| **Sin persistencia multi-sesión** | Bases de datos relacionales/NoSQL, Docker Volumes |
| **Sin Guardrails avanzados** | Content Moderation APIs, NeMo Guardrails |
| **Sin gestión multi-usuario** | Autenticación, WebSockets, Redis, Arquitectura Multi-tenant |
| **Sin Re-ranking de resultados** | Cross-Encoders, Cohere Rerank, FlashRank |
| **Tablas complejas de Excel** | Table Transformers, análisis estructural de dataframes |
| **Sin despliegue empresarial (OCI/AWS)** | Cloud Computing (OCI/GCP/AWS), Containers (Docker/K8s) |

---

<p align="center">
  Desarrollado para el Challenge Alura ONE 🚀
</p>
