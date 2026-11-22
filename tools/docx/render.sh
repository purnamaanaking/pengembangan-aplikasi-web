#!/bin/bash
# ./render.sh out/mNN.docx -> out/mNN.pdf lewat Microsoft Word (macOS).
# Mencetak "OK" jika berhasil. Jika Word gagal membuka file (dialog error), proses Word dihentikan dan dicetak "GAGAL".
C=~/Library/Containers/com.microsoft.Word/Data/paw-render; mkdir -p $C
B=$(basename "$1" .docx); cp "$1" $C/$B.docx; rm -f $C/$B.pdf
osascript -e "with timeout of 40 seconds
tell application \"Microsoft Word\"
open POSIX file \"$C/$B.docx\"
repeat 20 times
try
if (name of active document) is not missing value then exit repeat
end try
delay 1
end repeat
save as active document file name \"$C/$B.pdf\" file format format PDF
close active document saving no
end tell
end timeout" >/dev/null 2>&1
if [ -f $C/$B.pdf ]; then cp $C/$B.pdf "${1%.docx}.pdf"; echo OK; else pkill -KILL -x "Microsoft Word"; sleep 2; echo GAGAL; fi
