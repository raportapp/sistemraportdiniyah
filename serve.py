"""
Server Python sederhana untuk menjalankan aplikasi Sistem Raport Diniyah
(hasil build React/Vite) sebagai pengganti Firebase Hosting.

Cara pakai:
1. Build dulu aplikasi React-nya:
       npm run build
   Ini akan menghasilkan folder "dist/" berisi file statis.

2. Jalankan server ini:
       python serve.py
   Default jalan di port 8000. Bisa diubah lewat env var PORT.

3. Akses dari komputer sendiri:
       http://localhost:8000

4. Akses dari HP/laptop lain di WiFi yang sama:
   - Cari IP lokal komputer ini (jalankan "ipconfig" di cmd, lihat "IPv4 Address")
   - Buka di perangkat lain: http://<IP-KOMPUTER-INI>:8000

Catatan: Ini untuk LAN/uji coba. Untuk akses dari luar jaringan (internet),
server ini perlu dideploy ke platform seperti Railway/Render, atau
dipasang port forwarding di router (tidak disarankan untuk awam karena
risiko keamanan).
"""

import http.server
import os
import socketserver
import sys

DIST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
PORT = int(os.environ.get("PORT", 8000))


class SPARequestHandler(http.server.SimpleHTTPRequestHandler):
    """Serve static files, but fall back to index.html for unknown routes
    (needed for client-side routing in React apps)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def end_headers(self):
        # Prevent aggressive caching while testing
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def send_head(self):
        path = self.translate_path(self.path)
        if not os.path.exists(path) or os.path.isdir(path):
            # Fallback to index.html for SPA routes (e.g. /dashboard, /login)
            if not os.path.splitext(self.path)[1]:
                self.path = "/index.html"
        return super().send_head()


def main():
    if not os.path.isdir(DIST_DIR):
        print(f"ERROR: Folder 'dist' tidak ditemukan di {DIST_DIR}")
        print("Jalankan 'npm run build' dulu sebelum menjalankan server ini.")
        sys.exit(1)

    with socketserver.TCPServer(("0.0.0.0", PORT), SPARequestHandler) as httpd:
        print(f"Sistem Raport Diniyah berjalan di:")
        print(f"  - Lokal:  http://localhost:{PORT}")
        print(f"  - LAN:    http://<IP-komputer-ini>:{PORT}  (cek IP lewat 'ipconfig')")
        print("Tekan Ctrl+C untuk menghentikan server.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dihentikan.")


if __name__ == "__main__":
    main()
