# Catatan Uji Modul 12 — Laravel Database Tahap Lanjut (Eloquent ORM & Blade Templates)

Branch: `praktikum/modul-12-database-lanjut` (project di folder `modul-12-database-lanjut/`, dibuat dari `main`)

Modul ini melanjutkan project Modul 11. Project dibuat ulang dengan `composer create-project`, lalu kondisi akhir Modul 11 (Bootstrap via Sass, controller, view, migration, seeder) disalin sebagai titik awal. Lingkungan uji sama dengan [Modul 11](CATATAN-UJI-MODUL-11.md) (PHP 8.4.8, Laravel 13.43.0, MySQL 8.0.41).

## Relevansi dengan Laravel 13

**Relevan dan berjalan di Laravel 13 tanpa perubahan kode.** Relasi `hasMany`/`belongsTo`, `Model::all()`, `find()`, `save()`, `delete()`, serta Blade `@extends`, `@section`, `@yield`, `@include`, `@php`, `@error`, dan `@method` semuanya tidak berubah. Facade `Route` tetap bisa dipakai langsung di Blade (`Route::currentRouteName()`). Perbedaan kecil dengan versi Laravel yang dipakai saat modul ditulis ada di temuan no. 2.

Pendekatan layout dengan `@extends`/`@section` masih didukung penuh. Dokumentasi dan starter kit Laravel 13 lebih banyak memakai Blade component (`<x-layout>`), tetapi itu alternatif, bukan pengganti.

## Hasil

Pengujian dilakukan dua kali: setelah Bab 1–6 (Eloquent, view lama) dan setelah Bab 7–15 (Blade layout).

| Bab | Hasil |
| --- | --- |
| 1. Model `Position` dan `Employee` | OK. Relasi diuji lewat `tinker`: `Employee::find(2)->position->name` = `Back End Developer` |
| 2. List data (`Employee::all()`) | OK. Kolom Position tampil lewat `$employee->position->name` |
| 3. Form input (`Position::all()`, `save()`) | OK. Input salah menampilkan pesan per field (`@error`) dan border merah (`is-invalid`); input valid tersimpan. `created_at`/`updated_at` kini terisi otomatis |
| 4. Detail data (`find()`) | OK |
| 5. Form edit (`edit()`/`update()`) | OK. Form terisi data lama dan Position terpilih; saat validasi gagal, isian dan Position dari `old()` dipakai; update tersimpan. Lihat temuan no. 1 |
| 6. Hapus data | OK |
| 7. `layouts/nav.blade.php` | OK. Link aktif sesuai route. Lihat temuan no. 4 |
| 8. `layouts/app.blade.php` | OK. Semua halaman punya satu `<html>`, satu `<nav>`, dan memuat CSS/JS Vite |
| 9. `default.blade.php` | OK |
| 10. `employee/actions.blade.php` | OK. Variabel `$employee` dari `@foreach` terbaca di file yang di-`@include` |
| 11–14. Penyesuaian view employee | OK. Semua halaman 200 dengan judul yang benar |
| 15. Home dan Profile | OK. Lihat temuan no. 5 |
| CSRF | OK. POST tanpa token lewat `curl` ditolak 419 |
| `php artisan test` | OK, 2 tes lulus |

Tidak diuji: pembuatan laporan dan upload ke GitHub.

## Temuan yang perlu diperhatikan

1. **Bab 5 mengasumsikan `edit.blade.php` sudah ada.** Teksnya "Buka file View /views/employee/edit.blade.php", padahal file itu adalah hasil Tugas no. 2 Modul 11 (bukan langkah praktikum). Mahasiswa yang tidak mengerjakan tugas tersebut harus membuatnya sendiri. Di folder ini, `edit.blade.php` dibuat dari kerangka `create.blade.php` dengan form dari Bab 5, lalu disesuaikan di Bab 14. Saran: ganti menjadi "Buat file View baru ..." dan sertakan kerangka halamannya.

2. **Stub `make:model` di Laravel 13 lebih ringkas.** File hasil `php artisan make:model Position` hanya berisi `class Position extends Model { // }`, tanpa `use HasFactory;`. Kode di modul tetap berjalan karena trait itu masih ada. Saran: beri catatan bahwa isi file hasil generate berbeda dari modul dan mahasiswa cukup menyalin kode modul. Model `User` bawaan Laravel 13 juga memakai atribut PHP (`#[Fillable]`, `#[Hidden]`), yang mungkin membuat mahasiswa bingung jika membandingkan.

