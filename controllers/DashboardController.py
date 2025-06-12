from flask import Blueprint, render_template
from config import db

dashboard_bp = Blueprint('dashboard_bp', __name__)

# Setup MongoDB
santri_collection = db["santri"]

# Home
@dashboard_bp.route('/')
def home():
    total_santri = santri_collection.count_documents({})
    return render_template('index.html', total_santri=total_santri)