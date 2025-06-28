from app import app
from models import db, User

with app.app_context():
    admin = User(
        name="Admin",
        email="admin@if.com",
        password="123456",
        isAdmin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Admin criado com sucesso!")
