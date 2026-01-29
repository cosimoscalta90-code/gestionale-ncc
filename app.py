from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "ncc.db"

# Crea il database se non esiste
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabella clienti
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clienti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            telefono TEXT,
            email TEXT
        )
    """)
    # Tabella corse
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            ora TEXT,
            partenza TEXT,
            destinazione TEXT,
            prezzo REAL,
            stato TEXT,
            FOREIGN KEY(cliente_id) REFERENCES clienti(id)
        )
    """)
    conn.commit()
    conn.close()


# ROUTE principale
@app.route("/")
def index():
    return "<h1>Gestionale NCC pronto!</h1><p>Vai su /cliente per inserire clienti</p>"


# Inserisci cliente via web
@app.route("/cliente", methods=["GET", "POST"])
def cliente():
    if request.method == "POST":
        nome = request.form["nome"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clienti (nome, telefono, email) VALUES (?, ?, ?)",
            (nome, telefono, email))
        conn.commit()
        conn.close()

        return redirect("/cliente")

    # Form HTML
    return """
    <h2>Nuovo cliente</h2>
    <form method="post">
      <input name="nome" placeholder="Nome"><br>
      <input name="telefono" placeholder="Telefono"><br>
      <input name="email" placeholder="Email"><br>
      <button type="submit">Salva</button>
    </form>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
