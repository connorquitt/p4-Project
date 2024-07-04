from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

from config import db, bcrypt

class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    ##password_hash = db.Column(db.String(128), nullable=False)
    ##properties = db.relationship('Property', backref='owner', lazy=True)
    ##reviews = db.relationship('Review', backref='user', lazy=True)
    ##visits = db.relationship('Visit', backref='visitor', lazy=True)
    ##favorite_properties = db.relationship('FavoriteProperty', backref='favorite_properties', lazy=True)

    def __repr__(self):
        return f'<Employee {self.name}>'

    ##def set_password(self, password):
        ##self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    ##def check_password(self, password):
        ##return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    ##owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    ##visits = db.relationship('Visit', backref='visits_property', lazy=True)
    ##reviews = db.relationship('Review', backref='reviews_property', lazy=True)
    ##favorites = db.relationship('FavoriteProperty', backref='favorites_property', lazy=True)

    def __repr__(self):
        return f'<Project {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project': self.project,
            'description': self.description,
            'location': self.location,
            ##'owner_id': self.owner_id
        }

class Manager(db.Model, SerializerMixin):
    __tablename__ = 'managers'
    
    id = db.Column(db.Integer, primary_key=True)
    ##user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.Integer, nullable=False, Unique=True)
    ##password_hash = db.Column(db.String(128), nullable=False)
    ##need to connect to employees and meetings (boss has many employees and employees have many managers)
    
    def __repr__(self):
        return f'<Manager {self.username} | {self.id}>'
    
    ##def set_password(self, password):
        ##self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    ##def check_password(self, password):
        ##return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            ##'password': self.password ???? (not correct currently)
        }
    

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    ##created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id} by User {self.employee_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'employee_id': self.employee_id,
            ##'created_at': self.created_at
        }