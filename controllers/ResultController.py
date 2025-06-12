from flask import Blueprint, render_template
from config import db

result_bp = Blueprint('result_bp', __name__)

# Setup MongoDB
result_collection = db["result"]

# Tampilkan result
@result_bp.route('/result')
def result():
    result_list = result_collection.find()
    return render_template('result.html', result_list=result_list)