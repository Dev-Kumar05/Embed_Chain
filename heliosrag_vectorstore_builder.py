"""Vector Store Creation Script for bundled resources."""

import os
import sys
from pathlib import Path


# Ensure the top-level src directory is importable for package resolution
PROJECT_SRC = Path(__file__).resolve().parents[1]
if str(PROJECT_SRC) not in sys.path:
    sys.path.append(str(PROJECT_SRC))


from langchain_community.vectorstores import Chroma  # noqa: E402
from langchain_huggingface import HuggingFaceEmbeddings  # noqa: E402
from langchain.text_splitter import RecursiveCharacterTextSplitter  # noqa: E402
from langchain.schema import Document  # noqa: E402
from heliosrag.api.helio_config import settings  # noqa: E402
from heliosrag.helio_paths import RAW_DOCS_DIR, VECTORSTORE_DIR  # noqa: E402


def create_vector_store() -> bool:
    """Create and populate vector store from raw documents."""
    print("🚀 Creating Vector Store...")

    try:
        # Initialize embeddings
        print("📊 Loading embeddings model...")
        embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={"device": settings.embedding_model_device},
        )
        print("✅ Embeddings loaded successfully")

        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

        # Load documents from raw directory
        raw_dir = RAW_DOCS_DIR
        raw_dir.mkdir(parents=True, exist_ok=True)
        documents = []

        for file_path in raw_dir.glob("*.md"):
            print(f"📖 Processing {file_path.name}...")

            # Read file content
            with file_path.open("r", encoding="utf-8") as file_handle:
                content = file_handle.read()

            # Split into chunks
            chunks = text_splitter.split_text(content)

            # Create documents
            for chunk_index, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": file_path.name,
                        "chunk": chunk_index,
                        "total_chunks": len(chunks),
                    },
                )
                documents.append(doc)

            print(f"  ✅ Created {len(chunks)} chunks from {file_path.name}")

        print(f"\n📚 Total documents created: {len(documents)}")

        # Create vector store
        print("🔧 Creating vector store...")
        vectorstore_path = VECTORSTORE_DIR
        vectorstore_path.mkdir(parents=True, exist_ok=True)

        # Remove existing vectorstore if it exists
        if any(vectorstore_path.iterdir()):
            import shutil

            shutil.rmtree(vectorstore_path)
            vectorstore_path.mkdir(parents=True, exist_ok=True)
            print("🗑️  Removed existing vector store")

        # Create new vectorstore
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=str(vectorstore_path),
        )

        print("✅ Vector store created and populated!")

        # Test the vector store
        print("\n🔍 Testing vector store...")
        test_query = "How to initialize git repository?"
        search_results = vectorstore.similarity_search(test_query, k=3)

        print(f"📋 Search Results for: '{test_query}'")
        for index, doc in enumerate(search_results, 1):
            print(f"  {index}. {doc.page_content[:100]}...")
            print(f"     Source: {doc.metadata.get('source', 'Unknown')}")

        return True

    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Error creating vector store: {exc}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    SUCCESS = create_vector_store()
    if SUCCESS:
        print("\n🎉 Vector store created successfully!")
    else:
        print("\n❌ Failed to create vector store!")