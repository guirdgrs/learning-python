import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

con = sqlite3.connect(ROOT_PATH / "meu_banco.db")
cur = con.cursor()

def criar_tabela(conexao, cur):
  cur.execute("""CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL
  );""")

  conexao.commit()

def inserir_dados(conexao, cur, nome, email):
  data = [(nome, email)]
  cur.execute("INSERT INTO clientes (nome, email) VALUES(?, ?);", data)
  conexao.commit()
  
def atualizar_dados(conexao, cur, nome, email, id):
  data = [(nome, email, id)]
  cur.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?;", data)
  conexao.commit()

def excluir_dados(conexao, cur, id):
  cur.execute("DELETE FROM clientes WHERE id = ?;", (id,))
  conexao.commit()

def inserir_varios_dados(conexao, cur, data):
  try:
    cur.executemany("INSERT INTO clientes (nome, email) VALUES(?, ?);", data)
    conexao.commit()
  except Exception as e:
    print(e)
    conexao.rollback()

def ler_dados(cur):
  # cur.row_factory = sqlite3.Row | row_factory é uma funcao que retorna um dicionario
  cur.execute("SELECT * FROM clientes;")
  return cur.fetchall()

def ler_dados_id(cur, id):
  cur.execute("SELECT * FROM clientes WHERE id = ?;", (id,))
  return cur.fetchone()

clientes = ler_dados(cur)
for cliente in clientes:
  print(dict(cliente))
