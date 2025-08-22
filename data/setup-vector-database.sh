#!/bin/bash

# Vector Database Setup Script
# Sets up empty vector database and downloads required models

set -e

echo "🗃️ Setting up Vector Database..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR"
VECTOR_DB_DIR="$DATA_DIR/vector_db"

echo "📁 Vector database directory: $VECTOR_DB_DIR"

# Ensure directories exist
mkdir -p "$VECTOR_DB_DIR"/{chunks,embeddings,metadata,indices,config}

# Create empty index files
echo "📊 Initializing empty indices..."
echo "[]" > "$VECTOR_DB_DIR/chunks/chunks.json"
echo "[]" > "$VECTOR_DB_DIR/metadata/metadata.json"
echo "{}" > "$VECTOR_DB_DIR/indices/semantic_index.json"
echo "[]" > "$VECTOR_DB_DIR/indices/agent_observations.json"

# Download embedding model if not exists
echo "🤖 Checking embedding model..."
EMBEDDINGS_MODEL_DIR="$DATA_DIR/embeddings/sentence-transformers"
if [ ! -d "$EMBEDDINGS_MODEL_DIR" ]; then
    echo "📥 Downloading embedding model (this may take a few minutes)..."
    mkdir -p "$EMBEDDINGS_MODEL_DIR"
    
    # Create Python script to download model
    cat > "$DATA_DIR/download_model.py" << 'EOF'
import os
import sys
from sentence_transformers import SentenceTransformer

try:
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    cache_dir = sys.argv[1] if len(sys.argv) > 1 else "./embeddings"
    
    print(f"Downloading {model_name} to {cache_dir}...")
    model = SentenceTransformer(model_name, cache_folder=cache_dir)
    print("✅ Model downloaded successfully!")
    
except Exception as e:
    print(f"❌ Error downloading model: {e}")
    print("ℹ️ Model will be downloaded automatically when first used")
EOF
    
    # Try to download model
    if command -v python3 &> /dev/null; then
        python3 "$DATA_DIR/download_model.py" "$DATA_DIR/embeddings" || echo "⚠️ Model download failed - will download on first use"
    else
        echo "⚠️ Python3 not found - model will download on first use"
    fi
    
    # Clean up download script
    rm -f "$DATA_DIR/download_model.py"
else
    echo "✅ Embedding model already exists"
fi

# Create database status file
cat > "$VECTOR_DB_DIR/status.json" << EOF
{
    "status": "empty",
    "initialized_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "version": "1.0.0",
    "total_chunks": 0,
    "total_observations": 0,
    "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF

# Set permissions
chmod +x "$SCRIPT_DIR"/*.sh 2>/dev/null || true

echo "✅ Vector database setup complete!"
echo ""
echo "📊 Database Status:"
echo "   📍 Location: $VECTOR_DB_DIR"
echo "   📈 Status: Empty (ready for data)"
echo "   🔧 Config: $VECTOR_DB_DIR/config/database.json"
echo "   📝 Test data will be added during installation"
echo ""
echo "🚀 Ready for integration with MCP Vector Server!"

exit 0