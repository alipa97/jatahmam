from flask import Blueprint, render_template, request, redirect, url_for
from config import db
from bson.objectid import ObjectId

sesi_bp = Blueprint('sesi_bp', __name__)

# Setup MongoDB
sesi_collection = db["sesi_makan"]
lauk_collection = db["lauk"]

# Tampilkan daftar sesi
@sesi_bp.route('/sesi')
def sesi():
    sesi_list = list(sesi_collection.find())
    lauk_dict = {str(l['_id']): l['nama_lauk'] for l in lauk_collection.find()}

    # ubah ObjectId ke nama lauk
    for s in sesi_list:
        s['lauk_1_nama'] = lauk_dict.get(str(s['lauk_1']), 'Tidak ditemukan')
        s['lauk_2_nama'] = lauk_dict.get(str(s['lauk_2']), 'Tidak ditemukan')
        s['lauk_3_nama'] = lauk_dict.get(str(s['lauk_3']), 'Tidak ditemukan')

    return render_template('sesi.html', sesi_list=sesi_list)

# Tambah sesi makan
@sesi_bp.route('/sesi/tambah', methods=['GET', 'POST'])
def tambah_sesi():
    if request.method == 'POST':
        data = {
            'tanggal': request.form['tanggal'],
            'waktu': request.form['waktu'],
            'lauk_1': ObjectId(request.form['lauk_1']),
            'lauk_2': ObjectId(request.form['lauk_2']),
            'lauk_3': ObjectId(request.form['lauk_3']),
        }
        sesi_collection.insert_one(data)
        return redirect(url_for('sesi_bp.sesi'))

    lauk_list = list(lauk_collection.find())
    return render_template('form_sesi.html', lauk_list=lauk_list)