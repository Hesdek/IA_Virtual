import psycopg2
from config import DB_CONFIG

def connect():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        chat_id BIGINT PRIMARY KEY,
        nombre TEXT,
        edad INTEGER,
        peso REAL,
        altura REAL,
        objetivo TEXT,
        metas TEXT
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def guardar_usuario(chat_id, nombre, edad, peso, altura, objetivo, metas):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO usuarios (chat_id, nombre, edad, peso, altura, objetivo, metas)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (chat_id) DO UPDATE SET
            nombre = EXCLUDED.nombre,
            edad = EXCLUDED.edad,
            peso = EXCLUDED.peso,
            altura = EXCLUDED.altura,
            objetivo = EXCLUDED.objetivo,
            metas = EXCLUDED.metas;
        """, (chat_id, nombre, edad, peso, altura, objetivo, metas))
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error al guardar el usuario: {e}")
    finally:
        cur.close()
        conn.close()