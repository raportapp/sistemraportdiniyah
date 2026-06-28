@echo off
title Sistem Raport Diniyah - Server
color 0A

echo ============================================
echo   SISTEM RAPORT DINIYAH - PPTQ AL-HUSNA
echo ============================================
echo.

cd /d "%~dp0"

echo [1/3] Membangun aplikasi (build)...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "npm run build"

if not exist "dist" (
    echo.
    echo ============================================
    echo   GAGAL! Folder 'dist' tidak ditemukan.
    echo   Build aplikasi gagal. Periksa pesan error di atas.
    echo ============================================
    pause
    exit /b 1
)

echo.
echo [2/3] Build berhasil!
echo.
echo [3/3] Mencari alamat IP komputer ini di jaringan WiFi...
echo.
echo ============================================
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R /C:"IPv4 Address"') do (
    echo   Alamat untuk Guru:  http://%%a:8000
)
echo   Alamat di komputer ini:  http://localhost:8000
echo ============================================
echo.
echo Pastikan HP/Laptop guru terhubung ke WIFI YANG SAMA
echo dengan komputer ini, lalu buka alamat di atas.
echo.
echo JANGAN TUTUP jendela ini selama aplikasi masih dipakai.
echo Tekan CTRL+C untuk menghentikan server.
echo ============================================
echo.

python serve.py
if errorlevel 1 (
    echo.
    echo Mencoba dengan 'py' sebagai gantinya...
    py serve.py
)

pause
