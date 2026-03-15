# chunking.py

def chunk_text(paragraphs, size = 3):
    chunks = []
    for i in range(0, len(paragraphs), size):
        chunks = " ".join(paragraphs[i:i + size])
        chunks.append(chunks)
    return chunks