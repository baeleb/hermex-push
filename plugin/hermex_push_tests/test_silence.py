import pytest

from hermex_push import silence

CASES = [
    ("[SILENT]", True, "[SILENT]"),
    (" NO_REPLY. ", True, " NO_REPLY. "),
    ("*no reply*", True, "*no reply*"),
    ("[静默]", True, "[静默]"),
    ("[SILENT", False, "[SILENT"),
    ("", False, ""),
    ("Done.", False, "Done."),
    ("I stayed SILENT because nothing changed.", False, "I stayed SILENT because nothing changed."),
    ("Here is the answer.\n\n[SILENT]", False, "Here is the answer."),
    ("Here is the answer. [SILENT]", False, "Here is the answer. [SILENT]"),
    (None, False, None),
]


@pytest.mark.parametrize(("text", "silent", "delivered"), CASES)
def test_the_fallback_follows_the_gateway_rule(text, silent, delivered):
    assert silence._is_silence(text) is silent
    assert silence._strip_trailing_marker(text) == delivered


def test_the_host_gateway_agrees_with_the_fallback():
    try:
        from gateway.response_filters import is_intentional_silence_response, strip_trailing_silence_marker
    except ImportError:
        pytest.skip("no hermes-agent gateway with both silence helpers")
    for text, silent, delivered in CASES:
        assert is_intentional_silence_response(text) is silent
        assert strip_trailing_silence_marker(text) == delivered
