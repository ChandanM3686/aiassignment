"""
Knowledge Base Loader for the Math Mentor application.
Loads and chunks documents from the knowledge base directory.
Includes quota protection - skips embedding if already built.
"""

import os
from typing import List, Dict, Any, Tuple
from pathlib import Path

from config.settings import get_settings


class KnowledgeBaseLoader:
    """Loads and processes knowledge base documents."""
    
    def __init__(self, knowledge_base_path: str = None):
        """Initialize the loader.
        
        Args:
            knowledge_base_path: Path to knowledge base directory.
        """
        settings = get_settings()
        self.base_path = knowledge_base_path or settings.knowledge_base_path
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
    
    def load_all_documents(self) -> List[Dict[str, Any]]:
        """Load all documents from the knowledge base.
        
        Returns:
            List of document dicts with content and metadata.
        """
        documents = []
        
        # Walk through all subdirectories
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    doc = self._load_document(file_path)
                    if doc:
                        documents.append(doc)
        
        return documents
    
    def _load_document(self, file_path: str) -> Dict[str, Any]:
        """Load a single document.
        
        Args:
            file_path: Path to the document file.
            
        Returns:
            Dict with content and metadata.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata from path
            rel_path = os.path.relpath(file_path, self.base_path)
            parts = Path(rel_path).parts
            
            category = parts[0] if len(parts) > 1 else "general"
            filename = parts[-1].replace('.md', '')
            
            return {
                "content": content,
                "metadata": {
                    "source": rel_path,
                    "category": category,
                    "topic": filename,
                    "file_path": file_path
                }
            }
        except Exception as e:
            print(f"Error loading document {file_path}: {e}")
            return None
    
    def chunk_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> Tuple[List[str], List[Dict[str, Any]], List[str]]:
        """Chunk documents into smaller pieces.
        
        Args:
            documents: List of document dicts.
            
        Returns:
            Tuple of (chunks, metadatas, ids).
        """
        chunks = []
        metadatas = []
        ids = []
        
        for doc in documents:
            doc_chunks = self._chunk_text(doc["content"])
            
            for i, chunk in enumerate(doc_chunks):
                chunks.append(chunk)
                
                # Copy metadata and add chunk info
                metadata = doc["metadata"].copy()
                metadata["chunk_index"] = i
                metadata["total_chunks"] = len(doc_chunks)
                metadatas.append(metadata)
                
                # Create unique ID
                doc_id = f"{metadata['category']}_{metadata['topic']}_{i}"
                ids.append(doc_id)
        
        return chunks, metadatas, ids
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: The text to chunk.
            
        Returns:
            List of text chunks.
        """
        chunks = []
        
        # Split by sections (headers)
        sections = self._split_by_headers(text)
        
        for section in sections:
            # If section is small enough, keep it whole
            if len(section) <= self.chunk_size:
                if section.strip():
                    chunks.append(section.strip())
            else:
                # Split larger sections
                section_chunks = self._split_long_text(section)
                chunks.extend(section_chunks)
        
        return chunks if chunks else [text]
    
    def _split_by_headers(self, text: str) -> List[str]:
        """Split text at markdown headers.
        
        Args:
            text: The markdown text.
            
        Returns:
            List of sections.
        """
        lines = text.split('\n')
        sections = []
        current_section = []
        
        for line in lines:
            # Check if line is a header
            if line.startswith('#') and current_section:
                sections.append('\n'.join(current_section))
                current_section = [line]
            else:
                current_section.append(line)
        
        # Don't forget the last section
        if current_section:
            sections.append('\n'.join(current_section))
        
        return sections
    
    def _split_long_text(self, text: str) -> List[str]:
        """Split long text with overlap.
        
        Args:
            text: The text to split.
            
        Returns:
            List of overlapping chunks.
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at a sentence or paragraph
            if end < len(text):
                # Look for a good break point
                for break_char in ['\n\n', '\n', '. ', ', ']:
                    break_pos = text.rfind(break_char, start, end)
                    if break_pos != -1:
                        end = break_pos + len(break_char)
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start with overlap
            start = end - self.chunk_overlap
            if start <= 0:
                start = end
        
        return chunks


def is_knowledge_base_initialized() -> bool:
    """Check if the knowledge base is already initialized.
    
    Returns:
        True if ChromaDB has documents, False otherwise.
    """
    import chromadb
    from chromadb.config import Settings as ChromaSettings
    
    settings = get_settings()
    chroma_path = settings.chroma_db_path
    
    # Check if ChromaDB directory exists and has content
    if not os.path.exists(chroma_path):
        return False
    
    try:
        client = chromadb.PersistentClient(
            path=chroma_path,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Try to get the collection
        try:
            collection = client.get_collection(name="math_knowledge")
            count = collection.count()
            return count > 0
        except:
            return False
    except:
        return False


def initialize_knowledge_base():
    """Initialize the vector store with knowledge base documents.
    
    Skips initialization if already built to save API quota.
    """
    # Check if already initialized FIRST (before any API calls)
    if is_knowledge_base_initialized():
        print("✅ Knowledge base already initialized - skipping embedding to save quota")
        return None
    
    from .vector_store import VectorStore
    
    print("📚 Loading knowledge base documents...")
    loader = KnowledgeBaseLoader()
    documents = loader.load_all_documents()
    print(f"Loaded {len(documents)} documents")
    
    print("✂️ Chunking documents...")
    chunks, metadatas, ids = loader.chunk_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    print("🔧 Initializing vector store...")
    vector_store = VectorStore()
    
    # Double-check it's empty
    stats = vector_store.get_collection_stats()
    if stats["count"] > 0:
        print(f"✅ Vector store already contains {stats['count']} documents - skipping")
        return vector_store
    
    print(f"📤 Adding documents to vector store (this may take a few minutes)...")
    print("⏳ Using rate limiting to protect API quota...")
    vector_store.add_documents(chunks, metadatas, ids)
    
    stats = vector_store.get_collection_stats()
    print(f"✅ Vector store now contains {stats['count']} documents")
    
    return vector_store
