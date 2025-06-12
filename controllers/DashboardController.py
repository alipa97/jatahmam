from flask import Blueprint, render_template
from config import db

dashboard_bp = Blueprint('dashboard_bp', __name__)

# Setup MongoDB
santri_collection = db["santri"]
result_collection = db["results"]
lauk_collection = db["lauk"]

# Home
@dashboard_bp.route('/')
def home():
    # Hitung total santri dari koleksi santri
    total_santri = santri_collection.count_documents({})

    # Dictionary untuk menyimpan total setiap lauk
    lauk_total = {}

    # Ambil semua data dari koleksi result
    result_list = result_collection.find()

    # Proses setiap data result
    for result in result_list:
        frames = result.get('frames', {})
        for nama_lauk, count in frames.items():
            try:
                if int(count) == 1:  # pastikan nilai bisa dikonversi ke integer
                    lauk_total[nama_lauk] = lauk_total.get(nama_lauk, 0) + 1
            except ValueError:
                continue  # abaikan jika nilai tidak valid

    # Ubah dict ke list untuk ditampilkan di template
    lauk_stats = [
        {'nama_lauk': nama_lauk, 'count': count}
        for nama_lauk, count in lauk_total.items()
    ]

    # Kirim data ke template
    return render_template(
        'index.html',
        total_santri=total_santri,
        lauk_stats=lauk_stats,
        result_list=result_list
    )