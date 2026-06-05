SHELL := /bin/bash

.PHONY: test lint smoke check all pre-push eval

# Unit + integration tests (mocked Ollama, tmpdir graphs)
test:
	source .venv/bin/activate && python -m pytest tests/ -x -q --timeout=30

# Syntax check all Python files
lint:
	source .venv/bin/activate && python -m py_compile second_brain/*.py scripts/*.py

# Full pipeline smoke test (requires Ollama running)
smoke:
	source .venv/bin/activate && bash tests/smoke.sh

# Run all evaluations with threshold gates
# - Entity Resolution: B-Cubed F1 >= 0.80
# - Retrieval: Recall@5 >= threshold
# - Ontology health: Cat 8 drift < 10%
eval:
	@echo "=== Running Entity Resolution Evaluation ==="
	source .venv/bin/activate && python -m eval.run_er_eval --resolver
	@echo ""
	@echo "=== Running Retrieval Evaluation ==="
	source .venv/bin/activate && python -m eval.retrieval_eval
	@echo ""
	@echo "=== Running Ontology Health Check (Cat 8) ==="
	source .venv/bin/activate && python -m sme.cli cat8 --adapter ladybugdb --db data/graph.lbug --implied-ontology examples/good-dog-corpus/ontology.yaml
	@echo ""
	@echo "=== Running Ontology Health Check (Cat 4+5) ==="
	source .venv/bin/activate && python -m sme.cli check --adapter ladybugdb --db data/graph.lbug --auto-discover

# Dependency check
check:
	source .venv/bin/activate && python -m second_brain.check

# Run everything except smoke (no Ollama needed)
all: check lint test

# Run before pushing
pre-push: all
	@echo "All checks passed. Safe to push."
