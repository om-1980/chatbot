import sqlite3

DB_PATH = "database/voice_bot.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            intent TEXT,
            response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_interaction(user_query, intent, response):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO interactions (user_query, intent, response)
        VALUES (?, ?, ?)
    ''', (user_query, intent, response))
    conn.commit()
    conn.close()

def fetch_interaction_logs():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM interactions ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows
