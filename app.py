import os
# import subprocess # Removed subprocess
from flask import Flask, request, jsonify, render_template
# from werkzeug.utils import secure_filename # Removed secure_filename
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferMemory

# --- Configuration ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

# Adjust relative path assuming app.py is in the project root
PERSIST_DIRECTORY = "data/vector_store" 
if not os.path.exists(PERSIST_DIRECTORY):
     raise FileNotFoundError(f"Vector store directory not found at {os.path.abspath(PERSIST_DIRECTORY)}. Did you run the indexer script?")

MODEL_NAME = "gemini-1.5-flash-latest" # Or another Gemini model like "gemini-pro"
EMBEDDING_MODEL_NAME = "models/embedding-001" # Should match the one used in indexer.py
# UPLOAD_FOLDER = 'data/downloaded_files' # Removed upload folder config
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'md', 'docx'} # Removed allowed extensions

# --- Initialization ---
print("Initializing Flask app...")
app = Flask(__name__)

print("Initializing Embeddings Model...")
embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL_NAME, google_api_key=GOOGLE_API_KEY)
print("Embeddings Model Initialized.")

print(f"Loading Vector Store from: {os.path.abspath(PERSIST_DIRECTORY)}...")
vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
print("Vector Store Loaded.")

# Create retriever
retriever = vector_store.as_retriever(search_kwargs={'k': 5}) # Retrieve top 5 relevant chunks
print("Retriever created.")

print(f"Initializing LLM ({MODEL_NAME})...")
llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=GOOGLE_API_KEY, temperature=0.3)
print("LLM Initialized.")

# --- Memory Initialization ---
# Use a simple in-memory store. This will be lost on server restart.
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history", output_key='answer')
print("Memory initialized.")

# --- RAG Chain Definition ---

# Updated prompt to include chat history
RAG_PROMPT_TEMPLATE = """\
Eres un asistente para tareas de preguntas y respuestas. Usa las siguientes piezas de contexto recuperado para responder la pregunta. Si no sabes la respuesta, simplemente di que no lo sabes. Usa un máximo de tres oraciones y mantén la respuesta concisa.
Piensa paso a paso basándote SOLO en el contexto proporcionado y el historial de chat para responder la pregunta. Después de tu razonamiento, proporciona la respuesta final.

CONTEXTO:
{context}

HISTORIAL DE CHAT:
{chat_history}

PREGUNTA:
{question}

Respuesta final:
"""

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", RAG_PROMPT_TEMPLATE), # Keep the main instructions as system message
    MessagesPlaceholder(variable_name="chat_history"), # Placeholder for memory messages
    ("human", "{question}") # User's current question
])

def format_docs(docs):
    """Helper function to format retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

# Define function to load memory variables for the chain
# It needs to return a dict with keys matching the prompt input variables
def load_memory_variables(_): # Takes dummy input
    return memory.load_memory_variables({})["chat_history"] # Extract the history list

# Updated LangChain Expression Language (LCEL) chain with memory
rag_chain = (
    RunnablePassthrough.assign(
        context=(lambda x: x["question"]) | retriever | format_docs,
        # chat_history=RunnableLambda(memory.load_memory_variables) | itemgetter("chat_history") # Load history
        chat_history=RunnableLambda(load_memory_variables) # Load history using the helper function
    )
    | rag_prompt
    # Add a step to print the prompt before sending it to the LLM
    | RunnableLambda(lambda x: print(f"\n--- Prompt to LLM Start ---\n{x}\n--- Prompt to LLM End ---\n") or x)
    | llm
    | StrOutputParser()
)

# Create a new chain specifically for handling input/output and saving memory
# This structure helps manage the flow cleanly
# rag_chain_with_memory = RunnablePassthrough.assign(chat_history=RunnableLambda(load_memory_variables))
#    | rag_chain # Invoke the main RAG chain

# print("RAG Chain with Memory created.") # Commented out as the specific chain isn't used
print("RAG Chain definition completed.") # Adjusted print message

# --- Web Interface Route ---
@app.route('/')
def index():
    """Serves the main HTML interface."""
    return render_template('index.html')

# --- API Endpoint ---
@app.route('/ask', methods=['POST'])
def ask_question():
    """Receives a question, processes it through the RAG chain (with memory), and returns the answer."""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Missing 'question' in JSON payload"}), 400

    print(f"Received question: {question}")
    try:
        print("Invoking RAG chain with memory...")
        
        # Prepare inputs for the chain that expects memory loading
        inputs = {"question": question}
        # The RunnableLambda takes care of loading the history inside the chain
        
        answer = rag_chain.invoke(inputs) # Invoke the main chain
        
        # Save context to memory *after* invocation
        # Note: We manually save. More complex chains might handle this.
        memory.save_context(inputs, {"answer": answer})
        print("Saved interaction to memory.")
        
        print(f"Generated answer: {answer}")
        # Return only the answer, history is managed server-side
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error during RAG chain invocation: {e}")
        # Consider more specific error handling/logging
        return jsonify({"error": "Failed to process question"}), 500

# --- Main Execution ---
if __name__ == '__main__':
    print("Starting Flask server...")
    # Use host='0.0.0.0' to make it accessible on your network if needed
    app.run(debug=True, host='127.0.0.1', port=5000) 