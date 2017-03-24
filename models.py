from app import db
import datetime
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import sqlalchemy

class User(db.Model):
    
    __tablename__ = "users"
    
    user_uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    user_type = db.Column(db.String, default="person")
    data = db.Column(postgresql.JSONB, nullable=True)
    
class Oauth(db.Model):

    __tablename__ = "oauth"
    
    oauth_id = db.Column(db.String, primary_key=True)
    user_uuid = Column(UUID(as_uuid=True), db.ForeignKey("users.user_uuid"), nullable=False)
    access_token = db.Column(db.String, nullable=True)
    provider = db.Column(db.String, nullable=False)
    scopes = db.Column(postgresql.JSONB, nullable=True)
    data = db.Column(postgresql.JSONB, nullable=True)
    
class Session(db.Model):
    
    __tablename__ = "sessions"
    
    uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_uuid = Column(UUID(as_uuid=True), db.ForeignKey("users.user_uuid"), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    data = db.Column(postgresql.JSONB, nullable=True)

class SocrataDatasets(db.Model):
    
    __tablename__ = "socrata_datasets"
    
    domain_and_id = db.Column(db.String, primary_key=True)
    data = db.Column(postgresql.JSONB, nullable=False)

    