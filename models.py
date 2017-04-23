from app import db
import datetime
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import sqlalchemy
from slugify import slugify

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
    
    secret_uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    public_uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()")) # we have a public UUID because we have a public log
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_uuid = Column(UUID(as_uuid=True), db.ForeignKey("users.user_uuid"), nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    data = db.Column(postgresql.JSONB, nullable=True)

class SocrataDatasets(db.Model):
    
    __tablename__ = "socrata_datasets"
    
    domain_and_id = db.Column(db.String, primary_key=True)
    data = db.Column(postgresql.JSONB, nullable=False)

class PageViews(db.Model):
    
    __tablename__ = "page_views"
    
    uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    data = db.Column(postgresql.JSONB, nullable=False)

class PublicPageViews(db.Model):
    
    __tablename__ = "public_page_views"
    
    uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    data = db.Column(postgresql.JSONB, nullable=False)

class App(db.Model):
    
    __tablename__ = "apps"
    
    slug = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

class Nicknames(db.Model):
    __tablename__ = "nicknames"
    
    name = db.Column(db.String, primary_key=True)
    groupi = db.Column(db.Integer, index=True)