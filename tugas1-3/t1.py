import tree_sitter_python as tspython
from tree_sitter import Language, Parser

# Parser dibuat sekali, lalu dipakai untuk semua potongan kode
parser = Parser(Language(tspython.language()))

# ---------------------------------------------------------------
# Tiga potongan kode Python (parse() hanya menerima bytes -> b"...")
# ---------------------------------------------------------------
KODE_FUNGSI = b"""def sapa(nama):
    return nama
"""

KODE_IF_ELSE = b"""if umur >= 17:
    status = "dewasa"
else:
    status = "anak"
"""

KODE_KELAS = b"""class Mahasiswa:
    def halo(self):
        return "hai"
"""

# Kode fungsi yang sengaja dirusak: titik dua (:) setelah def sapa(nama) dihapus
KODE_RUSAK = b"""def sapa(nama)
    return nama
"""


def tampilkan_pohon(judul, kode):
    """Parse kode lalu cetak pohonnya (S-expression satu baris)."""
    tree = parser.parse(kode)
    print("=" * 60)
    print(judul)
    print("=" * 60)
    print(kode.decode())
    print("Pohon:")
    print(tree.root_node)
    print()
    return tree


# ---------------------------------------------------------------
# Langkah 1-4: cetak pohon tiap potongan kode
# ---------------------------------------------------------------
tree_fungsi = tampilkan_pohon("1. FUNGSI", KODE_FUNGSI)
tree_if = tampilkan_pohon("2. IF / ELSE", KODE_IF_ELSE)
tree_kelas = tampilkan_pohon("3. KELAS", KODE_KELAS)

# ---------------------------------------------------------------
# Langkah 5: lihat node anonim pada potongan FUNGSI
# root_node.children[0] = function_definition (anak pertama dari module)
# ---------------------------------------------------------------
print("=" * 60)
print("NODE ANONIM vs BERNAMA - anak langsung function_definition")
print("=" * 60)
fungsi = tree_fungsi.root_node.children[0]
for c in fungsi.children:
    print(c.type, "bernama" if c.is_named else "anonim")
print()

# Tanda ( dan ) ada satu tingkat lebih dalam, di dalam node 'parameters'
print("Anak-anak node 'parameters':")
parameters = fungsi.child_by_field_name("parameters")
for c in parameters.children:
    print(c.type, "bernama" if c.is_named else "anonim")
print()

# ---------------------------------------------------------------
# Beda children vs named_children (kriteria 'selesai' Tugas 1)
# ---------------------------------------------------------------
print("=" * 60)
print("children vs named_children pada function_definition")
print("=" * 60)
print("children       :", [c.type for c in fungsi.children])
print("named_children :", [c.type for c in fungsi.named_children])
print()

# ---------------------------------------------------------------
# Langkah 6: kode rusak -> cari ERROR atau MISSING
# ---------------------------------------------------------------
tree_rusak = tampilkan_pohon("4. KODE RUSAK (titik dua dihapus)", KODE_RUSAK)
print("root_node.has_error:", tree_rusak.root_node.has_error)