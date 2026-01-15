from datetime import datetime, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    ROLES = [
        ('admin', 'Administrator'),
        ('pflegekraft', 'Pflegekraft'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='pflegekraft')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def role_display(self):
        for code, name in self.ROLES:
            if code == self.role:
                return name
        return self.role

    def __repr__(self):
        return f'<User {self.email}>'


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    care_level = db.Column(db.Integer, nullable=True)  # Pflegegrad 1-5
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    entries = db.relationship('CareEntry', backref='client', lazy='dynamic',
                              cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Client {self.name}>'

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None


class CareEntry(db.Model):
    __tablename__ = 'care_entries'

    CATEGORIES = [
        ('grundpflege', 'Grundpflege'),
        ('medikamente', 'Medikamente'),
        ('vitalzeichen', 'Vitalzeichen'),
        ('ernaehrung', 'Ernährung'),
        ('mobilisation', 'Mobilisation'),
        ('besonderheiten', 'Besonderheiten'),
    ]

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    recorded_by = db.Column(db.String(100), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CareEntry {self.category} for Client {self.client_id}>'

    @property
    def category_display(self):
        for code, name in self.CATEGORIES:
            if code == self.category:
                return name
        return self.category
