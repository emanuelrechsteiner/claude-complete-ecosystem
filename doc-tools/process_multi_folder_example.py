#!/usr/bin/env python3
"""
Example: Process multiple folders with markdown files
Demonstrates recursive folder processing and output flattening
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

from DocPostProcessor import DocumentPostProcessor


async def process_multi_folder_docs():
    """Example: Process documentation from multiple folders."""
    print("🚀 Multi-Folder Documentation Processing Example")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Example folder structure:
    # Documentation/
    # ├── Anthropic/
    # │   ├── guides/
    # │   ├── api/
    # │   └── *.md files
    # ├── React/
    # │   ├── hooks/
    # │   ├── components/
    # │   └── *.md files
    # └── Shadcn/
    #     ├── components/
    #     └── *.md files
    
    # Configuration
    input_dir = "Documentation"  # Process all subfolders
    output_dir = "processed_docs/all_documentation"
    
    # Optional: Use OpenAI API for better classification
    api_key = os.getenv('OPENAI_API_KEY')
    
    print(f"📁 Input directory: {input_dir}")
    print(f"📂 Output directory: {output_dir}")
    print(f"🔍 Processing all subfolders recursively")
    print(f"📦 Flattening output to single directory")
    
    # Create processor
    processor = DocumentPostProcessor(input_dir, output_dir, api_key)
    
    # Process documents with recursive folder processing and flattened output
    summary = await processor.process_all_documents(
        recursive=True,      # Process all subfolders
        flatten_output=True  # Consolidate all output in single folder
    )
    
    # Display results
    print(f"\n✅ Processing Complete!")
    print(f"📁 Total documents: {summary['total_documents']}")
    print(f"📄 Total chunks: {summary['total_chunks']}")
    
    print(f"\n📊 Source Folders Processed:")
    for folder in summary.get('source_folders', []):
        print(f"  - {folder}")
    
    print(f"\n📊 Categories:")
    for category, count in summary['categories'].items():
        print(f"  - {category}: {count} documents")
    
    print(f"\n📂 Output Structure:")
    print(f"  - All cleaned documents: {output_dir}/cleaned/")
    print(f"  - All chunks: {output_dir}/chunks/")
    print(f"  - Vector DB index: {output_dir}/vector_db_index.json")
    print(f"  - Processing summary: {output_dir}/processing_summary.json")


async def process_specific_folders():
    """Example: Process only specific folders."""
    print("\n\n🎯 Selective Folder Processing Example")
    print("=" * 50)
    
    # Process only specific documentation folders
    folders_to_process = ["Documentation/Anthropic", "Documentation/React"]
    
    for folder in folders_to_process:
        if Path(folder).exists():
            print(f"\n📁 Processing: {folder}")
            
            output_dir = f"processed_docs/{Path(folder).name.lower()}"
            processor = DocumentPostProcessor(folder, output_dir)
            
            # Process without recursion (only files in the folder)
            summary = await processor.process_all_documents(
                recursive=False,
                flatten_output=True
            )
            
            print(f"  ✓ Processed {summary['total_documents']} documents")
            print(f"  ✓ Created {summary['total_chunks']} chunks")


async def process_preserve_structure():
    """Example: Process while preserving folder structure."""
    print("\n\n📁 Preserve Folder Structure Example")
    print("=" * 50)
    
    input_dir = "Documentation"
    output_dir = "processed_docs/structured"
    
    print(f"📁 Processing with preserved folder structure")
    print(f"📂 Input: {input_dir}")
    print(f"📂 Output: {output_dir}")
    
    processor = DocumentPostProcessor(input_dir, output_dir)
    
    # Process with folder structure preservation
    summary = await processor.process_all_documents(
        recursive=True,
        flatten_output=False  # Preserve folder structure in output
    )
    
    print(f"\n✅ Processed {summary['total_documents']} documents")
    print(f"📄 Total chunks: {summary['total_chunks']}")
    
    # Show how files are organized
    print(f"\n📊 Document Organization:")
    for doc in summary['documents'][:5]:  # Show first 5
        print(f"  - {doc['source_folder']} → {Path(doc['file']).name}")


def analyze_processed_output():
    """Analyze the processed output structure."""
    print("\n\n📊 Output Analysis")
    print("=" * 50)
    
    output_dir = Path("processed_docs/all_documentation")
    
    if output_dir.exists():
        # Count files in each directory
        cleaned_files = list((output_dir / "cleaned").glob("*.md"))
        chunk_dirs = list((output_dir / "chunks").iterdir())
        
        print(f"📁 Cleaned documents: {len(cleaned_files)}")
        print(f"📁 Chunk directories: {len(chunk_dirs)}")
        
        # Analyze file naming
        print(f"\n📝 Sample cleaned filenames (showing folder preservation):")
        for file in cleaned_files[:5]:
            print(f"  - {file.name}")
            
        # Check vector index
        vector_index_file = output_dir / "vector_db_index.json"
        if vector_index_file.exists():
            import json
            with open(vector_index_file, 'r') as f:
                vector_index = json.load(f)
            
            print(f"\n🔢 Vector database index:")
            print(f"  - Total chunks: {len(vector_index)}")
            
            # Analyze chunk sources
            sources = set()
            for chunk in vector_index:
                source = chunk['metadata'].get('source_file', 'unknown')
                sources.add(Path(source).parent.name if Path(source).parent.name else 'root')
            
            print(f"  - Source folders: {', '.join(sources)}")
    else:
        print("❌ No processed output found. Run process_multi_folder_docs() first.")


async def main():
    """Run all examples."""
    # Process all documentation folders
    await process_multi_folder_docs()
    
    # Process specific folders
    await process_specific_folders()
    
    # Process with structure preservation
    await process_preserve_structure()
    
    # Analyze output
    analyze_processed_output()


if __name__ == "__main__":
    print("📚 Multi-Folder Document Processing Examples")
    print("=" * 50)
    
    # Check if Documentation directory exists
    if not Path("Documentation").exists():
        print("❌ Error: Documentation directory not found!")
        print("Please ensure you have scraped documentation in the Documentation folder.")
    else:
        # Check what's available
        subdirs = [d for d in Path("Documentation").iterdir() if d.is_dir()]
        print(f"📁 Found {len(subdirs)} documentation folders:")
        for subdir in subdirs:
            md_files = list(subdir.rglob("*.md"))
            print(f"  - {subdir.name}: {len(md_files)} markdown files")
        
        print("\nStarting processing...\n")
        asyncio.run(main()) 