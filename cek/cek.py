import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')
BATAS_BARIS = 30  # fungsi dilaporkan kalau lebih dari ini


def cari_error(node):
    """Cari node pertama (urutan baca atas ke bawah) yang is_error atau is_missing."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        if child.has_error:  # hanya turun ke cabang yang memang mengandung error
            hasil = cari_error(child)
            if hasil:
                return hasil
    return None


def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode(errors='replace').strip()}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        fungsi = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            print(f"{path}:{fungsi.start_point[0] + 1}: fungsi {nama} terlalu panjang ({jumlah} baris)")

    # Fitur 3: file yang pohonnya mengandung error sintaks
    if tree.root_node.has_error:
        bermasalah = cari_error(tree.root_node)
        baris = bermasalah.start_point[0] + 1
        jenis = f"MISSING {bermasalah.type}" if bermasalah.is_missing else "ERROR"
        print(f"{path}:{baris}: sintaks bermasalah ({jenis})")


ABAIKAN = {".git", "venv", ".venv", "node_modules", "__pycache__"}  # folder yang dilewati

akar = Path(sys.argv[1])
for path in akar.rglob("*.py"):
    if ABAIKAN & set(path.relative_to(akar).parts):  # lewati folder di atas
        continue
    cek_file(path)