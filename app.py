from flask import Flask, request, redirect, render_template
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
    return render_template("index.html")

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

        return redirect("/agenda")

    return render_template("corsa.html")

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
    return render_template("agenda.html", corse=corse)

# --- Calendario ---
@app.route("/calendario")
def calendario():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, data, ora, partenza, destinazione FROM corse")
    corse = cursor.fetchall()
    conn.close()
    
    events = []
    for c in corse:
        events.append({
            'title': c[0],
            'start': f"{c[1]}T{c[2]}",
            'extendedProps': {
                'partenza': c[3],
                'destinazione': c[4]
            }
        })
    
    return render_template("calendario.html", events=events)

# --- Avvio server ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
