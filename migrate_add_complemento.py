from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Adicionar coluna complemento à tabela enderecos_cliente
    try:
        db.session.execute(text("ALTER TABLE enderecos_cliente ADD COLUMN complemento VARCHAR(100)"))
        db.session.commit()
        print("Coluna complemento adicionada com sucesso.")
    except Exception as e:
        print(f"Erro ao adicionar coluna: {e}")
        # Se já existe, ignora
