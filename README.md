# Tugas Awal Tree-sitter (Part 1)

Mata kuliah: Programming Language Pragmatics
Nama / NIM: [ISI]

Repositori ini berisi enam tugas untuk memahami Tree-sitter: membaca pohon sintaks, menelusurinya, menulis query, membuat grammar sendiri, mewarnai sintaks, dan membuat alat pemeriksa kode kecil. Laporan lengkapnya ada di [`laporan/laporan.md`](laporan/laporan.md).

## Isi repositori

| Folder / file | Isi | Tugas |
| --- | --- | --- |
| [`tugas1-3/`](tugas1-3/) | Skrip Python, file query `.scm`, dan output `.txt` | 1, 2, 3 |
| [`tree-sitter-filter/`](tree-sitter-filter/) | Grammar DSL filter: `grammar.js`, `test/corpus/`, `queries/highlights.scm` | 4, 5 |
| [`cek/`](cek/) | `cek.py` pemeriksa kode Python, beserta [README](cek/README.md) | 6 |
| [`laporan/`](laporan/) | Laporan dan tangkapan layar hasil tiap tugas | semua |
| `proposal-draf.md` | Draf proposal proyek (pendeteksi SQL injection berbasis Tree-sitter) | proposal |

## Prasyarat

- Python 3.10 atau lebih baru
- Node.js dan compiler C (untuk Tugas 4 dan 5)
- `tree-sitter-cli`

```bash
python -m pip install tree-sitter tree-sitter-python
npm install -g tree-sitter-cli
```

## Cara menjalankan

### Tugas 1 sampai 3

```bash
cd tugas1-3
python t1.py                              # Tugas 1: pohon, node anonim, kode rusak
python jelajah.py fungsi.py               # Tugas 2: penjelajah rekursif
python jelajah_cursor.py fungsi.py        # Tugas 2 (pengayaan): versi TreeCursor
python q.py contoh.py semua.scm           # Tugas 3: query semua identifier
python q_fungsi.py contoh.py fungsi.scm   # Tugas 3: nama fungsi dan jumlah parameter
python q.py contoh.py print.scm           # Tugas 3: pemanggilan print
python q.py contoh.py import.scm          # Tugas 3: import dan from-import
```

### Tugas 4 dan 5: grammar DSL filter

```bash
cd tree-sitter-filter
tree-sitter generate                      # membuat parser dari grammar.js
tree-sitter test                          # menjalankan kasus uji di test/corpus/
tree-sitter parse contoh.filter           # melihat pohon
tree-sitter highlight contoh.filter       # melihat pewarnaan sintaks
```

`tree-sitter highlight` membutuhkan konfigurasi sekali saja: jalankan `tree-sitter init-config`, lalu isi `parser-directories` di file konfigurasinya dengan folder induk dari `tree-sitter-filter`.

Grammar memakai gaya ES module (`export default grammar({ ... })`), sesuai `package.json` bawaan `tree-sitter init`.

### Tugas 6: `cek.py`

```bash
cd cek
python cek.py uji/
```

Penjelasan lengkap dan contoh output ada di [`cek/README.md`](cek/README.md).

## DSL filter singkat

Contoh kalimat yang dikenali grammar:

```
not archived = true and (status in ("open", "pending") or title contains "invoice") and priority >= 2
```

| Unsur | Bentuk |
| --- | --- |
| Perbandingan | `field operator nilai`, operator `=`, `!=`, `>`, `<`, `>=`, `<=` |
| Nilai | string `"..."`, angka, `true`, `false` |
| Daftar nilai | `field in ("a", "b", "c")` |
| Pencarian teks | `field contains "teks"` |
| Gabungan | `and`, `or`, `not`, dan tanda kurung |

Prioritas operator: `not` lebih kuat dari `and`, dan `and` lebih kuat dari `or`. Contoh: `a = 1 or b = 2 and c = 3` dibaca sebagai `a = 1 or (b = 2 and c = 3)`.