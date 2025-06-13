from flask import Blueprint, render_template, request
from config import db
from datetime import datetime, time
import pytz

result_bp = Blueprint('result_bp', __name__)
result_collection = db["results"]

@result_bp.route('/result')
def result():
    selected_date_str = request.args.get('date')
    selected_sesi = request.args.get('sesi', 'pagi')

    filtered_results = []

    if selected_date_str:
        try:
            # Ambil tanggal dari user
            date_obj = datetime.strptime(selected_date_str, '%Y-%m-%d')

            # Rentang waktu sesi dalam waktu lokal (WIB)
            sesi_ranges = {
                'pagi': (time(7, 0), time(8, 0)),
                'siang': (time(12, 30), time(14, 30)),
                'malam': (time(19, 30), time(20, 30)),
            }

            start_time, end_time = sesi_ranges.get(selected_sesi, (time(0, 0), time(23, 59)))

            # Gabung jadi datetime lokal
            wib = pytz.timezone("Asia/Jakarta")
            start_local = wib.localize(datetime.combine(date_obj, start_time))
            end_local = wib.localize(datetime.combine(date_obj, end_time))

            # Ambil semua data yang tanggalnya sama (dulu), lalu filter manual
            all_results = list(result_collection.find({}))

            for r in all_results:
                try:
                    ts_str = r.get('timestamp')
                    if not ts_str:
                        continue

                    # Parse string ISO timestamp ke datetime UTC
                    ts_utc = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                    ts_utc = ts_utc.replace(tzinfo=pytz.utc)

                    # Konversi ke waktu lokal (WIB)
                    ts_local = ts_utc.astimezone(wib)

                    # Filter berdasarkan tanggal dan jam lokal
                    if date_obj.date() == ts_local.date() and start_local <= ts_local <= end_local:
                        # Inject timestamp lokal buat ditampilkan nanti
                        r["timestamp_local"] = ts_local
                        filtered_results.append(r)
                except Exception:
                    continue  # skip kalau ada yang aneh

        except ValueError:
            pass  # salah input tanggal

    return render_template(
        'result.html',
        result_list=filtered_results,
        selected_date=selected_date_str,
        selected_sesi=selected_sesi
    )
