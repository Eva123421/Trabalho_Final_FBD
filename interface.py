import tkinter as tk
from tkinter import ttk, messagebox
from codigo import conectar

janela = tk.Tk()
janela.title("Sistema de Gestão de Armazém")
janela.geometry("1000x700")

abas = ttk.Notebook(janela)
abas.pack(fill='both', expand=True)

# -------------------------------
# Produto
# -------------------------------
aba_produto = ttk.Frame(abas)
abas.add(aba_produto, text="Produto")

#Formulario Produto
form_produto = tk.Frame(aba_produto)
form_produto.pack(pady=10)

entrys_produto = {}
campos_produto = ["produto_id", "nome", "descricao", "peso", "data_validade", "categoria_id"]
for i, campo in enumerate(campos_produto):
    tk.Label(form_produto, text=campo).grid(row=i, column=0)
    entry = tk.Entry(form_produto)
    entry.grid(row=i, column=1)
    entrys_produto[campo] = entry
frame_busca = tk.Frame(aba_produto)
frame_busca.pack(pady=10)

tk.Label(frame_busca, text="Buscar por ID:").grid(row=0, column=0)
entry_busca_id = tk.Entry(frame_busca)
entry_busca_id.grid(row=0, column=1)

tk.Label(frame_busca, text="Buscar por Nome:").grid(row=0, column=2)
entry_busca_nome = tk.Entry(frame_busca)
entry_busca_nome.grid(row=0, column=3)

