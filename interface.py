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
        cur.execute("SELECT * FROM Fornecedor")
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
            INSERT INTO Estoque (estoque_id, produto_id, local_id, quantidade)
            VALUES (%s, %s, %s, %s)
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
        cur.execute("SELECT estoque_id, produto_id, local_id, quantidade, data_ultima_movimentacao FROM Estoque")
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



janela.mainloop()
