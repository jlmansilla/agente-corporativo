# Corpus demostrativo RAG - NexusFlow Technologies

Este paquete contiene documentación **ficticia y consistente** de una plataforma SaaS de gestión de proyectos.

## Archivos

1. `01_Base_Conocimiento_NexusFlow.pdf` - producto, operaciones, seguridad, facturación y soporte.
2. `02_FAQ_Soporte_NexusFlow.docx` - preguntas y respuestas de soporte.
3. `03_Planes_Precios_NexusFlow.xlsx` - planes, límites, funciones y metadatos RAG.
4. `04_Overview_Operaciones_NexusFlow.pptx` - visión ejecutiva de producto y operaciones.
5. `05_Terminos_Uso_NexusFlow.md` - términos de uso ficticios.
6. `06_Intenciones_Soporte_NexusFlow.csv` - dataset de intenciones para recuperación/evaluación.
7. `07_Corpus_RAG_NexusFlow.json` - chunks normalizados y referencias cruzadas.
8. `08_Politica_Privacidad_NexusFlow.html` - política de privacidad ficticia.

## Reglas de coherencia

- Planes: Free, Team, Business y Enterprise.
- Precios fuente de verdad: archivo XLSX / chunks `PRICE-*`.
- Identificadores: `KB-*`, `FAQ-*`, `PRICE-*`, `PRIV-*`, `TERMS-*`.
- Idioma: `es-CL`; moneda: USD.
- Fecha de vigencia: `2026-07-21`; versión: `1.0`.

## Ingestión sugerida

- Extraer por encabezados y conservar `chunk_id`.
- Añadir filtros por `document_type`, `locale`, `version` y `effective_date`.
- Combinar búsqueda semántica y léxica para IDs, planes y términos exactos.
- Obligar al generador a citar `chunk_id` y abstenerse si no encuentra evidencia.
- Evaluar con preguntas de producto, soporte, precio, privacidad y conflictos entre documentos.

> Todo el contenido es sintético. Los textos legales requieren revisión profesional antes de uso real.
