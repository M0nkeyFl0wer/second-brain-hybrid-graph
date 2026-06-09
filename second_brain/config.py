"""
Configuration for open-second-brain.
Edit this file to match your setup. Defaults are fully local — no cloud needed.
"""

from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =============================================================================
# PATHS
# =============================================================================

# Where the graph database lives (LadybugDB directory)
GRAPH_DIR = _PROJECT_ROOT / "data" / "graph.lbug"

# Where the DuckDB chunk store lives (document chunks + embeddings + FTS/HNSW
# for chunk-level hybrid retrieval). Sits alongside the graph; the graph holds
# entities/edges, this holds the source text chunks they were extracted from.
CHUNK_STORE_PATH = _PROJECT_ROOT / "data" / "chunks.duckdb"

# Path to your Obsidian vault (required for vault ingestion)
VAULT_PATH = ""  # e.g., "~/obsidian-vault" or "~/Documents/SecondBrain"

# Where daily reflections are written
BRIEFING_DIR = _PROJECT_ROOT / "reflections"

# Where documents to ingest are placed
INGEST_DIR = _PROJECT_ROOT / "ingest"

# Directories to skip when scanning the vault
VAULT_IGNORE_DIRS = {".obsidian", ".trash", ".git", "templates", "node_modules"}

# =============================================================================
# PRIVACY MODE
# =============================================================================

# "local"  — All extraction via Ollama. Nothing leaves your machine.
# "hybrid" — Embeddings local. Extraction via remote LLM with ZDR.
# "remote" — Everything via remote API. Not recommended for personal notes.

PRIVACY_MODE = "local"

# =============================================================================
# LOCAL MODELS
# =============================================================================

EMBEDDING_MODEL = "nomic-embed-text"
EMBEDDING_DIM = 768

LOCAL_EXTRACTION_MODEL = "llama3.2:3b"  # or "mistral", "gemma2"

# =============================================================================
# REMOTE MODELS (only used in "hybrid" and "remote" modes)
# =============================================================================

REMOTE_API_BASE = ""
REMOTE_MODEL = ""
# API key: set via environment variable SECONDBRAIN_API_KEY

# =============================================================================
# EXTRACTION
# =============================================================================

MIN_CONFIDENCE = 0.5
MAX_ENTITIES_PER_DOC = 200
DEDUP_THRESHOLD = 0.92

# Use the optional Instructor backend for LLM extraction (schema-validated
# structured output + retry-on-validation-error). Requires the extra:
#   pip install 'open-second-brain[instructor]'
# Off by default — the core ships no instructor/openai SDK and uses urllib.
# Override at runtime with SECOND_BRAIN_USE_INSTRUCTOR=1.
USE_INSTRUCTOR = False

# =============================================================================
# HIDDEN CONNECTIONS
# =============================================================================

# Minimum cosine similarity to flag as a hidden connection
HIDDEN_CONNECTION_THRESHOLD = 0.7

# Number of nearest neighbors to check per entity
HIDDEN_CONNECTION_CANDIDATES = 20

# =============================================================================
# ANALYSIS
# =============================================================================

AUTO_ANALYSIS = False
PRUNE_AGE_DAYS = 14  # Longer for personal notes — ideas take time
MIN_COMMUNITY_SIZE = 3  # Smaller communities matter in personal graphs
MAX_CROSS_EDGES_FOR_GAP = 2
TOP_BETWEENNESS = 10

# =============================================================================
# DAILY REFLECTION
# =============================================================================

BRIEFING_SECTIONS = [
    "new_ideas",  # Entities added in last 24h
    "conflicting_beliefs",  # CONFLICTS_WITH edges found
    "knowledge_gaps",  # Community pairs with low cross-connection
    "hidden_connections",  # Semantically similar but unlinked entities
    "surprising_bridges",  # High betweenness on low-frequency entities
    "underdeveloped_ideas",  # Entities needing more connections
]
