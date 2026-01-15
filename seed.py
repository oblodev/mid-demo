"""
Seed-Skript für Demo-Daten
Erstellt Beispiel-Klienten, Pflegeeinträge und Benutzer für die Demo.
"""
from datetime import datetime, date, timedelta
from app import create_app, db
from app.models import Client, CareEntry, User

app = create_app()

# Demo-Benutzer
USERS = [
    {
        'email': 'admin@mid.at',
        'name': 'Admin Weber',
        'password': 'admin123',
        'role': 'admin'
    },
    {
        'email': 'anna@mid.at',
        'name': 'Anna Kramer',
        'password': 'pflege123',
        'role': 'pflegekraft'
    },
    {
        'email': 'thomas@mid.at',
        'name': 'Thomas Meier',
        'password': 'pflege123',
        'role': 'pflegekraft'
    },
]

# Demo-Daten
CLIENTS = [
    {
        'name': 'Maria Huber',
        'birth_date': date(1942, 5, 15),
        'address': 'Hauptstraße 42, 1010 Wien',
        'care_level': 3,
        'notes': 'Benötigt Unterstützung bei der Mobilisation. Sehr kommunikativ.'
    },
    {
        'name': 'Johann Schmidt',
        'birth_date': date(1938, 11, 3),
        'address': 'Linzer Straße 17, 4020 Linz',
        'care_level': 4,
        'notes': 'Diabetes Typ 2, Insulinpflichtig. Morgens und abends Blutzuckermessung.'
    },
    {
        'name': 'Elisabeth Bauer',
        'birth_date': date(1950, 8, 22),
        'address': 'Mozartgasse 8, 5020 Salzburg',
        'care_level': 2,
        'notes': 'Lebt alleine, Angehörige besuchen regelmäßig.'
    },
    {
        'name': 'Franz Müller',
        'birth_date': date(1935, 2, 28),
        'address': 'Bergweg 5, 6020 Innsbruck',
        'care_level': 5,
        'notes': 'Beatmungspflichtig. 24h-Betreuung erforderlich.'
    },
]

ENTRIES = [
    # Maria Huber
    {'client_idx': 0, 'category': 'grundpflege', 'description': 'Morgendliche Körperpflege durchgeführt. Patientin war gut gelaunt und kooperativ. Hautpflege mit Lotion.', 'recorded_by': 'Anna K.', 'hours_ago': 2},
    {'client_idx': 0, 'category': 'mobilisation', 'description': 'Transfer vom Bett in den Rollstuhl. Kurzer Spaziergang im Garten (ca. 15 min). Patientin genießt die frische Luft.', 'recorded_by': 'Thomas M.', 'hours_ago': 26},
    {'client_idx': 0, 'category': 'ernaehrung', 'description': 'Mittagessen gereicht. Hat gut gegessen, ca. 3/4 der Portion. Ausreichend getrunken.', 'recorded_by': 'Anna K.', 'hours_ago': 5},

    # Johann Schmidt
    {'client_idx': 1, 'category': 'medikamente', 'description': 'Morgendliche Medikamentengabe: Insulin 12 IE s.c., Metformin 1000mg. BZ-Wert nüchtern: 142 mg/dl.', 'recorded_by': 'Sandra L.', 'hours_ago': 3},
    {'client_idx': 1, 'category': 'vitalzeichen', 'description': 'Vitalzeichen-Kontrolle: RR 138/82 mmHg, Puls 76/min, Temp 36.4°C, SpO2 97%.', 'recorded_by': 'Sandra L.', 'hours_ago': 3},
    {'client_idx': 1, 'category': 'grundpflege', 'description': 'Ganzkörperwäsche im Bett. Inspektion der Füße wegen Diabetes - keine Auffälligkeiten. Eincremen der Haut.', 'recorded_by': 'Michael B.', 'hours_ago': 27},

    # Elisabeth Bauer
    {'client_idx': 2, 'category': 'grundpflege', 'description': 'Unterstützung beim Ankleiden. Patientin ist weitgehend selbstständig, benötigt nur minimale Hilfe.', 'recorded_by': 'Eva S.', 'hours_ago': 4},
    {'client_idx': 2, 'category': 'besonderheiten', 'description': 'Tochter war zu Besuch. Patientin freut sich über den Familienbesuch. Gute Stimmung.', 'recorded_by': 'Eva S.', 'hours_ago': 28},

    # Franz Müller
    {'client_idx': 3, 'category': 'vitalzeichen', 'description': 'Stündliche Kontrolle: RR 125/78, Puls 68, SpO2 98% unter Beatmung. Beatmungsgerät läuft stabil.', 'recorded_by': 'Peter H.', 'hours_ago': 1},
    {'client_idx': 3, 'category': 'grundpflege', 'description': 'Komplette Körperpflege im Bett. Lagerungswechsel durchgeführt. Hautinspektion: keine Druckstellen.', 'recorded_by': 'Maria W.', 'hours_ago': 6},
    {'client_idx': 3, 'category': 'medikamente', 'description': 'Alle Medikamente gemäß Plan verabreicht. Keine besonderen Vorkommnisse.', 'recorded_by': 'Peter H.', 'hours_ago': 8},
    {'client_idx': 3, 'category': 'besonderheiten', 'description': 'Patient wirkt heute sehr müde. Schlafqualität war laut Nachtdienst unruhig. Arzt informiert.', 'recorded_by': 'Maria W.', 'hours_ago': 10},
]


def seed_database():
    with app.app_context():
        # Bestehende Daten löschen
        CareEntry.query.delete()
        Client.query.delete()
        User.query.delete()
        db.session.commit()

        print("Erstelle Demo-Benutzer...")
        for user_data in USERS:
            user = User(
                email=user_data['email'],
                name=user_data['name'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        db.session.commit()

        print("Erstelle Demo-Klienten...")
        clients = []
        for client_data in CLIENTS:
            client = Client(**client_data)
            db.session.add(client)
            clients.append(client)
        db.session.commit()

        print("Erstelle Pflegeeinträge...")
        for entry_data in ENTRIES:
            client = clients[entry_data['client_idx']]
            entry = CareEntry(
                client_id=client.id,
                category=entry_data['category'],
                description=entry_data['description'],
                recorded_by=entry_data['recorded_by'],
                recorded_at=datetime.utcnow() - timedelta(hours=entry_data['hours_ago'])
            )
            db.session.add(entry)
        db.session.commit()

        print(f"\nErfolgreich erstellt:")
        print(f"  - {len(USERS)} Benutzer")
        print(f"  - {len(CLIENTS)} Klienten")
        print(f"  - {len(ENTRIES)} Pflegeeinträge")
        print("\nDemo-Zugangsdaten:")
        print("  Admin:      admin@mid.at / admin123")
        print("  Pflegekraft: anna@mid.at / pflege123")


if __name__ == '__main__':
    seed_database()
