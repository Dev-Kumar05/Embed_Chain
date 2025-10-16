# HelioRAG Knowledge Extraction System

A flexible and scalable Retrieval-Augmented Generation (RAG) system that allows users to upload documents (PDF, DOCX, TXT, MD) and ask questions about their content. HelioRAG uses advanced techniques like query expansion and vector search to provide accurate, context-aware answers powered by Google Gemini.



## Demo Video

https://drive.google.com/file/d/1UAsYdj2DBoHzZfwkCI5b7BCF9tgvmcFW/view?usp=sharing

> *Note:* The video demonstrates the complete workflow of the RAG system in action.





## Overview

This repository contains a complete RAG-based question-answering system with:

- **Document Upload & Processing**: Upload any PDF/DOCX/TXT/MD document
- **Intelligent Chunking**: Automatic text splitting and embedding generation
- **Vector Search**: Semantic search using ChromaDB and HuggingFace embeddings
- **Query Expansion**: Enhanced retrieval through paraphrasing
- **AI-Powered Answers**: Response generation using Google Gemini
- **Personal Knowledge Bases**: Each user gets their own isolated document store
- **RESTful API**: Built with FastAPI for easy integration
- **User-Friendly GUI**: Interactive Gradio interface

<p align="center">
   <img src="./resources/static/system_architecture.png" alt="System Architecture Diagram" width="600" />
</p>

### Technology Stack

