import sqlalchemy as sa
from app import db
from app.models import Event


def write_event(raw):
    db.session.add(raw_event=raw)
    db.session.commit()