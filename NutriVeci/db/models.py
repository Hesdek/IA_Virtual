import psycopg2
from config import DB_CONFIG

def connect():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        chat_id BIGINT PRIMARY KEY,
        nombre TEXT,
        edad INTEGER,
        peso REAL,
        altura REAL
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def guardar_usuario(chat_id, nombre, edad, peso, altura):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO usuarios (chat_id, nombre, edad, peso, altura)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (chat_id) DO UPDATE SET
        nombre = EXCLUDED.nombre,
        edad = EXCLUDED.edad,
        peso = EXCLUDED.peso,
        altura = EXCLUDED.altura;
    """, (chat_id, nombre, edad, peso, altura))
    conn.commit()
    cur.close()
    conn.close()
