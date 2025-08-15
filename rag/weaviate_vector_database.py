from rag.vectorstore import VectorStore, Document, Chunk, SearchResult
from rag.document_chunker import DocumentChunker
from typing import Callable, List, Any
from weaviate import WeaviateClient
from weaviate.classes.config import Configure
from weaviate.classes.query import MetadataQuery
from custom_errors.database_errors import DatabaseBatchingInsertionError

class WeaviateVectorDatabase(VectorStore):
    def __init__(self, client: WeaviateClient, name: str = "weaviate_vector_database"):
        super().__init__(client, name)

        if client.collections.exists("knowledge_base"):
            self.knowledge_base_collection = client.collections.get("knowledge_base")
        else:
            self.knowledge_base_collection = client.collections.create(
                name="knowledge_base",
                description="General knowledge base for the RAG system. Information needed for curriculum and lesson building will be pulled from here.",
                vector_config=Configure.Vectors.text2vec_ollama(
                    api_endpoint="http://host.docker.internal:11434",
                    model="nomic-embed-text"
                ),
            )
        
        self.collections = {
            "knowledge_base": self.knowledge_base_collection,
        }
        self.chunker = DocumentChunker(
            strategy="fixed",
            max_chunk_size=1500,
            overlap_ratio=0.1,
        )

    def get_collection(self, collection:str):
        collection_obj = self.collections.get(collection, None)
        if collection_obj is None: 
            raise ValueError(f"Unknown Collection: {collection}")
        return collection_obj

    def add_documents(
            self, 
            documents: List[Document], 
            collection_name: str = "knowledge_base",
            error_threshold: float = 0.05, 
            batch_size: int = 100,
        ):
        collection = self.get_collection(collection_name)
        chunks = self.chunker.chunk_documents(documents)
        with collection.batch.fixed_size(batch_size=batch_size) as batch:
            for chunk in chunks:
                batch.add_object(
                    {
                        "chunk_id": str(chunk.chunk_id),
                        "content": chunk.content,
                        "metadata": chunk.metadata.model_dump(),
                    }
                )
            if batch.number_errors > batch_size * error_threshold:
                raise DatabaseBatchingInsertionError("Error threshold exceeded")
            
    def _dynamic_search(
            self,
            query: str,
            search_function: Callable[..., Any],
            limit: int = 5,
            **kwargs,
    ) -> List[SearchResult]:
        query = query.strip()
        if not query:
            raise ValueError("Query can not be empty")
        if limit <= 0:
            raise ValueError("Query limit must be positive")
        try:    
            response = search_function(
                query=query,
                limit=limit,
                return_metadata=MetadataQuery(
                    score=True,
                    distance=True, 
                    certainty=True
                ),
                **kwargs,
            )
        except Exception as e:
            raise RuntimeError(f"Search failed [{search_function}]: {e}") from e
        return self._format_chunks(response.objects)

    def semantic_search(
            self, 
            query: str,
            collection_name:str = "knowledge_base",
            limit=5,
    ) -> List[SearchResult]:
        collection = self.get_collection(collection_name)
        return self._dynamic_search(
            query=query,
            limit=limit,
            search_function=collection.query.near_text
        )
    
    def keyword_search(
            self, 
            query: str, 
            collection_name: str = "knowledge_base",
            limit: int = 5
    ) -> List[SearchResult]:
        collection = self.get_collection(collection_name)
        return self._dynamic_search(
            query=query,
            limit=limit,
            search_function=collection.query.bm25
        )
    
    def hybrid_search(
            self, 
            query: str, 
            collection_name: str = "knowledge_base", 
            limit: int = 5, 
            alpha: float = 0.7) -> List[SearchResult]:
        collection = self.get_collection(collection_name)
        return self._dynamic_search(
            query=query,
            limit=limit,
            search_function=collection.query.hybrid,
            alpha=alpha
        )
    
    def _format_chunks(self, chunks):
        results = []
        for rank, chunk in enumerate(chunks, start=1):
            results.append(
                SearchResult(
                    chunk=chunk.properties,
                    similarity_score=chunk.metadata.score,
                    rank=rank,
                )
            )
        return results
    
    def clear_all_collections(self):
        for collection in self.collections:
            self.client.collections.get(collection).data.delete_many(
                where={
                    "path": ["id"],
                    "operator": "IsNotNull",
                    "valueText": ""
                }
            )

    def delete_all_collections(self):
        for collection in self.collections:
            self.client.collections.delete(collection)
        
    def cleanup(self):
        self.client.close()

    def check_failed_batch_objects(self):
        for object in self.knowledge_base_collection.batch.failed_objects:
            print(object)