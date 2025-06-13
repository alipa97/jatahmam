from flask import Blueprint, render_template, request
from config import db
from datetime import datetime, timedelta, time
import pytz

dashboard_bp = Blueprint('dashboard_bp', __name__)
santri_collection = db["santri"]
result_collection = db["results"]

@dashboard_bp.route('/')
def home():
    total_santri = santri_collection.count_documents({})

    selected_date_str = request.args.get('date')
    selected_sesi = request.args.get('sesi', 'pagi')

    today = datetime.now().date()
    if selected_date_str:
        try:
            end_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            end_date = today
    else:
        end_date = today

    start_date = end_date - timedelta(days=6)

    # WIB timezone
    wib = pytz.timezone("Asia/Jakarta")

    # Sesi ranges
    sesi_ranges = {
        'pagi': (time(7, 0), time(8, 0)),
        'siang': (time(12, 30), time(14, 30)),
        'malam': (time(19, 30), time(20, 30)),
    }
    start_time, end_time = sesi_ranges.get(selected_sesi, (time(0, 0), time(23, 59)))
    print(f"Selected sesi: {selected_sesi}, Start time: {start_time}, End time: {end_time}")

    # Ambil semua data dari Mongo
    all_results = list(result_collection.find({}))
    print(f"Total results fetched: {len(all_results)}")
    result_list = []

    for r in all_results:
        try:
            ts_str = r.get('timestamp')
            if not ts_str:
                continue

            # Parse ISO timestamp string to datetime UTC
            ts_utc = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
            ts_local = ts_utc.astimezone(wib)
            print(f"Processing result with timestamp: {ts_local.date()}")

            # Filter: Tanggal dalam 7 hari terakhir + waktu sesi
            # if start_date <= ts_local.date() <= end_date:
            #     print("ish")
            # if start_time <= ts_local.time() <= end_time:
            #     print("damn")
            if start_date <= ts_local.date() <= end_date and start_time <= ts_local.time() <= end_time:
                r['timestamp_local'] = ts_local
                result_list.append(r)
                print("bla")
        except Exception:
            continue

    print(f"Filtered result count: {len(result_list)}")

    # Hitung jumlah lauk
    lauk_total = {}
    for result in result_list:
        frames = result.get('frames', {})
        for nama_lauk, count in frames.items():
            try:
                lauk_total[nama_lauk] = lauk_total.get(nama_lauk, 0) + int(count)
            except (ValueError, TypeError):
                continue

    lauk_stats = [
        {"nama_lauk": nama_lauk, "count": count}
        for nama_lauk, count in lauk_total.items()
    ]
    lauk_stats_sorted = sorted(lauk_stats, key=lambda x: x["count"], reverse=True)
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