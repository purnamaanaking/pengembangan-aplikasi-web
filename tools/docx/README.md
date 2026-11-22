# Pembuat docx modul praktikum

Skrip untuk membangun file modul praktikum (`docs/modul-praktikum/*.docx`) dengan desain yang sama seperti Modul 09 dan 10: sampul gelap, daftar isi bernomor, blok kode berwarna, kotak catatan, header dan footer bernomor halaman.

Saat ini dipakai untuk Modul 11 dan 12. Modul 09 dan 10 dibuat dengan skrip lain yang tidak tersimpan, tetapi docx Modul 10 dipakai sebagai basis desain (styles, header, footer, theme, latar sampul).

## Isi folder

| File | Fungsi |
| --- | --- |
| `content_NN.py` | Isi modul NN: metadata sampul (`META`) dan fungsi `fill(b)` yang menyusun bab demi bab |
| `gen.py` | Pembangun dokumen: heading, paragraf, daftar, tabel, kotak catatan, blok kode, gambar, daftar isi, sampul |
| `hl.py` | Syntax highlighting (PHP, HTML/Blade, BASH, ENV, SQL) dengan palet warna Modul 09/10 |
| `src.py` | Mengambil kode langsung dari folder `modul-NN-*/`, supaya isi modul sama dengan kode yang sudah diuji |
| `build.py` | `python3 build.py NN` membuat `out/mNN.docx` |
| `render.sh` | Mengekspor docx ke PDF lewat Microsoft Word (macOS) |
| `pages.py` | Membaca PDF hasil render dan mencatat halaman setiap heading untuk daftar isi |
| `twopass.sh` | Build, render, isi nomor halaman daftar isi, ulangi sampai stabil |
| `sheet.py` | Menggabungkan beberapa halaman PDF jadi satu gambar untuk pengecekan visual |
| `templates/` | Potongan XML sampul, judul daftar isi, dan pengaturan halaman dari docx Modul 10 |
| `assets/` | Screenshot aplikasi dan diagram. Sumber diagram ada di `assets/diagrams.html` |

## Prasyarat

- Python 3. `build.py` hanya memakai pustaka standar.
- PyMuPDF untuk `pages.py` dan `sheet.py`: `python3 -m venv .venv && .venv/bin/pip install pymupdf`, lalu jalankan dengan `PY=.venv/bin/python`.
- Microsoft Word for Mac untuk `render.sh` dan `twopass.sh`. Tanpa Word, docx tetap bisa dibuat, tetapi nomor halaman di daftar isi bernilai 0.

## Cara pakai

```sh
cd tools/docx

# hanya membuat docx (nomor halaman daftar isi = 0)
python3 build.py 11

# membuat docx lengkap dengan nomor halaman daftar isi (butuh Word dan PyMuPDF)
PY=.venv/bin/python ./twopass.sh 11

# salin hasil ke folder modul
cp out/m11.docx ../../docs/modul-praktikum/Modul-11-Laravel-Database-Tahap-Dasar.docx
```

Sebelum menyalin, periksa tampilan PDF (`out/mNN.pdf`), misalnya dengan `python3 sheet.py out/m11.pdf out/cek.png 1 5`.

## Menulis isi modul

Setiap blok ditambahkan lewat object `b` di `fill(b)`:

```python
b.h1('3. Database dan konfigurasi')          # bab, masuk daftar isi
b.h2('3.1 Jalankan MySQL')                    # subbab, masuk daftar isi
b.p('Teks biasa dengan `kode` dan **tebal**.')
b.bullets([...]); b.steps([...]); b.checks([...])
b.code('PHP', method(M, CTRL, 'index'))      # label: PHP, HTML, BASH, ENV, SQL
b.note('catatan', 'Teks ...')                 # juga: laravel13, perhatian, analisis, screenshot
b.table(['Kolom A', 'Kolom B'], rows, [4819, 4819])   # lebar kolom total 9638
b.image(asset('m11-list.png'), 'Keterangan gambar.', 'Teks alternatif')
```

Daftar isi harus muat satu halaman. Jika meluber ke halaman berikutnya, gabungkan subbab yang pendek.

## Screenshot dan diagram

- Screenshot diambil dari aplikasi yang berjalan dengan viewport 1000 piksel dan skala 1,5 (hasil 1500 piksel lebar), supaya navbar Bootstrap tampil penuh.
- Diagram ditulis di `assets/diagrams.html`. Render setiap elemen `#erd`, `#flow11`, `#rel12`, dan `#blade12` dengan skala 1,5, misalnya lewat Playwright.

## Catatan

- Jika Word gagal membuka file (misalnya XML rusak), Word menampilkan dialog error yang menahan perintah berikutnya. `render.sh` menghentikan proses Word dalam kasus itu, jadi tutup dokumen Word lain sebelum menjalankannya.
- Validasi skema dapat dijalankan dengan skrip `validate.py` dari skill docx Claude Code.
