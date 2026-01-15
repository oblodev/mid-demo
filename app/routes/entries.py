from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Client, CareEntry
from app.forms import CareEntryForm

entries_bp = Blueprint('entries', __name__)


@entries_bp.route('/client/<int:client_id>')
@login_required
def list(client_id):
    client = Client.query.get_or_404(client_id)
    entries = client.entries.order_by(CareEntry.recorded_at.desc()).all()
    return render_template('entries/list.html', client=client, entries=entries)


@entries_bp.route('/client/<int:client_id>/new', methods=['GET', 'POST'])
@login_required
def create(client_id):
    client = Client.query.get_or_404(client_id)
    form = CareEntryForm()

    # Pre-fill recorded_by with current user's name
    if not form.recorded_by.data:
        form.recorded_by.data = current_user.name

    if form.validate_on_submit():
        entry = CareEntry(
            client_id=client.id,
            category=form.category.data,
            description=form.description.data,
            recorded_by=form.recorded_by.data
        )
        db.session.add(entry)
        db.session.commit()
        flash('Pflegeeintrag wurde erfolgreich erstellt.', 'success')
        return redirect(url_for('clients.detail', id=client.id))

    return render_template('entries/form.html', form=form, client=client)


@entries_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    entry = CareEntry.query.get_or_404(id)
    client_id = entry.client_id
    db.session.delete(entry)
    db.session.commit()
    flash('Pflegeeintrag wurde gelöscht.', 'warning')
    return redirect(url_for('clients.detail', id=client_id))
