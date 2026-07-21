# 🤖 Agente IA Corporativo — Challenge Alura ONE

Agente de inteligencia artificial que responde preguntas de colaboradores
basándose en documentos internos de la empresa.

## 🏗️ Arquitectura

Documento → Extracción → Limpieza → Chunking → Embeddings → Vector DB
                                                                  ↓
Pregunta del usuario → Embedding → Búsqueda por similitud → Top-k chunks
                                                                  ↓
                                              LLM + Contexto → Respuesta


## 🚀 Ejecutar localmente

bash
pip install -r requirements.txt
cp .env.example .env  # Agrega tu OPENAI_API_KEY
streamlit run app.py


## ☁️ Deploy en Streamlit Cloud

1. Sube el repo a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. En **Settings → Secrets**, agrega:
   ```toml
   OPENAI_API_KEY = "sk-tu-key-aqui"

    Deploy automático

📁 Formatos soportados
PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx),
Markdown, CSV, JSON, HTML, TXT
🛠️ Tecnologías

    Python + Streamlit (interfaz)
    LangChain (pipeline RAG)
    OpenAI Embeddings + GPT-4o-mini
    ChromaDB (vector store)


---

## 🧠 Mapa conceptual: ¿Qué hace cada pieza?

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


---

## ⚠️ Limitaciones de este prototipo (y qué estudiar para superarlas)

| Limitación | Concepto a estudiar |
|------------|-------------------|
| No tiene OCR para PDFs escaneados | Computer Vision, Tesseract |
| No persiste datos entre sesiones | Bases de datos, Docker volumes |
| No tiene guardrails avanzados | Content moderation, NeMo Guardrails |
| No tiene session management multi-usuario | WebSockets, Redis, arquitectura multi-tenant |
| No tiene re-ranking de resultados | Cross-encoders, Cohere Rerank |
| No maneja tablas complejas de Excel | Análisis estructural de datos |
| No se despliega en OCI (solo Streamlit Cloud) | Cloud computing, IaaS, networking |

---



