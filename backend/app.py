import os
import sqlite3
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-dev'

DB_PATH = os.environ.get('DB_PATH', '/app/data/events.db')
NOTIFIER_URL = os.environ.get('NOTIFIER_URL', 'http://mailer:5001/send-ticket')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    events = conn.execute("SELECT * FROM events ORDER BY id ASC").fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/register', methods=['POST'])
def register():
    event_id = request.form.get('event_id')
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()

    if not (event_id and full_name and email and phone):
        flash("Пожалуйста, заполните все поля формы.", "error")
        return redirect(url_for('index'))

    conn = get_db()
    try:
        event = conn.execute("SELECT title, seats_available FROM events WHERE id = ?", (event_id,)).fetchone()
        if not event:
            flash("Мероприятие не найдено.", "error")
            return redirect(url_for('index'))

        if event['seats_available'] <= 0:
            flash("К сожалению, свободные места закончились.", "error")
            return redirect(url_for('index'))

        conn.execute(
            "INSERT INTO registrations (event_id, full_name, email, phone) VALUES (?, ?, ?, ?)",
            (event_id, full_name, email, phone)
        )
        conn.execute("UPDATE events SET seats_available = seats_available - 1 WHERE id = ?", (event_id,))
        conn.commit()

        # Межсервисный вызов отдельного микросервиса mailer
        try:
            requests.post(NOTIFIER_URL, json={
                'recipient_email': email,
                'recipient_name': full_name,
                'event_title': event['title']
            }, timeout=3)
        except Exception as mail_err:
            print(f"[BACKEND WARNING] Mailer service call error: {mail_err}", flush=True)

        return render_template('success.html', name=full_name, event=event['title'], email=email)
    except Exception as e:
        conn.rollback()
        flash(f"Ошибка сохранения: {str(e)}", "error")
        return redirect(url_for('index'))
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
