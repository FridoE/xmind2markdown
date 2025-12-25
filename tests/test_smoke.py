def test_import():
    import sys
    from pathlib import Path
    import xmind2markdown
    output_md = Path("output.md")
    xmind2markdown.convert_xmind2markdown(Path("testfile.xmind"), output_md)
    testfile_md = Path("testfile.md")
    if output_md.read_text() == testfile_md.read_text(): 
        sys.exit(0)
    else:
        print("smoke test not successful!") 
        sys.exit(1)

if __name__ == '__main__':
    test_import()
