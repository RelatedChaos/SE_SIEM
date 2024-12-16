from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


import redis
import rq



class User(db.Model):
    #local keys
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    connection_method: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)

    #foreign keys

    #relationships
    incidents: so.WriteOnlyMapped['Incident'] = so.relationship(back_populates='responder')

    #helper functions
    def __repr__(self):
        return {'username': self.username,
                'id': self.id,
                'role': self.role}
    
    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }
        return data
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RetentionRule(db.Model):
    #local keys
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    event_q: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    retention_period: so.Mapped[int] = so.mapped_column(sa.Integer, index=True, unique=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    #foreign keys

    #relationships
    retention: so.WriteOnlyMapped['Event'] = so.relationship(back_populates='retention_perion')

    #helper functions

class Event(db.Model):
    #local keys
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    raw_event: so.Mapped[str] = so.mapped_column(sa.String(256))
    retention_period: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    p_datetime_timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    p_data: so.Mapped[str] = so.mapped_column(sa.String[256])

    #foreign keys
    retention_rule_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(RetentionRule.id), index=True)

    #relationships
    retention_perion: so.Mapped[RetentionRule] = so.relationship(back_populates='retention')
    part_of: so.Mapped['Incident'] = so.relationship(back_populates='incident_events')

    #helper functions
    def __repr__(self):
        return f'<b>Original Event:</b> {self.raw_event}'


class Configuration(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    config_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    config_type: so.Mapped[int] = so.mapped_column(sa.Integer, index=True, unique=True)
    value: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))



class CorrelationRule(db.Model):
    #local keys
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    rule_query: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)

    #foreign keys

    #relationships
    incidents: so.Mapped['Incident'] = so.relationship(back_populates='correlation_rule')

class Incident(db.Model):
    #local keys
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    incident_timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    status: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    notes: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)

    #foreign keys
    event_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Event.id),  index=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),  index=True)
    correlation_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(CorrelationRule.id),  index=True)

    #relationships
    incident_events: so.Mapped[Event] = so.relationship(back_populates='part_of')
    responder: so.Mapped[User] = so.relationship(back_populates='incidents')
    correlation_rule: so.Mapped[CorrelationRule] = so.relationship(back_populates='incidents')

    #helper functions


class AutomaticResponse(db.Model):
    #local keys
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    action_type: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    action_details: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    script_location: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    response_timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    status: so.Mapped[int] = so.mapped_column(sa.Integer, index=True, unique=True)

    #foreign keys

    #relationships




    




    


