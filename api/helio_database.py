from heliosrag.api.helio_config import settings
from heliosrag.api.interfaces.helio_database import DocumentStore
from heliosrag.helio_paths import VECTORSTORE_DIR

# ---------------------------- Load Database --------------------------- #

# Lazy load database to avoid startup issues
DATABASE = None


def get_database():
    """Lazy-load the database when needed."""
    global DATABASE
    if DATABASE is None:
        DATABASE = DocumentStore(
            model_name=settings.embedding_model,
            persist_directory=str(VECTORSTORE_DIR),  # Use the populated vectorstore
            device=settings.embedding_model_device
        )
        print(f"📊 Loaded vector database with {len(DATABASE.vector_store.get()['ids'])} documents")
    return DATABASE
