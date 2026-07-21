# 🤖 Agente IA Corporativo — NexusFlow (Challenge Alura ONE)

![Estado](https://img.shields.io/badge/Estado-Desplegado%20en%20Producci%C3%B3n-brightgreen?style=for-the-badge&logo=streamlit)
![Deploy](https://img.shields.io/badge/Deploy-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-121212?style=for-the-badge&logo=chainlink&logoColor=white)
![NVIDIA Build](https://img.shields.io/badge/NVIDIA_Build-meta%2Fllama--3.1--70b--instruct-76B900?style=for-the-badge&logo=nvidia&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-Compatible-412991?style=for-the-badge&logo=openai&logoColor=white)

Agente de Inteligencia Artificial Corporativo diseñado para responder preguntas de colaboradores y equipos de trabajo basándose de manera rigurosa, precisa y transparente en la documentación interna de la empresa mediante **RAG (Retrieval-Augmented Generation)**.

---

## 🌐 Demo en Vivo y Despliegue

La aplicación se encuentra **completamente desplegada y operativa** en Streamlit Cloud:

👉 **[https://agente-corporativo-8vbrjie2avhlznnubeffja.streamlit.app/](https://agente-corporativo-8vbrjie2avhlznnubeffja.streamlit.app/)**

---

## 📊 Estado Actual del Proyecto

| Componente | Estado Actual | Detalles de Implementación |
| :--- | :---: | :--- |
| **Aplicación Web / UI** | 🟢 **Operativo** | Interfaz interactiva en Streamlit con chat en tiempo real, métricas de dataset y visor de fuentes. |
| **Despliegue Cloud** | 🟢 **Publicado** | Desplegado en Streamlit Cloud con conexión segura a variables de entorno (`Secrets`). |
| **Motor RAG** | 🟢 **Operativo** | Pipeline completo: ingestión, extracción multiformato, chunking con metadatos, embeddings y almacenamiento vectorial. |
| **LLM Integrado** | 🟢 **Activo** | **NVIDIA Build** (`meta/llama-3.1-70b-instruct`) con fallback automático a APIs OpenAI compatibles. |
| **Vector Store** | 🟢 **Activo** | **ChromaDB** para búsqueda semántica por similitud coseno sobre vectores de alta dimensión. |
| **Base de Conocimiento** | 🟢 **Indexada** | Carga e ingestión automática al iniciar la app desde el repositorio institucional (`docs/`). |
| **Filtrado por Área** | 🟢 **Operativo** | Filtro dinámico por departamento (RH, Soporte, Legal, Operaciones, Marketing). |

---

## 📌 Tabla de Contenidos

- [🌐 Demo en Vivo y Despliegue](#-demo-en-vivo-y-despliegue)
- [📊 Estado Actual del Proyecto](#-estado-actual-del-proyecto)
- [✨ Características Principales](#-características-principales)
- [📁 Formatos y Base de Conocimiento](#-formatos-y-base-de-conocimiento)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [🏗️ Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [🧠 Mapa Conceptual](#-mapa-conceptual)
- [🚀 Instalación y Ejecución Local](#-instalación-y-ejecución-local)
- [☁️ Despliegue en Streamlit Cloud](#️-despliegue-en-streamlit-cloud)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚠️ Limitaciones y Próximos Pasos](#️-limitaciones-y-próximos-pasos)

---

## ✨ Características Principales

- 🔍 **Búsqueda Semántica de Alta Precisión**: Encuentra fragmentos relevantes dentro de los documentos utilizando embeddings vectoriales.
- 🎯 **Respuestas 100% Fundamentadas**: El modelo responde **exclusivamente** con base en el contexto extraído de los documentos cargados, evitando alucinaciones.
- ⚡ **Ingestión Multiformato Automática**: Procesa documentos PDF, Word, Excel, CSV, JSON, Markdown, PowerPoint y HTML directamente al iniciar la app.
- 📌 **Filtro por Departamento / Área**: Permite acotar las consultas a áreas específicas (RH, Soporte, Legal, Operacional, Marketing).
- 📎 **Transparencia y Citas de Fuentes**: Muestra los documentos, fragmentos y extractos exactos utilizados para construir cada respuesta.
- 💬 **Interfaz de Chat Moderna**: Experiencia fluida desarrollada en Streamlit con gestión de historial y métricas en tiempo real.

---

## 📁 Formatos y Base de Conocimiento

El motor RAG procesa los documentos institucionales organizados en las subcarpetas del directorio `docs/`:

| Categoría / Departamento | Formatos Soportados | Contenido Incluido en `docs/` |
| :--- | :--- | :--- |
| **🧑‍💼 Recursos Humanos (`rh/`)** | `.pdf`, `.docx`, `.xlsx`, `.csv`, `.md`, `.json` | Manual de bienvenida, políticas de trabajo remoto, matriz de cargos, FAQ de RH, código de conducta y corpus institucional. |
| **💻 Soporte Técnico (`soporte/`)** | `.pdf`, `.md`, `.json`, `.txt` | Guías de acceso VPN, restablecimiento de credenciales, políticas de seguridad TI y solución de problemas. |
| **⚖️ Legal y Compliance (`legal/`)** | `.pdf`, `.docx`, `.html` | Políticas de privacidad, términos de servicio, contratos tipo y normativas de protección de datos. |
| **⚙️ Operaciones (`operacional/`)** | `.pdf`, `.pptx`, `.xlsx` | Manuales de procedimientos operativos, flujo de trabajo interno y métricas de desempeño. |
| **📈 Marketing y Comercial (`marketing/`)** | `.pdf`, `.pptx`, `.md` | Planes de suscripción, estructura de precios, presentación comercial y material de marca. |

---

## 🛠️ Tecnologías Utilizadas

- **Frontend & UI**: [Streamlit](https://streamlit.io/) (v1.30+)
- **Orquestador RAG**: [LangChain](https://www.langchain.com/) (v0.2+)
- **LLM Principal**: [NVIDIA Build](https://build.nvidia.com/) (`meta/llama-3.1-70b-instruct`) con endpoint OpenAI-Compatible.
- **Embeddings**: `text-embedding-3-small` (OpenAI) / `nvidia/nv-embedqa-e5-v5` (NVIDIA)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Procesamiento de Documentos**: `pypdf`, `python-docx`, `openpyxl`, `python-pptx`, `beautifulsoup4`, `pandas`

---

## 🏗️ Arquitectura del Sistema

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        ENTRADA DE DOCUMENTOS                           │
│  Carpeta docs/ (PDF, DOCX, XLSX, CSV, JSON, MD, PPTX, HTML, TXT)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Extracción & Cleaning
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        PROCESAMIENTO Y CHUNKING                        │
│  RecursiveCharacterTextSplitter + Asignación de Metadatos y Categorías │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Generación de Vectores
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        VECTOR STORE (ChromaDB)                         │
│  Almacena fragmentos y embeddings de 1536 dimensiones                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Búsqueda por similitud
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        GENERACIÓN DE RESPUESTA                         │
│  Top-k Chunks Contexto + Prompt RAG ──▶ LLM (NVIDIA Build Llama 3.1)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Respuesta + Fuentes
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        INTERFAZ DE USUARIO                             │
│  Streamlit App Chat + Visualizador de Fuentes & Métricas de Dataset    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🧠 Mapa Conceptual

```text
┌─────────────────────────────────────────────────────────┐
│                    INTERFAZ (app.py)                    │
│  Streamlit: Chat, status badge, sidebar, filtro, fuentes│
└──────────────────────┬──────────────────────────────────┘
                       │ Invoca
                       ▼
┌──────────────────────────────────────────────────────────────┐
│               MOTOR RAG (rag_engine.py)                      │
│                                                              │
│  ┌─────────────┐     ┌──────────┐     ┌──────────────────┐   │
│  │ Extracción  │──▶  │ Limpieza │──▶  │ Chunking + Meta  │   │
│  │ por formato │     │ de texto │     │ datos por chunk  │   │
│  └─────────────┘     └──────────┘     └────────┬─────────┘   │
│                                                │             │
│                                                ▼             │
│  ┌──────────────────────────────────────────────────┐        │
│  │  EMBEDDINGS (texto → vector)                     │        │
│  └──────────────────────┬───────────────────────────┘        │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────┐        │
│  │  VECTOR STORE (ChromaDB)                         │        │
│  │  Almacena vectores + metadatos por departamento  │        │
│  └──────────────────────┬───────────────────────────┘        │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────┐        │
│  │  CONSULTA RAG                                    │        │
│  │  1. Pregunta → Embedding                         │        │
│  │  2. Búsqueda top-k (con/sin filtro de categoría) │        │
│  │  3. Contexto extraído → Prompt del LLM           │        │
│  │  4. NVIDIA Build Llama 3.1 genera respuesta      │        │
│  └──────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Instalación y Ejecución Local

### 1. Requisitos Previos
- Python 3.10 o superior.
- Una clave de API activa de **NVIDIA Build** (`NVIDIA_API_KEY`) o de **OpenAI** (`OPENAI_API_KEY`).

### 2. Clonar el Repositorio e Instalar Dependencias
```bash
git clone https://github.com/jlmansilla/agente-corporativo.git
cd agente-corporativo
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno
Copia el archivo `.env.example` a `.env` y configura tus credenciales:
```bash
cp .env.example .env
```

Edita `.env`:
```env
NVIDIA_API_KEY=nvapi-tu-api-key-aqui
LLM_PROVIDER=nvidia
LLM_BASE_URL=https://integrate.api.nvidia.com/v1
LLM_MODEL=meta/llama-3.1-70b-instruct
```

### 4. Iniciar la Aplicación
```bash
streamlit run app.py
```

---

## ☁️ Despliegue en Streamlit Cloud

El proyecto está configurado para desplegarse automáticamente en **Streamlit Cloud**:

1. Subir el repositorio a GitHub.
2. Ir a [share.streamlit.io](https://share.streamlit.io) y conectar el repositorio.
3. En **Settings → Secrets**, agregar la configuración del proveedor LLM:
   ```toml
   NVIDIA_API_KEY = "nvapi-tu-key-aqui"
   LLM_PROVIDER = "nvidia"
   LLM_BASE_URL = "https://integrate.api.nvidia.com/v1"
   LLM_MODEL = "meta/llama-3.1-70b-instruct"
   ```
4. El despliegue estará activo en:
   👉 **[https://agente-corporativo-8vbrjie2avhlznnubeffja.streamlit.app/](https://agente-corporativo-8vbrjie2avhlznnubeffja.streamlit.app/)**

---

## 📂 Estructura del Proyecto

```text
agente-corporativo/
├── .streamlit/         # Configuración visual y tema de Streamlit
├── docs/               # Base de conocimiento (rh, soporte, legal, operacional, marketing)
│   ├── legal/          # Documentos del departamento legal
│   ├── marketing/      # Documentos de comercial y marketing
│   ├── operacional/    # Documentos de operaciones
│   ├── rh/             # Documentos de recursos humanos
│   └── soporte/        # Documentos de soporte técnico
├── app.py              # Interfaz web interactiva (Streamlit Chat UI)
├── rag_engine.py       # Pipeline RAG (extracción, chunking, ChromaDB, QA)
├── requirements.txt    # Dependencias del proyecto
├── .env.example        # Plantilla de variables de entorno
└── readme.md           # Documentación y estado del proyecto
```

---

## ⚠️ Limitaciones y Próximos Pasos

| Limitación Actual | Solución Planeada / Próximo Paso |
| :--- | :--- |
| **Sin OCR para PDFs escaneados** | Integración de Tesseract OCR / Unstructured. |
| **Persistencia de conversación multi-sesión** | Integración con PostgreSQL / Redis para historial persistente. |
| **Guardrails de contenido** | Implementación de NeMo Guardrails o moderación de OpenAI. |
| **Re-ranking de fragmentos** | Incorporación de Cross-Encoder / Cohere Rerank / FlashRank. |
| **Autenticación multi-usuario** | Implementación de OAuth2 / Streamlit Authenticator. |

---

<p align="center">
  Desarrollado para el <b>Challenge Alura ONE</b> 🚀<br>
  🔗 <b>Deploy Oficial:</b> <a href="https://agente-corporativo-8vbrjie2avhlznnubeffja.streamlit.app/">Agente IA Corporativo en Streamlit Cloud</a>
</p>
