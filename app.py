from flask import Flask
from controllers.DashboardController import dashboard_bp
from controllers.SantriController import santri_bp
from controllers.LaukController import lauk_bp
from controllers.SesiController import sesi_bp
from controllers.LogController import log_bp
from controllers.ResultController import result_bp

app = Flask(__name__)
app.register_blueprint(santri_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(lauk_bp)
app.register_blueprint(sesi_bp)
app.register_blueprint(log_bp)
app.register_blueprint(result_bp)

if __name__ == '__main__':
    app.run(debug=True)