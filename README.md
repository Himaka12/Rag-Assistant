# Simple RAG Assistant

A simple terminal-based **Retrieval-Augmented Generation (RAG) Assistant** built with Python.

This project uses:

* **BAAI/bge-m3** from Hugging Face for embeddings
* **ChromaDB** as the vector database
* **Groq API** for the Large Language Model
* **PyPDF** for PDF text extraction
* **Python terminal** for user queries

The system allows users to add PDF or TXT documents, convert them into embeddings, store them in a vector database, and ask questions based on the uploaded documents.

---

## Project Overview

The RAG assistant contains two main pipelines:

1. **Ingestion Pipeline**
2. **Retrieval Pipeline**

The ingestion pipeline processes documents and stores their embeddings.

The retrieval pipeline accepts a user question, retrieves the most relevant document chunks, and sends them to the Groq LLM to generate an answer.

---

## RAG Architecture

```text
                INGESTION PIPELINE

PDF / TXT Documents
        |
        v
Extract Text
        |
        v
Clean Text
        |
        v
Split Into Chunks
        |
        v
BAAI/bge-m3
        |
        v
Create Embeddings
        |
        v
ChromaDB


                RETRIEVAL PIPELINE

User Question
        |
        v
BAAI/bge-m3
        |
        v
Question Embedding
        |
        v
Search ChromaDB
        |
        v
Retrieve Top Relevant Chunks
        |
        v
Question + Retrieved Context
        |
        v
Groq LLM
        |
        v
Generated Answer
        |
        v
Terminal
```

---

## Technologies Used

| Technology            | Purpose                                |
| --------------------- | -------------------------------------- |
| Python                | Main programming language              |
| Hugging Face          | Provides the BGE-M3 embedding model    |
| BAAI/bge-m3           | Converts text into embeddings          |
| Sentence Transformers | Loads and runs the embedding model     |
| ChromaDB              | Stores and retrieves vector embeddings |
| Groq API              | Provides the LLM for answer generation |
| openai/gpt-oss-20b    | LLM used through Groq                  |
| PyPDF                 | Extracts text from PDF files           |
| python-dotenv         | Loads API keys from the `.env` file    |

---

## Project Structure

```text
Rag-Assistant/
│
├── data/
│   └── warranty_guidelines.txt
│
├── chroma_db/
│   └── ...
│
├── .env
├── .gitignore
├── requirements.txt
├── ingest.py
├── chat.py
└── README.md
```

### File Description

#### `data/`

Contains the documents used by the RAG assistant.

Supported document types:

```text
.pdf
.txt
```

Example:

```text
data/warranty_guidelines.txt
```

---

#### `ingest.py`

Handles the ingestion pipeline.

It performs the following steps:

```text
Load Documents
      ↓
Extract Text
      ↓
Clean Text
      ↓
Split Text Into Chunks
      ↓
Generate BGE-M3 Embeddings
      ↓
Store Embeddings in ChromaDB
```

---

#### `chat.py`

Handles the retrieval and generation pipeline.

It performs:

```text
Accept User Question
      ↓
Generate Question Embedding
      ↓
Search ChromaDB
      ↓
Retrieve Relevant Chunks
      ↓
Create Context
      ↓
Send Context + Question to Groq
      ↓
Generate Answer
```

---

#### `chroma_db/`

Stores the vector embeddings created during the ingestion process.

This folder is automatically generated after running:

```bash
python ingest.py
```

---

#### `.env`

Stores the Groq API key.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Do not upload your `.env` file to GitHub.

---

## Requirements

Make sure Python is installed.

Recommended:

```text
Python 3.10+
```

Check your Python version:

```bash
python --version
```

---

## Installation

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

Move into the project directory:

```bash
cd Rag-Assistant
```

---

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should look similar to:

```text
(.venv) PS C:\Projects\Rag-Assistant>
```

---

### 3. Install Required Libraries

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## Required Libraries

The project uses the following libraries:

```text
torch
sentence-transformers
chromadb
pypdf
groq
python-dotenv
```

Example `requirements.txt`:

```txt
torch
sentence-transformers
chromadb
pypdf
groq
python-dotenv
```

---

## Groq API Setup

Create a file called:

```text
.env
```

Inside the project directory.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Example:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
```

Never upload your actual API key to GitHub.

---

## `.gitignore`

Recommended `.gitignore`:

```gitignore
.venv/
venv/
.env
chroma_db/
__pycache__/
*.pyc
```

---

## Add Documents

Place your documents inside the:

```text
data/
```

folder.

Example:

```text
data/
├── warranty_guidelines.txt
├── company_policy.pdf
└── product_information.txt
```

---

## Run the Ingestion Pipeline

Run:

```bash
python ingest.py
```

The program will:

1. Load the documents
2. Extract text
3. Clean the text
4. Split text into chunks
5. Load the BGE-M3 embedding model
6. Generate embeddings
7. Store embeddings in ChromaDB

Example output:

```text
Loading BGE-M3 embedding model...

Embedding model loaded.

Connecting to ChromaDB...

Reading: warranty_guidelines.txt

Creating embeddings for 10 chunks...

Saving embeddings to ChromaDB...

--------------------------------
Ingestion completed successfully!
--------------------------------
```

The first execution may take longer because the BGE-M3 model needs to be downloaded.

After downloading, the model is normally cached locally.

---

## Run the RAG Assistant

After ingestion is completed, run:

```bash
python chat.py
```

Example:

```text
====================================
       SIMPLE RAG ASSISTANT
====================================

Type 'exit' to stop.

You:
```

Enter a question:

```text
You: What is the warranty period?
```

Example response:

```text
Assistant:
All company products come with a 12-month warranty starting from the date of purchase.

