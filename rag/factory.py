"""
Factory module for creating RAG system components.

This module provides factory methods and utilities for easily creating
and configuring RAG system components with sensible defaults.
"""

import weaviate
from rag.weaviate_vector_database import WeaviateVectorDatabase

class VectorDatabaseFactory:
    """
    Factory for creating complete RAG systems.
    
    This factory provides methods to create fully configured RAG systems
    with different configurations and component combinations.
    """
    @staticmethod
    def build_local_weaviate_db() -> WeaviateVectorDatabase:
        client = weaviate.connect_to_local()
        db = WeaviateVectorDatabase(
            client=client,
            name="Local Docker Hosted Weaviate Vector Database"
        )
        return db
