from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    # Criar usuário admin se não existir
    if not Usuario.query.filter_by(email='admin@example.com').first():
        admin = Usuario(
            nome='Admin',
            email='admin@example.com',
            senha_hash=generate_password_hash('admin123'),
            ativo=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Usuário admin criado: admin@example.com / admin123")
    else:
        print("Usuário admin já existe.")
