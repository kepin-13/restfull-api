from flask import Blueprint, request, jsonify
from db import supabase_request
# Memanggil auth_middleware naik 1 folder ke atas
from backend.middlewares.auth_middleware import token_required

mahasiswa_bp = Blueprint('mahasiswa', __name__)

# ==========================================
# 1. AMBIL ALL DATA MAHASISWA (GET)
# ==========================================
@mahasiswa_bp.route('/mahasiswa', methods=['GET'])
@token_required
def get_mahasiswa():
    # Ambil data dari tabel data_mahasiswa di Supabase Cloud
    data, status_code = supabase_request("/rest/v1/data_mahasiswa", method="GET")
    return jsonify(data), status_code

# ==========================================
# 2. TAMBAH DATA MAHASISWA (POST)
# ==========================================
@mahasiswa_bp.route('/mahasiswa', methods=['POST'])
@token_required
def add_mahasiswa():
    body = request.get_json()
    data, status_code = supabase_request("/rest/v1/data_mahasiswa", method="POST", json_data=body)
    return jsonify({"message": "Data Mahasiswa Berhasil Ditambahkan!", "data": data}), status_code

# ==========================================
# 3. UBAH/EDIT DATA MAHASISWA (PUT) -> INI YANG BARU!
# ==========================================
@mahasiswa_bp.route('/mahasiswa/<int:id>', methods=['PUT'])
@token_required
def edit_mahasiswa(id):
    body = request.get_json()
    
    # Mengirim data update ke Supabase berdasarkan query id (?id=eq.X)
    data, status_code = supabase_request(f"/rest/v1/data_mahasiswa?id=eq.{id}", method="PATCH", json_data=body)
    
    return jsonify({"message": "Data Mahasiswa Berhasil Diperbarui!", "data": data}), status_code

# ==========================================
# 4. HAPUS DATA MAHASISWA (DELETE) -> INI YANG BARU!
# ==========================================
@mahasiswa_bp.route('/mahasiswa/<int:id>', methods=['DELETE'])
@token_required
def delete_mahasiswa(id):
    # Mengirim perintah hapus ke Supabase berdasarkan query id (?id=eq.X)
    data, status_code = supabase_request(f"/rest/v1/data_mahasiswa?id=eq.{id}", method="DELETE")
    
    return jsonify({"message": "Data Mahasiswa Berhasil Dihapus!"}), status_code