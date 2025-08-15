"""
Document processor for handling document ingestion and preprocessing.

This module handles document parsing, chunking, and preprocessing operations
to prepare documents for storage in the vector database.
"""

from rag.vectorstore import Document, Chunk, ChunkMetadata
from typing import List
import uuid

class DocumentChunker:
    def __init__(
            self, 
            strategy: str = "fixed",
            max_chunk_size: int = 1000,
            overlap_ratio: float = 0.1
    ):
        self.str_to_strategy = {
            "fixed": self.fixed_chunker,
            "recursive": self.recursive_chunker,
        }
        self.strategy = self.str_to_strategy.get(strategy, self.fixed_chunker)
        self.max_chunk_size = max_chunk_size
        self.overlap = int(overlap_ratio * max_chunk_size)

    def fixed_chunker(self, document: Document) -> List[Chunk]:
        content = document.content
        length = len(content)
        step_size = self.max_chunk_size - self.overlap

        estimated_chunks = (length + step_size - 1) // step_size
        chunks = [None] * estimated_chunks
        for index, i in enumerate(range(0, length, step_size)):
            chunk_content = content[i: i + self.max_chunk_size]
            chunk = Chunk(
                content=chunk_content,
                chunk_id=uuid.uuid4(),
                metadata=ChunkMetadata(
                    document_title=document.title,
                    chunk_size=len(chunk_content),
                    document_metadata=document.metadata,
                ),
            )
            chunks[index] = chunk
        return chunks

    def recursive_chunker(self, document: Document):
        # TODO: IMPLEMENT
        pass

    def semantic_chunker(self, document: Document):
        # TODO: IMPLEMENT
        pass

    def chunk_documents(
            self,
            documents: List[Document],
    ) -> List[Chunk]:
        chunks = []
        for document in documents:
            document_chunks = self.strategy(document)
            chunks.extend(document_chunks)

        return chunks