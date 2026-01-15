from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Client, CareEntry
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def dashboard():
    # Statistiken
    client_count = Client.query.count()
    today = datetime.utcnow().date()
    today_entries = CareEntry.query.filter(
        CareEntry.recorded_at >= datetime.combine(today, datetime.min.time())
    ).count()

    # Letzte Einträge
    recent_entries = CareEntry.query.order_by(
        CareEntry.recorded_at.desc()
    ).limit(10).all()

    return render_template('dashboard.html',
                           client_count=client_count,
                           today_entries=today_entries,
                           recent_entries=recent_entries)