3. **Teks Bab 1 tidak sama dengan kodenya.** Teks menyebut "function employee()" pada model Position, tetapi kodenya `employees()` (jamak, sesuai `hasMany`). Kode sudah benar; teks perlu diperbaiki.

4. **Navbar: link "Employee" hanya aktif di halaman list.** Kondisi `$currentRouteName == 'employees.index'` tidak aktif di halaman create, detail, dan edit. Ini sesuai kode modul, tetapi bisa dijadikan latihan: `request()->routeIs('employees.*')`. Label navbar juga berubah dari "Employee List" (Modul 10/11) menjadi "Employee".

5. **Profile kehilangan ikonnya.** Sebelum Bab 15, halaman Profile memakai ikon `bi-person-circle`; `default.blade.php` memakai `bi-house-fill` untuk semua halaman, jadi Profile ikut menampilkan ikon rumah. Hanya kosmetik.

6. **Form edit tidak punya border.** Di Bab 5, div form edit memakai `p-5 bg-light rounded-3 col-xl-6` tanpa `border`, sedangkan form create memakai `border`. Tampilannya sedikit berbeda (kosmetik).

7. **Masalah N+1 query (bahan diskusi).** `Employee::all()` lalu `$employee->position->name` di view menjalankan 1 query untuk employees + 1 query per baris. Dengan 3 data: 4 query; dengan `Employee::with('position')->get()`: 2 query. Laravel 13 tidak menolak lazy loading secara default, jadi tidak ada error. Ini kesempatan bagus untuk memperkenalkan eager loading.

8. **Validasi dan data yang tidak ada (sama seperti Modul 11).**
   - Email duplikat: error 500 (`Integrity constraint violation`), karena tidak ada aturan `unique`.
   - `/employees/999`: error 500 (`Attempt to read property "firstname" on null`).
   - Hapus id yang tidak ada: error 500 (`Call to a member function delete() on null`).

   `findOrFail($id)` akan mengubah dua kasus terakhir menjadi halaman 404. Bisa dijadikan pertanyaan atau tugas tambahan.

9. **Sisa import.** Setelah semua query diganti Eloquent, `use Illuminate\Support\Facades\DB;` di `EmployeeController` tidak terpakai lagi. Modul tidak memintanya dihapus, jadi dibiarkan.

10. **Penomoran dan teks.** Judul di Google Docs adalah "11 - ... (Modul 14 Praktikum)" dan sampul tertulis **MODUL 14**, tahun 2024. Typo: "Tambahkankan", "dimiiki", "inherintance", "memanggilkan". `{{-- Dan Seterusnya --}}` di Bab 12 dan 14 berarti isi form dari Bab 3 dan 5 tetap dipakai; ini cukup jelas, tetapi container berubah dari `mt-5` (Modul 10) menjadi `my-5`.

## Status perbaikan modul

Temuan di atas sudah diterapkan ke `modul-praktikum/Modul-12-Laravel-Database-Tahap-Lanjut.docx` (desain asli dipertahankan; tambahan ditulis sebagai kotak "Catatan"):

- Sampul dan judul isi menjadi **MODUL 12**, tahun 2026; nomor halaman daftar isi diperbarui. Typo "dimiliki", "Tambahkan", "inheritance", "memanggil" diperbaiki (temuan 10).
- Bab 1: teks "function employees()" dan catatan stub `make:model` Laravel 13 tanpa `HasFactory` (temuan 2 dan 3).
- Bab 2: catatan N+1 query dan eager loading `with('position')` (temuan 7). Bab 3: catatan timestamp otomatis pada Eloquent.
- Bab 4: catatan `findOrFail()`; label Position di Bab 4 dan 13 memakai `for="position"` (temuan 8).
- Bab 5: "Buat file View .../edit.blade.php" beserta petunjuk kerangkanya, dan form edit memakai class `border` seperti form create (temuan 1 dan 6).
- Bab 6: catatan import `DB` yang tidak terpakai (temuan 9). Bab 7: catatan `request()->routeIs('employees.*')` (temuan 4). Bab 15: catatan ikon Profile (temuan 5).

Kode di folder modul ikut disesuaikan: `employee/show.blade.php` memakai `for="position"` dan `employee/edit.blade.php` memakai `border`.
