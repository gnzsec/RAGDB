import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain.vectorstores import Chroma  # Deprecated import
from langchain_chroma import Chroma # Updated import
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader
)

# --- Configuration ---
load_dotenv()  # Load environment variables from .env file
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

SOURCE_DIRECTORY = "../data/downloaded_files"  # Directory with downloaded files
PERSIST_DIRECTORY = "../data/vector_store"   # Directory to store ChromaDB
CHUNK_SIZE = 1000  # Size of text chunks
CHUNK_OVERLAP = 100 # Overlap between chunks

# --- Initialization ---
def get_embeddings_model():
    """Initializes and returns the Google Generative AI Embeddings model."""
    print("Initializing Embeddings Model...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # Or "models/text-embedding-004"
    print("Embeddings Model Initialized.")
    return embeddings

def get_vector_store(embeddings):
    """Initializes and returns the Chroma vector store."""
    print(f"Initializing Vector Store (persisting to: {os.path.abspath(PERSIST_DIRECTORY)})...")
    vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    print("Vector Store Initialized.")
    return vector_store

# --- Document Loading and Processing (To be implemented) ---
def load_documents(directory_path):
    """Loads documents from the specified directory using appropriate loaders."""
    # Define loaders for different file types
    loaders = {
        ".pdf": PyPDFLoader,
        ".docx": UnstructuredWordDocumentLoader,
        ".txt": TextLoader,
        ".md": UnstructuredMarkdownLoader
    }
    # Use DirectoryLoader with custom loaders based on file extension
    # Note: This requires careful handling of how DirectoryLoader uses globs and loaders
    # A simpler approach might be to load all known types explicitly
    print(f"Loading documents from: {os.path.abspath(directory_path)}")
    
    # Example using specific loaders (more robust)
    all_docs = []
    for ext, loader_cls in loaders.items():
        try:
            print(f"\tLoading files with extension: *{ext}")
            loader = DirectoryLoader(directory_path, glob=f"**/*{ext}", loader_cls=loader_cls, 
                                     show_progress=True, use_multithreading=True, silent_errors=True)
            docs = loader.load()
            if docs:
                print(f"\tLoaded {len(docs)} {ext} document(s).")
                all_docs.extend(docs)
            else:
                 print(f"\tNo {ext} documents found or loaded.")
        except Exception as e:
            print(f"\tError loading {ext} files: {e}")
            continue # Continue with other file types

    if not all_docs:
        print("No documents were loaded successfully.")
        return []
        
    print(f"Total documents loaded: {len(all_docs)}")
    # print(f"First document content preview: {all_docs[0].page_content[:200]}...") # Optional preview
    return all_docs

def split_documents(documents):
    """Splits the loaded documents into chunks."""
    if not documents:
        print("No documents to split.")
        return []
    print(f"Splitting {len(documents)} documents into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    split_docs = text_splitter.split_documents(documents)
    print(f"Created {len(split_docs)} document chunks.")
    # print(f"First chunk preview: {split_docs[0].page_content[:200]}...") # Optional preview
    return split_docs

# --- Indexing Function (To be implemented) ---
def index_documents(documents, vector_store):
    """Adds document chunks to the vector store."""
    if not documents:
        print("No document chunks to index.")
        return
    print(f"Adding {len(documents)} document chunks to the vector store...")
    vector_store.add_documents(documents)
    # Chroma persists automatically when initialized with persist_directory
    # If using an in-memory version, you might need: vector_store.persist()
    print("Documents added to vector store.")

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Starting Indexing Process ---")
    embeddings_model = get_embeddings_model()
    vector_db = get_vector_store(embeddings_model) # Initialize Chroma first
    
    # 1. Load Documents
    loaded_docs = load_documents(SOURCE_DIRECTORY)
    
    if loaded_docs:
        # 2. Split Documents
        doc_chunks = split_documents(loaded_docs)
        
        if doc_chunks:
            # 3. Index Documents
            # Consider clearing the store if you want a fresh index each time
            # vector_db.delete_collection() # Use with caution!
            # vector_db = get_vector_store(embeddings_model) # Re-initialize after delete
            index_documents(doc_chunks, vector_db)
            print("--- Indexing Process Completed ---")
        else:
             print("--- Indexing Process Stopped: No chunks created ---")
    else:
        print("--- Indexing Process Stopped: No documents loaded ---") 