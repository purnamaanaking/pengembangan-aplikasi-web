# Alur kerja penyusunan modul praktikum

Dokumen ini mencatat cara setiap modul praktikum *Pengembangan Aplikasi Web* disiapkan di repositori ini, mulai dari modul lama di Google Docs sampai modul baru diletakkan di Google Drive. Pola ini dipakai untuk Modul 09 sampai 12 dan menjadi acuan untuk modul berikutnya.

Ringkasnya ada empat tahap: **uji modul**, **simulasikan ke project kode program**, **susun docx yang rapi juga di Google Docs**, lalu **letakkan di Google Drive**. Semua perubahan masuk ke `main` lewat pull request.

## 1. Uji modul

Sumbernya adalah modul lama di Google Docs (biasanya di folder minggu yang sesuai di Google Drive, lihat bagian 5).

1. Baca seluruh modul, termasuk gambar dan potongan kode.
2. Periksa relevansinya dengan Laravel 13: versi PHP, isi `.env` bawaan, stub hasil `make:*`, perintah Artisan, dan perilaku bawaan yang berubah (misalnya session dan cache yang kini disimpan di database).
3. Catat setiap temuan di `docs/CATATAN-UJI-MODUL-NN.md`: lingkungan uji, hasil per bab, temuan yang bisa membingungkan mahasiswa beserta sarannya, dan penyesuaian yang dilakukan di folder modul. Contoh: [`CATATAN-UJI-MODUL-11.md`](CATATAN-UJI-MODUL-11.md).

## 2. Simulasikan ke project kode program

Setiap modul dikerjakan sebagai project Laravel 13 tersendiri di folder `modul-NN-slug/`.

1. Buat project baru dengan `composer create-project laravel/laravel:^13.0 modul-NN-slug`.
2. Jika modul melanjutkan modul sebelumnya, salin kondisi akhir modul sebelumnya ke project baru sebagai titik awal (controller, view, route, migration, seeder, dan konfigurasi Bootstrap/Sass). Jangan berbagi kode atau dependensi antarfolder.
3. Kerjakan langkah modul satu per satu, dengan kode yang disalin persis dari modul. Jangan merapikan kode dengan formatter.
4. Jalankan dan uji aplikasinya:
   - `npm run build` (view memakai `@vite`), `php artisan serve`, dan `php artisan test`.
   - Uji setiap halaman lewat HTTP: status, isi tabel, validasi form, CSRF (419 tanpa token), dan alur tambah, ubah, hapus.
   - Untuk modul database, pakai MySQL lokal dengan database `data_master`. Modul 11 dan 12 memakai satu database yang sama, jadi `migrate:fresh --seed` di salah satu project mengosongkan data keduanya. Kembalikan data ke kondisi seed setelah pengujian.
5. Penyimpangan dari modul (misalnya route `/` diarahkan ke `/employees`) dicatat di catatan uji dan ditulis juga di docx, supaya kode dan modul tetap sama.

## 3. Susun docx yang rapi di Word dan Google Docs

Docx modul disimpan di `docs/modul-praktikum/Modul-NN-Judul.docx` dengan desain yang sama untuk semua modul: sampul gelap, daftar isi bernomor, blok kode berwarna, kotak Catatan/Perhatian, "Hasil yang diharapkan" dan "Pertanyaan" di setiap bab, "Pemecahan masalah", serta "Tugas dan pengumpulan".

1. Tulis isi modul di `tools/docx/content_NN.py`. Kode diambil langsung dari folder `modul-NN-slug/` lewat `src.py`, sehingga isi modul selalu sama dengan kode yang sudah diuji. Panduannya ada di [`tools/docx/README.md`](../tools/docx/README.md).
2. Siapkan gambar di `tools/docx/assets/`: screenshot aplikasi yang berjalan (viewport 1000 piksel, skala 1,5) dan diagram dari `assets/diagrams.html`.
3. Bangun docx dengan `./twopass.sh NN` (butuh Microsoft Word for Mac dan PyMuPDF). Skrip ini merender docx lewat Word dan mengisi nomor halaman daftar isi sampai stabil. Daftar isi harus muat satu halaman.
4. `gdocs_compat.py` dijalankan otomatis dan membuat docx rapi saat dibuka di Google Docs:
   - tab ditulis sebagai `<w:tab/>`;
   - nomor dan titik-titik daftar isi ditulis sebagai teks biasa;
   - sampul tanpa jarak baris "exact";
   - blok kode boleh terpotong di pergantian halaman, sehingga jumlah halaman Word dan Google Docs sama;
   - chip sampul diberi latar.
