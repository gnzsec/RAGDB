# RAGDB - Asistente Inteligente de Bases de Datos

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0-green.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.24-orange.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.0.7-purple.svg)

RAGDB es un asistente inteligente que utiliza técnicas de RAG (Retrieval Augmented Generation) para responder preguntas sobre bases de datos. Combina la potencia de los modelos de lenguaje de Google con una base de conocimiento especializada en bases de datos.

## 🚀 Características

- Interfaz web amigable
- Respuestas en español
- Memoria de conversación
- Búsqueda semántica en documentos
- Integración con Google Gemini
- Soporte para múltiples formatos de documentos

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

1. Inicia el servidor:
```bash
python app.py
```

2. Abre tu navegador en `http://127.0.0.1:5000`

3. ¡Comienza a hacer preguntas sobre bases de datos!

## 📚 Documentación

El proyecto incluye documentación sobre:
- Configuración de la API de Google
- Estructura del proyecto
- Formato de los documentos de conocimiento
- Personalización de respuestas

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
