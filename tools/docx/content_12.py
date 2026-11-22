from src import read, method, between, asset

M = 'modul-12-database-lanjut'
CTRL = 'app/Http/Controllers/EmployeeController.php'
V = 'resources/views/'

META = {
    'no': '12',
    'title_lines': ['Database', 'Tahap Lanjut', 'di Laravel 13'],
    'chips': ['eloquent', 'relationship', 'crud', 'blade layout'],
    'grid': {
        'PERANGKAT': 'PHP 8.3+, Composer, Node.js 20.19+ atau 22.12+, MySQL atau MariaDB, Git',
        'FILE PENDUKUNG': 'Tidak ada. Modul ini memakai project hasil Modul 11',
        'PRASYARAT': 'Modul 11: Laravel Database Tahap Dasar',
        'DIPERBARUI': '22 November 2026',
    },
    'doc_title': 'Modul 12 Praktikum: Laravel Database Tahap Lanjut (Eloquent ORM dan Blade Templates)',
}


def fill(b):
    # ------------------------------------------------------------------ 1
    b.h1('1. Pengantar')
    b.p('Praktikum ini melanjutkan Modul 11. Pada Modul 11 data karyawan dibaca dan diubah dengan raw SQL query dan query '
        'builder. Pada modul ini semua query tersebut diganti dengan **Eloquent ORM**, yaitu cara Laravel memperlakukan setiap '
        'tabel sebagai class (model) dan setiap baris sebagai object.')
    b.p('Bagian kedua modul merapikan view dengan **Blade templates**. Navbar dan kerangka HTML yang selama ini disalin ke '
        'setiap file dipindahkan ke satu layout, sehingga perubahan navbar cukup dilakukan di satu tempat.')
    b.h2('1.1 Tujuan praktikum')
    b.bullets([
        'Membuat model Eloquent dan mendefinisikan relasi one-to-many (`hasMany` dan `belongsTo`).',
        'Menampilkan, menambah, mengubah, dan menghapus data dengan Eloquent (CRUD lengkap).',
        'Memisahkan bagian view yang berulang dengan `@include`.',
        'Membuat layout utama dengan `@yield`, lalu memakainya di setiap halaman dengan `@extends` dan `@section`.',
    ])
    b.h2('1.2 Hasil akhir tiap bab')
    b.table(['Bab', 'Hasil', 'URL atau file', 'Materi'], [
        ['3', 'Model Position dan Employee', '`app/Models/`', 'Model dan relasi'],
        ['4', 'Employee List dengan Eloquent', '`/employees`', '`all()` dan relasi'],
        ['5', 'Create Employee dengan Eloquent', '`/employees/create`', '`new` dan `save()`'],
        ['6', 'Detail Employee dengan Eloquent', '`/employees/{id}`', '`find()`'],
        ['7', 'Fitur Edit Employee', '`/employees/{id}/edit`', '`find()` dan `save()`'],
        ['8', 'Hapus Employee dengan Eloquent', 'tombol hapus', '`delete()`'],
        ['9', 'Layout, navbar, dan actions terpisah', '`resources/views/layouts/`', '`@yield` dan `@include`'],
        ['10', 'Semua halaman memakai layout', 'semua halaman', '`@extends` dan `@section`'],
    ], [700, 3300, 3000, 2638])
    b.h2('1.3 Prasyarat')
    b.p('Anda sudah menyelesaikan Modul 11: database data_master berisi tabel positions dan employees, dan halaman Employee '
        'List, Create Employee, serta Detail Employee berjalan. Perangkat yang dibutuhkan sama dengan Modul 11, dan tidak ada file pendukung tambahan.')
    b.table(['Perangkat', 'Versi minimum', 'Perintah pengecekan'], [
        ['PHP', '8.3', '`php -v`'],
        ['Composer', '2.x', '`composer -V`'],
        ['Node.js', '20.19 atau 22.12', '`node -v`'],
        ['MySQL atau MariaDB', 'MySQL 8.0 atau MariaDB 10.3', 'phpMyAdmin, menu Home'],
        ['Git', 'versi terbaru', '`git --version`'],
    ], [2600, 3000, 4038])
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
    b.p('Bab ini menyiapkan salinan project Modul 11 dan memastikan database berisi data awal.')
    b.h2('2.1 Salin project Modul 11')
    b.p('Salin folder project Modul 11 menjadi folder baru bernama `modul12`, lalu hapus folder `.git` di dalam salinan, '
        'sama seperti persiapan Modul 11. Di macOS dan Linux, perintahnya sebagai berikut.')
    b.code('BASH', 'cp -R modul11 modul12\ncd modul12\nrm -rf .git')
    b.p('File `.env` ikut tersalin, sehingga project baru tetap terhubung ke database data_master.')
    b.h2('2.2 Siapkan database dan jalankan aplikasi')
    b.p('Pastikan MySQL berjalan di XAMPP Control Panel. Kembalikan isi database ke data awal agar hasil praktikum sama dengan modul.')
    b.code('BASH', 'php artisan migrate:fresh --seed')
    b.p('Jalankan aplikasi di dua terminal, lalu buka `http://localhost:8000`. Halaman utama langsung diarahkan ke `/employees` (diatur pada Modul 11), dan tabel menampilkan tiga karyawan seperti akhir Modul 11.')
    b.code('BASH', '# Terminal 1: Vite\nnpm run dev')
    b.code('BASH', '# Terminal 2: server Laravel\nphp artisan serve')

    # ------------------------------------------------------------------ 3
    b.h1('3. Model dan relasi')
    b.p('Model adalah class PHP yang mewakili satu tabel. Laravel menebak nama tabel dari nama model: model `Position` '
        'memakai tabel `positions`, dan model `Employee` memakai tabel `employees`. Relasi antartabel ditulis sebagai method di dalam model.')
    b.image(asset('rel12.png'), 'Relasi one-to-many antara model Position dan Employee.',
            'Diagram relasi Position hasMany Employee dan Employee belongsTo Position', border=False)
    b.h2('3.1 Buat model')
    b.code('BASH', 'php artisan make:model Position\nphp artisan make:model Employee')
    b.note('laravel13', 'File model hasil `make:model` di Laravel 13 hanya berisi kelas kosong tanpa baris `use HasFactory;`. '
           'Ganti isinya dengan kode pada subbab 3.2. Trait HasFactory tetap tersedia, sehingga kode berjalan normal.')
    b.h2('3.2 Tulis relasi pada model')
    b.p('Satu posisi dimiliki banyak karyawan. Tambahkan method `employees()` (bentuk jamak) yang mengembalikan `hasMany()`. '
        'Sesuaikan isi `app/Models/Position.php` seperti berikut.')
    b.code('PHP', read(M, 'app/Models/Position.php'))
    b.p('Setiap karyawan memiliki satu posisi. Tambahkan method `position()` (bentuk tunggal) yang mengembalikan `belongsTo()`. '
        'Eloquent mencari kolom `position_id` pada tabel employees dari nama method ini. Sesuaikan isi `app/Models/Employee.php`.')
    b.code('PHP', read(M, 'app/Models/Employee.php'))
    b.h2('3.3 Uji relasi dengan Tinker')
    b.p('Tinker adalah konsol interaktif Laravel. Jalankan perintah berikut, lalu ketik dua baris kode di bawahnya satu per satu.')
    b.code('BASH', 'php artisan tinker')
    b.code('PHP', "App\\Models\\Employee::find(2)->position->name\nApp\\Models\\Position::find(3)->employees->pluck('firstname')", label='TINKER')
    b.p('Baris pertama menghasilkan `"Back End Developer"`, dan baris kedua menghasilkan daftar berisi `"Berlian"`. Ketik `exit` untuk keluar dari Tinker.')
    b.h2('3.4 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Mengapa method pada model Position bernama `employees()` (jamak), sedangkan pada model Employee bernama `position()` (tunggal)?',
    ])

    # ------------------------------------------------------------------ 4
    b.h1('4. Menampilkan list data dengan Eloquent')
    b.h2('4.1 Ubah method index dan view')
    b.p('Buka `app/Http/Controllers/EmployeeController.php`. Tambahkan import kedua model di bagian atas file.')
    b.code('PHP', 'use App\\Models\\Employee;\nuse App\\Models\\Position;')
    b.p('Ganti method `index()` dengan kode berikut. Satu baris `Employee::all()` menggantikan query `select ... left join` dari Modul 11.')
    b.code('PHP', method(M, CTRL, 'index'))
    b.p('Buka `resources/views/employee/index.blade.php`. Ganti bagian `<tbody>` dengan kode berikut. Nama posisi kini dibaca '
        'lewat relasi `$employee->position->name`, dan id karyawan cukup `$employee->id` tanpa alias.')
    b.code('HTML', '''<tbody>
    @foreach ($employees as $employee)
        <tr>
            <td>{{ $employee->firstname }}</td>
            <td>{{ $employee->lastname }}</td>
            <td>{{ $employee->email }}</td>
            <td>{{ $employee->age }}</td>
            <td>{{ $employee->position->name }}</td>
            <td>
                {{-- ACTIONS SECTION --}}
                <div class="d-flex">
                    <a href="{{ route('employees.show', ['employee' => $employee->id]) }}" class="btn btn-outline-dark btn-sm me-2"><i class="bi-person-lines-fill"></i></a>
                    <a href="{{ route('employees.edit', ['employee' => $employee->id]) }}" class="btn btn-outline-dark btn-sm me-2"><i class="bi-pencil-square"></i></a>

                    <div>
                        <form action="{{ route('employees.destroy', ['employee' => $employee->id]) }}" method="POST">
                            @csrf
                            @method('delete')
                            <button type="submit" class="btn btn-outline-dark btn-sm me-2"><i class="bi-trash"></i></button>
                        </form>
                    </div>
                </div>
            </td>
        </tr>
    @endforeach
</tbody>''')
    b.h2('4.2 Hasil yang diharapkan')
    b.p('Buka `/employees`. Tampilannya sama persis dengan akhir Modul 11, tetapi data kini dibaca melalui Eloquent.')
    b.note('catatan', '`Employee::all()` lalu `$employee->position` di view menjalankan satu query tambahan untuk setiap baris '
           '(dikenal sebagai masalah N+1 query). Dengan tiga karyawan terjadi empat query. Untuk data yang banyak, gunakan '
           'eager loading `Employee::with(\'position\')->get()`, sehingga data posisi diambil sekaligus dan hanya terjadi dua query.')
    b.h2('4.3 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Ganti `Employee::all()` dengan `Employee::with(\'position\')->get()`. Apakah tampilan berubah? Jelaskan perbedaannya berdasarkan catatan di atas.',
    ])

    # ------------------------------------------------------------------ 5
    b.h1('5. Menambah data dengan Eloquent')
    b.h2('5.1 Ubah method create dan store')
    b.p('Ganti method `create()` dan `store()` dengan kode berikut. Validasinya tetap sama. Penyimpanan kini dilakukan dengan '
        'membuat object `Employee`, mengisi propertinya, lalu memanggil `save()`.')
    b.code('PHP', method(M, CTRL, 'create'))
    b.code('PHP', method(M, CTRL, 'store'))
    b.note('catatan', 'Berbeda dengan `DB::table()->insert()` pada Modul 11, method `save()` mengisi kolom created_at dan updated_at secara otomatis.')
    b.h2('5.2 Tampilkan pesan error di setiap field')
    b.p('Buka `resources/views/employee/create.blade.php`. Ganti seluruh elemen `<form>` dengan kode berikut. Kotak alert '
        'di atas form dihapus, dan pesan error kini tampil tepat di bawah field yang salah. Directive `@error` juga menambahkan '
        'class `is-invalid` sehingga field yang salah diberi garis merah.')
    b.code('HTML', between(read(M, V + 'employee/create.blade.php'), '<form action=', '</form>'))
    b.h2('5.3 Hasil yang diharapkan')
    b.bullets([
        'Data yang valid tersimpan dan muncul di Employee List. Di phpMyAdmin, kolom created_at baris tersebut berisi tanggal dan jam.',
        'Data yang salah menampilkan pesan merah di bawah field masing-masing (lihat gambar form Create Employee pada subbab 10.5).',
    ])
    b.h2('5.4 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Bandingkan isi kolom created_at untuk karyawan yang ditambahkan pada Modul 11 dan pada modul ini. Jelaskan penyebab perbedaannya.',
    ])

    # ------------------------------------------------------------------ 6
    b.h1('6. Menampilkan detail data dengan Eloquent')
    b.h2('6.1 Ubah method show dan view')
    b.code('PHP', method(M, CTRL, 'show'))
    b.p('Buka `resources/views/employee/show.blade.php`. Ganti baris yang menampilkan posisi dengan kode berikut. Bagian lain tidak berubah.')
    b.code('HTML', '<h5>{{ $employee->position->name }}</h5>')
    b.note('catatan', 'Jika id tidak ditemukan (misalnya `/employees/999`), `find()` mengembalikan null sehingga halaman menampilkan '
           'error `Attempt to read property "firstname" on null`. Ganti dengan `Employee::findOrFail($id)` agar Laravel menampilkan '
           'halaman 404. Hal yang sama berlaku untuk method edit(), update(), dan destroy().')
    b.h2('6.2 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Terapkan `findOrFail()` pada method `show()`, lalu buka `/employees/999`. Tunjukkan dan jelaskan hasilnya.',
    ])

    # ------------------------------------------------------------------ 7
    b.h1('7. Fitur edit dengan Eloquent')
    b.p('Fitur edit terdiri dari dua method: `edit()` menampilkan form yang terisi data lama, dan `update()` menyimpan perubahan. '
        'Jika fitur ini sudah dibuat pada tugas Modul 11, sesuaikan kodenya dengan bab ini.')
    b.h2('7.1 Isi method edit dan update')
    b.code('PHP', method(M, CTRL, 'edit'))
    b.code('PHP', method(M, CTRL, 'update'))
    b.h2('7.2 Buat view edit')
    b.p('Salin file `resources/views/employee/create.blade.php` menjadi `edit.blade.php` di folder yang sama. Di file baru, ganti '
        'seluruh elemen `<form>` dengan kode berikut. Kerangka halaman (head dan navbar) akan dirapikan pada Bab 10.')
    b.code('HTML', between(read(M, V + 'employee/edit.blade.php'), '<form action=', '</form>'))
    b.p('Form edit berbeda dari form create pada tiga hal:')
    b.bullets([
        '`action` mengarah ke route `employees.update` dengan id karyawan, dan `@method(\'put\')` mengubah permintaan POST menjadi PUT.',
        'Nilai awal setiap input diambil dari data karyawan. Jika validasi gagal (`$errors->any()`), nilai dari `old()` yang dipakai.',
        'Variabel `$selected` menentukan posisi yang terpilih dengan aturan yang sama.',
    ])
    b.h2('7.3 Hasil yang diharapkan')
    b.p('Klik tombol edit (ikon pensil) pada baris Adzanil. Form tampil dengan data Adzanil dan posisi Back End Developer terpilih. '
        'Ubah umur dan posisi, lalu klik **Edit**. Halaman kembali ke Employee List dengan data yang sudah berubah.')
    b.h2('7.4 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Mengapa form edit memakai `@method(\'put\')`? Tunjukkan route yang menerima permintaan tersebut pada hasil `php artisan route:list`.',
    ])

    # ------------------------------------------------------------------ 8
    b.h1('8. Menghapus data dengan Eloquent')
    b.h2('8.1 Ubah method destroy')
    b.code('PHP', method(M, CTRL, 'destroy'))
    b.note('catatan', 'Setelah semua query diganti dengan Eloquent, baris `use Illuminate\\Support\\Facades\\DB;` di EmployeeController '
           'tidak terpakai lagi dan boleh dihapus.')
    b.h2('8.2 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada bab ini.',
        'Tunjukkan isi EmployeeController setelah semua method memakai Eloquent. Method apa saja yang memakai model Position, dan mengapa?',
    ])

    # ------------------------------------------------------------------ 9
    b.h1('9. Blade layout dan include')
    b.p('Sampai bab ini, setiap view berisi kerangka HTML dan navbar yang sama. Bab ini memindahkan bagian yang berulang ke file tersendiri.')
    b.image(asset('blade12.png'), 'Susunan layout Blade yang dipakai semua halaman.',
            'Diagram layouts/app.blade.php berisi include nav dan yield content yang diisi halaman', border=False)
    b.h2('9.1 Navbar')
    b.p('Buat folder `resources/views/layouts/`, lalu buat file `nav.blade.php` dengan isi berikut. Variabel `$currentRouteName` '
        'menyimpan nama route yang sedang dibuka, sehingga menu yang sesuai diberi class `active`.')
    b.code('HTML', read(M, V + 'layouts/nav.blade.php'))
    b.note('catatan', 'Link Employee hanya aktif di halaman Employee List karena kondisinya membandingkan nama route secara persis '
           'dengan employees.index. Agar tetap aktif di halaman create, detail, dan edit, kondisinya dapat diganti dengan '
           '`request()->routeIs(\'employees.*\')` (soal 10.6 nomor 2).')
    b.h2('9.2 Layout utama')
    b.p('Buat file `resources/views/layouts/app.blade.php`. `@include` menyisipkan navbar, dan `@yield(\'content\')` menandai '
        'tempat yang akan diisi oleh setiap halaman.')
    b.code('HTML', read(M, V + 'layouts/app.blade.php'))
    b.h2('9.3 Konten default dan tombol aksi')
    b.p('Buat file `resources/views/default.blade.php`. Konten ini dipakai bersama oleh halaman Home dan My Profile.')
    b.code('HTML', read(M, V + 'default.blade.php'))
    b.p('Buat file `resources/views/employee/actions.blade.php`, lalu pindahkan isi kolom aksi dari `index.blade.php` ke file '
        'ini. Variabel `$employee` tetap terbaca karena file ini di-include dari dalam `@foreach`.')
    b.code('HTML', read(M, V + 'employee/actions.blade.php'))

    # ------------------------------------------------------------------ 10
    b.h1('10. Menerapkan layout pada semua view')
    b.p('Setiap view kini cukup berisi `@extends(\'layouts.app\')` dan bagian `@section(\'content\')`. Kerangka HTML dan navbar '
        'dihapus dari file view, karena sudah disediakan oleh layout.')
    b.h2('10.1 Employee List')
    b.p('Ganti seluruh isi `resources/views/employee/index.blade.php` dengan kode berikut.')
    b.code('HTML', read(M, V + 'employee/index.blade.php'))
    b.h2('10.2 Create Employee')
    b.p('Ganti seluruh isi `resources/views/employee/create.blade.php` dengan kode berikut. Isi form sama dengan subbab 5.2.')
    b.code('HTML', read(M, V + 'employee/create.blade.php'))
    b.h2('10.3 Detail dan Edit Employee')
    b.p('Ganti seluruh isi `resources/views/employee/show.blade.php` dengan kode berikut.')
    b.code('HTML', read(M, V + 'employee/show.blade.php'))
    b.p('Ganti seluruh isi `resources/views/employee/edit.blade.php` dengan kode berikut. Isi form sama dengan subbab 7.2.')
    b.code('HTML', read(M, V + 'employee/edit.blade.php'))
    b.h2('10.4 Home dan My Profile')
    b.p('Ganti seluruh isi `resources/views/home.blade.php` dan `resources/views/profile.blade.php` dengan kode yang sama berikut.')
    b.code('HTML', read(M, V + 'home.blade.php'))
    b.note('catatan', 'Template default.blade.php memakai ikon rumah (bi-house-fill), sehingga halaman My Profile juga '
           'menampilkan ikon rumah, tidak lagi ikon bi-person-circle seperti pada Modul 10.')
    b.h2('10.5 Hasil yang diharapkan')
    b.p('Semua halaman tampil sama seperti sebelumnya, tetapi navbar kini berasal dari satu file. Menu **Home** atau **Employee** '
        'tampil putih terang ketika halamannya sedang dibuka.')
    b.image(asset('m12-home.png'), 'Halaman /home memakai layout dan konten default.', 'Halaman Home dengan navbar dan kotak Well done this is Home')
    b.image(asset('m12-list.png'), 'Halaman /employees dengan menu Employee aktif.', 'Tabel Employee List dengan menu Employee aktif di navbar')
    b.image(asset('m12-create-errors.png'), 'Form Create Employee dengan pesan error di bawah setiap field.',
            'Form Create Employee dengan field bergaris merah dan pesan error', width_cm=13)
    b.image(asset('m12-edit.png'), 'Form Edit Employee yang terisi data Adzanil.', 'Form Edit Employee berisi data karyawan dan tombol Edit', width_cm=13)
    b.h2('10.6 Pertanyaan')
    b.steps([
        'Jelaskan dan dokumentasikan setiap kode program yang Anda kerjakan pada Bab 9 dan Bab 10, termasuk peran `@extends`, `@section`, `@yield`, dan `@include`.',
        'Ubah kondisi pada `nav.blade.php` agar menu Employee tetap aktif di halaman create, detail, dan edit. Tunjukkan hasilnya.',
        'Tambahkan satu menu baru di navbar (misalnya link ke halaman welcome). Berapa file yang perlu diubah? Bandingkan dengan Modul 10.',
    ])

    # ------------------------------------------------------------------ 11
    b.h1('11. Pemecahan masalah')
    b.p('Periksa tabel ini lebih dulu sebelum bertanya. Sebagian besar kendala berasal dari import model, nama relasi, atau lokasi file layout.')
    b.table(['Gejala', 'Penyebab', 'Solusi'], [
        ['Error `Class "App\\Http\\Controllers\\Employee" not found`', 'Import model belum ada', 'Tambahkan `use App\\Models\\Employee;` dan `use App\\Models\\Position;` (subbab 4.1)'],
        ['Error `Attempt to read property "name" on null`', 'Method `position()` belum ditulis di model Employee, atau ada `position_id` yang tidak cocok', 'Periksa subbab 3.2, lalu jalankan `php artisan migrate:fresh --seed`'],
        ['Error `Attempt to read property "firstname" on null`', 'Id karyawan tidak ditemukan', 'Pakai `findOrFail()` (catatan subbab 6.1)'],
        ['Error `View [layouts.app] not found`', 'File layout tidak berada di `resources/views/layouts/`', 'Periksa nama folder dan file pada Bab 9'],
        ['Navbar tampil dua kali', 'Navbar lama belum dihapus dari view', 'Ganti seluruh isi view sesuai Bab 10'],
        ['Error `Undefined variable $employee` di actions', '`@include(\'employee.actions\')` diletakkan di luar `@foreach`', 'Letakkan di dalam kolom tabel, di dalam `@foreach`'],
        ['Klik Edit menghasilkan error 405 Method Not Allowed', '`@method(\'put\')` hilang dari form edit', 'Periksa subbab 7.2'],
        ['Kode sudah disimpan, tetapi halaman masih versi lama', 'Laravel menyimpan salinan view (cache)', 'Tunggu 2–3 detik, atau jalankan `php artisan view:clear`'],
        ['Error `SQLSTATE[HY000] [2002] Connection refused`', 'Server MySQL belum berjalan', 'Start MySQL di XAMPP Control Panel'],
    ], [3400, 3000, 3238])

    # ------------------------------------------------------------------ 12
    b.h1('12. Tugas dan pengumpulan')
    b.h2('12.1 Tugas')
    b.p('Kerjakan seluruh tugas berikut secara individu.')
    b.steps([
        'Praktikkan seluruh poin praktikum dan jawab semua soal **Pertanyaan** pada Bab 3 sampai Bab 10.',
        'Dokumentasikan semuanya dalam bentuk laporan praktikum (PDF). Isinya screenshot kode program, screenshot output di browser, dan jawaban pertanyaan.',
        'Unggah project Laravel hasil praktikum ke GitHub.',
    ])
    b.h2('12.2 Unggah project ke GitHub')
    b.steps([
        'Buat repository **public** baru di akun GitHub Anda. Jangan menambahkan README, `.gitignore`, atau license, agar tidak terjadi konflik saat push pertama.',
        'Di folder project, jalankan perintah berikut. Ganti `<URL repository>` dengan alamat repository yang baru dibuat.',
    ])
    b.code('BASH', 'git init\ngit add .\ngit commit -m "Modul 12"\ngit branch -M main\ngit remote add origin <URL repository>\ngit push -u origin main')
    b.p('Folder `vendor`, folder `node_modules`, dan file `.env` tidak perlu dihapus. Ketiganya otomatis diabaikan oleh `.gitignore` bawaan Laravel, sehingga tidak ikut ter-upload.')
    b.h2('12.3 Pengumpulan')
    b.p('Cantumkan URL repository pada laporan praktikum. Kumpulkan laporan (.pdf) melalui LMS, paling lambat sebelum jadwal praktikum minggu depan.')
    b.h2('12.4 Daftar periksa sebelum mengumpulkan')
    b.checks([
        'Tidak ada lagi `DB::select()` atau `DB::table()` di EmployeeController.',
        'Tambah, detail, edit, dan hapus karyawan berjalan tanpa error.',
        'Hanya `layouts/nav.blade.php` yang berisi kode navbar.',
        'Halaman `/home`, `/profile`, `/employees`, `/employees/create`, `/employees/{id}`, dan `/employees/{id}/edit` memakai layout yang sama.',
        'Jawaban semua soal Pertanyaan ada di laporan, lengkap dengan screenshot.',
        'Repository GitHub berstatus public, dan URL-nya tercantum di laporan PDF.',
    ])
