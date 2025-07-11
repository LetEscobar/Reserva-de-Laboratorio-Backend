from app import app
from models import db, User

with app.app_context():

    if not User.query.filter_by(email="admin@estudante.ifms.edu.br").first():
        admin = User(
            name="Admin",
            email="admin@estudante.ifms.edu.br",
            password="Senha@123",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin criado com sucesso!")
    else:
        print("⚠️ Admin já existe")
