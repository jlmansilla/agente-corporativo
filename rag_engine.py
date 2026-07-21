"""
rag_engine.py
=============
Motor RAG del agente corporativo.

Este módulo implementa el pipeline completo:
  1. Extracción de texto por formato
  2. Limpieza del texto
  3. Chunking (división en fragmentos)
  4. Generación de embeddings
  5. Almacenamiento en vector store
  6. Recuperación y generación de respuesta

Cada función está documentada para que entiendas el POR QUÉ, no solo el QUÉ.
"""

import os
import re
import json
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field

# --- Extracción de documentos ---
from pypdf import PdfReader
from docx import Document as DocxDocument
from pptx import Presentation
import openpyxl
import pandas as pd
from bs4 import BeautifulSoup

# --- LangChain: chunking, embeddings, vector store, LLM ---
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.schema import Document as LangChainDocument


# ============================================================
# ESTRUCTURA DE DATOS
# ============================================================

@dataclass
class DocumentoProcesado:
    """Representa un documento después de la extracción y el chunking."""
    nombre_archivo: str
    categoria: str
    chunks: List[LangChainDocument] = field(default_factory=list)
    num_chunks: int = 0
    formato: str = ""


# ============================================================
# 1. EXTRACCIÓN DE TEXTO POR FORMATO
# ============================================================
# ¿POR QUÉ? Cada formato almacena el texto de forma distinta.
# Un PDF es un layout visual; un Word es XML estructurado;
# un Excel es una grilla de celdas. No se pueden tratar igual.

def extraer_pdf(ruta: str) -> str:
    """
    Extrae texto de un PDF nativo (generado digitalmente).
    
    Limitación: Si el PDF es escaneado (imágenes), esto devolverá
    texto vacío. En producción necesitarías OCR (pytesseract).
    """
    reader = PdfReader(ruta)
    paginas = []
    for i, pagina in enumerate(reader.pages):
        texto = pagina.extract_text() or ""
        if texto.strip():
            paginas.append(f"[Página {i+1}]\n{texto}")
    return "\n\n".join(paginas)


def extraer_word(ruta: str) -> str:
    """
    Extrae texto de un archivo Word (.docx).
    Preserva la estructura de títulos y párrafos,
    lo cual es importante para el chunking posterior.
    """
    doc = DocxDocument(ruta)
    partes = []
    for parrafo in doc.paragraphs:
        # Detectamos si es un título por el estilo del párrafo
        if parrafo.style and parrafo.style.name.startswith("Heading"):
            nivel = parrafo.style.name.replace("Heading ", "")
            partes.append(f"{'#' * int(nivel) if nivel.isdigit() else '#'} {parrafo.text}")
        elif parrafo.text.strip():
            partes.append(parrafo.text)
    
    # También extraemos texto de tablas si existen
    for tabla in doc.tables:
        for fila in tabla.rows:
            celdas = [celda.text.strip() for celda in fila.cells]
            partes.append(" | ".join(celdas))
    
    return "\n\n".join(partes)


def extraer_excel(ruta: str) -> str:
    """
    Extrae texto de un archivo Excel (.xlsx).
    
    Estrategia: Convertir cada hoja en texto estructurado,
    repitiendo los encabezados en cada fila para que cada
    línea sea comprensible de forma independiente.
    
    ¿POR QUÉ repetir encabezados? Porque cuando hagamos chunking,
    un fragmento podría contener solo filas sin encabezado,
    y perdería todo sentido.
    """
    wb = openpyxl.load_workbook(ruta, data_only=True)
    partes = []
    
    for hoja_nombre in wb.sheetnames:
        hoja = wb[hoja_nombre]
        partes.append(f"## Hoja: {hoja_nombre}")
        
        filas = list(hoja.iter_rows(values_only=True))
        if not filas:
            continue
        
        # Primera fila = encabezados
        encabezados = [str(c) if c is not None else "" for c in filas[0]]
        partes.append(" | ".join(encabezados))
        partes.append("-" * 40)
        
        # Filas de datos: repetimos el contexto del encabezado
        for fila in filas[1:]:
            valores = [str(c) if c is not None else "" for c in fila]
            if any(v.strip() for v in valores):
                # Formato: "Encabezado: Valor" para cada celda
                linea = " | ".join(
                    f"{enc}: {val}" 
                    for enc, val in zip(encabezados, valores) 
                    if val.strip()
                )
                partes.append(linea)
    
    return "\n".join(partes)


