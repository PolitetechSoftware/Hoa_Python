import sqlite3


def create_db():
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()

    # Create the table with cumulative fields
    c.execute('''
        CREATE TABLE IF NOT EXISTS function_metrics (
            func_name TEXT UNIQUE,
            num_calls INTEGER DEFAULT 0,
            avg_time REAL DEFAULT 0.0,
            num_errors INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

