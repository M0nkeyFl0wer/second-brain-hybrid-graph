"""Tests for retrieval-eval gate behavior."""

import sys

import pytest


class _OkResponse:
    def raise_for_status(self):
        return None


def test_retrieval_eval_fails_under_recall_threshold(monkeypatch):
    from eval import retrieval_eval

    monkeypatch.setattr(sys, "argv", ["retrieval_eval", "--fail-under", "0.50"])
    monkeypatch.setattr(retrieval_eval.requests, "post", lambda *_, **__: _OkResponse())
    monkeypatch.setattr(retrieval_eval, "run_eval", lambda **_: {})
    monkeypatch.setattr(retrieval_eval, "print_report", lambda *_: {"overall_recall": 0.49})

    with pytest.raises(SystemExit) as exc:
        retrieval_eval.main()

    assert exc.value.code == 1


def test_retrieval_eval_passes_at_recall_threshold(monkeypatch):
    from eval import retrieval_eval

    monkeypatch.setattr(sys, "argv", ["retrieval_eval", "--fail-under", "0.50"])
    monkeypatch.setattr(retrieval_eval.requests, "post", lambda *_, **__: _OkResponse())
    monkeypatch.setattr(retrieval_eval, "run_eval", lambda **_: {})
    monkeypatch.setattr(retrieval_eval, "print_report", lambda *_: {"overall_recall": 0.50})

    assert retrieval_eval.main() is None
