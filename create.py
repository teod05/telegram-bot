import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('messages.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY,
    message_history TEXT,
    token_spent INTEGER DEFAULT 0
)
''')
conn.commit()
conn.close()