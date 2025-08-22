#!/usr/bin/env python3
"""
Process test data (Claude Code documentation) into chunks for vector database.
This script converts raw markdown files into structured chunks with metadata.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Any
import re

def generate_chunk_id(content: str) -> str:
    """Generate a unique ID for a chunk based on its content."""
    return hashlib.md5(content.encode()).hexdigest()[:8]

def extract_title(content: str) -> str:
    """Extract title from markdown content."""
    lines = content.split('\n')
    for line in lines:
        if line.strip().startswith('#'):
            return line.strip('#').strip()
    return "Untitled"

def categorize_content(file_path: str, content: str) -> str:
    """Categorize content based on file name and content."""
    file_name = os.path.basename(file_path).lower()
    
    if 'quickstart' in file_name or 'getting' in content.lower()[:500]:
        return 'getting_started'
    elif 'troubleshoot' in file_name:
        return 'troubleshooting'
    elif 'security' in file_name:
        return 'security'
    elif 'memory' in file_name:
        return 'memory'
    elif 'mcp' in file_name:
        return 'mcp'
    elif 'workflow' in file_name:
        return 'workflows'
    elif 'reference' in file_name or 'cli' in file_name:
        return 'reference'
    elif 'config' in file_name or 'terminal' in file_name:
        return 'configuration'
    elif 'costs' in file_name or 'analytics' in file_name:
        return 'usage'
    else:
        return 'general'

def calculate_complexity(content: str) -> float:
    """Calculate content complexity score (0-1)."""
    # Simple heuristic based on code blocks, technical terms, and length
    code_blocks = content.count('```')
    technical_terms = len(re.findall(r'\b[A-Z]{2,}\b', content))
    length_factor = min(len(content) / 5000, 1.0)
    
    complexity = (code_blocks * 0.1 + technical_terms * 0.02 + length_factor * 0.3)
    return min(complexity, 1.0)

def split_into_chunks(content: str, max_chunk_size: int = 1000) -> List[str]:
    """Split content into semantic chunks."""
    chunks = []
    
    # Split by sections (headers)
    sections = re.split(r'\n(?=#)', content)
    
    current_chunk = ""
    for section in sections:
        if len(current_chunk) + len(section) < max_chunk_size:
            current_chunk += section + "\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = section
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # If no sections or very few chunks, split by paragraphs
    if len(chunks) <= 1:
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk.strip())
    
    return chunks

def process_markdown_file(file_path: str, base_dir: str) -> List[Dict[str, Any]]:
    """Process a single markdown file into chunks with metadata."""
    chunks = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.strip():
            return chunks
        
        doc_title = extract_title(content)
        category = categorize_content(file_path, content)
        complexity = calculate_complexity(content)
        
        # Get relative path for source tracking
        rel_path = os.path.relpath(file_path, base_dir)
        
        # Split into chunks
        content_chunks = split_into_chunks(content)
        
        for i, chunk_content in enumerate(content_chunks):
            chunk = {
                "chunk_id": generate_chunk_id(chunk_content),
                "content": chunk_content,
                "metadata": {
                    "source_file": rel_path,
                    "doc_title": doc_title,
                    "category": category,
                    "complexity": round(complexity, 5),
                    "chunk_index": i,
                    "total_chunks": len(content_chunks),
                    "type": "text"
                }
            }
            
            # Extract section title if present
            section_match = re.match(r'^#+\s+(.+)', chunk_content)
            if section_match:
                chunk["metadata"]["section_title"] = section_match.group(1)
            
            chunks.append(chunk)
    
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
    
    return chunks

def main():
    """Main processing function."""
    # Paths
    script_dir = Path(__file__).parent
    test_data_dir = script_dir / "test_data"
    output_dir = script_dir / "processed_test_data"
    chunks_dir = output_dir / "chunks"
    
    # Create output directories
    chunks_dir.mkdir(parents=True, exist_ok=True)
    
    print("📋 Processing Test Data for Vector Database")
    print("=" * 50)
    
    # Find all markdown files
    md_files = list(test_data_dir.glob("*.md"))
    print(f"📁 Found {len(md_files)} markdown files to process")
    
    all_chunks = []
    file_count = 0
    
    # Process each file
    for md_file in md_files:
        # Skip summary files
        if md_file.name.startswith('_') or 'summary' in md_file.name.lower():
            continue
        
        print(f"📄 Processing: {md_file.name}")
        chunks = process_markdown_file(str(md_file), str(script_dir))
        
        if chunks:
            # Save chunks for this file
            file_id = f"{file_count:04d}_{md_file.stem}"
            file_chunks_dir = chunks_dir / file_id
            file_chunks_dir.mkdir(exist_ok=True)
            
            for i, chunk in enumerate(chunks):
                chunk_file = file_chunks_dir / f"chunk_{i:03d}.json"
                with open(chunk_file, 'w', encoding='utf-8') as f:
                    json.dump(chunk, f, indent=2, ensure_ascii=False)
            
            all_chunks.extend(chunks)
            file_count += 1
            print(f"   ✅ Created {len(chunks)} chunks")
    
    # Create summary
    summary = {
        "total_files": file_count,
        "total_chunks": len(all_chunks),
        "categories": list(set(c["metadata"]["category"] for c in all_chunks)),
        "avg_complexity": sum(c["metadata"]["complexity"] for c in all_chunks) / len(all_chunks) if all_chunks else 0,
        "status": "completed"
    }
    
    # Save summary
    with open(output_dir / "processing_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\n" + "=" * 50)
    print("✅ Processing Complete!")
    print(f"📊 Summary:")
    print(f"   • Files processed: {summary['total_files']}")
    print(f"   • Total chunks created: {summary['total_chunks']}")
    print(f"   • Categories: {', '.join(summary['categories'])}")
    print(f"   • Average complexity: {summary['avg_complexity']:.2f}")
    print(f"   • Output directory: {output_dir}")
    
    return summary['total_chunks'] > 0

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)