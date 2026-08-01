from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create Chroma database
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)


def split_document(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def create_vector_store(document_id, chunks):
    ids = []
    embeddings = []

    for i, chunk in enumerate(chunks):
        embedding = model.encode(chunk).tolist()

        ids.append(f"{document_id}_{i}")
        embeddings.append(embedding)

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=[
            {"document_id": document_id}
            for _ in chunks
        ]
    )

    return len(chunks)
def search_document(query, n_results=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]