from flask import Blueprint, request, jsonify
import jwt
import datetime
# PERBAIKAN: Impor diarahkan ke lokasi absolut db.py dari root folder proyek
from db import supabase_request, JWT_SECRET

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username dan password wajib diisi"}), 400

    # Payload data yang dikirim ke tabel admin_users di Supabase Cloud
    # 💡 CATATAN: Pastikan nama kolom di tabel Supabase kamu adalah 'username' (huruf kecil semua).
    # Jika di Supabase nama kolomnya adalah 'email', ganti '"username": username' di bawah menjadi '"email": username'
    payload = {"username": username, "password": password}
    response_data, status_code = supabase_request("/rest/v1/admin_users", method="POST", json_data=payload)

    if status_code in [200, 201]:
        return jsonify({"message": "Registrasi Akun Supabase Berhasil!"}), 201
    else:
        # PERBAIKAN: Mengembalikan detail pesan eror asli dari Supabase agar mudah dilacak di frontend
        error_details = response_data.get('message') if isinstance(response_data, dict) else str(response_data)
        return jsonify({
            "message": "Gagal mendaftar ke Supabase", 
            "error": error_details
        }), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username dan password wajib diisi"}), 400

    # Cek kecocokan user ke tabel admin_users Supabase Cloud
    # 💡 CATATAN: Jika nama kolom di Supabase adalah 'email', ubah 'username=eq.' di bawah menjadi 'email=eq.'
    endpoint = f"/rest/v1/admin_users?username=eq.{username}&password=eq.{password}"
    user_list, status_code = supabase_request(endpoint, method="GET")

    if status_code == 200 and len(user_list) > 0:
        # Generasi Token JWT Internal untuk proteksi session login selama 2 jam
        token_payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")
        return jsonify({"message": "Login Berhasil!", "token": token}), 200
    else:
        return jsonify({"message": "Username atau Password salah!"}), 401