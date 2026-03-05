# 📊 SQLite vs PostgreSQL - Análise Comparativa

## 📌 Questão: Devo usar PostgreSQL no Render?

**Resposta Curta**: **SIM, PostgreSQL é recomendado para produção no Render**

---

## 🔄 Comparação Detalhada

| Aspecto | SQLite | PostgreSQL |
|---------|--------|-----------|
| **Setup** | Zero - apenas arquivo `.db` | Requer servidor, mas Render fornece |
| **Performance** | ~5K queries/seg | ~50K queries/seg |
| **Concorrência** | ❌ Fraco (locks de arquivo) | ✅ Excelente (multi-usuário) |
| **Tamanho DB** | Máx ~140TB teórico, 2GB prático | Ilimitado praticamente |
| **Backup** | Cópia de arquivo | Snapshots automáticos |
| **Escalabilidade** | Não | ✅ Sim |
| **Ideal Para** | Dev local, prototipagem | Produção, múltiplos usuários |
| **Licença** | Public Domain | Open Source (PostgreSQL License) |
| **Suporte** | Comunidade | Comunidade + Empresas |

---

## 🏗️ Seu Caso: OrçaWeb

### Características do Seu Sistema
- ✅ Múltiplos usuários simultâneos
- ✅ Dados críticos (orçamentos, clientes)
- ✅ Relações complexas entre tabelas
- ✅ Backup necessário
- ✅ Deploy em produção (Render)

### Recomendação
```
╔════════════════════════════════════════════════════════════════╗
║           🎯 USE POSTGRESQL EM PRODUÇÃO (RENDER)             ║
║                                                                ║
║  Razões:                                                       ║
║  1. SQLite locks = perda de dados em concorrência              ║
║  2. PostgreSQL = transações ACID = dados seguros              ║
║  3. Render oferece PostgreSQL gratuito (Tier Free)             ║
║  4. Migrações SQL mais robustas                                ║
║  5. Monitoramento melhor                                       ║
║                                                                ║
║  Para desenvolvimento local: SQLite está OK                   ║
║  Para produção: PostgreSQL OBRIGATÓRIO                        ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 💾 Estratégia Recomendada

### Desenvolvimento Local
```
DATABASE_URL = sqlite:///orcamentos.db  (arquivo local)

Vantagens:
✅ Zero setup
✅ Rápido
✅ Debug fácil
❌ Diferente de produção
```

### Produção (Render)
```
DATABASE_URL = postgresql://user:pass@host:5432/orcaweb

Vantagens:
✅ Idêntico a desenvolvimento
✅ Multi-usuário
✅ Transações ACID
✅ Backups automáticos
✅ Scalável
```

### Implementação
```python
# app/__init__.py
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///orcamentos.db'  # Default para dev local
)

# Isto permite:
# - Rodar localmente com SQLite
# - Rodar em Render com PostgreSQL
# Sem mudar código!
```

---

## 🐛 Problemas de SQLite em Produção

### 1. Concorrência
```
Usuário A: UPDATE orcamentos SET aprovado = TRUE WHERE id = 1
Usuário B: SELECT * FROM orcamentos WHERE cliente_id = 1

⚠️ ERRO: Database locked (arquivo está sendo escrito)
```

**PostgreSQL**: Múltiplos usuários leem/escrevem simultaneamente ✅

### 2. Corrupção de Dados
```
Aplicação cai durante escrita → arquivo SQLite fica corrompido
Dados perdidos permanentemente
```

**PostgreSQL**: Logs de transação = recuperação automática ✅

### 3. File System em Cloud
```
Render roda em containers efêmeros
/tmp/ é limpado entre redeploys
Arquivo .db sumiria!
```

**PostgreSQL**: Dados em servidor persistente ✅

---

## 🚀 Setup PostgreSQL no Render

### Passo 1: Criar Database (2 minutos)
1. Dashboard Render → **New** → **PostgreSQL**
2. Region: São Paulo
3. Clique **Create**

### Passo 2: Copiar URL
```
DATABASE_URL = postgresql://user:pass@orcaweb.render.com:5432/orcaweb
```

### Passo 3: Adicionar a Web Service
```
Environment Variables:
  DATABASE_URL = (copiar acima)
  SECRET_KEY = (gerar com: python -c "import secrets; print(secrets.token_hex(32))")
```

### Passo 4: Deploy
```
Build: pip install -r requirements.txt
Start: gunicorn wsgi:app
```

**Tempo total**: 5 minutos ⚡

---

## 💰 Custo no Render (Free Tier)

| Serviço | Limite | Custo |
|---------|--------|-------|
| Web Service | 50 free hours/month | $0.10/hour extra |
| PostgreSQL | 256 MB | $0 (free tier) |
| Bandwidth | Ilimitado | $0.10/GB extra |

**Para sua app**: **R$ 0 a R$ 5/mês** 🎉

(Pode usar como laboratório/prototipagem sem custo)

---

## 📈 Migração: SQLite → PostgreSQL

Se já está rodando em SQLite e quer migrar:

### Opção 1: Manual (Recomendado)
```bash
# Exportar dados do SQLite
sqlite3 orcamentos.db ".mode insert usuarios" > usuarios.sql

