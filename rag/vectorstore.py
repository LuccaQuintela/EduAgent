"""
Vector store abstraction for storing and retrieving document embeddings.

This module provides a unified interface for different vector database backends
and handles document storage, retrieval, and similarity search operations.
"""

from typing import List, Dict, Any, Optional
from uuid import UUID
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

class DocumentMetadata(BaseModel):
    source: Optional[str] = Field(None, description="URL source of the document")

class Document(BaseModel):
    """Represents a document in the vector store."""
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    metadata: DocumentMetadata = Field(default_factory=dict, description="Document metadata")

class ChunkMetadata(BaseModel):
    document_title: str = Field(..., description="Title of the document this chunk belongs to")
    chunk_size: int = Field(..., description="Size of the chunk")
    document_metadata: DocumentMetadata = Field(..., description="Metadata surround the source document")

class Chunk(BaseModel):
    """Represents a chunk of a document in the vector store."""
    chunk_id: UUID = Field(..., description="Unique chunk identifier")
    content: str = Field(..., description="Chunk content")
    metadata: ChunkMetadata = Field(..., description="Chunk metadata")

class SearchResult(BaseModel):
    """Represents a search result from the vector store."""
    chunk: Chunk = Field(..., description="Retrieved chunk")
    similarity_score: float = Field(..., description="Similarity score with query")
    rank: int = Field(..., description="Rank of the result")


class VectorStore(ABC):
    """
    Abstract base class for vector store implementations.
    
    This class defines the interface that all vector store backends must implement,
    allowing for easy switching between different vector databases.
    """
    
    def __init__(self, client: Any, name: str = "base_vector_store"):
        self.client = client
        self.name = name

    @abstractmethod
    async def add_documents(
        self, 
        documents: List[Document], 
        embeddings: List[List[float]], 
        collection_name: Optional[str] = None
    ):
        """
        Add documents with their embeddings to the vector store.
        
        Args:
            documents: List of documents to add
            embeddings: List of embeddings corresponding to documents
            collection_name: Optional collection name for organization
            
        Returns:
            Dictionary containing operation results
        """
        pass
    
    @abstractmethod
    async def semantic_search(
        self, 
        query: str,
        collection_name: str,
        limit: int,
    ) -> List[SearchResult]:
        pass

    @abstractmethod
    async def keyword_search(
        self, 
        query: str,
        collection_name: str,
        limit: int,
    ) -> List[SearchResult]:
        pass
    
    @abstractmethod
    async def hybrid_search(
        self, 
        query: str,
        collection_name: str,
        limit: int,
        alpha: float,
    ) -> List[SearchResult]:
        pass

    @abstractmethod
    def cleanup(self):
        """
        Cleanup the vector store before closing the applicaton..
        """
        pass
    
    @abstractmethod
    def clear_all_collections(self):
        """
        Delete all content stored in database.
        """
        pass

    @abstractmethod
    def delete_all_collections(self):
        """
        Delete all collections in the database.
        """
        pass