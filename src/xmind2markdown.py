import zipfile
import json
from pathlib import Path

MARKER_MAP = {
    "task-start": "○",
    "task-quarter": "◔",
    "task-half": "◑",
    "task-3quar": "◕",
    "task-done": "✔",

    "task-oct": "○",    # TODO: Find unicode symbol for octets
    "task-3oct": "◔",   # TODO: Find unicode symbol for octets
    "task-5oct": "◑",   # TODO: Find unicode symbol for octets
    "task-7oct": "◕",   # TODO: Find unicode symbol for octets

    "priority-1": "①",
    "priority-2": "②",
    "priority-3": "③",
    "priority-4": "④",
    "priority-5": "⑤",
    "priority-6": "⑥",
    "priority-7": "⑦",
    "priority-8": "⑧",
    "priority-9": "⑨",

    "symbol-star": "⭐",
    "symbol-exclam": "❗",
    "symbol-wrong" : "❌)", 

    "flag-red": "🚩", 
}

def markdown_heading(text: str, level: int) -> str:
    return f"{'#' * level} {text}\n\n"

def markdown_note(note: str) -> str:
    return f"> {note.strip()}\n\n"

def xmind_to_markdown(zf: zipfile.ZipFile) -> str:
    content = json.loads(zf.read("content.json"))
    markdown = []

    def extract_markers(topic: dict) -> str:
        markers_str = ""
        for m in topic.get("markers", []):
            marker = m["markerId"]
            if marker in MARKER_MAP:
                 markers_str += MARKER_MAP[marker]
            else: 
                print("Marker could not be converted: "+marker)
     
        return markers_str


    def parse_topic(topic, level=1):
        markers = extract_markers(topic)
        title = markers + topic.get("title", "Untitled")

        markdown.append(markdown_heading(title, level))

        note = topic.get("notes", {}).get("plain", {}).get("content")
        if note:
            markdown.append(markdown_note(note))

        for child in topic.get("children", {}).get("attached", []):
            parse_topic(child, level + 1)

    for sheet in content:
        parse_topic(sheet["rootTopic"])

    return "".join(markdown)

def convert_xmind2markdown(xmind_file: Path, markdown_file: Path):
        with zipfile.ZipFile(xmind_file) as zf:
            if "content.json" in zf.namelist():
                markdown = xmind_to_markdown(zf)
                markdown_file.write_text(markdown, encoding="utf-8")
            else:
                raise RuntimeError("XMind file could not be opened. Only XMind Files in modern format are supported.")

# -----------------------------
# CLI entry point
# -----------------------------
def main(): 
    import sys
    
    if len(sys.argv) == 3:
        xmind_file = Path(sys.argv[1])
        markdown_file = Path(sys.argv[2])
        convert_xmind2markdown(xmind_file, markdown_file)
    else:
        print("Usage: xmind2markdown input.xmind output.md")
        sys.exit(1)

if __name__ == '__main__':
    main()
