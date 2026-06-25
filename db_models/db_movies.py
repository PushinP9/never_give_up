from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, Text
from sqlalchemy.orm import declarative_base
from typing import Dict, Any
Base = declarative_base()
class MovieDBModel(Base):
    __tablename__ = 'movies'
    id = Column(String, primary_key=True)  # text в БД
    title = Column(String)  # text в БД
    description = Column(Text)  # text в БД
    release_year = Column(Integer)  # int в БД
    duration_minutes = Column(Integer)  # int в БД
    rating = Column(Float)  # float в БД
    genre = Column(String)  # text в БД
    director = Column(String)  # text в БД
    is_published = Column(Boolean)  # bool в БД
    created_at = Column(DateTime)  # timestamp в БД
    updated_at = Column(DateTime)  # timestamp в БД
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'release_year': self.release_year,
            'duration_minutes': self.duration_minutes,
            'rating': self.rating,
            'genre': self.genre,
            'director': self.director,
            'is_published': self.is_published,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    def __repr__(self):
        return f"<Movie(id='{self.id}', title='{self.title}')>"