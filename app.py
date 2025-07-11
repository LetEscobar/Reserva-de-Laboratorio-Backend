from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from flask_migrate import Migrate

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate = Migrate(app, db)
    
    CORS(app,
     resources={r"/*": {"origins": "http://localhost:5173"}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    from routes.auth import authBp
    from routes.admin import adminBp
    from routes.lab import labBp
    from routes.reservation import reservationBp
    from routes.class_public import classPublicBp

    app.register_blueprint(authBp, url_prefix='/auth')
    app.register_blueprint(adminBp, url_prefix='/admin')
    app.register_blueprint(labBp, url_prefix='/labs')
    app.register_blueprint(reservationBp, url_prefix='/reservations')
    app.register_blueprint(classPublicBp)

    @app.after_request
    def aplicar_cors_global(resposta):
        resposta.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        resposta.headers["Access-Control-Allow-Credentials"] = "true"
        resposta.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        resposta.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        return resposta

    return app

app = createApp()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
