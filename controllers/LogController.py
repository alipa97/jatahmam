from flask import Blueprint, render_template
from config import db

log_bp = Blueprint('log_bp', __name__)

# Setup MongoDB
log_collection = db["log"]

# Tampilkan log
@log_bp.route('/log')
def log():
    log_list = log_collection.find()
    return render_template('log.html', log_list-log_list)