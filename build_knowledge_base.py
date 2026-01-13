"""
Build Knowledge Base Script

Run this script ONCE before starting the app to build the vector store.
This script uses aggressive rate limiting to avoid API quota issues.

Usage:
    python build_knowledge_base.py
"""

import os
import sys
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import get_settings
from rag.knowledge_base import KnowledgeBaseLoader, is_knowledge_base_initialized


def build_with_rate_limiting():
    """Build the knowledge base with careful rate limiting."""
    
    # Check if already built
    if is_knowledge_base_initialized():
        print("✅ Knowledge base already built!")
        print("   If you want to rebuild, delete the data/chroma_db folder first.")
        return True
    
    print("=" * 60)
    print("📚 Building Math Mentor Knowledge Base")
    print("=" * 60)
    print()
    print("⚠️  This process uses the Gemini API for embeddings.")
    print("   It may take 5-10 minutes with rate limiting to avoid quota issues.")
    print()
    
    # Load documents
    print("📖 Loading documents...")
    loader = KnowledgeBaseLoader()
    documents = loader.load_all_documents()
    print(f"   Loaded {len(documents)} documents")
    
    # Chunk documents  
    print("✂️  Chunking documents...")
    chunks, metadatas, ids = loader.chunk_documents(documents)
    print(f"   Created {len(chunks)} chunks")
    print()
    
    # Import vector store (this will create the collection)
    from rag.vector_store import VectorStore
    
    print("🔧 Initializing vector store...")
    vector_store = VectorStore()
    
    # Check if already has data
    stats = vector_store.get_collection_stats()
    if stats["count"] > 0:
        print(f"✅ Already has {stats['count']} documents!")
        return True
    
    print()
    print(f"📤 Adding {len(chunks)} chunks to vector store...")
    print("   Rate limit: 5 chunks every 4 seconds")
    print()
    
    # Add in very small batches with long delays
    batch_size = 5
    delay_seconds = 4
    total_batches = (len(chunks) + batch_size - 1) // batch_size
    
    for i in range(0, len(chunks), batch_size):
        batch_num = i // batch_size + 1
        batch_docs = chunks[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        batch_meta = metadatas[i:i + batch_size]
        
        progress = (batch_num / total_batches) * 100
        print(f"   [{progress:5.1f}%] Processing batch {batch_num}/{total_batches}...", end="", flush=True)
        
        try:
            vector_store.collection.add(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
            print(" ✓")
        except Exception as e:
            print(f" ✗ Error: {e}")
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                print(f"\n⚠️  Rate limit hit! Waiting 60 seconds...")
                time.sleep(60)
                # Retry this batch
                try:
                    vector_store.collection.add(
                        documents=batch_docs,
                        metadatas=batch_meta,
                        ids=batch_ids
                    )
                    print(f"   Retry successful!")
                except Exception as e2:
                    print(f"   Retry failed: {e2}")
        
        # Rate limiting delay
        if i + batch_size < len(chunks):
            time.sleep(delay_seconds)
    
    print()
    stats = vector_store.get_collection_stats()
    print(f"✅ Done! Vector store now contains {stats['count']} documents")
    print()
    print("You can now run: streamlit run app.py")
    
    return True


if __name__ == "__main__":
    try:
        build_with_rate_limiting()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted! You can run this script again to continue.")
        print("   Already embedded chunks are cached and won't be re-embedded.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Try running again in a few minutes if this is a rate limit error.")
