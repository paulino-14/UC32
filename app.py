# Catálogo de Filmes - UC32
# Sistema CRUD com Flask + SQLite

import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave-secreta-do-trabalho"

# nome do arquivo do banco de dados
DATABASE = "filmes.db"


# ---------------------------------------------------
# Conexão com o banco
# ---------------------------------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    # row_factory deixa acessar as colunas pelo nome (filme["titulo"])
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------
# Cria a tabela automaticamente quando o app inicia
# ---------------------------------------------------
def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            genero TEXT NOT NULL,
            ano INTEGER NOT NULL,
            nota INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# chama aqui em cima (fora do __main__) pra funcionar também no gunicorn do Render
init_db()


# ---------------------------------------------------
# READ - listar todos os filmes
# ---------------------------------------------------
@app.route("/")
def index():
    conn = get_db()
    filmes = conn.execute("SELECT * FROM filmes ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", filmes=filmes)


# ---------------------------------------------------
# CREATE - cadastrar novo filme
# ---------------------------------------------------
@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        genero = request.form["genero"].strip()
        ano = request.form["ano"]
        nota = request.form["nota"]

        # validação simples: nota tem que ser de 1 a 10
        if not titulo or not genero or not ano or not nota:
            flash("Preencha todos os campos!")
            return render_template("form.html", filme=None)

        if int(nota) < 1 or int(nota) > 10:
            flash("A nota precisa ser de 1 a 10!")
            return render_template("form.html", filme=None)

        conn = get_db()
        conn.execute(
            "INSERT INTO filmes (titulo, genero, ano, nota) VALUES (?, ?, ?, ?)",
            (titulo, genero, int(ano), int(nota)),
        )
        conn.commit()
        conn.close()

        flash("Filme cadastrado com sucesso!")
        return redirect(url_for("index"))

    # se for GET só mostra o formulário vazio
    return render_template("form.html", filme=None)


# ---------------------------------------------------
# UPDATE - editar um filme
# ---------------------------------------------------
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = get_db()
    filme = conn.execute("SELECT * FROM filmes WHERE id = ?", (id,)).fetchone()

    # se não achou o filme volta pra lista
    if filme is None:
        conn.close()
        flash("Filme não encontrado!")
        return redirect(url_for("index"))

    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        genero = request.form["genero"].strip()
        ano = request.form["ano"]
        nota = request.form["nota"]

        if not titulo or not genero or not ano or not nota:
            conn.close()
            flash("Preencha todos os campos!")
            return render_template("form.html", filme=filme)

        if int(nota) < 1 or int(nota) > 10:
            conn.close()
            flash("A nota precisa ser de 1 a 10!")
            return render_template("form.html", filme=filme)

        conn.execute(
            "UPDATE filmes SET titulo = ?, genero = ?, ano = ?, nota = ? WHERE id = ?",
            (titulo, genero, int(ano), int(nota), id),
        )
        conn.commit()
        conn.close()

        flash("Filme atualizado com sucesso!")
        return redirect(url_for("index"))

    conn.close()
    return render_template("form.html", filme=filme)


# ---------------------------------------------------
# DELETE - excluir um filme
# ---------------------------------------------------
@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    conn = get_db()
    conn.execute("DELETE FROM filmes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash("Filme excluído!")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
