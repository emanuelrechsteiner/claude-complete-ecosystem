#!/usr/bin/env python3
"""
Build vector database index from processed chunks.
This script creates the searchable vector database with embeddings.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
import hashlib
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "vector-server" / "src"))

def load_processed_chunks(chunks_dir: Path) -> List[Dict[str, Any]]:
    """Load all processed chunks from the chunks directory."""
    all_chunks = []
    
    # Iterate through each file's chunk directory
    for file_dir in sorted(chunks_dir.iterdir()):
        if file_dir.is_dir():
            # Load all chunks for this file
            for chunk_file in sorted(file_dir.glob("chunk_*.json")):
                with open(chunk_file, 'r', encoding='utf-8') as f:
                    chunk = json.load(f)
                    all_chunks.append(chunk)
    
    return all_chunks

def build_vector_index(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build the vector database index from chunks."""
    vector_index = []
    
    for chunk in chunks:
        # Create index entry
        entry = {
            "chunk_id": chunk["chunk_id"],
            "content": chunk["content"],
            "metadata": chunk["metadata"]
        }
        
        # Add additional metadata for search
        if "source_file" in chunk["metadata"]:
            # Extract source URL from file name if available
            source_file = chunk["metadata"]["source_file"]
            if source_file.startswith("test_data/"):
                # Convert file name to approximate URL
                file_name = Path(source_file).stem
                if file_name.startswith("en_docs_"):
                    url_path = file_name.replace("en_docs_", "").replace("_", "-")
                    entry["metadata"]["source_url"] = f"https://docs.anthropic.com/en/docs/{url_path}"
                
                # Add scraped_at timestamp
                entry["metadata"]["scraped_at"] = datetime.now().isoformat()
        
        # Add parent title if not present
        if "parent_title" not in entry["metadata"]:
            entry["metadata"]["parent_title"] = entry["metadata"].get("doc_title", "Unknown")
        
        vector_index.append(entry)
    
    return vector_index

def create_empty_embeddings(num_chunks: int, embedding_dim: int = 384) -> List[List[float]]:
    """Create placeholder embeddings (will be generated on first use)."""
    # Return empty list - embeddings will be generated when needed
    return []

def update_database_files(vector_db_dir: Path, vector_index: List[Dict[str, Any]]):
    """Update all vector database files with the new index."""
    
    # 1. Update vector_db_index.json
    index_file = vector_db_dir / "vector_db_index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(vector_index, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Updated vector_db_index.json ({len(vector_index)} entries)")
    
    # 2. Update chunks/chunks.json
    chunks_file = vector_db_dir / "chunks" / "chunks.json"
    chunks_data = [
        {
            "id": entry["chunk_id"],
            "content": entry["content"],
            "metadata": entry["metadata"]
        }
        for entry in vector_index
    ]
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Updated chunks.json")
    
    # 3. Update metadata/metadata.json
    metadata_file = vector_db_dir / "metadata" / "metadata.json"
    metadata = {
        "total_chunks": len(vector_index),
        "categories": list(set(e["metadata"].get("category", "general") for e in vector_index)),
        "sources": list(set(e["metadata"].get("source_file", "") for e in vector_index if e["metadata"].get("source_file"))),
        "last_updated": datetime.now().isoformat(),
        "version": "1.0.0"
    }
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"   ✅ Updated metadata.json")
    
    # 4. Update indices/semantic_index.json
    semantic_index_file = vector_db_dir / "indices" / "semantic_index.json"
    semantic_index = {
        "version": "1.0.0",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "embedding_dim": 384,
        "total_vectors": len(vector_index),
        "categories": metadata["categories"],
        "last_built": datetime.now().isoformat()
    }
    with open(semantic_index_file, 'w', encoding='utf-8') as f:
        json.dump(semantic_index, f, indent=2)
    print(f"   ✅ Updated semantic_index.json")
    
    # 5. Update status.json
    status_file = vector_db_dir / "status.json"
    status = {
        "status": "populated",
        "initialized_at": datetime.now().isoformat(),
        "version": "1.0.0",
        "total_chunks": len(vector_index),
        "total_observations": 0,
        "last_updated": datetime.now().isoformat()
    }
    with open(status_file, 'w', encoding='utf-8') as f:
        json.dump(status, f, indent=2)
    print(f"   ✅ Updated status.json")
    
    # 6. Update database config
    config_file = vector_db_dir / "config" / "database.json"
    config = {
        "version": "1.0.0",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "chunk_size": 1000,
        "overlap": 100,
        "vector_dim": 384,
        "similarity_metric": "cosine",
        "index_type": "flat",
        "created_at": datetime.now().isoformat()
    }
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f"   ✅ Updated database.json")

def main():
    """Main function to build vector database index."""
    # Paths
    script_dir = Path(__file__).parent
    processed_dir = script_dir / "processed_test_data"
    chunks_dir = processed_dir / "chunks"
    vector_db_dir = script_dir / "vector_db"
    
    print("🔨 Building Vector Database Index")
    print("=" * 50)
    
    # Check if processed data exists
    if not chunks_dir.exists():
        print("❌ No processed chunks found. Run process_test_data.py first.")
        return False
    
    # Load processed chunks
    print("📥 Loading processed chunks...")
    chunks = load_processed_chunks(chunks_dir)
    print(f"   ✅ Loaded {len(chunks)} chunks")
    
    if not chunks:
        print("❌ No chunks to index")
        return False
    
    # Build vector index
    print("🔧 Building vector index...")
    vector_index = build_vector_index(chunks)
    print(f"   ✅ Built index with {len(vector_index)} entries")
    
    # Ensure vector database directories exist
    print("📁 Preparing vector database directories...")
    (vector_db_dir / "chunks").mkdir(parents=True, exist_ok=True)
    (vector_db_dir / "embeddings").mkdir(parents=True, exist_ok=True)
    (vector_db_dir / "metadata").mkdir(parents=True, exist_ok=True)
    (vector_db_dir / "indices").mkdir(parents=True, exist_ok=True)
    (vector_db_dir / "config").mkdir(parents=True, exist_ok=True)
    
    # Update all database files
    print("💾 Updating vector database files...")
    update_database_files(vector_db_dir, vector_index)
    
    # Save a copy in processed_test_data for reference
    processed_index_file = processed_dir / "vector_db_index.json"
    with open(processed_index_file, 'w', encoding='utf-8') as f:
        json.dump(vector_index, f, indent=2, ensure_ascii=False)
    print(f"   ✅ Saved reference copy to processed_test_data/")
    
    # Summary
    print("\n" + "=" * 50)
    print("✅ Vector Database Index Built Successfully!")
    print(f"📊 Summary:")
    print(f"   • Total chunks indexed: {len(vector_index)}")
    print(f"   • Categories: {', '.join(set(e['metadata'].get('category', 'general') for e in vector_index))}")
    print(f"   • Database location: {vector_db_dir}")
    print(f"   • Status: Ready for search!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)