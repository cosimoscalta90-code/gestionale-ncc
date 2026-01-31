from flask import Flask, request, redirect, render_template, url_for
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "ncc.db"

# -------------------------
# CREAZIONE DATABASE
# -------------------------
if not os.path.exists(DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE corse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            data TEXT,
            ora TEXT,
            partenza TEXT,
            destinazione TEXT,
            prezzo REAL,
            stato TEXT,
            telefono TEXT,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()


# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------
# NUOVA CORSA
# -------------------------
@app.route("/corsa", methods=["GET", "POST"])
def nuova_corsa():
    if request.method == "POST":
        cliente = request.form["cliente"]
        data = request.form["data"]
        ora = request.form["ora"]
        partenza = request.form["partenza"]
        destinazione = request.form["destinazione"]
        prezzo_base = float(request.form["prezzo"])

        # Gestione IVA
        if request.form.get("iva"):
            prezzo = prezzo_base * 1.10
        else:
            prezzo = prezzo_base

        telefono = request.form.get("telefono", "")
        note = request.form.get("note", "")

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO corse
            (cliente, data, ora, partenza, destinazione, prezzo, stato, telefono, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (cliente, data, ora, partenza, destinazione, prezzo, "", telefono,
              note))
        conn.commit()
        conn.close()
        return redirect(url_for("agenda"))

    return render_template("corsa.html", corsa=None)


# -------------------------
# MODIFICA CORSA
# -------------------------
@app.route("/corsa/<int:id>/modifica", methods=["GET", "POST"])
def modifica_corsa(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if request.method == "POST":
        cliente = request.form["cliente"]
        data = request.form["data"]
        ora = request.form["ora"]
        partenza = request.form["partenza"]
        destinazione = request.form["destinazione"]
        prezzo_base = float(request.form["prezzo"])

        # Gestione IVA
        if request.form.get("iva"):
            prezzo = prezzo_base * 1.10
        else:
            prezzo = prezzo_base

        telefono = request.form.get("telefono", "")
        note = request.form.get("note", "")

        cursor.execute(
            """
            UPDATE corse
            SET cliente=?, data=?, ora=?, partenza=?, destinazione=?, prezzo=?, telefono=?, note=?
            WHERE id=?
        """, (cliente, data, ora, partenza, destinazione, prezzo, telefono,
              note, id))
        conn.commit()
        conn.close()
        return redirect(url_for("agenda"))

    cursor.execute("SELECT * FROM corse WHERE id=?", (id, ))
    corsa = cursor.fetchone()
    conn.close()
    return render_template("corsa.html", corsa=corsa)


# -------------------------
# ELIMINA CORSA
# -------------------------
@app.route("/corsa/<int:id>/elimina")
def elimina_corsa(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM corse WHERE id=?", (id, ))
    conn.commit()
    conn.close()
    return redirect(url_for("agenda"))


# -------------------------
# AGENDA
# -------------------------
@app.route("/agenda")
def agenda():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, cliente, telefono, data, ora, partenza, destinazione, prezzo, note
        FROM corse
        ORDER BY data, ora
    """)
    corse = cursor.fetchall()
    conn.close()
    return render_template("agenda.html", corse=corse)


# -------------------------
# CALENDARIO
# -------------------------
@app.route("/calendario")
def calendario():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, cliente, data, ora, partenza, destinazione, telefono, note
        FROM corse
    """)
    corse = cursor.fetchall()
    conn.close()

    events = []
    for c in corse:
        events.append({
            "id": c[0],
            "title": c[1],
            "start": f"{c[2]}T{c[3]}",
            "url": f"/corsa/{c[0]}/modifica",
            "extendedProps": {
                "partenza": c[4],
                "destinazione": c[5],
                "telefono": c[6],
                "note": c[7]
            }
        })
    return render_template("calendario.html", events=events)


# -------------------------
# AVVIO SERVER
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
