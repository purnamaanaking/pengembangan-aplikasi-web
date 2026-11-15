# Catatan Uji Modul 10 — Pengenalan Controller dan View pada Laravel

Branch: `praktikum/modul-10-controller-view` (project di folder `modul-10-controller-view/`, dibuat dari `main`, terpisah dari Modul 09 sesuai instruksi modul)

## Lingkungan uji

| Komponen | Versi |
| --- | --- |
| PHP | 8.4.8 |
| Composer | 2.8.5 |
| Node.js / npm | 24.11.1 / 11.6.2 |
| Laravel | 13.x |
| Vite / laravel-vite-plugin | 8.3.8 / 3.2.1 |

## Hasil

Semua langkah Bab 1–5 dapat dikerjakan sesuai teks modul. Kode disalin apa adanya dari modul (tidak ada karakter non-ASCII, aman di-copy-paste).

| Bab | Hasil |
| --- | --- |
| 1. Persiapan project + halaman welcome | OK. Gambar Vite tampil, tombol Home tampil |
| 2. Home (`HomeController`, Basic Controller) | OK. `/home` 200 |
| 3. My Profile (`--invokable`) | OK. `/profile` 200 |
| 4. Employee List (`--resource`) | OK. `/employees` 200; `route:list` menampilkan 7 route resource + `home` + `profile` |
| 5. Create Employee | OK. Form tampil; validasi menampilkan 3 alert untuk input salah; input valid mengembalikan JSON |
| Soal: Displaying Validation Errors | OK, sudah ada di kode view modul |
| Soal: Repopulating Forms | OK setelah `value=""` diganti `value="{{ old('namaField') }}"` pada 4 input |
| Soal: CSRF Protection | OK. Lihat temuan no. 4 |
| Navbar Bootstrap di layar HP (375px) | OK. Tombol menu membuka navbar (JavaScript Bootstrap termuat) |
| `npm run build` | OK. `laravel.png` masuk manifest; semua halaman 200 |

Tidak diuji: pembuatan laporan, push ke GitHub (butuh akun/remote), dan perbandingan visual dengan gambar "Hasil Akhir Bab 1–5" di modul.

## Temuan yang perlu diperhatikan

1. **Gambar tidak disediakan.** Modul meminta `resources/images/laravel.png`, tetapi filenya tidak ada di modul. Tanpa file ini, halaman welcome error. Saran: sertakan tautan unduh gambar.
2. **Ringkasan perintah di Bab 1 tidak lengkap.** Perintah di modul hanya sampai `npm uninstall tailwindcss @tailwindcss/vite`. Langkah Modul 9 yang dirujuk (membuat `resources/sass/app.scss`, mengganti `vite.config.js` dan `resources/js/app.js`, menghapus `resources/css/app.css`) harus diulang mahasiswa. Jika terlewat, `vite.config.js` bawaan masih mengimpor `@tailwindcss/vite` yang sudah di-uninstall, sehingga `npm run dev` diperkirakan gagal (belum diuji terpisah). Saran: cantumkan langkah-langkah itu secara eksplisit.
3. **Pesan error di Bab 2 tidak persis sama.** Modul menyebut `Route [profile] not defined`, tetapi yang muncul lebih dulu adalah `Route [employees.index] not defined` karena link Employee List ada sebelum tombol My Profile di navbar. Maksudnya sama; sebaiknya teks disesuaikan.
4. **Catatan CSRF di modul akurat.** Permintaan POST tanpa token dari halaman yang sama (same-origin) tetap diterima (HTTP 200); permintaan tanpa token lewat `curl` ditolak dengan HTTP 419. Untuk bukti 419, mahasiswa memang harus memakai `curl` atau Postman.
5. **Soal Repopulating Forms.** Kode view di modul memakai `value=""`. Mahasiswa harus mengubahnya sendiri menjadi `value="{{ old('firstName') }}"` (dan seterusnya untuk `lastName`, `email`, `age`). Ini sesuai maksud soal, tetapi sebaiknya modul menyebut file mana yang diubah.
6. **Soal "Tunjukkan Route apa saja" (Bab 4).** Perintahnya tidak disebut; mahasiswa perlu mengingat `php artisan route:list` dari Modul 9 bab 4.12. Saran: beri petunjuk.
7. **Kecil:** nama atribut pada pesan validasi muncul dalam bahasa Inggris (`Last name harus diisi.`, `Isi age dengan angka`) karena modul tidak memakai terjemahan atribut. Kelas navbar `col-2` pada home/index/create tetapi `col-6` pada profile (tidak konsisten, hanya kosmetik).
