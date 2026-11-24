"""Hermes's live-gateway silence rule: a reply that is only a marker such as ``[SILENT]`` means the
agent chose not to answer, and a marker on a real reply's last line is not meant for the reader."""

from __future__ import annotations

import unicodedata
from typing import Any

# Copied from hermes-agent gateway/response_filters.py at 3b421578588243f920886e6fe79a6faa87ea026e
# (LIVE_GATEWAY_SILENT_MARKERS, _MARKER_LENGTH_CAP and the edge-punctuation rule) for hosts that
# predate strip_trailing_silence_marker (hermes-agent 0.21.x).
_MARKERS = frozenset({"[SILENT]", "SILENT", "NO_REPLY", "NO REPLY", "[静默]", "静默", "[沉默]", "沉默"})
_MARKER_LENGTH_CAP = 64


def _is_edge_punctuation(ch: str) -> bool:
    return ch not in "[]" and unicodedata.category(ch).startswith("P")


def _is_silence(text: Any) -> bool:
    stripped = text.strip() if isinstance(text, str) else ""
    if not 0 < len(stripped) <= _MARKER_LENGTH_CAP:
        return False
    start, end = 0, len(stripped)
    while start < end and _is_edge_punctuation(stripped[start]):
        start += 1
    while end > start and _is_edge_punctuation(stripped[end - 1]):
        end -= 1
    return any(" ".join(form.upper().split()) in _MARKERS for form in (stripped, stripped[start:end]))


def _strip_trailing_marker(text: Any) -> Any:
    if not isinstance(text, str):
        return text
    head, _, tail = text.rstrip().rpartition("\n")
    return head.rstrip() if head.strip() and _is_silence(tail) else text


try:
    from gateway.response_filters import is_intentional_silence_response, strip_trailing_silence_marker
except ImportError:
    is_intentional_silence_response = _is_silence
    strip_trailing_silence_marker = _strip_trailing_marker
