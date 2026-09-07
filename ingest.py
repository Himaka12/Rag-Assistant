from pathlib import Path
import hashlib
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


DATA_FOLDER = Path("data")
CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "rag_documents"
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"

CHUNK_SIZE = 350
CHUNK_OVERLAP = 60


def clean_text(text):
    text = text.replace("\n", " ")
    return " ".join(text.split())


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks


def load_pdf(file_path):
    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text:
            text = clean_text(text)

            documents.append(
                {
                    "text": text,
                    "page": page_number
                }
            )

    return documents


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    text = clean_text(text)

    return [
        {
            "text": text,
            "page": 1
        }
    ]


def create_id(source, page, chunk_number):
    unique_string = f"{source}-{page}-{chunk_number}"

    return hashlib.md5(
        unique_string.encode()
    ).hexdigest()


def main():

    print("\nLoading BGE-M3 embedding model...")

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    print("Embedding model loaded.\n")

    print("Connecting to ChromaDB...")

    client = chromadb.PersistentClient(
        path=CHROMA_FOLDER
    )

    # Delete previous collection so every ingestion starts clean
    try:
        client.delete_collection(
            name=COLLECTION_NAME
        )
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    all_chunks = []
    all_metadatas = []
    all_ids = []

    files = list(DATA_FOLDER.glob("*"))

    if not files:
        print("No documents found inside the data folder.")
        return

    for file_path in files:

        print(f"Reading: {file_path.name}")

        if file_path.suffix.lower() == ".pdf":
            pages = load_pdf(file_path)

        elif file_path.suffix.lower() == ".txt":
            pages = load_txt(file_path)

        else:
            print(
                f"Skipping unsupported file: {file_path.name}"
            )
            continue

        for page_data in pages:

            page_text = page_data["text"]
            page_number = page_data["page"]

            chunks = split_text(page_text)

            for chunk_number, chunk in enumerate(chunks):

                chunk_id = create_id(
                    file_path.name,
                    page_number,
                    chunk_number
                )

                all_chunks.append(chunk)

                all_ids.append(chunk_id)

                all_metadatas.append(
                    {
                        "source": file_path.name,
                        "page": page_number,
                        "chunk": chunk_number
                    }
                )

    if not all_chunks:
        print("No text could be extracted.")
        return

    print(
        f"\nCreating embeddings for "
        f"{len(all_chunks)} chunks..."
    )

    embeddings = embedding_model.encode(
        all_chunks,
        batch_size=8,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    print("\nSaving embeddings to ChromaDB...")

    collection.add(
        ids=all_ids,
        documents=all_chunks,
        embeddings=embeddings.tolist(),
        metadatas=all_metadatas
    )

    print("\n--------------------------------")
    print("Ingestion completed successfully!")
    print("--------------------------------")

    print(f"Documents/chunks stored: {collection.count()}")
    print(f"Vector database: {CHROMA_FOLDER}")


if __name__ == "__main__":
    main()