def extraer_powerpoint(ruta: str) -> str:
    """
    Extrae texto de un PowerPoint (.pptx).
    Incluye texto de diapositivas Y notas del orador,
    que suelen contener contexto adicional importante.
    """
    prs = Presentation(ruta)
    partes = []
    
    for i, slide in enumerate(prs.slides, 1):
        partes.append(f"## Diapositiva {i}")
        
        # Texto de los shapes (títulos, cuadros de texto, etc.)
        for shape in slide.shapes:
            if shape.has_text_frame:
                for parrafo in shape.text_frame.paragraphs:
                    if parrafo.text.strip():
                        partes.append(parrafo.text)
        
        # Notas del orador (contexto adicional)
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notas = slide.notes_slide.notes_text_frame.text.strip()
            if notas:
                partes.append(f"[Notas del orador]: {notas}")
    
    return "\n\n".join(partes)


def extraer_csv(ruta: str) -> str:
    """Extrae texto de un CSV convirtiéndolo en texto estructurado."""
    df = pd.read_csv(ruta)
    partes = [f"## Datos: {os.path.basename(ruta)}"]
    partes.append(f"Columnas: {', '.join(df.columns.tolist())}")
    partes.append(f"Total de registros: {len(df)}")
    partes.append("")
    
    # Convertir cada fila en una frase descriptiva
    for _, fila in df.iterrows():
        linea = " | ".join(f"{col}: {val}" for col, val in fila.items() if pd.notna(val))
        partes.append(linea)
    
    return "\n".join(partes)


def extraer_json(ruta: str) -> str:
    """
    Extrae texto de un JSON convirtiéndolo en texto legible.
    Maneja estructuras anidadas de forma recursiva.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    def json_a_texto(obj, nivel=0):
        lineas = []
        indent = "  " * nivel
        if isinstance(obj, dict):
            for clave, valor in obj.items():
                if isinstance(valor, (dict, list)):
                    lineas.append(f"{indent}{clave}:")
                    lineas.append(json_a_texto(valor, nivel + 1))
                else:
                    lineas.append(f"{indent}{clave}: {valor}")
        elif isinstance(obj, list):
            for item in obj:
                lineas.append(json_a_texto(item, nivel))
        else:
            lineas.append(f"{indent}{obj}")
        return "\n".join(lineas)
    
    return json_a_texto(data)


def extraer_html(ruta: str) -> str:
    """
    Extrae texto de un HTML eliminando todas las etiquetas.
    Mantiene solo el contenido legible.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    # Eliminar scripts y estilos
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    
    return soup.get_text(separator="\n", strip=True)


def extraer_markdown(ruta: str) -> str:
    """
    Lee un archivo Markdown. Se mantiene la estructura
    porque los encabezados (#, ##) son útiles para el chunking.
    """
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


# Mapa de extensiones → función de extracción
EXTRACTORES = {
    ".pdf": extraer_pdf,
    ".docx": extraer_word,
    ".doc": extraer_word,
    ".xlsx": extraer_excel,
    ".xls": extraer_excel,
    ".csv": extraer_csv,
    ".pptx": extraer_powerpoint,
    ".json": extraer_json,
    ".html": extraer_html,
    ".htm": extraer_html,
    ".md": extraer_markdown,
    ".txt": lambda ruta: open(ruta, "r", encoding="utf-8").read(),
}


def extraer_texto(ruta: str) -> str:
    """
    Función dispatcher: detecta el formato por extensión
    y llama al extractor correspondiente.
    """
    ext = os.path.splitext(ruta)[1].lower()
    extractor = EXTRACTORES.get(ext)
    if extractor is None:
        raise ValueError(f"Formato no soportado: {ext}")
    return extractor(ruta)


# ============================================================
# 2. LIMPIEZA DEL TEXTO
# ============================================================
# ¿POR QUÉ? El texto extraído tiene "ruido": espacios múltiples,
# saltos de línea innecesarios, caracteres de control, etc.
# Ese ruido degrada la calidad de los embeddings.

def limpiar_texto(texto: str) -> str:
    """Limpia el texto eliminando ruido sin perder contenido."""
    # Normalizar saltos de línea
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    # Reemplazar 3+ saltos de línea por 2 (separación de párrafos)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    # Reemplazar múltiples espacios por uno
    texto = re.sub(r"[ \t]+", " ", texto)
    # Eliminar caracteres de control (excepto \n y \t)
    texto = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", texto)
    # Eliminar espacios al inicio/fin de cada línea
    lineas = [linea.strip() for linea in texto.split("\n")]
    texto = "\n".join(lineas)
    return texto.strip()