5. Periksa hasilnya di dua tempat:
   - **Word:** lihat PDF hasil `twopass.sh` dan validasi skema docx.
   - **Google Docs:** unggah salinan ke folder uji di Drive dengan konversi ke Google Docs, ekspor ke PDF, lalu periksa sampul (satu halaman), footer (rata kanan), titik-titik daftar isi, dan kecocokan nomor halaman daftar isi dengan halaman tiap heading. Jika satu heading di dasar halaman berbeda letak, pakai `page_break=True` pada heading itu. Folder dan file uji dihapus setelah selesai.

## 4. Git dan pull request

- Setiap pekerjaan dibuat di branch baru: `praktikum/modul-NN-slug` untuk modul, atau nama deskriptif seperti `docs/...` untuk perubahan lain.
- Commit dan deskripsi PR berbahasa Indonesia dan tanpa atribusi Claude (tanpa `Co-Authored-By: Claude`, tanpa "Generated with Claude Code").
- Pekerjaan masuk ke `main` lewat pull request di GitHub, dengan merge commit. Jika PR baru dibuat dari branch PR lain yang belum di-merge, sebutkan urutan merge-nya di deskripsi PR.
- `.env`, `vendor/`, `node_modules/`, `public/build/`, dan `tools/docx/out/` tidak ikut di-commit.

## 5. Letakkan di Google Drive

Modul yang sudah selesai diletakkan di folder Google Drive [PAW - Pengembangan Aplikasi Web](https://drive.google.com/drive/folders/1tCxBAKtMVy3l-t8tSMI7tNYZN4bkb7mN).

Struktur folder (per 22 November 2026):

| Folder | Isi |
| --- | --- |
| `Week 01` sampai `Week 16` | Materi per pertemuan. Week 08 untuk UTS, Week 14 dan 15 untuk responsi, Week 16 untuk UAS |
| `Week 10` | Modul 09 dan Modul 10, slide, dan file pendukung (`laravel.png`, `main.svg`) |
| `Week 11` | Modul 11 dan Modul 12 |
| `Week 12` | Modul lama "Laravel Authentication" dan "Factory & File Storage" (kandidat modul berikutnya) |
| `_OLD` di dalam folder minggu | Versi lama yang sudah diganti |
| `Penilaian`, `RPS PAW Ganjil 2627.pdf` | Bukan bagian alur ini |

Aturan peletakan, mengikuti Modul 09 dan 10 di `Week 10`:

1. Letakkan modul di folder minggu tempat modul itu dipakai.
2. Unggah docx **dengan konversi ke Google Docs**, karena mahasiswa membukanya lewat Google Docs.
3. Beri nama `WW - PAK - PAW - Modul NN Praktikum - <Judul>`, dengan `WW` nomor minggu. Contoh: `10 - PAK - PAW - Modul 09 Praktikum - Routing dan Bundling Asset di Laravel 13`.
4. Pindahkan versi lama ke subfolder `_OLD` di folder minggu yang sama. Jangan menghapus file lama.
5. Setelah diunggah, buka hasilnya di Google Docs atau ekspor ke PDF, lalu pastikan tampilannya sama dengan pemeriksaan di tahap 3.

## Daftar periksa satu modul

- [ ] Temuan dan relevansi Laravel 13 tercatat di `docs/CATATAN-UJI-MODUL-NN.md`.
- [ ] Project `modul-NN-slug/` berjalan, `php artisan test` lulus, dan semua halaman diuji lewat HTTP.
- [ ] `docs/modul-praktikum/Modul-NN-*.docx` dibangun dari `tools/docx`, daftar isi satu halaman, lolos validasi.
- [ ] Tampilan di Word dan Google Docs sudah diperiksa: sampul, footer, titik-titik daftar isi, dan nomor halaman cocok.
- [ ] README, CLAUDE.md, dan dokumen ini diperbarui bila ada pola baru.
- [ ] Pull request dibuat ke `main` tanpa atribusi Claude.
- [ ] Modul diunggah ke folder minggu di Google Drive sebagai Google Docs dengan nama sesuai pola, dan versi lama dipindah ke `_OLD`.
