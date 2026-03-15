# chunking.py

from typing import List

def chunk_text(paragraphs: List[str], size: int = 3, max_chars: int = 1200) -> List[str]:
    """Group paragraph-like segments into bounded chunks."""
    cleaned = [p.strip() for p in paragraphs if p and p.strip()]
    if not cleaned:
        return []

    chunks: List[str] = []
    buffer: List[str] = []

    for part in cleaned:
        tentative = " ".join(buffer + [part])
        if buffer and (len(buffer) >= size or len(tentative) > max_chars):
            chunks.append(" ".join(buffer))
            buffer = [part]
        else:
            buffer.append(part)

    if buffer:
        chunks.append(" ".join(buffer))

    return chunks
