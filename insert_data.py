import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Configurações de conexão ao PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="supermercado",
    user="postgres",
    password="password"
)
cur = conn.cursor()

# Instancia o gerador de dados Faker
fake = Faker()

# Função para criar filiais
def create_filiais(n):
    filiais = []
    for _ in range(n):
        nome = fake.company()
        endereco = fake.street_address()
        cidade = fake.city()
        estado = fake.state()
        cep = fake.zipcode()
        filiais.append((nome, endereco, cidade, estado, cep))
    cur.executemany(
        "INSERT INTO Filiais (nome, endereco, cidade, estado, cep) VALUES (%s, %s, %s, %s, %s)",
        filiais
    )
    conn.commit()

# Função para criar produtos perecíveis
def create_produtos_pereciveis(n):
    produtos = []
    for _ in range(n):
        nome = fake.word()
        descricao = fake.text()
        preco = round(random.uniform(1.0, 100.0), 2)
        quantidade = random.randint(1, 100)
        data_validade = fake.date_between(start_date="today", end_date="+1y")
        categoria = fake.word(ext_word_list=['Laticínios', 'Carnes', 'Frutas', 'Verduras', 'Bebidas'])
        filial_id = random.randint(1, num_filiais)
        produtos.append((nome, descricao, preco, quantidade, data_validade, categoria, filial_id))
    cur.executemany(
        "INSERT INTO Produtos_Pereciveis (nome, descricao, preco, quantidade, data_validade, categoria, filial_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        produtos
    )
    conn.commit()

# Função para criar produtos não perecíveis
def create_produtos_nao_pereciveis(n):
    produtos = []
    for _ in range(n):
        nome = fake.word()
        descricao = fake.text()
        preco = round(random.uniform(1.0, 100.0), 2)
        quantidade = random.randint(1, 100)
        categoria = fake.word(ext_word_list=['Grãos', 'Enlatados', 'Bebidas', 'Snacks', 'Condimentos'])
        filial_id = random.randint(1, num_filiais)
        produtos.append((nome, descricao, preco, quantidade, categoria, filial_id))
    cur.executemany(
        "INSERT INTO Produtos_Nao_Pereciveis (nome, descricao, preco, quantidade, categoria, filial_id) VALUES (%s, %s, %s, %s, %s, %s)",
        produtos
    )
    conn.commit()

# Função para criar detalhes de preço e quantidade de produtos perecíveis
def create_detalhes_preco_quantidade_pereciveis():
    cur.execute("SELECT produto_id, preco, quantidade FROM Produtos_Pereciveis")
    produtos = cur.fetchall()
    detalhes = [(produto[0], produto[1], produto[2]) for produto in produtos]
    cur.executemany(
        "INSERT INTO Detalhes_Preco_Quantidade_Pereciveis (produto_id, preco, quantidade) VALUES (%s, %s, %s)",
        detalhes
    )
    conn.commit()

# Função para criar detalhes de preço e quantidade de produtos não perecíveis
def create_detalhes_preco_quantidade_nao_pereciveis():
    cur.execute("SELECT produto_id, preco, quantidade FROM Produtos_Nao_Pereciveis")
    produtos = cur.fetchall()
    detalhes = [(produto[0], produto[1], produto[2]) for produto in produtos]
    cur.executemany(
        "INSERT INTO Detalhes_Preco_Quantidade_Nao_Pereciveis (produto_id, preco, quantidade) VALUES (%s, %s, %s)",
        detalhes
    )
    conn.commit()

# Função para criar detalhes de descrição de produtos perecíveis
def create_detalhes_descricao_pereciveis():
    cur.execute("SELECT produto_id, descricao, data_validade FROM Produtos_Pereciveis")
    produtos = cur.fetchall()
    detalhes = [(produto[0], produto[1], produto[2]) for produto in produtos]
    cur.executemany(
        "INSERT INTO Detalhes_Descricao_Pereciveis (produto_id, descricao, data_validade) VALUES (%s, %s, %s)",
        detalhes
    )
    conn.commit()

# Função para criar detalhes de descrição de produtos não perecíveis
def create_detalhes_descricao_nao_pereciveis():
    cur.execute("SELECT produto_id, descricao FROM Produtos_Nao_Pereciveis")
    produtos = cur.fetchall()
    detalhes = [(produto[0], produto[1]) for produto in produtos]
    cur.executemany(
        "INSERT INTO Detalhes_Descricao_Nao_Pereciveis (produto_id, descricao) VALUES (%s, %s)",
        detalhes
    )
    conn.commit()

# Número de filiais a serem criadas
num_filiais = 100
create_filiais(num_filiais)

# Número de produtos a serem criados em cada categoria
num_produtos_pereciveis = 50000
num_produtos_nao_pereciveis = 50000
create_produtos_pereciveis(num_produtos_pereciveis)
create_produtos_nao_pereciveis(num_produtos_nao_pereciveis)

# Criar detalhes de produtos
create_detalhes_preco_quantidade_pereciveis()
create_detalhes_preco_quantidade_nao_pereciveis()
create_detalhes_descricao_pereciveis()
create_detalhes_descricao_nao_pereciveis()

# Fechar a conexão
cur.close()
conn.close()
