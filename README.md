# RAGDB - Asistente Inteligente de Bases de Datos

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.24-orange.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.0.7-purple.svg)

RAGDB es un asistente inteligente que utiliza técnicas de RAG (Retrieval Augmented Generation) para responder preguntas sobre cualquier tema basado en los documentos que le proporciones. Puedes cargar archivos en diferentes formatos (PDF, DOCX, TXT, MD) y el asistente aprenderá de su contenido para responder tus preguntas de manera precisa y contextualizada.

## 🚀 Características

- Interfaz web amigable
- Respuestas en español
- Memoria de conversación
- Búsqueda semántica en documentos
- Integración con Google Gemini
- Soporte para múltiples formatos de documentos (PDF, DOCX, TXT, MD)
- Carga de documentos para aprendizaje
- Próximamente: Integración con Google Drive para acceder a documentos directamente

## 📋 Requisitos Previos

- Python 3.13 o superior
- Cuenta de Google Cloud con API Key para Gemini
- Git

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/gnzsec/RAGDB.git
cd RAGDB
```

2. Crea y activa un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita el archivo .env con tu API Key de Google
```

## 🎮 Uso

1. Carga tus documentos en la carpeta `data/downloaded_files`

2. Ejecuta el script indexador para procesar los documentos:
```bash
python scripts/indexer.py
```

3. Inicia el servidor:
```bash
python app.py
```

4. Abre tu navegador en `http://127.0.0.1:5000`

5. ¡Comienza a hacer preguntas sobre el contenido de tus documentos!

## 📚 Documentación

El proyecto incluye documentación sobre:
- Configuración de la API de Google
- Estructura del proyecto
- Formato de los documentos soportados
- Personalización de respuestas
- Próximas características (Integración con Google Drive)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, lee las [guías de contribución](CONTRIBUTING.md) antes de enviar un pull request.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

- **Fidel Acevedo** - [gnzsec](https://github.com/gnzsec)

## 🙏 Agradecimientos

- Equipo de LangChain por su increíble framework
- Google por su API de Gemini
- Comunidad de código abierto
