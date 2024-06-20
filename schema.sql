-- Definindo o schema para o gerenciamento de estoque de um supermercado

-- Schema para Produtos Perecíveis
CREATE TABLE Produtos_Pereciveis (
    produto_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INT NOT NULL,
    data_validade DATE NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    filial_id INT NOT NULL
);

-- Schema para Produtos Não Perecíveis
CREATE TABLE Produtos_Nao_Pereciveis (
    produto_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INT NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    filial_id INT NOT NULL
);

-- Schema para Filiais
CREATE TABLE Filiais (
    filial_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    cep VARCHAR(20) NOT NULL
);

-- Índices para otimização de consultas
CREATE INDEX idx_nome_produtos_pereciveis ON Produtos_Pereciveis (nome);
CREATE INDEX idx_nome_produtos_nao_pereciveis ON Produtos_Nao_Pereciveis (nome);
CREATE INDEX idx_categoria_produtos_pereciveis ON Produtos_Pereciveis (categoria);
CREATE INDEX idx_categoria_produtos_nao_pereciveis ON Produtos_Nao_Pereciveis (categoria);
CREATE INDEX idx_filial_produtos_pereciveis ON Produtos_Pereciveis (filial_id);
CREATE INDEX idx_filial_produtos_nao_pereciveis ON Produtos_Nao_Pereciveis (filial_id);

-- Exemplo de tabelas verticalmente particionadas para dados frequentemente acessados

-- Tabela para detalhes de preço e quantidade de produtos perecíveis
CREATE TABLE Detalhes_Preco_Quantidade_Pereciveis (
    produto_id SERIAL PRIMARY KEY,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES Produtos_Pereciveis(produto_id)
);

-- Tabela para detalhes de preço e quantidade de produtos não perecíveis
CREATE TABLE Detalhes_Preco_Quantidade_Nao_Pereciveis (
    produto_id SERIAL PRIMARY KEY,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INT NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES Produtos_Nao_Pereciveis(produto_id)
);

-- Tabela para detalhes de descrição de produtos perecíveis
CREATE TABLE Detalhes_Descricao_Pereciveis (
    produto_id SERIAL PRIMARY KEY,
    descricao TEXT,
    data_validade DATE NOT NULL,
    FOREIGN KEY (produto_id) REFERENCES Produtos_Pereciveis(produto_id)
);

-- Tabela para detalhes de descrição de produtos não perecíveis
CREATE TABLE Detalhes_Descricao_Nao_Pereciveis (
    produto_id SERIAL PRIMARY KEY,
    descricao TEXT,
    FOREIGN KEY (produto_id) REFERENCES Produtos_Nao_Pereciveis(produto_id)

);
