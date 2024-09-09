import sqlite3
from datetime import datetime

from celery import Celery

app = Celery('project', broker='redis://localhost:6379/0')


@app.task
def save_metrics_to_db(metrics):
    conn = sqlite3.connect('metrics.db')
    c = conn.cursor()

    for func_name, data in metrics.items():
        # Fetch current values
        c.execute('''
            SELECT num_calls, avg_time, num_errors FROM function_metrics WHERE func_name = ?
        ''', (func_name,))
        row = c.fetchone()

        if row:
            # Calculate new cumulative values
            current_calls, current_avg_time, current_errors = row
            new_calls = current_calls + data['num_calls']
            new_errors = current_errors + data['num_errors']

            # Calculate new average time
            new_avg_time = (current_avg_time * current_calls + data['avg_time'] * data['num_calls']) / new_calls

            # Update the record
            c.execute('''
                UPDATE function_metrics
                SET num_calls = ?, avg_time = ?, num_errors = ?, updated_at = ?
                WHERE func_name = ?
            ''', (new_calls, new_avg_time, new_errors, datetime.now(), func_name))
        else:
            # Insert new record
            c.execute('''
                INSERT INTO function_metrics (func_name, num_calls, avg_time, num_errors, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (func_name, data['num_calls'], data['avg_time'], data['num_errors'], datetime.now(), datetime.now()))

    conn.commit()
    conn.close()
