from src import read, method, migration, between, asset

M = 'modul-11-database-dasar'
CTRL = 'app/Http/Controllers/EmployeeController.php'

META = {
    'no': '11',
    'title_lines': ['Database', 'Tahap Dasar', 'di Laravel 13'],
    'chips': ['mysql', 'migration', 'seeder', 'raw sql', 'query builder'],
    'grid': {
        'PERANGKAT': 'PHP 8.3+, Composer, Node.js 20.19+ atau 22.12+, MySQL atau MariaDB, Git',
        'FILE PENDUKUNG': 'Tidak ada. Modul ini memakai project hasil Modul 10',
        'PRASYARAT': 'Modul 10: Pengenalan Controller dan View pada Laravel',
        'DIPERBARUI': '22 November 2026',
    },
    'doc_title': 'Modul 11 Praktikum: Laravel Database Tahap Dasar',
}

ENV_BEFORE = '''DB_CONNECTION=sqlite
# DB_HOST=127.0.0.1
# DB_PORT=3306
# DB_DATABASE=laravel
# DB_USERNAME=root
# DB_PASSWORD='''

ENV_AFTER = '''DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=data_master
DB_USERNAME=root
DB_PASSWORD='''


def fill(b):
    # ------------------------------------------------------------------ 1
    b.h1('1. Pengantar')
    b.p('Praktikum ini melanjutkan Modul 10. Pada Modul 10, tabel karyawan masih berisi data yang ditulis langsung di view, '
        'dan form Create Employee hanya menampilkan kembali data yang dikirim. Pada modul ini data tersebut dipindahkan ke '
        'database MySQL, sehingga aplikasi "Data Master" dapat menampilkan, menambah, melihat detail, dan menghapus data karyawan.')
    b.p('Struktur tabel dibuat dengan **migration**, data awal diisi dengan **seeder**, lalu data dibaca dan diubah dari '
        'controller melalui dua cara: **raw SQL query** (perintah SQL ditulis langsung) dan **query builder** (perintah SQL '
        'disusun dengan method PHP).')
    b.h2('1.1 Tujuan praktikum')
    b.bullets([
        'Menghubungkan project Laravel ke database MySQL melalui file `.env`.',
        'Membuat struktur tabel yang saling berelasi (one-to-many) dengan migration.',
        'Mengisi data awal dengan seeder.',
        'Menampilkan, menambah, menampilkan detail, dan menghapus data dengan raw SQL query dan query builder.',
    ])
    b.h2('1.2 Hasil akhir tiap bab')
    b.table(['Bab', 'Hasil', 'URL atau perintah', 'Cara mengakses data'], [
        ['3', 'Database `data_master` terhubung', '`.env`', '-'],
        ['4', 'Tabel `positions` dan `employees`', '`php artisan migrate`', 'Migration'],
        ['5', 'Data awal 3 posisi dan 3 karyawan', '`php artisan db:seed`', 'Seeder (query builder)'],
        ['6', 'Employee List dari database', '`/employees`', 'Raw SQL query'],
        ['7', 'Create Employee tersimpan ke database', '`/employees/create`', 'Raw SQL dan query builder'],
        ['8', 'Detail Employee', '`/employees/{id}`', 'Raw SQL query'],
        ['9', 'Hapus Employee', 'tombol hapus di `/employees`', 'Query builder'],
    ], [700, 3100, 2900, 2938])
    b.h2('1.3 Prasyarat')
    b.p('Anda sudah menyelesaikan Modul 10, termasuk halaman Employee List dan form Create Employee. Tidak ada file '
        'pendukung tambahan. Selain perangkat Modul 10, modul ini membutuhkan server database MySQL atau MariaDB beserta phpMyAdmin.')
    b.table(['Perangkat', 'Versi minimum', 'Perintah pengecekan'], [
        ['PHP', '8.3', '`php -v`'],
        ['Composer', '2.x', '`composer -V`'],
        ['Node.js', '20.19 atau 22.12', '`node -v`'],
        ['MySQL atau MariaDB', 'MySQL 8.0 atau MariaDB 10.3', 'phpMyAdmin, menu Home'],
        ['Git', 'versi terbaru', '`git --version`'],
    ], [2600, 3000, 4038])
    b.note('laravel13', 'Laravel 13 membutuhkan PHP 8.3 atau lebih baru, sedangkan XAMPP versi terakhir masih membawa PHP 8.2. '
           'Karena itu XAMPP hanya dipakai untuk menjalankan MySQL (MariaDB) dan phpMyAdmin. Perintah `php artisan` tetap '
           'dijalankan dengan PHP yang sudah dipakai sejak Modul 09 (misalnya dari Laravel Herd atau Laragon), bukan PHP bawaan XAMPP.')
    b.h2('1.4 Cara memakai modul')
    b.bullets([
        'Kerjakan bab secara berurutan. Setiap bab melanjutkan hasil bab sebelumnya.',
        'Blok kode dapat disalin langsung. Perintah terminal ditulis tanpa tanda prompt.',
        'Bagian **Hasil yang diharapkan** dipakai untuk memeriksa pekerjaan Anda. Screenshot dari hasil itu juga menjadi bahan laporan.',
        'Setelah menyimpan file PHP atau Blade, halaman di browser terkadang baru berubah 2–3 detik kemudian. Tunggu sebentar, lalu muat ulang (refresh) halaman.',
        'Soal berlabel **Pertanyaan** dijawab dalam laporan praktikum.',
    ])

    # ------------------------------------------------------------------ 2
    b.h1('2. Persiapan project')
    b.p('Bab ini menyiapkan salinan project Modul 10 sebagai titik awal, sehingga project Modul 10 yang sudah di-upload tetap utuh.')
    b.h2('2.1 Salin project dan arahkan halaman utama')
    b.p('Salin folder project Modul 10 menjadi folder baru bernama `modul11`, lalu hapus folder `.git` di dalam salinan. '
        'Penyalinan boleh dilakukan lewat File Explorer atau Finder. Di macOS dan Linux, perintahnya sebagai berikut.')
    b.code('BASH', 'cp -R modul10 modul11\ncd modul11\nrm -rf .git')
    b.note('catatan', 'Folder `.git` dihapus agar salinan ini nanti di-upload ke repository GitHub baru, bukan ke repository Modul 10. '
           'Jika folder `vendor` atau `node_modules` tidak ikut tersalin, jalankan `composer install` dan `npm install` di folder `modul11`.')
    b.p('Mulai modul ini, halaman utama langsung diarahkan ke Employee List. Buka `routes/web.php`, lalu ganti route `/` '
        'bawaan (yang menampilkan view welcome) dengan baris berikut. `Route::redirect()` sudah dipelajari pada Modul 09.')
    b.code('PHP', "Route::redirect('/', '/employees');")
    b.h2('2.2 Jalankan aplikasi')
    b.p('Buka dua terminal di folder project, lalu jalankan satu perintah di tiap terminal. Biarkan keduanya tetap berjalan sampai praktikum selesai.')
    b.code('BASH', '# Terminal 1: Vite\nnpm run dev')
    b.code('BASH', '# Terminal 2: server Laravel\nphp artisan serve')
    b.p('Buka `http://localhost:8000`. Browser langsung diarahkan ke `/employees`, dan halaman masih menampilkan tiga karyawan yang ditulis langsung di view, sama seperti akhir Modul 10.')

    # ------------------------------------------------------------------ 3
    b.h1('3. Database dan konfigurasi')
    b.p('Laravel tidak membuat server database sendiri. Server MySQL dijalankan lewat XAMPP (atau aplikasi sejenis), '
        'database dibuat lewat phpMyAdmin, lalu Laravel diberi tahu cara terhubung melalui file `.env`.')
    b.h2('3.1 Jalankan MySQL')
    b.steps([
        'Buka XAMPP Control Panel.',
        'Klik **Start** pada baris **Apache** (dibutuhkan oleh phpMyAdmin) dan baris **MySQL**.',
        'Buka `http://localhost/phpmyadmin` di browser.',
    ])
    b.h2('3.2 Buat database data_master')
    b.p('Di phpMyAdmin, buka tab **Databases**, isi nama database `data_master`, lalu klik **Create**.')
    b.image(asset('phpmyadmin.png'), 'Membuat database data_master melalui tab Databases di phpMyAdmin.',
            'Tab Databases di phpMyAdmin dengan isian nama database dan tombol Create', width_cm=12)
    b.p('Cara lain, buka tab **SQL** di phpMyAdmin lalu jalankan perintah berikut.')
    b.code('SQL', 'CREATE DATABASE data_master;')
    b.h2('3.3 Atur file .env')
    b.p('Buka file `.env` di folder project, lalu cari bagian konfigurasi database. Pada Laravel 13 isi bawaannya seperti '
        'berikut: `DB_CONNECTION` bernilai `sqlite`, dan lima baris di bawahnya masih diawali tanda `#` (dikomentari).')
    b.code('ENV', ENV_BEFORE, label='ENV · SEBELUM')
    b.p('Ubah `DB_CONNECTION` menjadi `mysql`, hapus tanda `#` di depan kelima baris tersebut, lalu isi `DB_DATABASE` '
        'dengan `data_master`. Hasilnya seperti berikut.')
    b.code('ENV', ENV_AFTER, label='ENV · SESUDAH')
    b.note('laravel13', 'Jika hanya `DB_DATABASE` yang diubah, Laravel tetap memakai SQLite dan mencari file bernama data_master, '
           'sehingga muncul error `Database file at path [data_master] does not exist`. Pastikan `DB_CONNECTION` sudah bernilai `mysql`.')
    b.p('Nilai `DB_USERNAME=root` dan `DB_PASSWORD` kosong adalah bawaan XAMPP. Sesuaikan jika server MySQL Anda memakai user atau password lain.')
    b.h2('3.4 Hasil yang diharapkan')
    b.p('Jalankan perintah berikut. Laravel menampilkan ringkasan koneksi dengan baris `MySQL`, `Connection mysql`, dan `Database data_master`.')
    b.code('BASH', 'php artisan db:show')
    b.note('perhatian', 'Setelah langkah ini, semua halaman aplikasi menampilkan error `Table \'data_master.sessions\' doesn\'t exist`. '
           'Laravel 13 menyimpan session, cache, dan antrean (queue) di database, sedangkan database data_master masih kosong. '
           'Error ini normal dan hilang setelah `php artisan migrate` dijalankan pada Bab 4.')
    b.h2('3.5 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap langkah yang Anda kerjakan pada bab ini.',
        'Jelaskan arti setiap variabel `DB_*` pada file `.env`. Mengapa `DB_CONNECTION` harus diubah, padahal yang dipakai adalah database bernama data_master?',
    ])

    # ------------------------------------------------------------------ 4
    b.h1('4. Membuat tabel dengan migration')
    b.p('Migration adalah file PHP yang mendefinisikan struktur tabel. Karena berupa kode, struktur database dapat dibuat '
        'ulang di komputer lain cukup dengan satu perintah, tanpa membuat tabel satu per satu lewat phpMyAdmin.')
    b.h2('4.1 Rancangan tabel')
    b.p('Aplikasi memakai dua tabel. Setiap karyawan memiliki satu posisi, dan satu posisi dapat dimiliki banyak karyawan. '
        'Hubungan ini disebut **one-to-many** dan diwujudkan oleh kolom `position_id` pada tabel `employees`.')
    b.image(asset('erd.png'), 'Rancangan tabel employees dan positions.', 'Diagram tabel employees dan positions dengan relasi position_id ke id',
            border=False)
    b.h2('4.2 Migration tabel positions')
    b.p('Buat file migration untuk tabel `positions`.')
    b.code('BASH', 'php artisan make:migration create_positions_table')
    b.p('Laravel membuat file baru di folder `database/migrations/` dengan nama berawalan tanggal dan jam, misalnya '
        '`2026_11_22_000214_create_positions_table.php`. Sesuaikan isinya seperti berikut.')
    b.code('PHP', migration(M, 'positions'))
    b.h2('4.3 Migration tabel employees')
    b.p('Buat file migration untuk tabel `employees` **setelah** migration positions.')
    b.code('BASH', 'php artisan make:migration create_employees_table')
    b.code('PHP', migration(M, 'employees'))
    b.p('`foreignId(\'position_id\')->constrained()` membuat kolom `position_id` sekaligus foreign key yang merujuk kolom `id` '
        'pada tabel `positions`. Nama tabel tujuan ditebak Laravel dari nama kolom.')
    b.note('perhatian', 'Laravel menjalankan migration sesuai urutan tanggal dan jam pada nama file. Karena tabel employees '
           'merujuk tabel positions, migration positions harus dibuat lebih dulu. Jika urutannya terbalik, `php artisan migrate` '
           'gagal karena tabel positions belum ada.')
    b.h2('4.4 Jalankan migration')
    b.code('BASH', 'php artisan migrate')
    b.p('Perintah ini menjalankan semua migration yang belum pernah dijalankan: tiga migration bawaan Laravel dan dua migration yang baru dibuat.')
    b.h2('4.5 Hasil yang diharapkan')
    b.bullets([
        'Terminal menampilkan lima baris migration berstatus `DONE`.',
        'Di phpMyAdmin, database data_master berisi tabel `employees` dan `positions`, ditambah tabel bawaan Laravel 13: `users`, '
        '`password_reset_tokens`, `sessions`, `cache`, `cache_locks`, `jobs`, `job_batches`, `failed_jobs`, dan `migrations`.',
        'Halaman aplikasi tidak lagi menampilkan error tabel `sessions`.',
    ])
    b.h2('4.6 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Apa fungsi method `up()` dan `down()` pada file migration? Kapan method `down()` dijalankan?',
        'Tunjukkan struktur tabel employees di phpMyAdmin (tab Structure), termasuk foreign key `position_id`.',
    ])

    # ------------------------------------------------------------------ 5
    b.h1('5. Mengisi data awal dengan seeder')
    b.p('Seeder adalah class yang mengisi tabel dengan data awal atau data contoh. Seeder pada modul ini memakai '
        '`DB::table()->insert()`, yaitu query builder untuk perintah INSERT.')
    b.h2('5.1 Buat seeder positions dan employees')
    b.p('Buat dua file seeder, satu untuk setiap tabel.')
    b.code('BASH', 'php artisan make:seeder PositionSeeder\nphp artisan make:seeder EmployeeSeeder')
    b.p('Sesuaikan isi `database/seeders/PositionSeeder.php` seperti berikut.')
    b.code('PHP', read(M, 'database/seeders/PositionSeeder.php'))
    b.p('Sesuaikan isi `database/seeders/EmployeeSeeder.php` seperti berikut. Nilai `position_id` 1, 2, dan 3 merujuk tiga posisi dari PositionSeeder.')
    b.code('PHP', read(M, 'database/seeders/EmployeeSeeder.php'))
    b.h2('5.2 Daftarkan seeder')
    b.p('`DatabaseSeeder` adalah seeder utama yang dijalankan oleh `php artisan db:seed`. Ganti **seluruh** isi '
        '`database/seeders/DatabaseSeeder.php` dengan kode berikut. Isi bawaannya (membuat user "Test User") tidak dipakai pada modul ini.')
    b.code('PHP', read(M, 'database/seeders/DatabaseSeeder.php'))
    b.p('Urutan di dalam `call()` penting: PositionSeeder harus dijalankan lebih dulu karena data karyawan merujuk id posisi.')
    b.h2('5.3 Jalankan seeder')
    b.code('BASH', 'php artisan db:seed')
    b.note('perhatian', 'Jalankan `php artisan db:seed` cukup sekali. Jika dijalankan lagi, data positions terduplikasi dan '
           'EmployeeSeeder gagal karena kolom email harus unik (`Duplicate entry`). Untuk mengulang dari awal, jalankan '
           '`php artisan migrate:fresh --seed`. Perintah ini menghapus semua tabel, menjalankan ulang migration, lalu menjalankan seeder.')
    b.h2('5.4 Hasil yang diharapkan')
    b.p('Di phpMyAdmin, tabel `positions` berisi tiga baris (FE, BE, SA) dan tabel `employees` berisi tiga baris (Purnama, '
        'Adzanil, Berlian). Kolom `created_at` dan `updated_at` bernilai NULL karena `DB::table()->insert()` tidak mengisinya otomatis.')
    b.h2('5.5 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Apa yang terjadi jika urutan PositionSeeder dan EmployeeSeeder di dalam `call()` ditukar? Coba, lalu jelaskan hasilnya.',
    ])

    # ------------------------------------------------------------------ 6
    b.h1('6. Menampilkan list data (raw SQL query)')
    b.p('Halaman Employee List kini membaca data dari database. Query ditulis sebagai teks SQL biasa lalu dijalankan dengan `DB::select()`.')
    b.image(asset('flow11.png'), 'Alur data dari MySQL ke halaman Employee List.', 'Diagram alur Browser, Route, EmployeeController, MySQL, dan View',
            border=False)
    b.h2('6.1 Isi method index')
    b.p('Buka `app/Http/Controllers/EmployeeController.php`. Tambahkan import Facade DB di bagian atas file.')
    b.code('PHP', 'use Illuminate\\Support\\Facades\\DB;')
    b.p('Ganti method `index()` dengan kode berikut.')
    b.code('PHP', method(M, CTRL, 'index'))
    b.p('Kedua tabel sama-sama memiliki kolom `id`. Karena itu query memberi nama lain (alias) `employee_id` untuk id karyawan '
        'dan `position_name` untuk nama posisi, agar keduanya tidak tertukar saat dibaca di view.')
    b.h2('6.2 Tampilkan data di view')
    b.p('Buka `resources/views/employee/index.blade.php`. Ganti seluruh elemen `<table>` yang berisi data contoh dengan kode berikut. '
        'Kolom **Position** ditambahkan, dan baris tabel kini dibuat oleh `@foreach`.')
    b.code('HTML', between(read(M, 'resources/views/employee/index.blade.php'), '<table class=', '</table>'))
    b.h2('6.3 Hasil yang diharapkan', page_break=True)
    b.p('Buka `/employees`. Tabel menampilkan tiga karyawan dari database lengkap dengan nama posisinya.')
    b.image(asset('m11-list.png'), 'Halaman /employees dengan data dari database.', 'Tabel Employee List dengan kolom Position berisi data dari database')
    b.h2('6.4 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Apa perbedaan `left join` dan `join` (inner join)? Kapan hasil keduanya berbeda?',
    ])

    # ------------------------------------------------------------------ 7
    b.h1('7. Menambah data (insert)')
    b.p('Form Create Employee kini memiliki pilihan Position yang diambil dari database, dan data yang valid disimpan ke tabel employees.')
    b.h2('7.1 Isi method create')
    b.p('Ganti method `create()` dengan kode berikut. Daftar posisi dikirim ke view bersama judul halaman.')
    b.code('PHP', method(M, CTRL, 'create'))
    b.h2('7.2 Tambahkan pilihan Position di view')
    b.p('Buka `resources/views/employee/create.blade.php`. Tambahkan kode berikut tepat setelah `div` berisi input Age, '
        'masih di dalam `div class="row"` yang sama.')
    b.code('HTML', '''<div class="col-md-12 mb-3">
    <label for="position" class="form-label">Position</label>
    <select name="position" id="position" class="form-select">
        @foreach ($positions as $position)
            <option value="{{ $position->id }}" {{ old('position') == $position->id ? 'selected' : '' }}>{{ $position->code.' - '.$position->name }}</option>
        @endforeach
    </select>
    @error('position')
        <div class="text-danger"><small>{{ $message }}</small></div>
    @enderror
</div>''')
    b.p('`old(\'position\') == $position->id` membuat pilihan yang terakhir dikirim tetap terpilih ketika form kembali karena validasi gagal.')
    b.h2('7.3 Isi method store')
    b.p('Ganti method `store()` dengan kode berikut. Validasinya sama dengan Modul 10. Bedanya, data yang lolos validasi kini '
        'disimpan dengan query builder `DB::table()->insert()`, lalu pengguna diarahkan kembali ke Employee List.')
    b.code('PHP', method(M, CTRL, 'store'))
    b.h2('7.4 Uji form')
    b.p('Buka `http://localhost:8000/employees/create`, lalu coba kasus berikut.')
    b.table(['Kasus', 'Isian', 'Hasil yang diharapkan'], [
        ['Input benar', 'First Name `Budi`, Last Name `Santoso`, Email `budi@example.com`, Age `30`, Position `BE`',
         'Kembali ke `/employees`, baris Budi Santoso (Back End Developer) muncul di tabel'],
        ['Input salah', 'Email `budi-email`, Age `dua puluh`, nama dikosongkan',
         'Form tampil lagi dengan pesan error; Position yang dipilih tetap terpilih'],
        ['Email sudah ada', 'Ulangi kasus pertama dengan email yang sama',
         'Error `Integrity constraint violation`, lihat catatan di bawah'],
    ], [1900, 4000, 3738])
    b.image(asset('m11-create.png'), 'Form Create Employee dengan pilihan Position dari database.',
            'Form Create Employee berisi input nama, email, umur, dan pilihan Position', width_cm=13)
    b.note('catatan', 'Aturan validasi belum memeriksa apakah email sudah terdaftar, sedangkan kolom email bersifat unik. '
           'Akibatnya, email yang sama ditolak oleh database, bukan oleh validasi. Pencegahannya adalah aturan '
           '`unique:employees,email` pada field email, yang dibahas pada soal 2 di bawah.')
    b.h2('7.5 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Tambahkan aturan `unique:employees,email` pada field email beserta pesan error-nya. Tunjukkan hasilnya ketika email yang sama disimpan dua kali.',
        'Mengapa method `store()` diakhiri dengan `redirect()->route(\'employees.index\')`, bukan `view()`?',
    ])

    # ------------------------------------------------------------------ 8
    b.h1('8. Menampilkan detail data')
    b.p('Tombol detail (ikon kartu) pada Employee List membuka `/employees/{id}`. Laravel meneruskan nilai id dari URL ke method `show()`.')
    b.h2('8.1 Isi method show', page_break=True)
    b.code('PHP', method(M, CTRL, 'show'))
    b.p('Tanda `?` adalah parameter binding: nilai `$id` dikirim terpisah dari teks SQL, sehingga aman dari SQL injection. '
        '`DB::select()` selalu menghasilkan array, sehingga `collect(...)->first()` dipakai untuk mengambil satu baris saja.')
    b.h2('8.2 Buat view detail')
    b.p('Buat file `resources/views/employee/show.blade.php` dengan isi berikut.')
    b.code('HTML', read(M, 'resources/views/employee/show.blade.php'))
    b.h2('8.3 Hasil yang diharapkan')
    b.p('Klik tombol detail pada baris Purnama. Halaman menampilkan nama, email, umur, dan posisi karyawan tersebut.')
    b.image(asset('m11-show.png'), 'Halaman detail karyawan /employees/1.', 'Halaman Detail Employee berisi First Name, Last Name, Email, Age, dan Position',
            width_cm=12)
    b.note('catatan', 'Jika id tidak ditemukan (misalnya `/employees/999`), `$employee` bernilai null dan halaman menampilkan error '
           '`Attempt to read property "firstname" on null`. Cara menanganinya dibahas pada Modul 12.')
    b.h2('8.4 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Apa risikonya jika `$id` digabung langsung ke teks SQL, misalnya `"... where employees.id = " . $id`?',
    ])

    # ------------------------------------------------------------------ 9
    b.h1('9. Menghapus data')
    b.p('Tombol hapus (ikon tempat sampah) sudah ada sejak Modul 10. Tombol itu berada di dalam form yang memakai `@csrf` dan '
        '`@method(\'delete\')`, sehingga permintaannya diteruskan ke method `destroy()`.')
    b.h2('9.1 Isi method destroy')
    b.code('PHP', method(M, CTRL, 'destroy'))
    b.p('Untuk menguji, klik tombol hapus pada baris karyawan yang Anda tambahkan di Bab 7. Halaman kembali ke `/employees` dan baris tersebut hilang dari tabel dan dari phpMyAdmin.')
    b.h2('9.2 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Apa yang terjadi jika baris `->where(\'id\', $id)` dihapus dari method `destroy()`? Jawab tanpa mencobanya.',
    ])

    # ------------------------------------------------------------------ 10
    b.h1('10. Pemecahan masalah')
    b.p('Periksa tabel ini lebih dulu sebelum bertanya. Sebagian besar kendala berasal dari konfigurasi `.env` atau urutan migration dan seeder.')
    b.table(['Gejala', 'Penyebab', 'Solusi'], [
        ['`Database file at path [data_master] does not exist`', '`DB_CONNECTION` masih `sqlite`', 'Ubah menjadi `mysql` dan hapus tanda `#` pada baris `DB_*` (subbab 3.3)'],
        ['`Table \'data_master.sessions\' doesn\'t exist`', 'Migration belum dijalankan', 'Jalankan `php artisan migrate`'],
        ['`SQLSTATE[HY000] [2002] Connection refused`', 'Server MySQL belum berjalan', 'Start MySQL di XAMPP Control Panel'],
        ['`Unknown database \'data_master\'`', 'Database belum dibuat atau namanya berbeda', 'Buat database di phpMyAdmin (subbab 3.2)'],
        ['`Access denied for user \'root\'`', 'Username atau password tidak sesuai', 'Samakan `DB_USERNAME` dan `DB_PASSWORD` dengan server MySQL'],
        ['Migration employees gagal karena tabel positions belum ada', 'Migration employees dibuat lebih dulu', 'Hapus kedua file migration, lalu buat ulang dengan urutan positions, kemudian employees'],
        ['`Duplicate entry` saat `db:seed`', 'Seeder dijalankan lebih dari sekali', 'Jalankan `php artisan migrate:fresh --seed`'],
        ['Error `Class "App\\Http\\Controllers\\DB" not found`', 'Import Facade DB belum ada', 'Tambahkan `use Illuminate\\Support\\Facades\\DB;` di atas controller'],
        ['Error `Undefined variable $positions`', 'Method `create()` belum mengirim `$positions`', 'Periksa subbab 7.1'],
        ['`Integrity constraint violation` saat menyimpan', 'Email sudah terdaftar', 'Pakai email lain, atau tambahkan aturan `unique` (soal 7.5)'],
        ['Tombol edit menampilkan halaman kosong', 'Method `edit()` belum diisi', 'Hal ini wajar. Fitur edit adalah bagian dari tugas (subbab 11.1)'],
    ], [3400, 2900, 3338])

    # ------------------------------------------------------------------ 11
    b.h1('11. Tugas dan pengumpulan')
    b.h2('11.1 Tugas')
    b.p('Kerjakan seluruh tugas berikut secara individu.')
    b.steps([
        'Praktikkan seluruh poin praktikum dan jawab semua soal **Pertanyaan** pada Bab 3 sampai Bab 9.',
        'Buat fitur **Edit**: isi method `edit()` dan `update()` pada EmployeeController, lalu buat view '
        '`resources/views/employee/edit.blade.php` berisi form yang terisi data lama. Tombol edit pada Employee List harus '
        'membuka form tersebut, dan perubahan tersimpan ke database. File ini dipakai lagi pada Modul 12.',
        'Ubah semua query yang ditulis dengan raw SQL query (method `index()`, `create()`, dan `show()`) menjadi query builder.',
        'Dokumentasikan semuanya dalam bentuk laporan praktikum (PDF). Isinya screenshot kode program, screenshot output di browser, dan jawaban pertanyaan.',
        'Unggah project Laravel hasil praktikum ke GitHub.',
    ])
    b.p('Petunjuk tugas 3: setiap bagian raw SQL memiliki padanan method query builder berikut.')
    b.table(['Raw SQL', 'Query builder'], [
        ['`select * from positions`', '`DB::table(\'positions\')->get()`'],
        ['`left join positions on employees.position_id = positions.id`', '`->leftJoin(\'positions\', \'employees.position_id\', \'=\', \'positions.id\')`'],
        ['`select *, employees.id as employee_id`', '`->select(\'*\', \'employees.id as employee_id\')`'],
        ['`where employees.id = ?` lalu ambil satu baris', '`->where(\'employees.id\', $id)->first()`'],
    ], [4500, 5138])
    b.h2('11.2 Unggah project ke GitHub')
    b.steps([
        'Buat repository **public** baru di akun GitHub Anda. Jangan menambahkan README, `.gitignore`, atau license, agar tidak terjadi konflik saat push pertama.',
        'Di folder project, jalankan perintah berikut. Ganti `<URL repository>` dengan alamat repository yang baru dibuat.',
    ])
    b.code('BASH', 'git init\ngit add .\ngit commit -m "Modul 11"\ngit branch -M main\ngit remote add origin <URL repository>\ngit push -u origin main')
    b.p('Folder `vendor`, folder `node_modules`, dan file `.env` tidak perlu dihapus. Ketiganya otomatis diabaikan oleh `.gitignore` '
        'bawaan Laravel, sehingga tidak ikut ter-upload. Karena `.env` tidak ikut, konfigurasi database tidak tersimpan di GitHub.')
    b.h2('11.3 Pengumpulan')
    b.p('Cantumkan URL repository pada laporan praktikum. Kumpulkan laporan (.pdf) melalui LMS, paling lambat sebelum jadwal praktikum minggu depan.')
    b.h2('11.4 Daftar periksa sebelum mengumpulkan')
    b.checks([
        '`php artisan migrate:fresh --seed` berjalan tanpa error.',
        'Halaman `/employees`, `/employees/create`, dan `/employees/{id}` dapat dibuka tanpa error.',
        'Tambah, edit, dan hapus karyawan tersimpan ke database (cek di phpMyAdmin).',
        'Tidak ada lagi `DB::select()` di EmployeeController (tugas 3).',
        'Jawaban semua soal Pertanyaan ada di laporan, lengkap dengan screenshot.',
        'Repository GitHub berstatus public, dan URL-nya tercantum di laporan PDF.',
    ])
