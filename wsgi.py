#from app import create_app
#
#app = create_app()
#
#if __name__ == '__main__':
#    app.run(debug=True)

from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash
import os
import app.models

# cria o Flask app corretamente
flask_app = create_app()

# cria tabelas e admin
with flask_app.app_context():
    db.create_all()

    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    if not Usuario.query.filter_by(email=admin_email).first():
        admin = Usuario(
            nome="Admin",
            email=admin_email,
            senha_hash=generate_password_hash(admin_password),
            ativo=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Usuario admin criado")

    else:
        print("Usuario admin ja existe")

# variável que o gunicorn usa
app = flask_app
