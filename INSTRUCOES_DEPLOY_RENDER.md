# 🚀 Guia Completo de Deploy no Render

## ✅ Pré-requisitos

- [x] Código do projeto no GitHub (repositório público ou privado)
- [x] Conta no Render (https://render.com)
- [x] `requirements.txt` atualizado com todas as dependências
- [x] `wsgi.py` configurado corretamente
- [x] Variáveis de ambiente definidas

---

## 📋 Passo 1: Preparar Código para Produção

### 1.1 Verificar `requirements.txt`
Ensure que está com as versões corretas:

```txt
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
psycopg2-binary==2.9.11
email-validator==2.1.0
gunicorn==21.2.0
```

### 1.2 Verificar `wsgi.py`
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)  # IMPORTANTE: debug=False em produção
```

### 1.3 Verificar `app/__init__.py`
```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Configurações para produção
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key-mudar')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///orcamentos.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,  # Verifica conexão antes de usar
    }

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    CSRFProtect(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import Usuario
    return Usuario.query.get(int(user_id))
```

### 1.4 Criar `.gitignore`
```gitignore
# Virtual Environment
venv/
env/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Flask
instance/
.webassets-cache
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
.env.local
.env.*.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

### 1.5 Fazer Push para GitHub
```bash
git add .
git commit -m "Preparar para deploy Render"
git push origin main
```

---

## 📊 Passo 2: Criar Banco de Dados PostgreSQL no Render

1. **Acessar Render Dashboard**: https://dashboard.render.com

2. **Criar PostgreSQL Database**:
   - Clique em **New** → **PostgreSQL**
   - **Name**: `orcaweb-db` (ou o nome que desejar)
   - **Region**: São Paulo, Brazil (recomendado para Brasil) ou `Seatle/Virginia`
   - **PostgreSQL Version**: 14+ (recomendado)
   - **Database**: `orcaweb` (será criado automaticamente)
   - **User**: `postgres` (padrão)
   - **Clique Create Database**

3. **Copiar Connection String**:
   - Após criar, você verá a URL da conexão
   - Formato: `postgresql://user:password@host:5432/database`
   - **IMPORTANTE**: Salvar em local seguro (não commitir!)

---

## 🌐 Passo 3: Criar Web Service no Render

### 3.1 Iniciar novo Web Service
1. Dashboard Render → **New** → **Web Service**
2. **Connect from GitHub**:
   - Autorizar Render a acessar seu GitHub
   - Selecionar o repositório `app-web-orcamento`
   - Clique **Connect**

### 3.2 Configurar Web Service
Preencher os campos:

| Campo | Valor |
|-------|-------|
| **Name** | `orcaweb` |
| **Environment** | `Python 3` |
| **Region** | São Paulo (mesmo da DB) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn wsgi:app` |

### 3.3 Adicionar Environment Variables
Clique em **Add Environment Variable** para cada um:

```
SECRET_KEY = (gerar valor aleatório, veja abaixo)
DATABASE_URL = (copiar da PostgreSQL que criou)
FLASK_ENV = production
ADMIN_EMAIL = admin@example.com
ADMIN_PASSWORD = (gerar senha forte)
```

#### Gerar SECRET_KEY Seguro:
```bash
# No terminal local:
python -c "import secrets; print(secrets.token_hex(32))"

# Saída exemplo: 3a7f9c2e1b8d4c5a9e7b3f2c8d1a4e6f7c9b2e5d
```

#### Gerar ADMIN_PASSWORD:
```bash
python -c "import secrets; print(secrets.token_urlsafe(16))"

# Saída exemplo: aBcDeFgHiJkLmNoP
```

### 3.4 Clique Create Web Service
- Render iniciará o build automaticamente
- Você pode monitorar o progresso na aba **Logs**
- Build deve levar 2-5 minutos

---

## 🗄️ Passo 4: Inicializar Banco de Dados

Após o Web Service ser deployado com sucesso, você precisa criar as tabelas.

### Opção A: Via Script Python (Recomendado)

1. **Modificar temporariamente `wsgi.py`**:
```python
from app import create_app, db
from app.models import Usuario, Cliente, ContatoCliente, EnderecoCliente, Item, Orcamento, OrcamentoItem
from werkzeug.security import generate_password_hash
import os

app = create_app()

# Criar todas as tabelas
with app.app_context():
    db.create_all()
    
    # Criar usuário admin padrão
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    
    existing_admin = Usuario.query.filter_by(email=admin_email).first()
    if not existing_admin:
        admin = Usuario(
            nome="Administrador",
            email=admin_email,
            senha_hash=generate_password_hash(admin_password),
            ativo=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Usuário admin criado: {admin_email}")
    else:
        print("⚠️  Usuário admin já existe")

if __name__ == '__main__':
    app.run(debug=False)
```

2. **Fazer push desta versão**:
```bash
git add wsgi.py
git commit -m "Adicionar inicialização de DB ao deploy"
git push origin main
```

3. **Trigger redeploy no Render**:
   - Dashboard → `orcaweb` → **Deployments**
   - Clique **Manual Deploy** ou aguarde auto-deploy do commit

4. **Verificar logs**:
   - Aba **Logs** deve mostrar:
     ```
     ✅ Usuário admin criado: admin@example.com
     ```

5. **Reverter `wsgi.py` para versão normal** (sem a lógica de DB):
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
```

```bash
git add wsgi.py
git commit -m "Remover inicialização de DB"
git push origin main
```

### Opção B: Via Terminal PostgreSQL (Alternativa)

Se tiver psql instalado localmente:

```bash
# Copiar DATABASE_URL do Render
psql postgresql://user:password@host:5432/database < create_tables.sql
```

---

## 🔗 Passo 5: Verificar Deploy

### 5.1 Acessar Aplicação
- Após deploy bem-sucedido, Render fornecerá um URL público
- Formato: `https://orcaweb.onrender.com`
- Clique no link do Render Dashboard ou na aba **View Logs**

### 5.2 Testar Login
- Email: `admin@example.com`
- Senha: A que você definiu em `ADMIN_PASSWORD`

### 5.3 Verificar Banco de Dados
- Dashboard Render → PostgreSQL Service
- Aba **Connections**
- Usar DBeaver ou pgAdmin para verificar as tabelas

---

## 🔄 Passo 6: Configurações Avançadas (Opcional)

### 6.1 Custom Domain
1. Dashboard → Web Service → **Settings**
2. Scroll para **Custom Domain**
3. Adicionar domínio (ex: `orcaweb.com.br`)
4. Configurar DNS do registrar com CNAME fornecido

### 6.2 Auto-Deploy
- Render deploya automaticamente a cada push no GitHub
- Você pode desabilitar em **Settings** → **Auto-Deploy**

### 6.3 Health Checks
- Render faz health checks automáticos
- Se aplicação cair, tenta reiniciar
- Configurável em **Settings** → **Health Check Path**

### 6.4 Log Retention
- Logs são mantidos por 7 dias no plano gratuito
- Plano pago oferece mais retenção

---

## 🐛 Troubleshooting

### Erro: "Application failed to start"

**Causa provável**: Banco de dados não inicializado

**Solução**:
```bash
# Verificar logs
# Dashboard → Logs → ver erro exato

# Comum: psycopg2 import error
# Solução: Garantir que psycopg2-binary está em requirements.txt

# Ou: DATABASE_URL mal formatada
# Solução: Verificar em Render → Environment Variables
```

### Erro: "No such file or directory: 'static/logo.png'"

**Causa**: Arquivo de imagem não commitado no Git

**Solução**:
```bash
# Criar logo.png em static/
# Ou remover referência se não for crítico
git add static/
git commit -m "Adicionar assets estáticos"
git push
```

### Erro: "CSRF token missing"

**Causa**: SESSION_COOKIE_SECURE não está configurado para HTTPS

**Solução**: Adicionar em `app/__init__.py`:
```python
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

### Aplicação lenta em produção

**Causas**: Pool de conexão, queries N+1, sem índices

**Soluções**:
1. Aumentar pool size em `app/__init__.py`
2. Adicionar índices no PostgreSQL:
   ```sql
   CREATE INDEX idx_orcamento_cliente ON orcamentos(cliente_id);
   CREATE INDEX idx_orcamento_usuario ON orcamentos(usuario_id);
   ```
3. Usar lazy loading estratégico

### Banco de dados cheio/quota excedida

**Render free**: 
- 256 MB PostgreSQL
- Armazenar dados otimizados
- Limpar tabelas antigas regularmente

---

## 💾 Passo 7: Backup e Recuperação

### 7.1 Backup do PostgreSQL
```bash
# Render faz backups automáticos
# Dashboard → PostgreSQL → Backups

# Backup manual:
pg_dump postgresql://user:pass@host:5432/db > backup.sql
```

### 7.2 Restaurar Backup
```bash
psql postgresql://user:pass@host:5432/db < backup.sql
```

### 7.3 Exportar Dados
```bash
# CSV de toda tabela
\copy (SELECT * FROM clientes) TO 'clientes.csv' WITH CSV HEADER;
```

---

## 📊 Monitoramento Contínuo

### Verificações Regulares
- [ ] Logs de erro no Render Dashboard
- [ ] Performance do Web Service (CPU, Memory)
- [ ] Uso de banco de dados
- [ ] SSL Certificate (renovação automática)

### Alerts Recomendados (Plano Pago)
- CPU > 80%
- Memory > 90%
- Web Service restarts > 3/dia
- Database connection errors

---

## 🔐 Segurança em Produção

✅ **Checklist de Segurança**:

- [x] `SECRET_KEY` é aleatória e forte (32+ chars)
- [x] `DEBUG = False` em produção
- [x] HTTPS ativado (Render default)
- [x] CSRF protection habilitada
- [x] Senhas hasheadas (werkzeug.security)
- [x] SQL Injection protegido (SQLAlchemy ORM)
- [x] XSS protegido (Jinja2 auto-escape)
- [x] `.env` não commitido no Git
- [x] PostgreSQL com firewall (Render default)
- [x] Session cookies com flags secure

---

## 📈 Próximos Passos

1. **Monitorar produção** por 1-2 semanas
2. **Coletar feedback** de usuários
3. **Adicionar features** baseado em uso real
4. **Escalar recursos** conforme crescimento

---

## 🆘 Contato/Support

- **Render Support**: https://support.render.com
- **Flask Docs**: https://flask.palletsprojects.com
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **PostgreSQL Docs**: https://www.postgresql.org/docs

---

**Versão**: 1.0  
**Data**: Fevereiro 2026  
**Plataforma**: Render.com  
**Stack**: Flask + PostgreSQL + Gunicorn
