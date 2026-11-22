# Pengembangan Aplikasi Web

Repositori praktikum mata kuliah **Pengembangan Aplikasi Web**. Setiap modul praktikum dikerjakan sebagai proyek Laravel 13 tersendiri di folder `modul-NN-*`, lengkap dengan modul cetaknya (`.docx`) dan catatan hasil uji.

## Daftar modul

| Modul | Topik | Folder | Branch pengerjaan |
| --- | --- | --- | --- |
| 09 | Routing dan Bundling Asset di Laravel (Vite, Bootstrap, Sass) | [`modul-09-routing/`](modul-09-routing) | `praktikum/modul-09-routing` |
| 10 | Pengenalan Controller dan View pada Laravel (controller, resource controller, Blade, validasi form) | [`modul-10-controller-view/`](modul-10-controller-view) | `praktikum/modul-10-controller-view` |
| 11 | Laravel Database Tahap Dasar (MySQL, migration, seeder, raw SQL, query builder) | [`modul-11-database-dasar/`](modul-11-database-dasar) | `praktikum/modul-11-database-dasar` |
| 12 | Laravel Database Tahap Lanjut (Eloquent ORM, relasi, Blade layout `@extends`/`@include`) | [`modul-12-database-lanjut/`](modul-12-database-lanjut) | `praktikum/modul-12-database-lanjut` |

Setiap modul adalah proyek yang berdiri sendiri: dibuat dari awal dengan `composer create-project`, tanpa kode atau dependensi bersama. Modul 10 tidak melanjutkan proyek Modul 09. Modul 11 dan 12 melanjutkan materi modul sebelumnya, jadi kondisi akhir modul sebelumnya disalin ke project baru sebagai titik awal. Tidak ada `composer.json` atau `package.json` di root repositori, jadi semua perintah dijalankan di dalam folder modul.

## Prasyarat

- PHP 8.3 atau lebih baru (diuji dengan 8.4) dan Composer
- Node.js dan npm (diuji dengan Node 24)
- MySQL atau MariaDB untuk Modul 11 dan 12 (diuji dengan MySQL 8.0)

## Menjalankan sebuah modul

```sh
cd modul-10-controller-view    # atau modul-09-routing

composer setup                 # install dependensi, salin .env, buat APP_KEY, migrate, npm install, npm run build
composer dev                   # jalankan server, queue, log, dan Vite sekaligus
```

Aplikasi dapat dibuka di <http://localhost:8000>.

Modul 11 dan 12 memakai MySQL. Buat database `data_master` lebih dulu (lihat `DB_*` di `.env.example`), lalu jalankan `composer setup` dan `php artisan db:seed`. Untuk mengulang data dari awal: `php artisan migrate:fresh --seed`.

Jika hanya ingin server dan Vite, jalankan `php artisan serve` dan `npm run dev` di dua terminal. Setelah mengubah halaman, `npm run build` menghasilkan aset produksi.

Semua view memanggil `@vite`, sehingga folder `public/build/` (tidak ikut di-commit) harus sudah ada. Jalankan `npm run build` atau `npm run dev` lebih dulu sebelum membuka halaman atau menjalankan tes.

## Pengujian

```sh
php artisan test                                                   # semua tes
php artisan test --filter=test_the_application_returns_a_successful_response   # satu tes
```

Tes bawaan Modul 09 **gagal** (status 302, bukan 200). Ini sesuai modul: `Route::redirect('/', '/routing')` menimpa route `/` bawaan. Tes Modul 10, 11, dan 12 lulus.

## Dokumentasi

| Berkas | Isi |
| --- | --- |
| [`docs/modul-praktikum/Modul-09-Routing-dan-Bundling-Asset-di-Laravel.docx`](docs/modul-praktikum/Modul-09-Routing-dan-Bundling-Asset-di-Laravel.docx) | Modul praktikum 09 |
| [`docs/modul-praktikum/Modul-10-Pengenalan-Controller-dan-View-pada-Laravel.docx`](docs/modul-praktikum/Modul-10-Pengenalan-Controller-dan-View-pada-Laravel.docx) | Modul praktikum 10 |
| [`docs/CATATAN-UJI-MODUL-09.md`](docs/CATATAN-UJI-MODUL-09.md) | Hasil uji Modul 09 dan temuan yang bisa membingungkan mahasiswa |
| [`docs/CATATAN-UJI-MODUL-10.md`](docs/CATATAN-UJI-MODUL-10.md) | Hasil uji Modul 10 dan temuan yang bisa membingungkan mahasiswa |
| [`docs/modul-praktikum/Modul-11-Laravel-Database-Tahap-Dasar.docx`](docs/modul-praktikum/Modul-11-Laravel-Database-Tahap-Dasar.docx) | Modul praktikum 11 (sampul tertulis Modul 13) |
| [`docs/modul-praktikum/Modul-12-Laravel-Database-Tahap-Lanjut.docx`](docs/modul-praktikum/Modul-12-Laravel-Database-Tahap-Lanjut.docx) | Modul praktikum 12 (sampul tertulis Modul 14) |
| [`docs/CATATAN-UJI-MODUL-11.md`](docs/CATATAN-UJI-MODUL-11.md) | Hasil uji Modul 11, relevansi dengan Laravel 13, dan temuan |
| [`docs/CATATAN-UJI-MODUL-12.md`](docs/CATATAN-UJI-MODUL-12.md) | Hasil uji Modul 12, relevansi dengan Laravel 13, dan temuan |

Kode di folder modul mengikuti modul cetaknya, termasuk bagian yang sengaja berurutan atau bertumpuk untuk keperluan latihan (misalnya urutan route di Modul 09). Karena itu, kode tidak dirapikan dengan formatter.

## Konvensi

- Folder modul: `modul-NN-slug/`, dikerjakan di branch `praktikum/modul-NN-slug`, lalu digabung ke `main` lewat pull request di GitHub. Perubahan lain juga dikerjakan di branch baru dan masuk lewat pull request.
- Pesan commit praktikum berbentuk `Praktikum Modul NN: <judul modul>`.
- `.env`, `vendor/`, `node_modules/`, dan `public/build/` tidak ikut di-commit.
- `CLAUDE.md` dan `AGENTS.md` di dalam folder modul adalah berkas bawaan `composer create-project` Laravel 13 (petunjuk memasang Laravel Boost), bukan bagian dari praktikum. Panduan untuk Claude Code ada di [`CLAUDE.md`](CLAUDE.md) di root.