def inserir_produto():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Produto (produto_id, nome, descricao, peso, data_validade, categoria_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(entrys_produto[c].get() for c in campos_produto))
        con.commit()
        cur.close()
        con.close()
        listar_produtos()
        messagebox.showinfo("Sucesso", "Produto inserido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_produtos():
    for i in tree_produto.get_children():
        tree_produto.delete(i)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Produto p ORDER BY p.produto_id ASC")
        for row in cur.fetchall():
            tree_produto.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_produto():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE Produto
            SET nome = %s,
                descricao = %s,
                peso = %s,
                data_validade = %s,
                categoria_id = %s
            WHERE produto_id = %s
        """, (
            entrys_produto["nome"].get(),
            entrys_produto["descricao"].get(),
            entrys_produto["peso"].get(),
            entrys_produto["data_validade"].get(),
            entrys_produto["categoria_id"].get(),
            entrys_produto["produto_id"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_produtos()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_produto():
    selected = tree_produto.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um produto para remover.")
        return

    valores = tree_produto.item(selected, 'values')
    produto_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o produto ID {produto_id}?\nTodos os registros relacionados também serão removidos.")
    if not confirm:
        return

    try:
        con = conectar()
        cur = con.cursor()
    
        # Agora pode remover o produto
        cur.execute("DELETE FROM Produto WHERE produto_id = %s", (produto_id,))

        con.commit()
        cur.close()
        con.close()
        listar_produtos()
        messagebox.showinfo("Sucesso", "Produto e registros relacionados removidos com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def buscar_produto():
    id_busca = entry_busca_id.get().strip()
    nome_busca = entry_busca_nome.get().strip()

    query = "SELECT * FROM Produto WHERE 1=1"
    params = []

    if id_busca:
        query += " AND produto_id = %s"
        params.append(id_busca)

    if nome_busca:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome_busca}%")

    for i in tree_produto.get_children():
        tree_produto.delete(i)

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            tree_produto.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))



#Botões Produto
tk.Button(form_produto, text="Inserir Produto", command=inserir_produto).grid(row=len(campos_produto), columnspan=2, pady=10)
tk.Button(form_produto, text="Atualizar Produto", command=atualizar_produto).grid(row=len(campos_produto)+1, columnspan=2, pady=5)
tk.Button(form_produto, text="Remover Produto", command=remover_produto).grid(row=len(campos_produto)+2, columnspan=2, pady=5)
tk.Button(frame_busca, text="Buscar", command=buscar_produto).grid(row=0, column=4, padx=10)


tree_produto = ttk.Treeview(aba_produto, columns=campos_produto, show='headings')
for c in campos_produto:
    tree_produto.heading(c, text=c)
tree_produto.pack(fill='both', expand=True, padx=10, pady=10)

tk.Button(aba_produto, text="Listar Produtos", command=listar_produtos).pack(pady=10)

# -------------------------------
# Fornecedor
# -------------------------------
aba_fornecedor = ttk.Frame(abas)
abas.add(aba_fornecedor, text="Fornecedor")

#Formulario Fornecedor
form_forn = tk.Frame(aba_fornecedor)
form_forn.pack(pady=10)

entrys_forn = {}
campos_forn = ["fornecedor_id", "nome", "cnpj", "endereco", "telefone", "email"]
for i, campo in enumerate(campos_forn):
    tk.Label(form_forn, text=campo).grid(row=i, column=0)
    entry = tk.Entry(form_forn)
    entry.grid(row=i, column=1)
    entrys_forn[campo] = entry
frame_busca_forn = tk.Frame(aba_fornecedor)
frame_busca_forn.pack(pady=10)

tk.Label(frame_busca_forn, text="Buscar por ID:").grid(row=0, column=0)
entry_busca_forn_id = tk.Entry(frame_busca_forn)
entry_busca_forn_id.grid(row=0, column=1)

tk.Label(frame_busca_forn, text="Buscar por Nome:").grid(row=0, column=2)
entry_busca_forn_nome = tk.Entry(frame_busca_forn)
entry_busca_forn_nome.grid(row=0, column=3)

def inserir_fornecedor():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Fornecedor (fornecedor_id, nome, cnpj, endereco, telefone, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(entrys_forn[c].get() for c in campos_forn))
        con.commit()
        cur.close()
        con.close()
        listar_fornecedores()
        messagebox.showinfo("Sucesso", "Fornecedor inserido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_fornecedores():
    for i in tree_forn.get_children():
        tree_forn.delete(i)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Fornecedor f ORDER BY f.fornecedor_id ASC")
        for row in cur.fetchall():
            tree_forn.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_fornecedor():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE Fornecedor
            SET nome = %s,
                cnpj = %s,
                endereco = %s,
                telefone = %s,
                email = %s
            WHERE fornecedor_id = %s
        """, (
            entrys_forn["nome"].get(),
            entrys_forn["cnpj"].get(),
            entrys_forn["endereco"].get(),
            entrys_forn["telefone"].get(),
            entrys_forn["email"].get(),
            entrys_forn["fornecedor_id"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_fornecedores()
        messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_fornecedor():
    selected = tree_forn.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um fornecedor para remover.")
        return

    valores = tree_forn.item(selected, 'values')
    fornecedor_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o fornecedor ID {fornecedor_id}?")
    if not confirm:
        return

    try:
        con = conectar()
        cur = con.cursor()

        # Remover fornecedor (e os relacionamentos em ProdutoFornecedor, se necessário em trigger ou manual)
        cur.execute("DELETE FROM Fornecedor WHERE fornecedor_id = %s", (fornecedor_id,))

        con.commit()
        cur.close()
        con.close()
        listar_fornecedores()
        messagebox.showinfo("Sucesso", "Fornecedor removido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def buscar_fornecedor():
    id_busca = entry_busca_forn_id.get().strip()
    nome_busca = entry_busca_forn_nome.get().strip()

    query = "SELECT * FROM Fornecedor WHERE 1=1"
    params = []

    if id_busca:
        query += " AND fornecedor_id = %s"
        params.append(id_busca)

    if nome_busca:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome_busca}%")

    for i in tree_forn.get_children():
        tree_forn.delete(i)

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            tree_forn.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

tk.Button(form_forn, text="Inserir Fornecedor", command=inserir_fornecedor).grid(row=len(campos_forn), columnspan=2, pady=10)

tree_forn = ttk.Treeview(aba_fornecedor, columns=campos_forn, show='headings')
for c in campos_forn:
    tree_forn.heading(c, text=c)
tree_forn.pack(fill='both', expand=True, padx=10, pady=10)

#Botões Fornecedor
tk.Button(aba_fornecedor, text="Listar Fornecedores", command=listar_fornecedores).pack(pady=10)
tk.Button(form_forn, text="Atualizar Fornecedor", command=atualizar_fornecedor).grid(row=len(campos_forn)+1, columnspan=2, pady=5)
tk.Button(form_forn, text="Remover Fornecedor", command=remover_fornecedor).grid(row=len(campos_forn)+2, columnspan=2, pady=5)
tk.Button(frame_busca_forn, text="Buscar", command=buscar_fornecedor).grid(row=0, column=4, padx=10)

# -------------------------------
# Estoque
# -------------------------------
aba_estoque = ttk.Frame(abas)
abas.add(aba_estoque, text="Estoque")

#Formulario Estoque
form_estoque = tk.Frame(aba_estoque)
form_estoque.pack(pady=10)

entrys_estoque = {}
campos_estoque = ["estoque_id", "produto_id", "local_id", "quantidade"]
for i, campo in enumerate(campos_estoque):
    tk.Label(form_estoque, text=campo).grid(row=i, column=0)
    entry = tk.Entry(form_estoque)
    entry.grid(row=i, column=1)
    entrys_estoque[campo] = entry

frame_busca_estoque = tk.Frame(aba_estoque)
frame_busca_estoque.pack(pady=10)

tk.Label(frame_busca_estoque, text="Buscar por ID:").grid(row=0, column=0)
entry_busca_estoque_id = tk.Entry(frame_busca_estoque)
entry_busca_estoque_id.grid(row=0, column=1)

tk.Label(frame_busca_estoque, text="Buscar por Produto ID:").grid(row=0, column=2)
entry_busca_estoque_produto = tk.Entry(frame_busca_estoque)
entry_busca_estoque_produto.grid(row=0, column=3)

def inserir_estoque():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Estoque (estoque_id, produto_id, local_id, quantidade,data_ultima_movimentacao)
            VALUES (%s, %s, %s, %s,CURRENT_DATE)
        """, tuple(entrys_estoque[c].get() for c in campos_estoque))
        con.commit()
        cur.close()
        con.close()
        listar_estoques()
        messagebox.showinfo("Sucesso", "Estoque inserido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_estoques():
    for i in tree_estoque.get_children():
        tree_estoque.delete(i)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Estoque e ORDER BY e.estoque_id ASC")
        for row in cur.fetchall():
            tree_estoque.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_estoque():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE Estoque
            SET produto_id = %s,
                local_id = %s,
                quantidade = %s
            WHERE estoque_id = %s
        """, (
            entrys_estoque["produto_id"].get(),
            entrys_estoque["local_id"].get(),
            entrys_estoque["quantidade"].get(),
            entrys_estoque["estoque_id"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_estoques()
        messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_estoque():
    selected = tree_estoque.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um registro de estoque para remover.")
        return

    valores = tree_estoque.item(selected, 'values')
    estoque_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o estoque ID {estoque_id}?")
    if not confirm:
        return

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM Estoque WHERE estoque_id = %s", (estoque_id,))
        con.commit()
        cur.close()
        con.close()
        listar_estoques()
        messagebox.showinfo("Sucesso", "Estoque removido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def buscar_estoque():
    id_busca = entry_busca_estoque_id.get().strip()
    prod_busca = entry_busca_estoque_produto.get().strip()

    query = "SELECT estoque_id, produto_id, local_id, quantidade, data_ultima_movimentacao FROM Estoque WHERE 1=1"
    params = []

    if id_busca:
        query += " AND estoque_id = %s"
        params.append(id_busca)

    if prod_busca:
        query += " AND produto_id = %s"
        params.append(prod_busca)

    for i in tree_estoque.get_children():
        tree_estoque.delete(i)

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            tree_estoque.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

#Botões Estoque
tk.Button(form_estoque, text="Inserir Estoque", command=inserir_estoque).grid(row=len(campos_estoque), columnspan=2, pady=10)
tk.Button(form_estoque, text="Atualizar Estoque", command=atualizar_estoque).grid(row=len(campos_estoque)+1, columnspan=2, pady=5)
tk.Button(form_estoque, text="Remover Estoque", command=remover_estoque).grid(row=len(campos_estoque)+2, columnspan=2, pady=5)
tk.Button(frame_busca_estoque, text="Buscar", command=buscar_estoque).grid(row=0, column=4, padx=10)


tree_estoque = ttk.Treeview(aba_estoque, columns=["estoque_id", "produto_id", "local_id", "quantidade", "data_ultima_movimentacao"], show='headings')
for c in ["estoque_id", "produto_id", "local_id", "quantidade", "data_ultima_movimentacao"]:
    tree_estoque.heading(c, text=c)
tree_estoque.pack(fill='both', expand=True, padx=10, pady=10)

tk.Button(aba_estoque, text="Listar Estoques", command=listar_estoques).pack(pady=10)

# -------------------------------
# Categoria
# -------------------------------
aba_categoria = ttk.Frame(abas)
abas.add(aba_categoria, text="Categoria")

# Formulário Categoria
form_categoria = tk.Frame(aba_categoria)
form_categoria.pack(pady=10)

entrys_categoria = {}
campos_categoria = ["categoria_id", "nome"]
for i, campo in enumerate(campos_categoria):
    tk.Label(form_categoria, text=campo).grid(row=i, column=0)
    entry = tk.Entry(form_categoria)
    entry.grid(row=i, column=1)
    entrys_categoria[campo] = entry

# Campo de busca por ID
frame_busca_categoria = tk.Frame(aba_categoria)
frame_busca_categoria.pack(pady=10)

tk.Label(frame_busca_categoria, text="Buscar por ID:").grid(row=0, column=0)
entry_busca_categoria_id = tk.Entry(frame_busca_categoria)
entry_busca_categoria_id.grid(row=0, column=1)

tk.Label(frame_busca_categoria, text="Buscar por nome:").grid(row=0, column=2)
entry_busca_categoria_nome = tk.Entry(frame_busca_categoria)
entry_busca_categoria_nome.grid(row=0, column=3)

# Funções Categoria
def inserir_categoria():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Categoria (categoria_id, nome)
            VALUES (%s, %s)
        """, tuple(entrys_categoria[c].get() for c in campos_categoria))
        con.commit()
        cur.close()
        con.close()
        listar_categorias()
        messagebox.showinfo("Sucesso", "Categoria inserida com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_categorias():
    for i in tree_categoria.get_children():
        tree_categoria.delete(i)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria ORDER BY categoria_id ASC")
        for row in cur.fetchall():
            tree_categoria.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_categoria():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE Categoria
            SET nome = %s
            WHERE categoria_id = %s
        """, (
            entrys_categoria["nome"].get(),
            entrys_categoria["categoria_id"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_categorias()
        messagebox.showinfo("Sucesso", "Categoria atualizada com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_categoria():
    selected = tree_categoria.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione uma categoria para remover.")
        return

    valores = tree_categoria.item(selected, 'values')
    categoria_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover a categoria ID {categoria_id}?")
    if not confirm:
        return

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM Categoria WHERE categoria_id = %s", (categoria_id,))
        con.commit()
        cur.close()
        con.close()
        listar_categorias()
        messagebox.showinfo("Sucesso", "Categoria removida com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def buscar_categoria():
    id_busca = entry_busca_categoria_id.get().strip()
    nome_busca = entry_busca_categoria_nome.get().strip()

    query = "SELECT categoria_id, nome FROM Categoria WHERE 1=1"
    params = []

    if id_busca:
        query += " AND categoria_id = %s"
        params.append(id_busca)
    if nome_busca:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome_busca}%")
    for i in tree_categoria.get_children():
        tree_categoria.delete(i)

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            tree_categoria.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Botões Categoria
tk.Button(form_categoria, text="Inserir Categoria", command=inserir_categoria).grid(row=len(campos_categoria), columnspan=2, pady=10)
tk.Button(form_categoria, text="Atualizar Categoria", command=atualizar_categoria).grid(row=len(campos_categoria)+1, columnspan=2, pady=5)
tk.Button(form_categoria, text="Remover Categoria", command=remover_categoria).grid(row=len(campos_categoria)+2, columnspan=2, pady=5)
tk.Button(frame_busca_categoria, text="Buscar", command=buscar_categoria).grid(row=0, column=4, padx=10)


tree_categoria = ttk.Treeview(aba_categoria, columns=["categoria_id", "nome"], show='headings')
for c in ["categoria_id", "nome"]:
    tree_categoria.heading(c, text=c)
tree_categoria.pack(fill='both', expand=True, padx=10, pady=10)

tk.Button(aba_categoria, text="Listar Categorias", command=listar_categorias).pack(pady=10)



# -------------------------------
# Local de Armazenagem
# -------------------------------
aba_local = ttk.Frame(abas)
abas.add(aba_local, text="LocalArmazenagem")

# Formulário Local
form_local = tk.Frame(aba_local)
form_local.pack(pady=10)

entrys_local = {}
campos_local = ["local_id", "nome", "tipo", "capacidade_maxima", "descricao"]
for i, campo in enumerate(campos_local):
    tk.Label(form_local, text=campo).grid(row=i, column=0)
    entry = tk.Entry(form_local)
    entry.grid(row=i, column=1)
    entrys_local[campo] = entry

# Campo de busca 
frame_busca_local = tk.Frame(aba_local)
frame_busca_local.pack(pady=10)

tk.Label(frame_busca_local, text="Buscar por ID:").grid(row=0, column=0)
entry_busca_local_id = tk.Entry(frame_busca_local)
entry_busca_local_id.grid(row=0, column=1)

tk.Label(frame_busca_local, text="Buscar por Nome:").grid(row=0, column=2)
entry_busca_local_nome = tk.Entry(frame_busca_local)
entry_busca_local_nome.grid(row=0, column=3)

# Funções Local
def inserir_local():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO LocalArmazenagem (local_id, nome, tipo, capacidade_maxima, descricao)
            VALUES (%s, %s, %s, %s, %s)
        """, tuple(entrys_local[c].get() for c in campos_local))
        con.commit()
        cur.close()
        con.close()
        listar_locais()
        messagebox.showinfo("Sucesso", "Local inserido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_locais():
    for i in tree_local.get_children():
        tree_local.delete(i)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM LocalArmazenagem ORDER BY local_id ASC")
        for row in cur.fetchall():
            tree_local.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_local():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE LocalArmazenagem
            SET nome = %s,
                tipo = %s,
                capacidade_maxima = %s,
                descricao = %s
            WHERE local_id = %s
        """, (
            entrys_local["nome"].get(),
            entrys_local["tipo"].get(),
            entrys_local["capacidade_maxima"].get(),
            entrys_local["descricao"].get(),
            entrys_local["local_id"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_locais()
        messagebox.showinfo("Sucesso", "Local atualizado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_local():
    selected = tree_local.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um local para remover.")
        return

    valores = tree_local.item(selected, 'values')
    local_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o local ID {local_id}?")
    if not confirm:
        return

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM LocalArmazenagem WHERE local_id = %s", (local_id,))
        con.commit()
        cur.close()
        con.close()
        listar_locais()
        messagebox.showinfo("Sucesso", "Local removido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def buscar_local():
    id_busca = entry_busca_local_id.get().strip()
    nome_busca = entry_busca_local_nome.get().strip()

    query = "SELECT local_id, nome, tipo, capacidade_maxima, descricao FROM LocalArmazenagem WHERE 1=1"
    params = []

    if id_busca:
        query += " AND local_id = %s"
        params.append(id_busca)

    if nome_busca:
        query += " AND nome ILIKE %s"
        params.append(f"%{nome_busca}%")

    for i in tree_local.get_children():
        tree_local.delete(i)

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            tree_local.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Botões LocalArmazenagem
tk.Button(form_local, text="Inserir Local", command=inserir_local).grid(row=len(campos_local), columnspan=2, pady=10)
tk.Button(form_local, text="Atualizar Local", command=atualizar_local).grid(row=len(campos_local)+1, columnspan=2, pady=5)
tk.Button(form_local, text="Remover Local", command=remover_local).grid(row=len(campos_local)+2, columnspan=2, pady=5)
tk.Button(frame_busca_local, text="Buscar", command=buscar_local).grid(row=0, column=4, padx=10)


tree_local = ttk.Treeview(aba_local, columns=campos_local, show='headings')
for c in campos_local:
    tree_local.heading(c, text=c)
tree_local.pack(fill='both', expand=True, padx=10, pady=10)

tk.Button(aba_local, text="Listar Locais", command=listar_locais).pack(pady=10)


# -------------------------------
# Inventário
# -------------------------------
aba_inventario = ttk.Frame(abas)
abas.add(aba_inventario, text="Inventário")

# Formulário Inventário
form_inventario = tk.Frame(aba_inventario)
form_inventario.pack(pady=10)

entrys_inventario = {}
campos_inventario = ["inventario_id", "produto_id", "local_id", "quantidade_sistema", "quantidade_fisica", "observacoes"]
for i, campo in enumerate(campos_inventario):
    tk.Label(form_inventario, text=campo).grid(row=i, column=0)
    entry = tk.Entry(form_inventario)
    entry.grid(row=i, column=1)
    entrys_inventario[campo] = entry


frame_busca_inventario = tk.Frame(aba_inventario)
frame_busca_inventario.pack(pady=10)

tk.Label(frame_busca_inventario, text="Buscar por ID:").grid(row=0, column=0)
entry_busca_inventario_id = tk.Entry(frame_busca_inventario)
entry_busca_inventario_id.grid(row=0, column=1)

tk.Label(frame_busca_inventario, text="Buscar por LocalID:").grid(row=0, column=2)
entry_busca_inventario_localID = tk.Entry(frame_busca_inventario)
entry_busca_inventario_localID.grid(row=0, column=3)

# Funções Inventário
def inserir_inventario():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            INSERT INTO Inventario (inventario_id, produto_id, local_id, data, quantidade_sistema, quantidade_fisica, observacoes)
            VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, %s)
        """, (
            entrys_inventario["inventario_id"].get(),
            entrys_inventario["produto_id"].get(),
            entrys_inventario["local_id"].get(),
            entrys_inventario["quantidade_sistema"].get(),
            entrys_inventario["quantidade_fisica"].get(),
            entrys_inventario["observacoes"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_inventarios()
        messagebox.showinfo("Sucesso", "Inventário inserido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_inventarios():
    for i in tree_inventario.get_children():
        tree_inventario.delete(i)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT * FROM Inventario ORDER BY inventario_id ASC")
        for row in cur.fetchall():
            tree_inventario.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_inventario():
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("""
            UPDATE Inventario
            SET produto_id = %s,
                local_id = %s,
                quantidade_sistema = %s,
                quantidade_fisica = %s,
                observacoes = %s
            WHERE inventario_id = %s
        """, (
            entrys_inventario["produto_id"].get(),
            entrys_inventario["local_id"].get(),
            entrys_inventario["quantidade_sistema"].get(),
            entrys_inventario["quantidade_fisica"].get(),
            entrys_inventario["observacoes"].get(),
            entrys_inventario["inventario_id"].get()
        ))
        con.commit()
        cur.close()
        con.close()
        listar_inventarios()
        messagebox.showinfo("Sucesso", "Inventário atualizado com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_inventario():
    selected = tree_inventario.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um inventário para remover.")
        return

    valores = tree_inventario.item(selected, 'values')
    inventario_id = valores[0]

    confirm = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o inventário ID {inventario_id}?")
    if not confirm:
        return

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM Inventario WHERE inventario_id = %s", (inventario_id,))
        con.commit()
        cur.close()
        con.close()
        listar_inventarios()
        messagebox.showinfo("Sucesso", "Inventário removido com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def buscar_inventario():
    id_busca = entry_busca_inventario_id.get().strip()
    localID_busca = entry_busca_inventario_localID.get().strip()

    query = "SELECT inventario_id, produto_id, local_id, data, quantidade_sistema, quantidade_fisica, observacoes FROM Inventario WHERE 1=1"
    params = []

    if id_busca:
        query += " AND inventario_id = %s"
        params.append(id_busca)

    if localID_busca:
        query += " AND local_id = %s"
        params.append(localID_busca)

    for i in tree_inventario.get_children():
        tree_inventario.delete(i)

    try:
        con = conectar()
        cur = con.cursor()
        cur.execute(query, tuple(params))
        for row in cur.fetchall():
            tree_inventario.insert("", tk.END, values=row)
        cur.close()
        con.close()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Botões Inventário
tk.Button(form_inventario, text="Inserir Inventário", command=inserir_inventario).grid(row=len(campos_inventario), columnspan=2, pady=10)
tk.Button(form_inventario, text="Atualizar Inventário", command=atualizar_inventario).grid(row=len(campos_inventario)+1, columnspan=2, pady=5)
tk.Button(form_inventario, text="Remover Inventário", command=remover_inventario).grid(row=len(campos_inventario)+2, columnspan=2, pady=5)
tk.Button(frame_busca_inventario, text="Buscar", command=buscar_inventario).grid(row=0, column=4, padx=10)

# Treeview Inventário
tree_inventario = ttk.Treeview(aba_inventario, columns=["inventario_id", "produto_id", "local_id", "data", "quantidade_sistema", "quantidade_fisica", "observacoes"], show='headings')
for c in ["inventario_id", "produto_id", "local_id", "data", "quantidade_sistema", "quantidade_fisica", "observacoes"]:
    tree_inventario.heading(c, text=c)
tree_inventario.pack(fill='both', expand=True, padx=10, pady=10)

tk.Button(aba_inventario, text="Listar Inventários", command=listar_inventarios).pack(pady=10)

#--------------------------------
# Consultas Avançadas
#--------------------------------
aba_consultas = ttk.Frame(abas)
abas.add(aba_consultas, text="Consultas Avançadas")

# Frame de botão e resultado
frame_top = ttk.Frame(aba_consultas)
frame_top.pack(pady=10)

# Botão para executar a consulta
def executar_consulta():
    try:
        conn = conectar()
        cur = conn.cursor()

        # Consulta: quantidade de produtos por fornecedor
        cur.execute("""
            SELECT 
                f.nome AS fornecedor,
                COUNT(pf.produto_id) AS quantidade_produtos
            FROM 
                Fornecedor f
            JOIN 
                ProdutoFornecedor pf ON f.fornecedor_id = pf.fornecedor_id
            GROUP BY 
                f.nome
            ORDER BY 
                quantidade_produtos DESC;
        """)

        # Limpar tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Inserir resultados
        for linha in cur.fetchall():
            tabela.insert('', 'end', values=linha)

        cur.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao executar consulta:\n{e}")

# Botão
botao_consulta = ttk.Button(frame_top, text="Mostrar Produtos por Fornecedor", command=executar_consulta)
botao_consulta.pack()

# Tabela para exibir os resultados
colunas = ("Fornecedor", "Quantidade de Produtos")
tabela = ttk.Treeview(aba_consultas, columns=colunas, show="headings", height=10)

for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, width=250)

tabela.pack(pady=10)



janela.mainloop()
