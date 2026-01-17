from . import db
from flask_login import UserMixin
from datetime import datetime

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    ativo = db.Column(db.Boolean, default=True)

    orcamentos = db.relationship('Orcamento', backref='usuario', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    observacoes = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    contatos = db.relationship('ContatoCliente', backref='cliente', lazy=True)
    enderecos = db.relationship('EnderecoCliente', backref='cliente', lazy=True)
    orcamentos = db.relationship('Orcamento', backref='cliente', lazy=True)

class ContatoCliente(db.Model):
    __tablename__ = 'contatos_cliente'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # telefone, whatsapp, email, outro
    valor = db.Column(db.String(100), nullable=False)
    principal = db.Column(db.Boolean, default=False)

class EnderecoCliente(db.Model):
    __tablename__ = 'enderecos_cliente'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    logradouro = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=False)

class Item(db.Model):
    __tablename__ = 'itens'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # produto/serviço
    descricao = db.Column(db.Text)  # Campo extra sugerido
    unidade = db.Column(db.String(20), default='unidade')  # Campo extra sugerido
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    orcamento_itens = db.relationship('OrcamentoItem', backref='item', lazy=True)

class Orcamento(db.Model):
    __tablename__ = 'orcamentos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    endereco_cliente_id = db.Column(db.Integer, db.ForeignKey('enderecos_cliente.id'), nullable=False)
    data_orcamento = db.Column(db.Date, nullable=False)
    data_validade = db.Column(db.Date, nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    aprovado = db.Column(db.Boolean, default=False)

    endereco = db.relationship('EnderecoCliente', backref='orcamentos')
    itens = db.relationship('OrcamentoItem', backref='orcamento', lazy=True, cascade='all, delete-orphan')

class OrcamentoItem(db.Model):
    __tablename__ = 'orcamento_itens'
    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamentos.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('itens.id'), nullable=False)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)
    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
