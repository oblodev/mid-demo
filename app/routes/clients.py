from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, send_file
from flask_login import login_required, current_user
from app import db
from app.models import Client, CareEntry
from app.forms import ClientForm
from app.pdf_generator import generate_client_report


def admin_required(f):
    """Decorator: Nur Admins haben Zugriff"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Diese Aktion erfordert Administrator-Rechte.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/')
@login_required
def list():
    search = request.args.get('search', '')
    if search:
        clients = Client.query.filter(
            Client.name.ilike(f'%{search}%')
        ).order_by(Client.name).all()
    else:
        clients = Client.query.order_by(Client.name).all()
    return render_template('clients/list.html', clients=clients, search=search)


@clients_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            birth_date=form.birth_date.data,
            address=form.address.data,
            care_level=int(form.care_level.data) if form.care_level.data else None,
            notes=form.notes.data
        )
        db.session.add(client)
        db.session.commit()
        flash(f'Klient "{client.name}" wurde erfolgreich angelegt.', 'success')
        return redirect(url_for('clients.detail', id=client.id))
    return render_template('clients/form.html', form=form, title='Neuer Klient')


@clients_bp.route('/<int:id>')
@login_required
def detail(id):
    client = Client.query.get_or_404(id)
    entries = client.entries.order_by(CareEntry.recorded_at.desc()).limit(20).all()
    return render_template('clients/detail.html', client=client, entries=entries)


@clients_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    client = Client.query.get_or_404(id)
    form = ClientForm(obj=client)
    if form.validate_on_submit():
        client.name = form.name.data
        client.birth_date = form.birth_date.data
        client.address = form.address.data
        client.care_level = int(form.care_level.data) if form.care_level.data else None
        client.notes = form.notes.data
        db.session.commit()
        flash(f'Klient "{client.name}" wurde aktualisiert.', 'success')
        return redirect(url_for('clients.detail', id=client.id))

    # Pre-fill care_level as string for select field
    if client.care_level:
        form.care_level.data = str(client.care_level)

    return render_template('clients/form.html', form=form,
                           title=f'Klient bearbeiten: {client.name}',
                           client=client)


@clients_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(id):
    client = Client.query.get_or_404(id)
    name = client.name
    db.session.delete(client)
    db.session.commit()
    flash(f'Klient "{name}" wurde gelöscht.', 'warning')
    return redirect(url_for('clients.list'))


@clients_bp.route('/<int:id>/export')
@login_required
def export_pdf(id):
    """Exportiert alle Pflegeeinträge eines Klienten als PDF."""
    client = Client.query.get_or_404(id)
    entries = client.entries.order_by(CareEntry.recorded_at.desc()).all()

    pdf_buffer = generate_client_report(client, entries)

    # Dateiname: Klientenname_Datum.pdf
    from datetime import datetime
    filename = f"Pflegebericht_{client.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
