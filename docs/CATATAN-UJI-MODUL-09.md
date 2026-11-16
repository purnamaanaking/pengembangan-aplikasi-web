# Catatan Uji Modul 09 — Routing dan Bundling Asset di Laravel

Branch: `praktikum/modul-09-routing` (project di folder `modul-09-routing/`)

## Lingkungan uji

| Komponen | Versi |
| --- | --- |
| PHP | 8.4.8 |
| Composer | 2.8.5 |
| Node.js / npm | 24.11.1 / 11.6.2 |
| Laravel | 13.x (`composer create-project laravel/laravel`) |
| Vite / laravel-vite-plugin | 8.3.8 / 3.2.1 |

## Hasil

Semua langkah Bab 1–4 dapat dikerjakan sesuai teks modul dan menghasilkan keluaran yang dimaksud.
Kode dari modul disalin apa adanya (tanpa karakter non-ASCII/smart quote, jadi aman di-copy-paste dari Google Docs).

| Bab | Hasil |
| --- | --- |
| 1. Generate project + Bootstrap | OK |
| 2. Vite (`npm run dev` dan `npm run build`) | OK. Console menampilkan `[vite] connected.`; `main.svg` masuk manifest; tidak ada peringatan Sass |
| 3. Uji Bootstrap + Icons | OK. Tombol biru + ikon centang tampil |
| 4.1–4.11 | OK. 14 link di halaman `/routing` dicek, semua sesuai |
| 4.12 `route:list` | OK |
| 4.13 `route:cache` / `route:clear` | OK. Di Laravel 13 `route:cache` berhasil walau route memakai Closure |
| Tugas: `.gitignore` | Terverifikasi: `vendor`, `node_modules`, `.env` diabaikan |

Tidak diuji: Tugas no. 2 (memindahkan project statis milik mahasiswa), pembuatan laporan, dan `git push` ke GitHub (butuh akun/remote).

## Temuan yang perlu diperhatikan (bukan error, tapi bisa membingungkan mahasiswa)

1. **Gambar tidak disediakan.** Modul meminta `resources/images/main.svg`, tetapi tidak menyediakan filenya. Tanpa file ini, halaman error. Saran: tambahkan tautan unduh atau sertakan gambarnya di modul.
2. **4.2 View Route.** Dua `Route::view('/view_route', ...)` memakai URI yang sama; yang kedua menimpa yang pertama. Hasilnya benar (`Purnama`), tetapi mahasiswa mungkin bingung kenapa ada dua baris. Saran: beri keterangan bahwa baris kedua menimpa.
3. **4.4 Redirect Route.** `Route::redirect('/', '/routing')` menimpa route `/` bawaan (welcome). Setelah ini halaman Bab 2–3 tidak bisa lagi dibuka lewat `/`. Saran: minta mahasiswa mengambil screenshot Bab 3 sebelum mengerjakan 4.4.
4. **4.7 Regex Constraint.** Halaman 404 hanya muncul **sebelum** 4.10 dikerjakan. Setelah Fallback Route ada, URL yang sama menampilkan `This is Fallback Route`. Saran: minta mahasiswa menguji dan mengambil screenshot 404 tepat setelah 4.7.
5. **4.9 Route Priority.** Sebelum baris pertama di-comment: `This is Route One` (pola `{rpId}` terdaftar lebih dulu). Sesudah di-comment: `This is Route 2`, bukan `Route 1`, karena untuk URI yang persis sama definisi terakhir yang berlaku. Ini kunci jawaban analisis; mahasiswa sering mengira yang pertama menang.
6. **Akhir Bab 1.** Modul meminta `php artisan serve` setelah `resources/css/app.css` dihapus, padahal `welcome.blade.php` bawaan masih memanggilnya lewat `@vite`. Membuka `localhost:8000` pada titik itu diperkirakan error (`Vite manifest not found`); belum diuji terpisah. Saran: tambahkan catatan "halaman baru bisa dibuka setelah Bab 2".
7. **`composer create-project` Laravel 13** juga membuat `CLAUDE.md` dan `AGENTS.md` berisi instruksi memasang Laravel Boost. Tidak memengaruhi modul, tetapi mahasiswa yang memakai asisten AI bisa terdorong memasang paket yang tidak ada di modul.
8. **Kecil:** `npm install` dijalankan dua kali (Bab 1 dan Bab 2). Tidak berbahaya.