# ============================================================
# 3. CHUNKING (División en fragmentos)
# ============================================================
# ¿POR QUÉ? Los documentos completos son demasiado grandes para:
#   a) Caber en la ventana de contexto del LLM
#   b) Generar embeddings precisos (un embedding de 100 páginas
#      "diluye" el significado de cada parte)
#
# La estrategia de chunking es una DECISIÓN DE DISEÑO crítica:
#   - Chunks muy grandes → embeddings imprecisos, exceden contexto
#   - Chunks muy pequeños → pierden contexto, respuesta fragmentaria
#   - Sin overlap → se cortan ideas a la mitad
#   - Con overlap → se preserva continuidad entre fragmentos

def crear_chunks(
    texto: str,
    nombre_archivo: str,
    categoria: str,
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> List[LangChainDocument]:
    """
    Divide el texto en fragmentos con metadatos.
    
    Usa RecursiveCharacterTextSplitter que intenta dividir
    respetando la estructura natural del texto:
    primero por secciones (##), luego párrafos (\n\n),
    luego oraciones (. ), y finalmente por tamaño.
    
    Parámetros:
        chunk_size: Tamaño máximo de cada fragmento (en caracteres)
        chunk_overlap: Superposición entre fragmentos consecutivos
                       para no cortar ideas a la mitad
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", ", ", " "],
        length_function=len,
    )
    
    fragmentos = splitter.split_text(texto)
    
    # Convertir a LangChain Documents con metadatos
    # ¿POR QUÉ metadatos? Para poder filtrar búsquedas por categoría,
    # citar la fuente al usuario, y rastrear el origen de cada respuesta.
    documentos = []
    for i, fragmento in enumerate(fragmentos):
        doc = LangChainDocument(
            page_content=fragmento,
            metadata={
                "archivo": nombre_archivo,
                "categoria": categoria,
                "chunk_index": i,
                "total_chunks": len(fragmentos),
                # Hash para identificar chunks duplicados
                "chunk_hash": hashlib.md5(fragmento.encode()).hexdigest()[:8],
            }
        )
        documentos.append(doc)
    
    return documentos


# ============================================================
# 4. MOTOR RAG PRINCIPAL
# ============================================================

class MotorRAG:
    """
    Orquesta todo el pipeline RAG:
    ingesta de documentos → embeddings → vector store → consulta.
    
    Uso:
        motor = MotorRAG()
        motor.ingestar_documento("politica.pdf", "RH")
        respuesta, fuentes = motor.consultar("¿Cuántos días de vacaciones tengo?")
    """
    
    def __init__(self, modelo_embedding: str = "text-embedding-3-small"):
        """
        Inicializa el motor con los componentes del pipeline.
        
        El modelo de embedding convierte texto → vector numérico.
        'text-embedding-3-small' es el modelo de OpenAI:
        - 1536 dimensiones
        - Buen balance calidad/costo
        - Multilingüe (funciona bien en español)
        """
        self.embeddings = OpenAIEmbeddings(model=modelo_embedding)
        self.vectorstore: Optional[Chroma] = None
        self.documentos_ingestados: List[Dict] = []
        
        # LLM para generar respuestas
        # gpt-4o-mini: buen balance calidad/costo para este caso
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,  # Baja temperatura = respuestas más precisas y menos "creativas"
        )
    
    def ingestar_documento(
        self,
        ruta: str,
        categoria: str = "General",
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ) -> DocumentoProcesado:
        """
        Pipeline completo de ingesta de UN documento:
        extraer → limpiar → chunking → embeddings → vector store
        
        Retorna un objeto con información del procesamiento.
        """
        nombre = os.path.basename(ruta)
        ext = os.path.splitext(ruta)[1].lower()
        
        # Paso 1: Extracción
        texto_crudo = extraer_texto(ruta)
        
        # Paso 2: Limpieza
        texto_limpio = limpiar_texto(texto_crudo)
        
        # Paso 3: Chunking con metadatos
        chunks = crear_chunks(
            texto_limpio, nombre, categoria, chunk_size, chunk_overlap
        )
        
        # Paso 4: Embeddings + almacenamiento en vector store
        # ChromaDB genera los embeddings automáticamente usando
        # el modelo que le pasamos, y los almacena localmente.
        if self.vectorstore is None:
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                collection_name="documentos_corporativos",
            )
        else:
            self.vectorstore.add_documents(chunks)
        
        # Registro para la interfaz
        resultado = DocumentoProcesado(
            nombre_archivo=nombre,
            categoria=categoria,
            chunks=chunks,
            num_chunks=len(chunks),
            formato=ext,
        )
        self.documentos_ingestados.append({
            "archivo": nombre,
            "categoria": categoria,
            "formato": ext,
            "chunks": len(chunks),
        })
        
        return resultado
    
    def consultar(
        self,
        pregunta: str,
        categoria_filtro: Optional[str] = None,
        k: int = 5,
    ) -> Tuple[str, List[Dict]]:
        """
        Realiza una consulta RAG completa:
        1. Convierte la pregunta en embedding
        2. Busca los k chunks más similares en el vector store
        3. Inyecta esos chunks como contexto en el prompt
        4. El LLM genera una respuesta fundamentada
        
        Parámetros:
            pregunta: La pregunta del colaborador
            categoria_filtro: Si se especifica, solo busca en esa categoría
            k: Cuántos fragmentos recuperar (más = más contexto, pero más tokens)
        
        Retorna:
            (respuesta_texto, lista_de_fuentes)
        """
        if self.vectorstore is None:
            return "⚠️ No hay documentos cargados. Por favor, sube documentos primero.", []
        
        # Paso 1: Recuperación (retrieval)
        # Si hay filtro de categoría, aplicamos metadata filter
        if categoria_filtro and categoria_filtro != "Todas":
            retriever = self.vectorstore.as_retriever(
                search_kwargs={
                    "k": k,
                    "filter": {"categoria": categoria_filtro}
                }
            )
        else:
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": k}
            )
        
        documentos_recuperados = retriever.invoke(pregunta)
        
        if not documentos_recuperados:
            return (
                "🔍 No encontré información relevante en los documentos disponibles "
                "para responder tu pregunta. Intenta reformularla o verifica que "
                "los documentos relacionados estén cargados.",
                []
            )
        
        # Paso 2: Construcción del contexto
        contexto_partes = []
        fuentes = []
        for i, doc in enumerate(documentos_recuperados, 1):
            contexto_partes.append(
                f"[Fuente {i}: {doc.metadata.get('archivo', 'desconocido')} "
                f"| Categoría: {doc.metadata.get('categoria', 'N/A')} "
                f"| Fragmento {doc.metadata.get('chunk_index', '?')}]\n"
                f"{doc.page_content}"
            )
            fuentes.append({
                "archivo": doc.metadata.get("archivo", "desconocido"),
                "categoria": doc.metadata.get("categoria", "N/A"),
                "fragmento": doc.metadata.get("chunk_index", "?"),
                "contenido_preview": doc.page_content[:200] + "...",
            })
        
        contexto = "\n\n---\n\n".join(contexto_partes)
        
        # Paso 3: Prompt al LLM
        # Este prompt es crítico: define el comportamiento del agente.
        system_prompt = """Eres un asistente corporativo de recursos internos. 
Tu función es responder preguntas de los colaboradores basándote EXCLUSIVAMENTE 
en los documentos proporcionados como contexto.

REGLAS ESTRICTAS:
1. Responde SOLO con información presente en los documentos del contexto.
2. Si la información no está en los documentos, di claramente: 
   "No encontré esa información en los documentos disponibles."
3. NUNCA inventes información, cifras, fechas o políticas.
4. Cita las fuentes al final de tu respuesta indicando el nombre del archivo.
5. Si la pregunta es ambigua, pide aclaración antes de responder.
6. Responde en el mismo idioma en que te pregunten.
7. Sé claro, conciso y profesional.

FORMATO DE RESPUESTA:
- Responde la pregunta de forma directa
- Si es relevante, usa listas o pasos numerados
- Al final, incluye una sección "📎 Fuentes consultadas" con los archivos usados"""

        human_prompt = f"""DOCUMENTOS DE CONTEXTO:
{contexto}

---

PREGUNTA DEL COLABORADOR: {pregunta}

Responde basándote exclusivamente en los documentos de contexto proporcionados."""

        # Paso 4: Generación de respuesta
        respuesta = self.llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt},
        ])
        
        return respuesta.content, fuentes
    
    def obtener_categorias(self) -> List[str]:
        """Retorna las categorías de los documentos ingestados."""
        categorias = set()
        for doc in self.documentos_ingestados:
            categorias.add(doc["categoria"])
        return sorted(categorias)
    
    def obtener_resumen(self) -> List[Dict]:
        """Retorna un resumen de los documentos ingestados."""
        return self.documentos_ingestados