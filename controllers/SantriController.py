from flask import Blueprint, render_template, request, redirect, url_for
from config import db
from bson.objectid import ObjectId

santri_bp = Blueprint('santri_bp', __name__)

# Setup MongoDB
santri_collection = db["santri"]

# Tampilkan daftar santri
@santri_bp.route('/santri')
def santri():
    santri_list = santri_collection.find()
    return render_template('santri.html', santri_list=santri_list, edit_mode=False)

# Tambah santri
@santri_bp.route('/santri/add', methods=['POST'])
def add_santri():
    nis = request.form['nis']
    nama = request.form['nama']
    kelas = request.form['kelas']

    # cekik apakah NIS sudah ada
    if santri_collection.find_one({'nis': nis}):
        santri_list = santri_collection.find()
        return render_template('santri.html', santri_list=santri_list, error="NIS sudah ada", edit_mode=False)
    
    santri_collection.insert_one({'nis': nis, 'nama': nama, 'kelas': kelas})
    return redirect(url_for('santri_bp.santri'))

# Ambil data untuk edit
@santri_bp.route('/santri/edit/<nis>', methods=['GET'])
def get_edit_santri(nis):
    santri_data = santri_collection.find_one({"nis": nis})
    santri_list = list(santri_collection.find())
    return render_template('santri.html', santri_data=santri_data, santri_list=santri_list, edit_mode=True)

# Update santri
@santri_bp.route('/santri/update/<nis>', methods=['POST'])
def update_santri(nis):
    nis_baru = request.form['nis']
    nama = request.form['nama']
    kelas = request.form['kelas']
    nis_lama = request.form['nis_lama']

    # Cek apakah NIS baru sudah ada
    if nis_baru != nis_lama and santri_collection.find_one({'nis': nis_baru}):
        santri_list = santri_collection.find()
        return render_template('santri.html', santri_list=santri_list, error="NIS baru sudah ada", edit_mode=True, santri_data={'nis': nis_lama, 'nama': nama, 'kelas': kelas})
    
    santri_collection.update_one({'nis': nis_lama}, {'$set': {'nis': nis_baru, 'nama': nama, 'kelas': kelas}})
    return redirect(url_for('santri_bp.santri'))

# Hapus santri
@santri_bp.route('/santri/delete/<id>')
def delete_santri(id):
    santri_collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('santri_bp.santri'))
