# Add any model classes for Flask-SQLAlchemy here
from datetime import datetime
from app import db

class Movie(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index=True, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    poster = db.Column(db.String(80), default="movie_image.png")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __init__(self, title, description, poster):
        self.title = title
        self.description = description
        self.poster = poster
        self.created_at = datetime.strftime(datetime.now(), "%Y-%B-%d %H:%M:%S")