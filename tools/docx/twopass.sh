#!/bin/bash
# ./twopass.sh NN
# Build out/mNN.docx, render dengan Word, ambil nomor halaman tiap heading,
# lalu build ulang sampai nomor halaman di daftar isi stabil.
set -e
cd "$(dirname "$0")"
PY=${PY:-python3}
N=$1; O=out/m$N.docx
$PY build.py $N >/dev/null
[ "$(./render.sh $O)" = OK ] || { echo "Word gagal membuka $O"; exit 1; }
$PY pages.py $O $N | cut -c1-40
for i in 1 2 3; do
  cp $O.pages.json out/p$N.json
  $PY build.py $N out/p$N.json >/dev/null
  [ "$(./render.sh $O)" = OK ] || { echo "Word gagal membuka $O"; exit 1; }
  $PY pages.py $O $N >/dev/null
  if cmp -s out/p$N.json $O.pages.json; then echo "stabil: $O dan ${O%.docx}.pdf"; exit 0; fi
done
echo "nomor halaman belum stabil"
