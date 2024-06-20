import psycopg2
from faker import Faker
import random
import time

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

# Função para inserir dados em massa
def insert_massive_data(n):
    produtos_pereciveis = []
    produtos_nao_pereciveis = []
    for _ in range(n):
        # Dados para produtos perecíveis
        nome_p = fake.word()
        descricao_p = fake.text()
        preco_p = round(random.uniform(1.0, 100.0), 2)
        quantidade_p = random.randint(1, 100)
        data_validade_p = fake.date_between(start_date="today", end_date="+1y")
        categoria_p = fake.word(ext_word_list=['Laticínios', 'Carnes', 'Frutas', 'Verduras', 'Bebidas'])
        filial_id_p = random.randint(1, 10)
        produtos_pereciveis.append((nome_p, descricao_p, preco_p, quantidade_p, data_validade_p, categoria_p, filial_id_p))

        # Dados para produtos não perecíveis
        nome_np = fake.word()
        descricao_np = fake.text()
        preco_np = round(random.uniform(1.0, 100.0), 2)
        quantidade_np = random.randint(1, 100)
        categoria_np = fake.word(ext_word_list=['Grãos', 'Enlatados', 'Bebidas', 'Snacks', 'Condimentos'])
        filial_id_np = random.randint(1, 10)
        produtos_nao_pereciveis.append((nome_np, descricao_np, preco_np, quantidade_np, categoria_np, filial_id_np))
    
    # Inserindo dados nas tabelas
    start_time = time.time()
    cur.executemany(
        "INSERT INTO Produtos_Pereciveis (nome, descricao, preco, quantidade, data_validade, categoria, filial_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        produtos_pereciveis
    )
    conn.commit()
    pereciveis_insert_time = time.time() - start_time
    
    start_time = time.time()
    cur.executemany(
        "INSERT INTO Produtos_Nao_Pereciveis (nome, descricao, preco, quantidade, categoria, filial_id) VALUES (%s, %s, %s, %s, %s, %s)",
        produtos_nao_pereciveis
    )
    conn.commit()
    nao_pereciveis_insert_time = time.time() - start_time
    
    return pereciveis_insert_time, nao_pereciveis_insert_time

# Função para realizar consultas de estoque
def query_stock(n):
    start_time = time.time()
    for _ in range(n):
        filial_id = random.randint(1, 10)
        cur.execute("SELECT * FROM Produtos_Pereciveis WHERE filial_id = %s", (filial_id,))
        cur.fetchall()
    pereciveis_query_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(n):
        filial_id = random.randint(1, 10)
        cur.execute("SELECT * FROM Produtos_Nao_Pereciveis WHERE filial_id = %s", (filial_id,))
        cur.fetchall()
    nao_pereciveis_query_time = time.time() - start_time
    
    return pereciveis_query_time, nao_pereciveis_query_time

# Função para realizar atualizações de inventário
def update_inventory(n):
    start_time = time.time()
    for _ in range(n):
        produto_id = random.randint(1, 10000)
        nova_quantidade = random.randint(1, 200)
        cur.execute("UPDATE Produtos_Pereciveis SET quantidade = %s WHERE produto_id = %s", (nova_quantidade, produto_id))
    conn.commit()
    pereciveis_update_time = time.time() - start_time
    
    start_time = time.time()
    for _ in range(n):
        produto_id = random.randint(1, 10000)
        nova_quantidade = random.randint(1, 200)
        cur.execute("UPDATE Produtos_Nao_Pereciveis SET quantidade = %s WHERE produto_id = %s", (nova_quantidade, produto_id))
    conn.commit()
    nao_pereciveis_update_time = time.time() - start_time
    
    return pereciveis_update_time, nao_pereciveis_update_time

# Função para adicionar novas filiais
def add_new_filiais(n):
    filiais = []
    for _ in range(n):
        nome_f = fake.company()
        endereco_f = fake.address()
        cidade_f = fake.city()
        estado_f = fake.state()
        cep_f = fake.zipcode()
        filiais.append((nome_f, endereco_f, cidade_f, estado_f, cep_f))
    
    start_time = time.time()
    cur.executemany(
        "INSERT INTO Filiais (nome, endereco, cidade, estado, cep) VALUES (%s, %s, %s, %s, %s)",
        filiais
    )
    conn.commit()
    filiais_insert_time = time.time() - start_time
    
    return filiais_insert_time

# Função principal para executar os testes
def main():
    num_records = 10000
    num_queries = 1000
    num_updates = 1000
    num_filiais = 100

    # Inserir dados em massa
    pereciveis_insert_time, nao_pereciveis_insert_time = insert_massive_data(num_records)
    print(f"Inserção de {num_records} produtos perecíveis: {pereciveis_insert_time:.2f} segundos")
    print(f"Inserção de {num_records} produtos não perecíveis: {nao_pereciveis_insert_time:.2f} segundos")
    
    # Consultar estoque
    pereciveis_query_time, nao_pereciveis_query_time = query_stock(num_queries)
    print(f"Consulta de estoque {num_queries} vezes para produtos perecíveis: {pereciveis_query_time:.2f} segundos")
    print(f"Consulta de estoque {num_queries} vezes para produtos não perecíveis: {nao_pereciveis_query_time:.2f} segundos")
    
    # Atualizar inventário
    pereciveis_update_time, nao_pereciveis_update_time = update_inventory(num_updates)
    print(f"Atualização de inventário {num_updates} vezes para produtos perecíveis: {pereciveis_update_time:.2f} segundos")
    print(f"Atualização de inventário {num_updates} vezes para produtos não perecíveis: {nao_pereciveis_update_time:.2f} segundos")
    
    # Adicionar novas filiais
    filiais_insert_time = add_new_filiais(num_filiais)
    print(f"Inserção de {num_filiais} novas filiais: {filiais_insert_time:.2f} segundos")

# Executar a função principal
if __name__ == "__main__":
    main()

# Fechar a conexão
cur.close()
conn.close()
