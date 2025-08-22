#!/usr/bin/env python3
"""
Example usage of the Document Post-Processor
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from DocPostProcessor import DocumentPostProcessor


async def process_anthropic_docs():
    """Example: Process Anthropic documentation."""
    print("🚀 Processing Anthropic Documentation")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Configuration
    input_dir = "Documentation/Anthropic"
    output_dir = "processed_docs/anthropic"
    
    # Optional: Use OpenAI API for better classification
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Create processor
    processor = DocumentPostProcessor(input_dir, output_dir, api_key)
    
    # Process documents
    summary = await processor.process_all_documents()
    
    # Display results
    print(f"\n✅ Processing Complete!")
    print(f"📁 Total documents: {summary['total_documents']}")
    print(f"📄 Total chunks: {summary['total_chunks']}")
    print(f"\n📊 Categories:")
    for category, count in summary['categories'].items():
        print(f"  - {category}: {count} documents")
    
    print(f"\n📂 Output saved to: {output_dir}")
    print(f"  - Cleaned documents: {output_dir}/cleaned/")
    print(f"  - Chunks: {output_dir}/chunks/")
    print(f"  - Vector DB index: {output_dir}/vector_db_index.json")


async def process_custom_docs():
    """Example: Process custom documentation with specific settings."""
    from DocPostProcessor import DocumentStructurer, DocumentCleaner
    
    print("\n🔧 Custom Processing Example")
    print("=" * 50)
    
    # Custom cleaner with additional patterns
    cleaner = DocumentCleaner()
    cleaner.header_patterns.extend([
        r'Custom Header Pattern.*?\n',
        r'Copyright.*?\n'
    ])
    
    # Custom structurer with different chunk size
    structurer = DocumentStructurer(chunk_size=500, chunk_overlap=100)
    
    # Process a single file
    input_file = Path("Documentation/Anthropic/claude.md")
    if input_file.exists():
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata and clean
        metadata, raw_content = cleaner.extract_metadata(content)
        cleaned_content = cleaner.clean_document(raw_content)
        
        print(f"Original length: {len(raw_content)} chars")
        print(f"Cleaned length: {len(cleaned_content)} chars")
        print(f"Reduction: {(1 - len(cleaned_content)/len(raw_content))*100:.1f}%")
        
        # Structure into chunks
        chunks = structurer.structure_document(cleaned_content, metadata)
        print(f"\nCreated {len(chunks)} chunks")
        print(f"Average chunk size: {sum(c.tokens for c in chunks) / len(chunks):.0f} tokens")


def create_vector_db_pipeline():
    """Example: Create a pipeline for vector database preparation."""
    print("\n🔄 Vector Database Pipeline Example")
    print("=" * 50)
    
    output_dir = Path("processed_docs/anthropic")
    vector_index_file = output_dir / "vector_db_index.json"
    
    if vector_index_file.exists():
        import json
        
        with open(vector_index_file, 'r') as f:
            vector_index = json.load(f)
        
        print(f"Loaded {len(vector_index)} chunks for vector database")
        
        # Example: Prepare for embedding
        print("\n📊 Sample chunks for embedding:")
        for i, chunk in enumerate(vector_index[:3]):
            print(f"\nChunk {i+1}:")
            print(f"  ID: {chunk['chunk_id']}")
            print(f"  Category: {chunk['metadata'].get('category', 'unknown')}")
            print(f"  Content preview: {chunk['content'][:100]}...")
        
        print("\n💡 Next steps:")
        print("1. Use an embedding model (e.g., OpenAI embeddings, sentence-transformers)")
        print("2. Generate embeddings for each chunk")
        print("3. Store in vector database (e.g., Pinecone, Weaviate, ChromaDB)")
        print("4. Implement semantic search over the documentation")
    else:
        print("❌ No processed documents found. Run process_anthropic_docs() first.")


async def main():
    """Run all examples."""
    # Process Anthropic documentation
    await process_anthropic_docs()
    
    # Show custom processing example
    await process_custom_docs()
    
    # Show vector DB pipeline
    create_vector_db_pipeline()


if __name__ == "__main__":
    print("📚 Document Post-Processor Examples")
    print("=" * 50)
    
    # Check if input directory exists
    if not Path("Documentation/Anthropic").exists():
        print("❌ Error: Documentation/Anthropic directory not found!")
        print("Please run the scraper first to download documentation.")
    else:
        asyncio.run(main()) 