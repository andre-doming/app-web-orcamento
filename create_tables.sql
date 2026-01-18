-- Script SQL para criar tabelas no PostgreSQL

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    observacoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contatos_cliente (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    tipo VARCHAR(20) NOT NULL,
    valor VARCHAR(100) NOT NULL,
    principal BOOLEAN DEFAULT FALSE
);

CREATE TABLE enderecos_cliente (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    logradouro VARCHAR(200) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(100),
    bairro VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    cep VARCHAR(10) NOT NULL
);

CREATE TABLE itens (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    descricao TEXT,
    unidade VARCHAR(20) DEFAULT 'unidade',
    valor_unitario NUMERIC(10, 2) NOT NULL
);

CREATE TABLE orcamentos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    endereco_cliente_id INTEGER NOT NULL REFERENCES enderecos_cliente(id),
    data_orcamento DATE NOT NULL,
    data_validade DATE NOT NULL,
    valor_total NUMERIC(10, 2) NOT NULL DEFAULT 0,
    aprovado BOOLEAN DEFAULT FALSE
);

CREATE TABLE orcamento_itens (
    id SERIAL PRIMARY KEY,
    orcamento_id INTEGER NOT NULL REFERENCES orcamentos(id),
    item_id INTEGER NOT NULL REFERENCES itens(id),
    quantidade NUMERIC(10, 2) NOT NULL,
    valor_unitario NUMERIC(10, 2) NOT NULL,
    valor_total NUMERIC(10, 2) NOT NULL
);

-- Inserir usuário admin
INSERT INTO usuarios (nome, email, senha_hash, ativo) VALUES ('Admin', 'admin@example.com', 'pbkdf2:sha256:600000$your_hash_here', TRUE);
-- Nota: Substitua 'your_hash_here' pelo hash real gerado pelo Flask
