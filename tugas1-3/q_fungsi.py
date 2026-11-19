import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

# matches() mengembalikan daftar (indeks_pola, {nama_capture: [node, ...]})
# Satu match = satu fungsi, sehingga nama dan parameternya tidak tertukar
for _, cap in QueryCursor(Query(PY, pola)).matches(tree.root_node):
    nama = cap["nama"][0].text.decode()
    # named_child_count = jumlah anak bernama = jumlah parameter
    # (tanda baca "(", ")", "," bersifat anonim sehingga tidak ikut terhitung)
    jumlah = cap["params"][0].named_child_count
    print(nama, jumlah)