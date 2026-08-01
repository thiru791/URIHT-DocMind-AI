import re
from collections import Counter

# Lightweight in-memory document store
document_store = {}


def split_document(text, chunk_size=500):
    """
    Split extracted PDF text into manageable chunks.
    """
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


def tokenize(text):
    """
    Convert text into simple lowercase words.
    """
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())


def create_vector_store(document_id, chunks):
    """
    Store document chunks in memory.

    This replaces the heavy SentenceTransformer + ChromaDB
    system so the application can run on low-memory servers.
    """

    document_store[document_id] = chunks

    return len(chunks)


def search_document(query, n_results=3, document_id=None):
    """
    Lightweight relevance search.

    Scores chunks based on the number of words from the
    user's question that appear in each chunk.
    """

    query_words = set(tokenize(query))

    if not query_words:
        return []

    # If a document ID is provided, search only that document.
    if document_id is not None:
        chunks = document_store.get(document_id, [])
    else:
        # Search across the currently stored documents.
        chunks = []

        for document_chunks in document_store.values():
            chunks.extend(document_chunks)

    if not chunks:
        return []

    scored_chunks = []

    for chunk in chunks:

        chunk_words = tokenize(chunk)

        if not chunk_words:
            continue

        word_counts = Counter(chunk_words)

        score = 0

        for word in query_words:
            score += word_counts.get(word, 0)

        if score > 0:
            scored_chunks.append((score, chunk))

    # Highest relevance first
    scored_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    results = [
        chunk
        for score, chunk in scored_chunks[:n_results]
    ]

    # If no exact keyword matches were found,
    # return the first few chunks so Gemini still
    # has document context.
    if not results:
        results = chunks[:n_results]

    return results