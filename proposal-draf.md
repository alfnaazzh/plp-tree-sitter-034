# Pendeteksi Potensi SQL Injection pada Kode Python Web Berbasis Tree-sitter

Draf proposal proyek. Tema: pemanfaatan tree-sitter untuk pengembangan aplikasi web enterprise.

Nama / NIM: (isi sebelum dikumpulkan)

## 1. Judul

Pendeteksi Potensi SQL Injection pada Kode Python Web Berbasis Tree-sitter.

## 2. Masalah

Pada aplikasi web enterprise, query SQL sering dibentuk dengan menyisipkan input pengguna langsung ke teks query (penggabungan string `+`, f-string, `%`, atau `.format()`), sehingga rentan SQL injection. Yang mengalami: developer, reviewer, dan tim keamanan. Pengecekan manual lambat pada basis kode besar, dan celah mudah terlewat saat code review.

## 3. Kenapa tidak cukup dengan AI saja

AI bersifat probabilistik (hasil bisa berbeda tiap dijalankan) dan memakai token per file, sehingga mahal untuk basis kode besar. Tool berbasis tree-sitter deterministik (input sama, hasil sama), hampir tanpa biaya per pengecekan, dan bisa dijalankan di CI pada setiap commit. Dibanding regex, query membaca struktur pohon: pada percobaan awal, pemanggilan `execute` yang ditulis multi-baris tetap terdeteksi, dan teks di dalam komentar tidak ikut terdeteksi.

## 4. Bahasa, framework, dan grammar

Python (kode web Flask/Django dengan `sqlite3` atau `psycopg2`). Grammar: `tree-sitter-python` (tersedia di PyPI), dipakai lewat binding Python `tree-sitter`.

## 5. Contoh kode

**Harus terdeteksi** (`cur` = kursor database):

```python
cur.execute("SELECT * FROM users WHERE name = '" + nama + "'")     # penggabungan +
cur.execute(f"SELECT * FROM users WHERE name = '{nama}'")          # f-string
cur.execute("SELECT * FROM users WHERE name = '%s'" % nama)        # format %
cur.execute("SELECT * FROM users WHERE name = '{}'".format(nama))  # .format()
```

**Tidak boleh terdeteksi**:

```python
cur.execute("SELECT * FROM users WHERE name = ?", (nama,))   # parameter terikat
cur.execute("SELECT * FROM users")                           # string konstan
cur.execute(f"SELECT * FROM users")                          # f-string tanpa sisipan
print(f"mencari {nama}")                                     # bukan pemanggilan execute
```

## 6. Rancangan query (S-expression)

Tiga aturan berbagi satu kerangka. Titik (`.`) berarti argumen pertama; bagian `POLA` berbeda per aturan.

Kerangka:

```scheme
(call
  function: (attribute attribute: (identifier) @metode)
  arguments: (argument_list . POLA @sql)
  (#match? @metode "^(execute|executemany)$"))
```

Isi `POLA` per aturan:

```scheme
; A  penggabungan
(binary_operator operator: "+")

; B  f-string
(string (interpolation))

; C1 format %
(binary_operator left: (string) operator: "%")

; C2 .format()  (ditambah predikat (#eq? @fmt "format") pada kerangka)
(call function: (attribute object: (string)
                           attribute: (identifier) @fmt))
```

Aturan ini sudah dijalankan pada contoh kode di poin 5: keempat baris rentan terdeteksi dan keempat baris aman tidak.

## 7. Bentuk output

Laporan di terminal, satu baris per temuan (`file:baris: aturan: potongan kode`) beserta ringkasan jumlah. Opsi `--json` untuk dibaca mesin, dan kode keluar tidak nol bila ada temuan agar bisa menjadi quality gate di CI.

## 8. Cara evaluasi

(a) Corpus kecil buatan sendiri berisi kasus rentan dan aman (poin 5). (b) Satu proyek kuliah dan satu repositori open source berbasis Flask atau Django, dipilih sebelum evaluasi dimulai. Cek manual 20 temuan (atau semuanya bila kurang) dan hitung presisi = temuan benar / total temuan. Periksa juga beberapa file acak secara manual untuk memperkirakan temuan yang terlewat.

## 9. Rencana kerja dan risiko

**Rencana kerja per minggu:**

- **Minggu 1:** aturan A dan B, tes corpus, program penjalan.
- **Minggu 2:** aturan C, uji pada repositori nyata, perbaikan aturan.
- **Minggu 3:** output JSON dan kode keluar, evaluasi manual, laporan.

**Risiko:**

1. *False positive*: penggabungan dua string konstan (`"SELECT * " + "FROM users"`) ikut terdeteksi pada percobaan awal. Rencana mitigasi: filter tambahan di Python.
2. *False negative*: query dibangun di variabel lebih dulu lalu `cur.execute(q)` tidak terdeteksi karena tidak ada analisis aliran data.
3. Pemanggilan SQL mentah lewat ORM belum tercakup.

Karena itu skop dibatasi pada tiga aturan.