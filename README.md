# MID Pflegedokumentation

Eine Flask-basierte Web-Applikation zur digitalen Dokumentation von Pflegeleistungen.

**Demo-Projekt für MID - Meine Intensivpflege Daheim**

## Features

- **Klienten-Verwaltung**: Anlegen, Bearbeiten und Verwalten von Klienten mit Pflegegrad
- **Pflegedokumentation**: Erfassung von Pflegeeinträgen nach Kategorien (Grundpflege, Medikamente, Vitalzeichen, etc.)
- **Dashboard**: Übersicht mit Statistiken und letzten Einträgen
- **Responsive Design**: Optimiert für Desktop und mobile Endgeräte

## Tech-Stack

- **Backend**: Flask 3.0, SQLAlchemy, Flask-Migrate
- **Datenbank**: PostgreSQL
- **Frontend**: Jinja2 Templates, Bootstrap 5
- **Formulare**: Flask-WTF, WTForms

## Installation

### 1. Repository klonen

```bash
cd /Users/dawidkostka/software/demo
```

### 2. Virtuelle Umgebung erstellen

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL-Datenbank erstellen

```bash
createdb mid_pflegedoku
```

### 5. Datenbank-Migrationen ausführen

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. (Optional) Demo-Daten laden

```bash
python seed.py
```

### 7. Applikation starten

```bash
python run.py
```

Die App läuft unter: http://localhost:5000

## Projektstruktur

```
mid_pflegedoku/
├── app/
│   ├── __init__.py           # App Factory
│   ├── models.py             # Datenbank-Modelle
│   ├── forms.py              # WTForms
│   ├── routes/               # Blueprints
│   │   ├── main.py           # Dashboard
│   │   ├── clients.py        # Klienten CRUD
│   │   └── entries.py        # Pflegeeinträge
│   ├── templates/            # Jinja2 Templates
│   └── static/               # CSS, Assets
├── config.py                 # Konfiguration
├── requirements.txt          # Dependencies
├── seed.py                   # Demo-Daten
└── run.py                    # Entry Point
```

## Konfiguration

Umgebungsvariablen in `.env`:

```
DATABASE_URL=postgresql://localhost/mid_pflegedoku
SECRET_KEY=your-secret-key
FLASK_ENV=development
```

## Screenshots

*(Demo-Screenshots hier einfügen)*

---

Entwickelt mit Python & Flask
# mid-demo
