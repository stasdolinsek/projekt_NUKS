import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Povezava uspešna. SQLite baza podatkov je verzije:", sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS txt_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content TEXT NOT NULL
            );
        """)
        print("Tabela ustvarjena uspešno.")
    except Error as e:
        print(e)

def add_txt_file(conn, filename, content):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO txt_files (filename, content) VALUES (?, ?)", (filename, content))
            print("Datoteka uspešno shranjena.")
    except Error as e:
        print(e)

def get_all_txt_files(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM txt_files")
        rows = cursor.fetchall()
        files = [{"id": row[0], "filename": row[1], "content": row[2]} for row in rows]
        return files
    except Error as e:
        print(e)
        return []

def delete_txt_file(file_id, db_file):
    conn = create_connection(db_file)
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM txt_files WHERE id = ?", (file_id,))
        conn.commit()
        rowcount = cursor.rowcount
        conn.close()
        return rowcount
