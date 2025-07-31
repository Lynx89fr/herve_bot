@echo off
setlocal

REM 🔹 Chemin vers ffmpeg (change si besoin)
set FFMPEG=C:\ffmpeg\bin\ffmpeg.exe

REM 🔹 Conversion tous les fichiers .ogg -> .mp4 (fond noir)
for %%f in (*.ogg) do (
  echo Conversion de %%f ...
  "%FFMPEG%" -f lavfi -i "color=c=black:s=720x720" -i "%%f" -shortest -c:v libx264 -c:a aac "%%~nf.mp4"
)

echo ✅ Conversion terminée !
pause