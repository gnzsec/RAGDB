Quiero crear una solución que me permita consultar archivos que subo a Google Drive como si fueran una base de conocimientos inteligente.

Diseñá un sistema donde:

1. El usuario sube documentos (PDF, DOCX, TXT, MD) a una carpeta específica en Google Drive.
2. Un script o servicio detecta automáticamente nuevos archivos, los descarga y los procesa.
3. Los archivos se convierten en texto, se segmentan y se transforman en vectores usando embeddings (OpenAI, Gemini o Cohere).
4. Estos vectores se almacenan en una base vectorial (ej: FAISS, ChromaDB o Weaviate).
5. El sistema ofrece una API o interfaz web para que el usuario pueda hacer preguntas.
6. Al recibir una pregunta, la IA:
   - Recupera los fragmentos más relevantes desde el vector store
   - Usa un modelo LLM (ej: GPT-4 o Gemini) para generar una respuesta **sólo basada en esos documentos**
   - Mantiene el contexto conversacional si se desea

Incluir:
- Código Python para la indexación automática desde Google Drive usando la API.
- Uso de LangChain o LlamaIndex para la gestión de documentos, embeddings y consultas.
- Ejemplo de interfaz simple (CLI o Flask API) para enviar preguntas y recibir respuestas.
- Prompt base para el modelo LLM que restrinja las respuestas solo al contenido de los documentos.
- Buenas prácticas para mantener la precisión y actualizar la base de conocimientos con nuevos archivos.

El resultado debe ser funcional y extensible. Idealmente, usará Gemini como backend para las respuestas contextuales, pero debe ser fácilmente adaptable.
