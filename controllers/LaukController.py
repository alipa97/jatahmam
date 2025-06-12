from flask import Blueprint, render_template, request, redirect, url_for
from config import db
from bson.objectid import ObjectId

lauk_bp = Blueprint('lauk_bp', __name__)

# Setup MongoDB
lauk_collection = db["lauk"]

# Tampilkan daftar lauk
@lauk_bp.route('/lauk')
def lauk():
    lauk_list = lauk_collection.find()
    return render_template('lauk.html', lauk_list=lauk_list, edit_mode=False)

# Tambah lauk
@lauk_bp.route('/lauk/add', methods=['POST'])
def add_lauk():
    nama_lauk = request.form['nama_lauk'].strip().lower()

    # Cek apakah nama lauk sudah ada
    if lauk_collection.find_one({'nama_lauk': nama_lauk}):
        lauk_list = lauk_collection.find()
        return render_template('lauk.html', lauk_list=lauk_list, error="Lauk sudah terdaftar", edit_mode=False)
    
    lauk_collection.insert_one({'nama_lauk': nama_lauk})
    return redirect(url_for('lauk_bp.lauk'))

# Ambil data untuk edit
@lauk_bp.route('/lauk/edit/<id>', methods=['GET'])
def get_edit_lauk(id):
    lauk_data = lauk_collection.find_one({"_id": ObjectId(id)})
    lauk_list = lauk_collection.find()
    return render_template('lauk.html', lauk_data=lauk_data, lauk_list=lauk_list, edit_mode=True)

# Update lauk
@lauk_bp.route('/lauk/update/<id>', methods=['POST'])
def update_lauk(id):
    nama_lauk_baru = request.form['nama_lauk_baru'].strip().lower()
    nama_lauk_lama = request.form['nama_lauk_lama'].strip().lower()

    # Cek jika nama baru berbeda dan sudah ada yang pakai
    if nama_lauk_baru != nama_lauk_lama and lauk_collection.find_one({'nama_lauk': nama_lauk_baru}):
        lauk_list = lauk_collection.find()
        lauk_data = {"_id": ObjectId(id), "nama_lauk": nama_lauk_lama}
        return render_template('lauk.html', lauk_list=lauk_list, error="Lauk baru sudah ada", edit_mode=True, lauk_data=lauk_data)

    lauk_collection.update_one({'_id': ObjectId(id)}, {'$set': {'nama_lauk': nama_lauk_baru}})
    return redirect(url_for('lauk_bp.lauk'))

# Hapus lauk
@lauk_bp.route('/lauk/delete/<id>')
def delete_lauk(id):
    lauk_collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('lauk_bp.lauk'))