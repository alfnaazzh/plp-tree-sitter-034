import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

    # Telusuri SEMUA child, pakai enumerate supaya kita tahu nomor urutnya (i)
    for i, child in enumerate(node.children):
        if not child.is_named:  # lewati node anonim seperti =, def, :, (, )
            continue
        nama_field = node.field_name_for_child(i)  # nama peran child ini (bisa None)
        jelajah(child, kedalaman + 1, nama_field)  # petugas mencatat bawahannya


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah(tree.root_node)