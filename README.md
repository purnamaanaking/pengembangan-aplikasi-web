# Pengembangan Aplikasi Web

Repositori praktikum mata kuliah **Pengembangan Aplikasi Web**. Setiap modul praktikum dikerjakan sebagai proyek Laravel 13 tersendiri di folder `modul-NN-*`, lengkap dengan modul cetaknya (`.docx`) dan catatan hasil uji.

## Daftar modul

| Modul | Topik | Folder | Branch pengerjaan |
| --- | --- | --- | --- |
| 09 | Routing dan Bundling Asset di Laravel (Vite, Bootstrap, Sass) | [`modul-09-routing/`](modul-09-routing) | `praktikum/modul-09-routing` |
| 10 | Pengenalan Controller dan View pada Laravel (controller, resource controller, Blade, validasi form) | [`modul-10-controller-view/`](modul-10-controller-view) | `praktikum/modul-10-controller-view` |

Setiap modul adalah proyek yang berdiri sendiri: dibuat dari awal dengan `composer create-project`, tanpa kode atau dependensi bersama. Modul 10 tidak melanjutkan proyek Modul 09. Tidak ada `composer.json` atau `package.json` di root repositori, jadi semua perintah dijalankan di dalam folder modul.

## Prasyarat

- PHP 8.3 atau lebih baru (diuji dengan 8.4) dan Composer
- Node.js dan npm (diuji dengan Node 24)

## Menjalankan sebuah modul

```sh
cd modul-10-controller-view    # atau modul-09-routing

composer setup                 # install dependensi, salin .env, buat APP_KEY, migrate, npm install, npm run build
composer dev                   # jalankan server, queue, log, dan Vite sekaligus
```

Aplikasi dapat dibuka di <http://localhost:8000>.

Jika hanya ingin server dan Vite, jalankan `php artisan serve` dan `npm run dev` di dua terminal. Setelah mengubah halaman, `npm run build` menghasilkan aset produksi.

Semua view memanggil `@vite`, sehingga folder `public/build/` (tidak ikut di-commit) harus sudah ada. Jalankan `npm run build` atau `npm run dev` lebih dulu sebelum membuka halaman atau menjalankan tes.

## Pengujian

```sh
php artisan test                                                   # semua tes
php artisan test --filter=test_the_application_returns_a_successful_response   # satu tes
```

Tes bawaan Modul 09 **gagal** (status 302, bukan 200). Ini sesuai modul: `Route::redirect('/', '/routing')` menimpa route `/` bawaan. Tes Modul 10 lulus.

## Dokumentasi

| Berkas | Isi |
| --- | --- |
| [`docs/modul-praktikum/Modul-09-Routing-dan-Bundling-Asset-di-Laravel.docx`](docs/modul-praktikum/Modul-09-Routing-dan-Bundling-Asset-di-Laravel.docx) | Modul praktikum 09 |
| [`docs/modul-praktikum/Modul-10-Pengenalan-Controller-dan-View-pada-Laravel.docx`](docs/modul-praktikum/Modul-10-Pengenalan-Controller-dan-View-pada-Laravel.docx) | Modul praktikum 10 |
| [`docs/CATATAN-UJI-MODUL-09.md`](docs/CATATAN-UJI-MODUL-09.md) | Hasil uji Modul 09 dan temuan yang bisa membingungkan mahasiswa |
| [`docs/CATATAN-UJI-MODUL-10.md`](docs/CATATAN-UJI-MODUL-10.md) | Hasil uji Modul 10 dan temuan yang bisa membingungkan mahasiswa |

Kode di folder modul mengikuti modul cetaknya, termasuk bagian yang sengaja berurutan atau bertumpuk untuk keperluan latihan (misalnya urutan route di Modul 09). Karena itu, kode tidak dirapikan dengan formatter.

## Konvensi

- Folder modul: `modul-NN-slug/`, dikerjakan di branch `praktikum/modul-NN-slug`, lalu digabung ke `main` dengan merge commit.
- Pesan commit praktikum berbentuk `Praktikum Modul NN: <judul modul>`.
- `.env`, `vendor/`, `node_modules/`, dan `public/build/` tidak ikut di-commit.
- `CLAUDE.md` dan `AGENTS.md` di dalam folder modul adalah berkas bawaan `composer create-project` Laravel 13 (petunjuk memasang Laravel Boost), bukan bagian dari praktikum. Panduan untuk Claude Code ada di [`CLAUDE.md`](CLAUDE.md) di root.
