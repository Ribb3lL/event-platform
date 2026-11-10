CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    location TEXT NOT NULL,
    description TEXT,
    seats_total INTEGER NOT NULL,
    seats_available INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

INSERT INTO events (title, date, location, description, seats_total, seats_available) VALUES 
('DevOps Meetup 2026', '20.11.2026 18:00', 'Зал 1', 'Митап по контейнеризации и CI/CD', 50, 48),
('HighLoad Conf Online', '05.12.2026 11:00', 'Онлайн-трансляция', 'Архитектура микросервисов', 200, 185),
('AI & Data Workshop', '18.12.2026 14:00', 'Ауд. 302', 'Практика ML-пайплайнов', 30, 24);

INSERT INTO admins (username, password_hash) VALUES 
('admin', 'pbkdf2:sha256:260000$adminhash$demo');
