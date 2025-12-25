def test_import():
    import sys, os
    from pathlib import Path
    import xmind2markdown
    exit_value = 0
    output_md = Path("output.md")
    xmind2markdown.convert_xmind2markdown(Path("testfile.xmind"), output_md)
    testfile_md = Path("testfile.md")
    if output_md.read_text() != testfile_md.read_text(): 
        exit_value = 1
    
    os.remove("output.md")
    sys.exit(exit_value)

if __name__ == '__main__':
    test_import()
