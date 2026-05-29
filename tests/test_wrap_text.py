import pytest
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register fonts for stringWidth
try:
    pdfmetrics.registerFont(TTFont("NotoSans", "fonts/NotoSans-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("NotoSans-Bold", "fonts/NotoSans-Bold.ttf"))
except Exception:
    pytest.skip("Noto Sans fonts not available", allow_module_level=True)

from engine.pdf_builder import _wrap_text
import engine.styles as S


class TestWrapText:
    def test_short_text_fits_one_line(self):
        lines = _wrap_text("Hello world", "NotoSans", 10, 500)
        assert lines == ["Hello world"]

    def test_long_text_wraps(self):
        text = "This is a long sentence that should be wrapped across multiple lines when the max width is small"
        lines = _wrap_text(text, "NotoSans", 10, 150)
        assert len(lines) >= 3
        for line in lines:
            assert pdfmetrics.stringWidth(line, "NotoSans", 10) <= 150

    def test_single_long_word(self):
        lines = _wrap_text("Supercalifragilisticexpialidocious", "NotoSans", 10, 100)
        assert len(lines) == 1
        assert lines[0] == "Supercalifragilisticexpialidocious"

    def test_empty_string(self):
        lines = _wrap_text("", "NotoSans", 10, 200)
        assert lines == []

    def test_exact_fit(self):
        text = "Hi"
        w = pdfmetrics.stringWidth(text, "NotoSans", 10)
        lines = _wrap_text(text, "NotoSans", 10, w)
        assert len(lines) == 1

    def test_preserves_all_words(self):
        text = "one two three four five six"
        lines = _wrap_text(text, "NotoSans", 10, 200)
        reconstructed = " ".join(lines)
        assert reconstructed == text


class TestWrapWithDifferentFonts:
    def test_bold_takes_more_space(self):
        text = "Same text content for comparison"
        regular_lines = _wrap_text(text, "NotoSans", 10, 150)
        bold_lines = _wrap_text(text, "NotoSans-Bold", 10, 150)
        assert len(bold_lines) >= len(regular_lines)

    def test_larger_size_wraps_more(self):
        text = "This sentence will wrap differently depending on font size settings"
        small_lines = _wrap_text(text, "NotoSans", 8, 200)
        large_lines = _wrap_text(text, "NotoSans", 14, 200)
        assert len(large_lines) >= len(small_lines)
