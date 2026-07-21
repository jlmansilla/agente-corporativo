"""
app.py
======
Interfaz web del Agente IA Corporativo.

Desplegado con:
  - Motor RAG: NVIDIA Build (build.nvidia.com) con modelo z.ai/glm-5.2
  - Ingesta automática: Documentación corporativa del repositorio (docs/)
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno (.env)
load_dotenv()

from rag_engine import MotorRAG, obtener_secret


# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="Agente IA Corporativo — NexusFlow",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .stChatMessage { border-radius: 10px; }
    .fuente-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #76B900;
        margin: 5px 0;
        font-size: 0.85em;
    }
    .status-badge {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 6px 12px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# INICIALIZACIÓN DEL ESTADO DE SESIÓN E INGESTA AUTOMÁTICA
# ============================================================

if "motor_rag" not in st.session_state:
    with st.spinner("🚀 Inicializando Agente RAG e ingestando documentos del repositorio..."):
        # Inicializa con NVIDIA Build (z.ai/glm-5.2) por defecto
        st.session_state.motor_rag = MotorRAG()
        # Ingesta automáticamente los documentos institucionales del repositorio
        st.session_state.motor_rag.ingestar_directorio("docs")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# ============================================================
# SIDEBAR: INFORMACIÓN Y ESTADO DEL REPOSITORIO
# ============================================================
with st.sidebar:
    st.title("🏢 Agente Corporativo")
    st.markdown('<div class="status-badge">🟢 Modelo: NVIDIA Build (z.ai/glm-5.2)</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # --- Estado del Repositorio de Documentos ---
    resumen_docs = st.session_state.motor_rag.obtener_resumen()
    total_docs = len(resumen_docs)
    total_chunks = sum(d.get("chunks", 0) for d in resumen_docs)
    
    st.subheader("📚 Base de Conocimiento")
    col1, col2 = st.columns(2)
    col1.metric("Documentos", total_docs)
    col2.metric("Fragmentos", total_chunks)
    
    # --- Filtro de Categorías ---
    categorias_disponibles = ["Todas"] + st.session_state.motor_rag.obtener_categorias()
    filtro_categoria = st.selectbox(
        "🔍 Filtrar área de búsqueda:",
        options=categorias_disponibles,
        index=0,
        help="Permite acotar la búsqueda semántica a un departamento específico."
    )
    
    # --- Lista de documentos ingestados del repositorio ---
    with st.expander(f"📄 Ver documentos del repositorio ({total_docs})"):
        if resumen_docs:
            for doc in resumen_docs:
                st.markdown(
                    f"• **{doc['archivo']}**  \n"
                    f"&nbsp;&nbsp;&nbsp;📁 *{doc['categoria']}* ({doc['chunks']} chunks)"
                )
        else:
            st.info("No se encontraron documentos en la carpeta 'docs/'")
            
    st.divider()
    
    # Botón para limpiar chat
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()


# ============================================================
# PANEL PRINCIPAL: CHAT CON EL AGENTE IA
# ============================================================
st.title("🤖 Agente IA Corporativo — NexusFlow")
st.caption(
    "Responde preguntas institucionales basándose **exclusivamente** en los documentos "
    "procesados del repositorio mediante RAG con **NVIDIA Build (z.ai/glm-5.2)**."
)

# --- Renderizar historial de chat ---
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.markdown(mensaje["contenido"])
        
        # Muestra fuentes si existen
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
if prompt := st.chat_input("Escribe tu pregunta sobre políticas de RH, soporte, legal o procesos corporativos..."):
    
    # Agregar mensaje del usuario al historial
    st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generar respuesta con el motor RAG
    with st.chat_message("assistant"):
        with st.spinner("🔍 Consultando base de conocimiento con NVIDIA Build (z.ai/glm-5.2)..."):
            try:
                cat_filtro = None if filtro_categoria == "Todas" else filtro_categoria
                respuesta, fuentes = st.session_state.motor_rag.consultar(
                    pregunta=prompt,
                    categoria_filtro=cat_filtro,
                    k=5,
                )
                
                st.markdown(respuesta)
                
                # Mostrar fuentes consultadas
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
                
                # Guardar respuesta en historial
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

# --- Pantalla de bienvenida previa a enviar mensajes ---
if not st.session_state.mensajes:
    st.markdown("""
    ---
    ### 👋 ¡Bienvenido al Asistente Corporativo!
    
    La base de conocimiento interna ha sido cargada automáticamente desde los documentos del repositorio.
    Puedes realizar cualquier pregunta sobre los procesos y políticas de la empresa:
    
    | Área | Ejemplos de Preguntas |
    | :--- | :--- |
    | 🧑‍💼 **Recursos Humanos** | *"¿Cuántos días de vacaciones me corresponden al año?"* |
    | 💻 **Soporte y Sistemas** | *"¿Cómo configuro el acceso a la VPN o restablezco mi contraseña?"* |
    | ⚖️ **Legal y Compliance** | *"¿Cuáles son los términos y la política de privacidad de los datos?"* |
    | ⚙️ **Operaciones** | *"¿Cuál es la visión general de los procesos operativos de NexusFlow?"* |
    | 📈 **Marketing y Comercial** | *"¿Cuáles son los planes de precios y modelos de suscripción?"* |
    
    *Powered by **NVIDIA Build (z.ai/glm-5.2)** + **RAG**.*
    """)