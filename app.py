from flask import Flask, request, redirect, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "ncc.db"

# --- Creazione database ---
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            data TEXT,
            ora TEXT,
            partenza TEXT,
            destinazione TEXT,
            prezzo REAL,
            stato TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Home page ---
@app.route("/")
def index():
    return """
    <h1>Gestionale NCC pronto!</h1>
    <p><a href='/corsa'>Inserisci nuova corsa</a></p>
    <p><a href='/agenda'>Visualizza agenda corse</a></p>
    """

# --- Inserimento corsa ---
@app.route("/corsa", methods=["GET", "POST"])
def corsa():
    if request.method == "POST":
        cliente = request.form["cliente"]
        data = request.form["data"]
        ora = request.form["ora"]
        partenza = request.form["partenza"]
        destinazione = request.form["destinazione"]
        prezzo = request.form["prezzo"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO corse (cliente, data, ora, partenza, destinazione, prezzo, stato) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (cliente, data, ora, partenza, destinazione, prezzo, "")
        )
        conn.commit()
        conn.close()

        return redirect("/corsa")

    html = """
    <h2>Nuova corsa</h2>
    <form method="post">
      <input name="cliente" placeholder="Nome cliente" required><br>
      <input type="date" name="data" required><br>
      <input type="time" name="ora" required><br>
      <input name="partenza" placeholder="Partenza" required><br>
      <input name="destinazione" placeholder="Destinazione" required><br>
      <input name="prezzo" placeholder="Prezzo (€)" required><br>
      <button type="submit">Salva corsa</button>
    </form>
    <br>
    <a href='/agenda'>Vai all'agenda corse</a> | <a href='/'>Home</a>
    """
    return render_template_string(html)

# --- Agenda corse ---
@app.route("/agenda")
def agenda():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cliente, data, ora, partenza, destinazione, prezzo FROM corse ORDER BY data, ora"
    )
    corse = cursor.fetchall()
    conn.close()

    html = "<h2>Agenda corse</h2>"
    html += "<table border='1' cellpadding='5'><tr><th>Cliente</th><th>Data</th><th>Ora</th><th>Partenza</th><th>Destinazione</th><th>Prezzo (€)</th></tr>"
    for c in corse:
        html += f"<tr><td>{c[0]}</td><td>{c[1]}</td><td>{c[2]}</td><td>{c[3]}</td><td>{c[4]}</td><td>{c[5]}</td></tr>"
    html += "</table>"
    html += "<br><a href='/corsa'>Nuova corsa</a> | <a href='/'>Home</a>"

    return html

# --- Avvio server ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
