from flask import Blueprint, render_template, request
from config import db
from datetime import datetime, timedelta

# Setup Blueprint dan koleksi MongoDB
dashboard_bp = Blueprint('dashboard_bp', __name__)
santri_collection = db["santri"]
result_collection = db["results"]
lauk_collection = db["lauk"]

# Home
@dashboard_bp.route('/')
def home():
    total_santri = santri_collection.count_documents({})

    # Ambil parameter filter
    selected_date_str = request.args.get('date')
    selected_sesi = request.args.get('sesi', 'pagi')

    # Default: hari ini dan 7 hari ke belakang
    today = datetime.now().date()
    if selected_date_str:
        try:
            end_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            end_date = today
    else:
        end_date = today
    start_date = end_date - timedelta(days=6)

    # Filter data result berdasarkan rentang tanggal dan sesi
    query = {
        'timestamp': {
            '$gte': datetime.combine(start_date, datetime.min.time()),
            '$lte': datetime.combine(end_date, datetime.max.time())
        },
        'sesi': selected_sesi
    }

    result_list = list(result_collection.find(query))

    # Hitung jumlah pengambilan lauk
    lauk_total = {}
    for result in result_list:
        frames = result.get('frames', {})
        for nama_lauk, count in frames.items():
            lauk_total[nama_lauk] = lauk_total.get(nama_lauk, 0) + int(count)

    # Ubah ke list untuk template
    lauk_stats = [
        {'nama_lauk': nama_lauk, 'count': count}
        for nama_lauk, count in lauk_total.items()
    ]

    # Leaderboard (top 3 lauk)
    lauk_stats_sorted = sorted(lauk_stats, key=lambda x: x['count'], reverse=True)
    leaderboard = lauk_stats_sorted[:3]

    return render_template(
        'index.html',
        total_santri=total_santri,
        lauk_stats=lauk_stats,
        leaderboard=leaderboard,
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        selected_sesi=selected_sesi,
        result_list=result_list
    )