- **API Framework**: [FastAPI](https://fastapi.tiangolo.com/) - High-performance REST API
- **User Interface**: [Gradio](https://gradio.app/) - Interactive web interface
- **RAG Framework**: [LangChain](https://langchain.com/) - RAG pipeline orchestration
- **LLM**: Google Gemini - AI-powered answer generation
- **Embeddings**: HuggingFace Transformers - Semantic document encoding
- **Vector Store**: ChromaDB - Efficient similarity search


## User Flow

1. **Upload Document**: User uploads a PDF/DOCX/TXT/MD file via GUI or API
2. **Document Processing**: System extracts text and splits into chunks
3. **Vector Storage**: Chunks are embedded and stored in user's personal vector database
4. **Ask Questions**: User submits questions about their uploaded documents
5. **RAG Retrieval**: System retrieves relevant chunks using semantic search
6. **AI Response**: Google Gemini generates accurate answers based on retrieved context
7. **Get Answer**: User receives a well-formatted, context-aware response


## Screenshots

### User Interface
![User Interface](./resources/static/screenshot_gui.png)

### API Endpoints
![API Endpoints](./resources/static/screenshot_api.png)


## Installation

This setup assumes that Python 3.10+ is installed. If not, you can use [pyenv](https://github.com/pyenv/pyenv#installation) to manage your Python versions.

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Dev-Kumar05/Embed_Chain.git
   cd RAG-based-Knowledge-Extraction-Challenge
   ```

2. **Install Poetry for dependency management**:
   ```bash
   pip install poetry
   ```

3. **Install project dependencies**:
   ```bash
   poetry install
   ```

4. **Configure API Keys**:
   - Rename `.env-template` to `.env`
   - Add your Google Gemini API key:
     ```env
     GOOGLE_API_KEY=your_gemini_api_key_here
     ```
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

5. **Optional - Set up HuggingFace credentials** (for embedding models):
   ```bash
   huggingface-cli login
   ```
   Get your token from [Hugging Face account settings](https://huggingface.co/settings/tokens)

## Usage

### Start Backend

To start the REST API, run:

```bash
python src/heliosrag/helio_main.py
```

The server will start on port 8082. Access the API documentation at: [http://localhost:8082/docs](http://localhost:8082/docs)

#### Key API Endpoints

- `POST /documents/upload` - Upload a document (PDF/DOCX/TXT/MD)
- `GET /documents/list/{user_id}` - List all uploaded documents
- `POST /generate-answer` - Ask questions about uploaded documents
- `DELETE /documents/{user_id}/{document_name}` - Delete a document

### Start Frontend

To start the user interface:

```bash
python src/heliosrag/gui/helio_enhanced_main.py
```

The GUI will be available at: [http://localhost:7860/](http://localhost:7860/)


## System Architecture

### Document Processing Pipeline

#### Phase 1: Document Upload & Text Extraction

1. User uploads a document (PDF, DOCX, TXT, or MD)
2. System extracts raw text from the document
3. Text is validated for content

#### Phase 2: Chunking & Embedding

1. Documents are split into manageable chunks (1000 chars with 200 char overlap)
2. Metadata is attached (filename, chunk_id, document_type)
3. Each chunk is converted to embeddings using HuggingFace models
4. Chunks are stored in user's personal ChromaDB vector store

#### Phase 3: Question Answering

1. User submits a question
2. Question is expanded/paraphrased for better retrieval
3. Similar chunks are retrieved from vector store using semantic search
4. Retrieved context is sent to Google Gemini
5. Gemini generates a comprehensive answer based on the context
6. Response is returned to the user

### Key Features

- **No Hardcoding**: System works with ANY document type - no domain-specific assumptions
- **Personal Knowledge Bases**: Each user gets isolated storage via unique user_id
- **Combined Search**: Option to search both personal and default knowledge bases
- **Intelligent Retrieval**: Query expansion improves search accuracy
- **Context-Aware**: Gemini only answers based on provided document context

#### Example of a Processed Document

The final document is augmented with the original section title and hypothetical questions:

```
Page title: Initializing A Repository In An Existing Directory
Filename: git tutorial

Related Questions:
- 1. If I have a directory that is not currently being version controlled with Git, what command do I type to start controlling it with Git? (Answer: $ git init)
- 2. Where in the file system should I navigate to in order to type the command to start controlling my project directory with Git? (Answer: To the project directory)
- 3. How do the directions for navigating to the project directory differ depending on the operating system? (Answer:

Page Content:
If you have a project directory that is currently not under version control and you want to start controlling it with Git, you first need to go to that project's directory. If you've never done this, it looks a little different depending on which system you're running: for Linux:
$ cd /home/user/my_project for macOS:
$ cd /Users/user/my_project for Windows:
$ cd C:/Users/user/my_project and type:
$ git init This creates a new subdirectory named .git that contains all of your necessary repository files - a Git repository skeleton. At this point, nothing in your project is tracked yet. See Git Internals for 26 more information about exactly what files are contained in the .git directory you just created.

If you want to start version-controlling existing files (as opposed to an empty directory), you should probably begin tracking those files and do an initial commit. You can accomplish that with a few git add commands that specify the files you want to track, followed by a git commit:
$ git add *.c
```

### Retrieval and Question-Answering Process

![Question Answering Pipeline](./resources/static/question-answering-pipeline.png)


1. The user enters a query
2. To perform **Query Expansion**, we ask a model to paraphrase the original query, generating three alternative queries. The intuition is that the model can generate queries focusing on different aspects of the input prompt
3. For each paraphrased query, as well as the original one, we retrieve *k* documents from the vector store
4. The context and the original query are combined in a question answering prompt
5. Finally, a large language model (LLM) is asked to use the combined context to answer the original query

#### Example for Generated Hypothetical Questions

```
Document: Conda is an open-source package management system and environment management system that runs on Windows, macOS, and Linux. Conda quickly installs, runs, and updates packages and their dependencies.


Generated Hypothetical Questions:
1. How does Conda differ from other package management systems in terms of installation and updating procedures?
2. Can you describe the cross-platform compatibility of Conda, and how does it affect its usability for developers working on different operating systems?
3. How does Conda ensure that the dependencies of a package are also installed and updated alongside it, and what impact does this have on the overall package management experience?
```

## Further Thoughts on System Design and Scalability

To enhance scalability in the current system, I recommend the following architectural changes based on best practices for designing scalable systems:

- **Microservices Architecture**: Transitioning to a microservices approach by decoupling services based on their specific concerns will allow for more efficient scaling and faster deployment of new features. This will also enable independent scaling of each service, with a load balancer to distribute traffic across service instances, improving overall system performance under high load.

- **Vendor-Agnostic Abstraction Layer**: Introducing a common interface through wrapper classes for LLM and database vendors will decouple the system from specific vendors. This not only provides flexibility in switching vendors without significant refactoring but also allows scaling across multiple providers to meet demand more effectively.

- **Controller/Worker Scaling Model**: Implementing a controller/worker architecture will provide dynamic vertical scaling capabilities. Each LLM worker instance would handle a specific model, and the controller could dynamically assign additional worker instances as needed. This ensures efficient resource allocation, whether adding workers for different models or increasing capacity to handle surges in demand for existing models.


!["Pipeline"](./resources/static/scaleable_system_architecture.png)


# Embed_Chain