# Importar em PostgreSQL
psql -U postgres -d orcaweb -f usuarios.sql
```

### Opção 2: Python (Mais fácil)
```python
from app import create_app, db
from app.models import *

# Contexto SQLite (local)
app_sqlite = create_app()
app_sqlite.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orcamentos.db'

with app_sqlite.app_context():
    usuarios = Usuario.query.all()
    dados = [u.to_dict() for u in usuarios]

# Contexto PostgreSQL (Render)
app_pg = create_app()
app_pg.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'

with app_pg.app_context():
    for user_data in dados:
        u = Usuario(**user_data)
        db.session.add(u)
    db.session.commit()
```

---

## ⚙️ Compatibilidade de Código

### ✅ O código Flask funciona EXATAMENTE igual

```python
# Seu código atual funciona 100% com PostgreSQL
# Não precisa mudar nada!

from app import create_app

app = create_app()  # Funciona com qualquer BD

# Seu models.py:
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # SQLAlchemy abstrai SQLite vs PostgreSQL

# Suas rotas:
@bp.route('/usuarios')
def usuarios():
    usuarios = Usuario.query.all()  # Funciona igual em qualquer BD
    return render_template('usuarios.html', usuarios=usuarios)
```

**SQLAlchemy ORM**: Compatível com ambos ✅

---

## 🔧 Configuração Recomendada (Híbrida)

### Local (Development)
```python
# .env (nunca commitir)
DATABASE_URL=sqlite:///orcamentos.db
FLASK_ENV=development
SECRET_KEY=dev-key-123
```

### Render (Production)
```
Dashboard → Web Service → Environment
DATABASE_URL = postgresql://...
FLASK_ENV = production
SECRET_KEY = gerar com secrets.token_hex(32)
```

### Código (Neutro)
```python
# app/__init__.py
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'sqlite:///orcamentos.db'  # Fallback para dev
)

# Funciona em ambos os contextos!
```

---

## 📋 Checklist: PostgreSQL no Render

- [ ] Criar PostgreSQL no Render Dashboard
- [ ] Copiar DATABASE_URL fornecida
- [ ] Adicionar variável de ambiente na Web Service
- [ ] Configurar SECRET_KEY
- [ ] Fazer push do código
- [ ] Render faz auto-deploy
- [ ] Verificar logs
- [ ] Testar login
- [ ] Verificar dados no banco

---

## 🆘 Troubleshooting PostgreSQL

### Erro: "could not translate host name to address"
**Causa**: DATABASE_URL inválida
**Solução**: Copiar exatamente do Render Dashboard

### Erro: "psycopg2: connection refused"
**Causa**: PostgreSQL não está rodando
**Solução**: Verificar em Render → Services → PostgreSQL está "available"

### Erro: "permission denied for schema public"
**Causa**: Usuário sem permissões
**Solução**: Render fornece usuário com permissões corretas, verificar URL

### Aplicação lenta
**Causa**: Falta de indexes, queries N+1
**Solução**: Adicionar indexes em FKs:
```sql
CREATE INDEX idx_orcamento_cliente ON orcamentos(cliente_id);
CREATE INDEX idx_orcamento_usuario ON orcamentos(usuario_id);
```

---

## 📚 Recursos

- PostgreSQL Free Tier Render: https://render.com/pricing
- Docs Render PostgreSQL: https://render.com/docs/databases
- SQLAlchemy PostgreSQL: https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
- Comparação SQLite vs PostgreSQL: https://www.sqlite.org/whentouse.html

---

## 🎯 Resumo Executivo

```
┌─────────────────────────────────────────────────────────────┐
│                    RECOMENDAÇÃO FINAL                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Desenvolvimento Local:  SQLite 🔄 (arquivo local)          │
│ Produção (Render):     PostgreSQL ✅ (servidor)            │
│                                                             │
│ Seu código Flask:      FUNCIONA EM AMBOS (SQLAlchemy)      │
│ Custo no Render:       R$ 0 (free tier)                    │
│ Setup Time:            5 minutos                           │
│                                                             │
│ RESULTADO: 🚀 Sistema profissional e escalável             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**Conclusão**: Para seu sistema OrçaWeb em produção, **PostgreSQL no Render é a escolha correta**. Você mantém SQLite localmente (fácil) e PostgreSQL em produção (seguro). O código Flask funciona identicamente em ambos. **Recomendação: Implemente PostgreSQL desde o início** ✅

---

**Criado em**: Fevereiro 2026  
**Para**: OrçaWeb - Decisão SQLite vs PostgreSQL
