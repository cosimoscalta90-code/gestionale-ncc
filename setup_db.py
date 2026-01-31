import sqlite3

DB_NAME = "ncc.db"

# Connessione al database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


# Funzione per verificare se una colonna esiste
def column_exists(table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in cursor.fetchall()]
    return column in columns


# Aggiunge la colonna telefono se non esiste
if not column_exists("corse", "telefono"):
    try:
        cursor.execute("ALTER TABLE corse ADD COLUMN telefono TEXT")
        print("Colonna 'telefono' aggiunta.")
    except sqlite3.OperationalError as e:
        print(f"Errore nell'aggiunta della colonna 'telefono': {e}")

# Aggiunge la colonna note se non esiste
if not column_exists("corse", "note"):
    try:
        cursor.execute("ALTER TABLE corse ADD COLUMN note TEXT")
        print("Colonna 'note' aggiunta.")
    except sqlite3.OperationalError as e:
        print(f"Errore nell'aggiunta della colonna 'note': {e}")

# Commit e chiusura della connessione
conn.commit()
conn.close()

print("Database aggiornato!")
