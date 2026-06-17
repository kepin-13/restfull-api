from flask import Flask
from flask_cors import CORS
# Mengarah ke folder backend, routes, dan file mahasiswa
from backend.routes.auth import auth_bp
from backend.routes.mahasiswa import mahasiswa_bp

app = Flask(__name__)
CORS(app)  # Mengaktifkan CORS agar Frontend HTML bisa akses

# Daftarkan Blueprint Routes
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(mahasiswa_bp, url_prefix='/api')

if __name__ == '__main__':
    print("Server Backend Flask Berjalan di http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)