Sources used:
1. warranty_guidelines.txt - Page 1
```

---

## Example Questions

If you are using the sample warranty guideline document, you can ask:

```text
What is the warranty period?
```

```text
What damages are not covered by warranty?
```

```text
How can I make a warranty claim?
```

```text
How long does the warranty inspection take?
```

```text
Can I claim warranty without a receipt?
```

```text
What are the support hours?
```

```text
What happens if my warranty claim is approved?
```

---

## Ingestion Pipeline Explanation

The ingestion pipeline prepares documents so that they can later be searched efficiently.

### Step 1 - Document Loading

The application reads documents from:

```text
data/
```

PDF files are processed using PyPDF.

TXT files are read directly using Python.

---

### Step 2 - Text Cleaning

Extracted text is cleaned by removing unnecessary spaces and line breaks.

Example:

```text
Students     must maintain
80% attendance.
```

Becomes:

```text
Students must maintain 80% attendance.
```

---

### Step 3 - Chunking

Large documents are divided into smaller sections called chunks.

Example:

```text
Document
   ↓
Chunk 1
Chunk 2
Chunk 3
Chunk 4
```

Chunking allows the RAG system to retrieve only relevant information instead of sending the complete document to the LLM.

---

### Step 4 - Embedding Generation

Each chunk is converted into an embedding using:

```text
BAAI/bge-m3
```

An embedding is a numerical representation of text.

Example:

```text
"Warranty period is 12 months"
```

is converted internally into something similar to:

```text
[0.14, -0.32, 0.75, 0.08, ...]
```

---

### Step 5 - Vector Storage

The generated embeddings are stored in:

```text
ChromaDB
```

The system also stores metadata such as:

```text
Source File
Page Number
Chunk Number
```

---

## Retrieval Pipeline Explanation

The retrieval pipeline starts when the user asks a question.

### Step 1 - User Question

Example:

```text
What are the support hours?
```

---

### Step 2 - Question Embedding

The question is converted into an embedding using the same BGE-M3 model.

---

### Step 3 - Vector Search

The question embedding is compared with the stored document embeddings.

ChromaDB finds the most similar chunks.

Example:

```text
Customer Support

Monday to Friday
9:00 AM to 5:00 PM
```

---

### Step 4 - Context Creation

The retrieved chunks are combined into a context.

Example:

```text
Context:

Customers can contact the support team for warranty assistance.

Support Hours:
Monday to Friday
9:00 AM to 5:00 PM
```

---

### Step 5 - LLM Generation

The context and user question are sent to Groq.

The current model used in this project is:

```text
openai/gpt-oss-20b
```

The LLM then generates the final answer.

Example:

```text
The customer support team is available Monday to Friday from 9:00 AM to 5:00 PM.
```

---

## Why Use RAG?

A normal LLM mainly answers using information learned during its training.

A RAG system allows the LLM to answer questions using custom documents.

Example:

```text
Normal LLM
User Question
     ↓
LLM
     ↓
Answer
```

RAG:

```text
User Question
     ↓
Search Your Documents
     ↓
Retrieve Relevant Information
     ↓
Send Information to LLM
     ↓
Answer
```

This makes RAG useful for systems such as:

* Company policy assistants
* Warranty assistants
* University handbook assistants
* Customer support assistants
* Product documentation assistants
* Internal knowledge assistants
* FAQ assistants

---

## Example Use Case

This project currently includes a sample:

```text
Warranty Claim Guideline
```

The RAG assistant can answer questions such as:

```text
How long is the warranty?
```

```text
Does warranty cover water damage?
```

```text
What documents are needed to claim warranty?
```

```text
What are the customer support hours?
```

The assistant retrieves the relevant information from the warranty guideline document before generating an answer.

---

## Important Security Note

Never commit API keys to GitHub.

Make sure:

```text
.env
```

is included in:

```text
.gitignore
```

Example:

```gitignore
.env
```

If an API key is accidentally uploaded publicly, revoke the key immediately and create a new one.

---

## Limitations

This is a simple educational RAG implementation.

Current limitations include:

* Only PDF and TXT files are supported
* No graphical user interface
* Retrieval uses basic vector similarity search
* No reranking
* No conversation memory
* No authentication
* No web search
* No document upload interface
* Large embedding models may require more memory and storage

---

## Future Improvements

Possible improvements include:

* Add DOCX support
* Add CSV support
* Add web document support
* Add hybrid search
* Add reranking
* Add chat history
* Add source citations
* Add similarity score filtering
* Add automatic document updates
* Add a web interface
* Add user authentication
* Add multiple vector collections
* Add metadata filtering

---

## How to Stop the Assistant

While the assistant is running, enter:

```text
exit
```

or:

```text
quit
```

Example:

```text
You: exit

Goodbye!
```

---

## Main Commands

### Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Ingest Documents

```bash
python ingest.py
```

### Start RAG Assistant

```bash
python chat.py
```

---

## Workflow Summary

```text
1. Add documents to data/
          ↓
2. Run python ingest.py
          ↓
3. Documents are chunked
          ↓
4. BGE-M3 creates embeddings
          ↓
5. ChromaDB stores embeddings
          ↓
6. Run python chat.py
          ↓
7. Ask a question
          ↓
8. BGE-M3 embeds the question
          ↓
9. ChromaDB retrieves relevant chunks
          ↓
10. Groq generates an answer
```

---

## Author

Developed as a simple project to understand and demonstrate the basic concepts of **Retrieval-Augmented Generation (RAG)**, document ingestion, vector embeddings, semantic retrieval, and Large Language Model integration.

---

## License

This project is intended for educational and learning purposes.
