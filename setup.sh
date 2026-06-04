#!/bin/bash
# Setup script for open-second-brain
# Run: bash setup.sh

set -e

echo "=== open-second-brain setup ==="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required. Install from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages — from requirements.txt so the full stack lands
# (duckdb, pyyaml, pyvis, fastmcp included). Installing a hand-typed subset
# here used to silently omit duckdb, so the DuckDB chunk store couldn't run
# even after a "successful" setup.
echo ""
echo "Installing Python packages from requirements.txt..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Download spaCy model (NLP extraction fallback path)
echo ""
echo "Downloading language model for NLP extraction..."
python -m spacy download en_core_web_sm --quiet

# Check Ollama
echo ""
if command -v ollama &> /dev/null; then
    echo "Ollama found. Pulling embedding model..."
    ollama pull nomic-embed-text
    echo "Pulling extraction model (llama3.2:3b — small + fast)..."
    ollama pull llama3.2:3b
    echo "Models ready."
else
    echo "WARNING: Ollama not found."
    echo "Install from https://ollama.com/download"
    echo "Then run: ollama pull nomic-embed-text && ollama pull llama3.2:3b"
fi

# Create directories
echo ""
echo "Creating directories..."
mkdir -p data ingest briefings

# Verify
echo ""
echo "Verifying installation..."
python3 -c "
import ladybug; print(f'  LadybugDB: {ladybug.__version__}')
import pyarrow; print(f'  PyArrow: {pyarrow.__version__}')
import spacy; print(f'  spaCy: {spacy.__version__}')
import networkx; print(f'  NetworkX: {networkx.__version__}')
try:
    import ripser; print(f'  Ripser: OK')
except: print('  Ripser: not available (optional)')
"

echo ""
echo "=== Setup complete ==="
echo ""
echo "Next steps (the core pipeline — ingest -> graph -> query/viz):"
echo "  1. Try the bundled demo:  python scripts/ingest_obsidian.py \\"
echo "         --vault examples/good-dog-corpus/vault \\"
echo "         --ontology examples/good-dog-corpus/ontology.yaml"
echo "  2. Inspect the graph:     python -m second_brain.check"
echo "  3. Search it:             python scripts/search_cli.py --query 'your search'"
echo "  4. Visualize it:          python scripts/visualize.py"
echo ""
echo "Or point it at your own content:"
echo "  python scripts/ingest_folder.py     (a folder of documents)"
echo "  python scripts/ingest_obsidian.py   (an Obsidian vault)"
echo ""
echo "Use your own ontology with --ontology path/to/ontology.yaml (see ONTOLOGY.md)."
echo "Edit second_brain/config.py to configure paths and privacy mode."
echo ""
echo "Experimental stages (enrichment loop, MCP server, dashboard, daily"
echo "briefing) are documented in the README under 'Pipeline maturity'."
