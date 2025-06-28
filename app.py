from flask import Flask
from config import Config
from models import db

def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

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

    return app

app = createApp()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
