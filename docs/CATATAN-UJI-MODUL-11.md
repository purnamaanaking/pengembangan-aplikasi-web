# Catatan Uji Modul 11 — Laravel Database Tahap Dasar

Branch: `praktikum/modul-11-database-dasar` (project di folder `modul-11-database-dasar/`, dibuat dari `main`)

Modul ini melanjutkan project Modul 10 (`EmployeeController`, view `employee/*`). Karena setiap folder modul adalah project terpisah, project dibuat ulang dengan `composer create-project`, lalu kondisi akhir Modul 10 (Bootstrap via Sass, controller, view, route) disalin sebagai titik awal sebelum langkah Modul 11 dikerjakan.

## Lingkungan uji

| Komponen | Versi |
| --- | --- |
| PHP | 8.4.8 |
| Composer | 2.8.5 |
| Node.js / npm | 24.11.1 / 11.6.2 |
| Laravel | 13.43.0 |
| Vite / laravel-vite-plugin | 8.3.8 / 3.2.1 |
| MySQL | 8.0.41 (Homebrew, bukan XAMPP; dijalankan di port 3307 khusus untuk pengujian) |

## Relevansi dengan Laravel 13

Materi inti modul (migration, seeder, Facade `DB`, raw SQL, query builder, resource controller) **masih relevan dan berjalan di Laravel 13 tanpa perubahan kode**. Stub `make:migration` dan `make:seeder` di Laravel 13 identik strukturnya dengan kode di modul. Yang sudah usang adalah bagian lingkungan dan konfigurasi (Bab 1–3), lihat temuan no. 1–4.

## Hasil

| Bab | Hasil |
| --- | --- |
| 1. Aktifkan MySQL, buat database `data_master` | OK (diuji dengan MySQL 8, bukan XAMPP). Lihat temuan no. 2 |
| 2. Setup `.env` | **Gagal jika diikuti persis.** Lihat temuan no. 1 |
| 3. Skema database | OK. Diagram di modul berasal dari Laravel versi lama, lihat temuan no. 3 |
| 4. Migration `positions` dan `employees` | OK. 5 migration berjalan; FK `employees_position_id_foreign` terbentuk |
| 5. Seeder | OK. 3 positions dan 3 employees masuk. Lihat temuan no. 5 |
| 6. List data (raw SQL + `left join`) | OK. `/employees` 200, 3 baris dengan kolom Position |
| 7. Input data (select Position + insert) | OK. Dropdown berisi `FE/BE/SA`; input salah menampilkan 4 alert dan pilihan Position tetap terpilih; input valid tersimpan lalu redirect ke `/employees` |
| 8. Detail data (`show.blade.php`) | OK. `/employees/{id}` menampilkan 5 field. Lihat temuan no. 7 |
| 9. Hapus data (query builder) | OK. Tombol hapus (`DELETE`) menghapus baris dan redirect ke list |
| CSRF | OK. POST tanpa token lewat `curl` ditolak 419 |
| `php artisan test` | OK, 2 tes lulus (tes memakai SQLite in-memory dari `phpunit.xml`) |
| Query modul di SQLite | OK. Migration, seeder, dan raw SQL `left join` juga jalan di SQLite (alternatif tanpa MySQL) |

Tidak diuji: XAMPP/phpMyAdmin (lingkungan uji macOS), pembuatan laporan, upload ke GitHub. Bagian **Tugas** (fitur Edit dan konversi raw SQL ke query builder) tidak dikerjakan di folder ini karena kodenya tidak ada di modul; fitur Edit dikerjakan di Modul 12 dengan kode dari modul tersebut.

## Temuan yang perlu diperhatikan

1. **Bab 2 tidak cukup untuk Laravel 13 (paling penting).** Sejak Laravel 11, `.env` bawaan berisi `DB_CONNECTION=sqlite` dan baris `DB_HOST`, `DB_PORT`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD` dalam keadaan dikomentari (`#`). Jika mahasiswa hanya mengubah `DB_DATABASE=data_master` seperti instruksi modul, Laravel mencari **file SQLite** bernama `data_master`:

   ```
   SQLiteDatabaseDoesNotExistException
   Database file at path [data_master] does not exist.
   ```

   Saran: ubah instruksi menjadi "set `DB_CONNECTION=mysql`, hapus tanda `#` pada lima baris `DB_*`, lalu isi `DB_DATABASE=data_master`". Screenshot `.env` di modul juga perlu diganti; yang sekarang berasal dari Laravel 10 (ada `BROADCAST_DRIVER`, `CACHE_DRIVER`, `SESSION_DRIVER=file`, folder `modul-05`).

2. **XAMPP dan versi PHP.** Laravel 13 butuh PHP 8.3 ke atas, sedangkan rilis resmi XAMPP terakhir yang ditemukan saat pengujian (8.2.12, November 2023) membawa PHP 8.2. Periksa kembali halaman unduh apachefriends.org sebelum modul dibagikan. XAMPP tetap bisa dipakai **hanya untuk MySQL/MariaDB dan phpMyAdmin**, asalkan PHP yang menjalankan `php artisan` berasal dari instalasi lain (Herd, Laragon, atau PHP mandiri) yang dipakai sejak Modul 09. Saran: tegaskan hal ini di Bab 1, dan ganti screenshot XAMPP Control Panel v3.2.1 (2013, Windows 7).

