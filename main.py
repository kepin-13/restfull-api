from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Impor koneksi database dari file database.py
from database import supabase, table_name

app = FastAPI(title="Panel Admin Mahasiswa - Cute Pink Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schema Pydantic
class MahasiswaBase(BaseModel):
    nim: str
    nama: str
    jurusan: str

class MahasiswaUpdate(BaseModel):
    nama: str | None = None
    jurusan: str | None = None


# ==========================================
# 1. HALAMAN UTAMA (TEMA PINK & PUTIH)
# ==========================================
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CRUD Mahasiswa - Pink & White Theme</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { 
                background-color: #fff0f5; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            }
            .navbar-panel { 
                background: #ffffff; 
                box-shadow: 0 2px 10px rgba(255, 182, 193, 0.3); 
                padding: 15px 30px; 
                margin-bottom: 30px;
                border-bottom: 3px solid #ffb6c1;
            }
            .card-header-custom { 
                background-color: #ff69b4; 
                color: white; 
                font-weight: 600; 
                font-size: 1.1rem; 
                text-align: center;
            }
            .card { 
                border: none; 
                box-shadow: 0 4px 15px rgba(255, 105, 180, 0.1); 
                border-radius: 12px; 
                overflow: hidden; 
                background-color: #ffffff;
            }
            .btn-pink {
                background-color: #ff69b4;
                color: white;
                font-weight: bold;
                border: none;
            }
            .btn-pink:hover {
                background-color: #ff1493;
                color: white;
            }
            .table-pink-header {
                background-color: #ffe4e1 !important; 
                color: #d147a3;
            }
            .form-control:focus {
                border-color: #ff69b4;
                box-shadow: 0 0 0 0.25rem rgba(255, 105, 180, 0.25);
            }
        </style>
    </head>
    <body>

        <div class="navbar-panel d-flex justify-content-between align-items-center">
            <h2 class="m-0" style="font-weight: 400; color: #ff69b4;">Panel <strong style="color: #d147a3;">Admin</strong></h2>
        </div>

        <div class="container-fluid px-4">
            <div class="row g-4">
                
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header card-header-custom py-3" id="formHeader">Input Mahasiswa</div>
                        <div class="card-body p-4">
                            <form id="formMahasiswa">
                                <div class="mb-3">
                                    <label class="form-label small fw-bold" style="color: #6c757d;">NIM</label>
                                    <input type="text" id="nim" class="form-control" placeholder="Contoh: 241080200107" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label small fw-bold" style="color: #6c757d;">Nama Lengkap</label>
                                    <input type="text" id="nama" class="form-control" placeholder="Masukkan nama..." required>
                                </div>
                                <div class="mb-4">
                                    <label class="form-label small fw-bold" style="color: #6c757d;">Jurusan</label>
                                    <input type="text" id="jurusan" class="form-control" placeholder="Contoh: Informatika" required>
                                </div>
                                <button type="submit" class="btn btn-pink w-100 py-2" id="btnSimpan">Simpan Data</button>
                            </form>
                        </div>
                    </div>
                </div>

                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header card-header-custom py-3">Daftar Mahasiswa</div>
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-hover align-middle mb-0">
                                    <thead>
                                        <tr class="table-pink-header">
                                            <th class="ps-4">NIM</th>
                                            <th>Nama</th>
                                            <th>Jurusan</th>
                                            <th class="text-center" style="width: 150px;">Aksi</th>
                                        </tr>
                                    </thead>
                                    <tbody id="tabelMahasiswa">
                                        </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <script>
            const apiUrl = 'http://127.0.0.1:8000/api/mahasiswa';
            let isEditMode = false;

            async function muatData() {
                try {
                    const res = await fetch(apiUrl);
                    const result = await res.json();
                    const tbody = document.getElementById('tabelMahasiswa');
                    tbody.innerHTML = '';

                    if(!result.data || result.data.length === 0) {
                        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4">Belum ada data mahasiswa.</td></tr>`;
                        return;
                    }

                    result.data.forEach(mhs => {
                        tbody.innerHTML += `
                            <tr>
                                <td class="ps-4 fw-semibold" style="color: #d147a3;">${mhs.nim}</td>
                                <td>${mhs.nama}</td>
                                <td>${mhs.jurusan}</td>
                                <td class="text-center">
                                    <button class="btn btn-sm btn-warning text-white fw-bold me-1" onclick="siapEdit('${mhs.nim}', '${mhs.nama}', '${mhs.jurusan}')">Edit</button>
                                    <button class="btn btn-sm btn-danger fw-bold" onclick="hapusMahasiswa('${mhs.nim}')">Hapus</button>
                                </td>
                            </tr>
                        `;
                    });
                } catch (error) {
                    console.error("Gagal memuat data:", error);
                }
            }

            document.getElementById('formMahasiswa').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const nim = document.getElementById('nim').value;
                const nama = document.getElementById('nama').value;
                const jurusan = document.getElementById('jurusan').value;

                const data = { nim, nama, jurusan };

                try {
                    let response;
                    if (isEditMode) {
                        response = await fetch(`${apiUrl}/${nim}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ nama, jurusan })
                        });
                    } else {
                        response = await fetch(apiUrl, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(data)
                        });
                    }

                    const resData = await response.json();
                    if (!response.ok) throw new Error(resData.detail || "Terjadi kesalahan");

                    alert(resData.message);
                    resetForm();
                    muatData();
                } catch (error) {
                    alert("Error: " + error.message);
                }
            });

            function siapEdit(nim, nama, jurusan) {
                document.getElementById('nim').value = nim;
                document.getElementById('nim').disabled = true;
                document.getElementById('nama').value = nama;
                document.getElementById('jurusan').value = jurusan;
                
                document.getElementById('formHeader').innerText = "Perbarui Mahasiswa";
                document.getElementById('btnSimpan').innerText = "Perbarui Data";
                document.getElementById('btnSimpan').className = "btn btn-warning w-100 py-2 text-white fw-bold";
                isEditMode = true;
            }

            async function hapusMahasiswa(nim) {
                if (confirm(`Apakah kamu yakin ingin menghapus NIM ${nim}?`)) {
                    try {
                        const response = await fetch(`${apiUrl}/${nim}`, { method: 'DELETE' });
                        const resData = await response.json();
                        alert(resData.message);
                        muatData();
                    } catch (error) {
                        alert("Gagal menghapus data");
                    }
                }
            }

            function resetForm() {
                document.getElementById('formMahasiswa').reset();
                document.getElementById('nim').disabled = false;
                document.getElementById('formHeader').innerText = "Input Mahasiswa";
                document.getElementById('btnSimpan').innerText = "Simpan Data";
                document.getElementById('btnSimpan').className = "btn btn-pink w-100 py-2";
                isEditMode = false;
            }

            window.onload = muatData;
        </script>
    </body>
    </html>
    """

# ==========================================
# 2. ENDPOINT API BACKEND (SUPABASE)
# ==========================================

@app.post("/api/mahasiswa", status_code=status.HTTP_201_CREATED)
def create_mahasiswa(mhs: MahasiswaBase):
    try:
        existing = supabase.table(table_name).select("nim").eq("nim", mhs.nim).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="NIM sudah terdaftar!")

        response = supabase.table(table_name).insert(mhs.model_dump()).execute()
        return {"message": "Data mahasiswa berhasil ditambahkan!", "data": response.data[0]}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mahasiswa")
def get_all_mahasiswa():
    try:
        response = supabase.table(table_name).select("*").order("nim").execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/mahasiswa/{nim}")
def update_mahasiswa(nim: str, mhs_update: MahasiswaUpdate):
    try:
        existing = supabase.table(table_name).select("*").eq("nim", nim).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

        update_data = {k: v for k, v in mhs_update.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="Tidak ada data yang diubah")

        response = supabase.table(table_name).update(update_data).eq("nim", nim).execute()
        return {"message": "Data mahasiswa berhasil diperbarui!", "data": response.data[0]}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/mahasiswa/{nim}")
def delete_mahasiswa(nim: str):
    try:
        existing = supabase.table(table_name).select("*").eq("nim", nim).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

        supabase.table(table_name).delete().eq("nim", nim).execute()
        return {"message": f"Mahasiswa dengan NIM {nim} berhasil dihapus!"}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))