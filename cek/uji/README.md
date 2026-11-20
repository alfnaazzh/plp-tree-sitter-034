# cek.py: pemeriksa kode Python berbasis tree-sitter

`cek.py` memeriksa semua file `.py` di sebuah folder (termasuk subfolder) dan melaporkan tiga hal:

1. **Komentar `TODO` atau `FIXME`**, beserta file dan nomor barisnya (query tree-sitter dengan predikat `#match?`).
2. **Fungsi yang lebih dari 30 baris**, beserta nama dan jumlah barisnya (dihitung dari `start_point` dan `end_point`). Batasnya bisa diubah lewat konstanta `BATAS_BARIS` di `cek.py`.
3. **File yang pohonnya mengandung error sintaks** (`root_node.has_error`), beserta baris pertama yang bermasalah.

## Pemasangan

Butuh Python 3.10 atau lebih baru.

```bash
python -m pip install tree-sitter tree-sitter-python
```

## Cara menjalankan

Dari dalam folder `cek/`:

```bash
python cek.py <folder>
```

Contoh:

```bash
python cek.py uji/
```

Folder `.git`, `venv`, `.venv`, `node_modules`, dan `__pycache__` dilewati.

Format tiap baris laporan: `<file>:<baris>: <temuan>`.

## Contoh output

Pada folder `uji/` (berisi tiga file uji buatan sendiri: `todo.py`, `panjang.py`, `rusak.py`):

```
uji/rusak.py:1: sintaks bermasalah (ERROR)
uji/todo.py:2: # TODO: tambahkan validasi input
uji/todo.py:6: # FIXME: hasilnya salah untuk bilangan negatif
uji/panjang.py:1: fungsi proses terlalu panjang (36 baris)
```

Pada repositori nyata `pallets/itsdangerous` (commit `672971d`, 15 file `.py`):

```
src/itsdangerous/serializer.py:190: fungsi __init__ terlalu panjang (45 baris)
src/itsdangerous/signer.py:129: fungsi __init__ terlalu panjang (45 baris)
src/itsdangerous/signer.py:182: fungsi derive_key terlalu panjang (32 baris)
src/itsdangerous/timed.py:182: # TODO: Signature is incompatible because parameters were added
src/itsdangerous/timed.py:185: fungsi loads terlalu panjang (36 baris)
src/itsdangerous/timed.py:72: fungsi unsign terlalu panjang (87 baris)
src/itsdangerous/url_safe.py:23: fungsi load_payload terlalu panjang (31 baris)
```

Urutan baris bisa berbeda antar komputer, dan di Windows jalur file memakai `\`.

## Catatan dan batasan

- **Semua fungsi dihitung**, termasuk method di dalam kelas dan fungsi bersarang. Panjang fungsi dihitung dari baris `def` sampai baris terakhir isinya.
- **Baris error** adalah baris awal node `ERROR` atau `MISSING` pertama di pohon. Parser sering membungkus area yang lebih besar dari typo-nya, jadi baris itu menunjukkan dari mana area bermasalah mulai, bukan selalu baris typo.
- Hanya file `.py` yang diperiksa.