import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah_cursor(root):
    cursor = root.walk()  # cursor = "jari" yang berjalan di atas pohon, mulai dari akar
    kedalaman = 0

    while True:
        node = cursor.node
        if node.is_named:  # hanya node bernama yang dicetak
            baris, kolom = node.start_point
            field = cursor.field_name  # nama field node saat ini (None jika tidak ada)
            label = f"{field}: " if field else ""
            print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

        # 1) Turun ke anak pertama, kalau ada
        if cursor.goto_first_child():
            kedalaman += 1
            continue

        # 2) Tidak punya anak: pindah ke saudara berikutnya.
        #    Kalau tidak ada saudara lagi, naik ke induk lalu coba lagi.
        while not cursor.goto_next_sibling():
            if not cursor.goto_parent():
                return  # sudah kembali ke akar -> selesai
            kedalaman -= 1


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
jelajah_cursor(tree.root_node)