import requests

# Kredensial Supabase Cloud Anda
SUPABASE_URL = "https://dyxbbebqbaophfmzfszo.supabase.co"
SUPABASE_KEY = "sb_publishable_whn-MrX5CsjIfyqAzzQZVw_lT5sp2eR"
JWT_SECRET = "kunci_rahasia_jwt_mahasiswa_pink_999"

def supabase_request(endpoint, method="GET", json_data=None, custom_headers=None):
    url = f"{SUPABASE_URL}{endpoint}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    if custom_headers:
        headers.update(custom_headers)
        
    try:
        if method == "POST":
            response = requests.post(url, headers=headers, json=json_data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=json_data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)
            
        return response.json(), response.status_code
    except Exception as e:
        return {"message": f"Koneksi Supabase Gagal: {str(e)}"}, 500