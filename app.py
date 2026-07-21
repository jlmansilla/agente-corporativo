"""
app.py
======
Interfaz web del Agente IA Corporativo.

Estructura de la interfaz:
  - Sidebar: Carga de documentos + configuración
  - Panel principal: Chat con el agente

Para ejecutar localmente:
    streamlit run app.py

Para deploy en Streamlit Cloud:
    1. Subir a GitHub
    2. Conectar repo en share.streamlit.io
    3. Configurar OPENAI_API_KEY en Secrets
"""

import streamlit as st
import tempfile
import os
from datetime import datetime

from rag_engine import MotorRAG, EXTRACTORES


# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="Agente IA Corporativo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================
st.markdown("""
<style>
    .stChatMessage { border-radius: 10px; }
    .fuente-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #1a73e8;
        margin: 5px 0;
        font-size: 0.85em;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# INICIALIZACIÓN DEL ESTADO DE SESIÓN
# ============================================================
# ¿POR QUÉ session_state? Streamlit re-ejecuta todo el script
# en cada interacción. session_state persiste datos entre
# re-ejecuciones (como el motor RAG y el historial de chat).

if "motor_rag" not in st.session_state:
    st.session_state.motor_rag = MotorRAG()

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if "documentos_cargados" not in st.session_state:
    st.session_state.documentos_cargados = []


# ============================================================
# SIDEBAR: CARGA DE DOCUMENTOS Y CONFIGURACIÓN
# ============================================================
with st.sidebar:
    st.title("📂 Gestión de Documentos")
    st.caption("Sube los documentos internos de la empresa")
    
    # --- Selector de categoría ---
    # ¿POR QUÉ categorías? Para poder filtrar búsquedas
    # y organizar el conocimiento por área de negocio.
    categoria = st.selectbox(
        "Categoría del documento:",
        [
            "Recursos Humanos",
            "Financiero y Contable",
            "Operacional",
            "Estratégico",
            "Legal y Compliance",
            "Marketing y Comercial",
            "Datos y Sistemas",
            "Comunicación Interna",
            "General",
        ],
        help="Clasifica el documento para mejorar la precisión de las búsquedas."
    )
    
    # --- Upload de archivos ---
    # Aceptamos todos los formatos del desafío
    archivos = st.file_uploader(
        "Selecciona archivo(s):",
        type=["pdf", "docx", "doc", "xlsx", "xls", "csv", 
              "pptx", "json", "html", "htm", "md", "txt"],
        accept_multiple_files=True,
        help="Formatos soportados: PDF, Word, Excel, PowerPoint, "
             "Markdown, CSV, JSON, HTML, TXT"
    )
    
    # --- Parámetros de chunking (avanzado) ---
    with st.expander("⚙️ Parámetros de procesamiento (avanzado)"):
        chunk_size = st.slider(
            "Tamaño del chunk (caracteres):",
            min_value=200, max_value=2000, value=800, step=100,
            help="Fragmentos más grandes = más contexto por chunk, "
                 "pero embeddings menos precisos."
        )
        chunk_overlap = st.slider(
            "Overlap entre chunks:",
            min_value=0, max_value=400, value=150, step=50,
            help="Superposición para no cortar ideas a la mitad."
        )
    
    # --- Botón de procesamiento ---
    if archivos:
        if st.button("🔄 Procesar documentos", type="primary", use_container_width=True):
            progress = st.progress(0)
            status = st.empty()
            
            for i, archivo in enumerate(archivos):
                status.text(f"Procesando: {archivo.name}...")
                
                # Guardar temporalmente (Streamlit no da ruta directa)
                with tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix=os.path.splitext(archivo.name)[1]
                ) as tmp:
                    tmp.write(archivo.read())
                    tmp_path = tmp.name
                
                try:
                    resultado = st.session_state.motor_rag.ingestar_documento(
                        ruta=tmp_path,
                        categoria=categoria,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap,
                    )
                    
                    st.session_state.documentos_cargados.append({
                        "nombre": resultado.nombre_archivo,
                        "categoria": resultado.categoria,
                        "formato": resultado.formato,
                        "chunks": resultado.num_chunks,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    })
                    
                    st.success(
                        f"✅ **{archivo.name}** → {resultado.num_chunks} fragmentos"
                    )
                except Exception as e:
                    st.error(f"❌ Error con {archivo.name}: {str(e)}")
                finally:
                    os.unlink(tmp_path)  # Limpiar archivo temporal
                
                progress.progress((i + 1) / len(archivos))
            
            status.text("¡Procesamiento completado!")
            st.rerun()
    
    # --- Resumen de documentos cargados ---
    if st.session_state.documentos_cargados:
        st.divider()
        st.subheader(f"📚 Documentos cargados ({len(st.session_state.documentos_cargados)})")
        
        for doc in st.session_state.documentos_cargados:
            st.markdown(
                f"📄 **{doc['nombre']}**  \n"
                f"&nbsp;&nbsp;&nbsp;📁 {doc['categoria']} | "
                f"🔢 {doc['chunks']} chunks | "
                f"🕐 {doc['timestamp']}"
            )
        
        # Métricas
        total_chunks = sum(d["chunks"] for d in st.session_state.documentos_cargados)
        col1, col2 = st.columns(2)
        col1.metric("Documentos", len(st.session_state.documentos_cargados))
        col2.metric("Fragmentos", total_chunks)
        
        # Botón para reiniciar
        if st.button("🗑️ Reiniciar todo", use_container_width=True):
            st.session_state.motor_rag = MotorRAG()
            st.session_state.mensajes = []
            st.session_state.documentos_cargados = []
            st.rerun()


# ============================================================
# PANEL PRINCIPAL: CHAT CON EL AGENTE
# ============================================================
st.title("🤖 Agente IA Corporativo")
st.caption(
    "Consulta la base de conocimiento de la empresa. "
    "El agente responde basándose **exclusivamente** en los documentos cargados."
)

# --- Filtro de categoría para la consulta ---
categorias_disponibles = ["Todas"] + st.session_state.motor_rag.obtener_categorias()
if len(categorias_disponibles) > 1:
    filtro_categoria = st.selectbox(
        "🔍 Filtrar por categoría (opcional):",
        categorias_disponibles,
        horizontal=True,
    )
else:
    filtro_categoria = "Todas"

# --- Renderizar historial de chat ---
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])
        
        # Si es respuesta del asistente, mostrar fuentes
        if mensaje["rol"] == "assistant" and mensaje.get("fuentes"):
            with st.expander("📎 Fuentes consultadas"):
                for fuente in mensaje["fuentes"]:
                    st.markdown(
                        f'<div class="fuente-box">'
                        f'📄 <b>{fuente["archivo"]}</b> | '
                        f'📁 {fuente["categoria"]} | '
                        f'Fragmento #{fuente["fragmento"]}<br>'
                        f'<i>"{fuente["contenido_preview"]}"</i>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )

# --- Input del usuario ---
if prompt := st.chat_input("Escribe tu pregunta sobre los documentos de la empresa..."):
    
    # Verificar que haya documentos cargados
    if not st.session_state.documentos_cargados:
        st.warning("⚠️ Primero debes cargar documentos en el panel lateral.")
        st.stop()
    
    # Agregar mensaje del usuario al historial
    st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generar respuesta con el motor RAG
    with st.chat_message("assistant"):
        with st.spinner("🔍 Buscando en los documentos..."):
            try:
                respuesta, fuentes = st.session_state.motor_rag.consultar(
                    pregunta=prompt,
                    categoria_filtro=filtro_categoria,
                    k=5,
                )
                
                st.markdown(respuesta)
                
                # Mostrar fuentes
                if fuentes:
                    with st.expander("📎 Fuentes consultadas"):
                        for fuente in fuentes:
                            st.markdown(
                                f'<div class="fuente-box">'
                                f'📄 <b>{fuente["archivo"]}</b> | '
                                f'📁 {fuente["categoria"]} | '
                                f'Fragmento #{fuente["fragmento"]}<br>'
                                f'<i>"{fuente["contenido_preview"]}"</i>'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                
                # Guardar en historial
                st.session_state.mensajes.append({
                    "rol": "assistant",
                    "contenido": respuesta,
                    "fuentes": fuentes,
                })
                
            except Exception as e:
                error_msg = f"❌ Error al procesar la consulta: {str(e)}"
                st.error(error_msg)
                st.session_state.mensajes.append({
                    "rol": "assistant",
                    "contenido": error_msg,
                })

# --- Mensaje de bienvenida si no hay mensajes ---
if not st.session_state.mensajes:
    st.markdown("""
    ---
    ### 👋 ¡Bienvenido!
    
    Soy el asistente de conocimiento interno de la empresa. 
    Puedo responder preguntas sobre:
    
    | Área | Ejemplos de preguntas |
    |------|----------------------|
    | 🧑‍💼 Recursos Humanos | *"¿Cuántos días de vacaciones tengo?"* |
    | 💰 Financiero | *"¿Cuál es el proceso para rendir gastos?"* |
    | ⚖️ Legal | *"¿Qué dice la política de privacidad sobre mis datos?"* |
    | 🔧 Operacional | *"¿Cuál es el procedimiento de onboarding?"* |
    
    **Para empezar:**
    1. Sube documentos en el panel lateral ←
    2. Selecciona la categoría correspondiente
    3. Haz clic en "Procesar documentos"
    4. ¡Pregúntame lo que necesites!
    """)