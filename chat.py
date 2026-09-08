import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer


CHROMA_FOLDER = "chroma_db"
COLLECTION_NAME = "rag_documents"

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"

GROQ_MODEL = "openai/gpt-oss-20b"

TOP_K = 4


load_dotenv()


def load_system():

    print("\nLoading BGE-M3 embedding model...")

    embedding_model = SentenceTransformer(
        EMBEDDING_MODEL_NAME
    )

    print("Embedding model loaded.")

    print("Connecting to ChromaDB...")

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_FOLDER
    )

    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY was not found in the .env file."
        )

    groq_client = Groq(
        api_key=groq_api_key
    )

    return embedding_model, collection, groq_client


def retrieve_documents(
    question,
    embedding_model,
    collection
):

    question_embedding = embedding_model.encode(
        question,
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=TOP_K,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return documents, metadatas, distances


def create_context(documents, metadatas):

    context_parts = []

    for i, document in enumerate(documents):

        metadata = metadatas[i]

        source = metadata.get(
            "source",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        context_part = (
            f"[Source: {source}, Page: {page}]\n"
            f"{document}"
        )

        context_parts.append(context_part)

    return "\n\n".join(context_parts)


def generate_answer(
    question,
    context,
    groq_client
):

    system_prompt = """
You are a helpful RAG assistant.

Answer the user's question using only the provided context.

Rules:
1. Use the provided context as your source of information.
2. Do not invent information.
3. If the answer cannot be found in the context, say:
   "I could not find that information in the documents."
4. Keep the answer clear and concise.
"""

    user_prompt = f"""
CONTEXT:

{context}


QUESTION:

{question}


ANSWER:
"""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content


def print_sources(
    documents,
    metadatas,
    distances
):

    print("\nSources used:")

    for i, metadata in enumerate(metadatas):

        source = metadata.get(
            "source",
            "Unknown"
        )

        page = metadata.get(
            "page",
            "Unknown"
        )

        print(
            f"{i + 1}. "
            f"{source} - "
            f"Page {page} - "
            f"Distance: {distances[i]:.4f}"
        )


def main():

    try:

        embedding_model, collection, groq_client = (
            load_system()
        )

    except Exception as error:

        print(f"\nError: {error}")

        print(
            "\nMake sure you ran:"
            "\npython ingest.py"
        )

        return

    print("\n====================================")
    print("       SIMPLE RAG ASSISTANT")
    print("====================================")

    print("\nType 'exit' to stop.\n")

    while True:

        question = input("You: ").strip()

        if not question:
            continue

        if question.lower() in [
            "exit",
            "quit"
        ]:
            print("\nGoodbye!")
            break

        print("\nSearching documents...")

        documents, metadatas, distances = (
            retrieve_documents(
                question,
                embedding_model,
                collection
            )
        )

        context = create_context(
            documents,
            metadatas
        )

        answer = generate_answer(
            question,
            context,
            groq_client
        )

        print("\nAssistant:")
        print(answer)

        print_sources(
            documents,
            metadatas,
            distances
        )

        print("\n------------------------------------")


if __name__ == "__main__":
    main()