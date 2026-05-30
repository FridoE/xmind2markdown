from pathlib import Path
import xmind2markdown

TESTS_DIR = Path(__file__).parent


def test_conversion(tmp_path):
    output = tmp_path / "output.md"
    xmind2markdown.convert_xmind2markdown(TESTS_DIR / "testfile.xmind", output)
    assert output.read_text() == (TESTS_DIR / "testfile.md").read_text()
