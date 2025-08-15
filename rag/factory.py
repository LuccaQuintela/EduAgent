"""
Factory module for creating RAG system components.

This module provides factory methods and utilities for easily creating
and configuring RAG system components with sensible defaults.
"""

import threading
import weaviate
from rag.weaviate_vector_database import WeaviateVectorDatabase

class VectorDatabaseFactory:
    _lock = threading.Lock()
    _shared_db = None

    @staticmethod
    def build_local_weaviate_db() -> WeaviateVectorDatabase:
        if VectorDatabaseFactory._shared_db is not None:
            return VectorDatabaseFactory._shared_db
        with VectorDatabaseFactory._lock:
            if VectorDatabaseFactory._shared_db is None:
                client = weaviate.connect_to_local()
                VectorDatabaseFactory._shared_db = WeaviateVectorDatabase(
                    client=client,
                    name="Local Docker Hosted Weaviate Vector Database",
                )
            return VectorDatabaseFactory._shared_db