3. **Halaman langsung error 500 setelah Bab 2, sebelum Bab 4.** Laravel 13 memakai `SESSION_DRIVER=database`, `CACHE_STORE=database`, dan `QUEUE_CONNECTION=database`. Database `data_master` yang baru dibuat masih kosong, sehingga setiap halaman (termasuk `/home`) gagal dengan `Table 'data_master.sessions' doesn't exist` sampai `php artisan migrate` dijalankan. Saran: tambahkan catatan "halaman akan error sampai migrate dijalankan di Bab 4", atau minta mahasiswa menjalankan `php artisan migrate` di akhir Bab 2.

4. **Diagram skema (Bab 3) memuat tabel versi lama.** Diagram menampilkan `personal_access_tokens` (Sanctum, tidak terpasang di Laravel 13) dan tidak menampilkan tabel bawaan Laravel 13: `sessions`, `cache`, `cache_locks`, `jobs`, `job_batches`. Tabel yang benar-benar terbentuk setelah migrate: `cache, cache_locks, employees, failed_jobs, job_batches, jobs, migrations, password_reset_tokens, positions, sessions, users`. Inti diagram (`employees` → `positions`) tetap benar.

5. **Menjalankan `db:seed` dua kali gagal.** Pada percobaan kedua, `positions` bertambah 3 baris duplikat (id 4–6), lalu `EmployeeSeeder` gagal karena email unik (`Duplicate entry 'purnama.anaking@gmail.com'`). Saran: sebutkan `php artisan migrate:fresh --seed` untuk mengulang dari awal.

6. **Urutan pembuatan migration penting.** `employees` punya foreign key ke `positions`, jadi migration `positions` harus dibuat lebih dulu (urutan di modul sudah benar). Jika mahasiswa membalik urutan, `migrate` gagal karena tabel `positions` belum ada. Layak diberi catatan singkat.

7. **Validasi belum mencakup kasus database.**
   - Email yang sudah ada menyebabkan error 500 (`Integrity constraint violation`) karena aturan validasi tidak memakai `unique:employees,email`.
   - `/employees/{id}` dengan id yang tidak ada menyebabkan error 500 (`Attempt to read property "firstname" on null`).
   - `position` tidak divalidasi (`required|exists:positions,id`).
   
   Ini sesuai cakupan modul dasar, tetapi bisa dijadikan pertanyaan atau tugas tambahan.

8. **Tombol Edit di list membuka halaman kosong.** Method `edit()` masih stub kosong dari `--resource`, sehingga `/employees/{id}/edit` menghasilkan HTTP 200 tanpa isi. Ini sesuai karena fitur Edit adalah Tugas no. 2. Perlu diketahui bahwa **Modul 12 Bab 5 mengasumsikan `edit.blade.php` sudah dibuat** dari tugas ini.

9. **Kolom `created_at`/`updated_at` bernilai `NULL`** untuk data dari seeder dan dari `store()`, karena `DB::table()->insert()` tidak mengisi timestamp secara otomatis (berbeda dengan Eloquent di Modul 12). Bisa dijadikan bahan diskusi perbandingan.

10. **Penomoran dan teks.** Judul di Google Docs adalah "11 - ... (Modul 13 Praktikum)" dan sampul tertulis **MODUL 13**, tahun 2024. Typo: "Definiskan", "System Analist" (data seeder; dibiarkan agar sesuai screenshot). Pada `show.blade.php`, label Position memakai `for="age"` (kosmetik).

## Penyesuaian di folder modul

- `.env.example` diubah ke konfigurasi MySQL sesuai modul (`DB_CONNECTION=mysql`, `DB_DATABASE=data_master`, port 3306). Buat database `data_master` lebih dulu, lalu jalankan `php artisan migrate --seed`.
- Selain itu, semua kode disalin apa adanya dari modul.

## Status perbaikan modul

`modul-praktikum/Modul-11-Laravel-Database-Tahap-Dasar.docx` ditulis ulang dengan desain dan struktur Modul 09/10 (sampul gelap, daftar isi bernomor, subbab Tujuan/Hasil akhir/Prasyarat, blok kode berwarna, kotak Catatan/Perhatian, Hasil yang diharapkan, Pertanyaan per bab, Pemecahan masalah, Tugas dan daftar periksa). Isi teknisnya tetap mengikuti modul asli, dan semua temuan di atas sudah diterapkan:

- Nomor modul menjadi **11**, Laravel 13, diperbarui 22 November 2026.
- Bab 1.3: catatan PHP 8.3+ dan XAMPP hanya untuk MySQL/phpMyAdmin (temuan 2). Screenshot XAMPP Control Panel lama dihapus dan diganti langkah tertulis.
- Bab 3: blok `.env` sebelum/sesudah dengan `DB_CONNECTION=mysql`, catatan error SQLite, `php artisan db:show` untuk mengecek koneksi, dan peringatan error tabel `sessions` sebelum migrate (temuan 1 dan 3).
- Bab 4: diagram tabel baru (hanya `employees` dan `positions`), daftar tabel bawaan Laravel 13, dan peringatan urutan migration (temuan 4 dan 6).
- Bab 5: `DatabaseSeeder` diganti seluruhnya, peringatan `db:seed` dua kali dan `migrate:fresh --seed`, penjelasan timestamp `NULL` (temuan 5 dan 9).
- Bab 6–9: penjelasan alias `employee_id`, parameter binding `?`, tabel uji form termasuk email duplikat, catatan id tidak ditemukan, label `for="position"` (temuan 7 dan 10).
- Bab 11 (Tugas): fitur Edit dijelaskan eksplisit dan disebut akan dipakai Modul 12; petunjuk padanan raw SQL ke query builder untuk tugas konversi (temuan 8).
- Kode di modul diambil langsung dari folder `modul-11-database-dasar/` yang sudah diuji; screenshot diambil dari aplikasi yang berjalan.
