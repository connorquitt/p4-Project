from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class EmployeeMeeting(db.Model, SerializerMixin):
    __tablename__ = 'employee_meetings'

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), primary_key=True)
    role = db.Column(db.String)
    rsvp = db.Column(db.Boolean)

    role = db.relationship('Employee', back_populates='employee_meetings')
    employee = db.relationship('Employee', back_populates='employee_meetings')
    meeting = db.relationship('Meeting', back_populates='employee_meetings')

    def to_dict(self):
        return {
            'employee_id': self.employee_id,
            'meeting_id': self.meeting_id,
            'role': self.role,
            'rsvp': self.rsvp,
        }

    def __repr__(self):
        return f'<EmployeeMeeting Employee: {self.employee_id}, Meeting: {self.meeting_id}>'

class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'

    serialize_rules = ('-reviews.employee', '-meetings.employees', '-assignments.employee')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    hire_date = db.Column(db.Date, nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))

    manager = db.relationship('Manager', back_populates='employees')
    reviews = db.relationship('Review', back_populates='employee')
    employee_meetings = db.relationship('EmployeeMeeting', back_populates='employee')
    meetings = association_proxy('employee_meetings', 'meeting')
    assignments = db.relationship('Assignment', back_populates='employee', cascade='all, delete-orphan')
    projects = association_proxy('assignments', 'project', creator=lambda project_obj: Assignment(project=project_obj))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'hire_date': self.hire_date,
            'manager': self.manager.to_dict() if self.manager else None,
            'meetings': [meeting.to_dict() for meeting in self.meetings]
        }

    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'

    @validates('name')
    def validate_name(self, key, username):
        if not isinstance(username, str):
            raise ValueError('Invalid name')
        return username
    
    @validates('manager_id')
    def validate_manager_id(self, key, manager_id):
        if not isinstance(manager_id, int):
            raise ValueError('Invalid manager ID')
        return manager_id

class Manager(db.Model, SerializerMixin):
    __tablename__ = 'managers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    department = db.Column(db.String, nullable=False)

    employees = db.relationship('Employee', back_populates='manager')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department
        }

    def __repr__(self):
        return f'<Manager {self.id}, {self.name}, {self.department}>'

    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str):
            raise ValueError('Invalid name')
        return name

    @validates('department')
    def validate_department(self, key, department):
        if not isinstance(department, str):
            raise ValueError('Invalid department')
        return department

class Meeting(db.Model, SerializerMixin):
    __tablename__ = 'meetings'

    serialize_rules = ('-employees.meetings',)  # Avoid recursion by excluding employees

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)

    employee_meetings = db.relationship('EmployeeMeeting', back_populates='meeting')
    employees = association_proxy('employee_meetings', 'employee')

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'scheduled_time': self.scheduled_time,
            'location': self.location,
            'employees': [employee.name for employee in self.employees]
        }

    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'

    @validates('topic')
    def validate_topic(self, key, topic):
        if not isinstance(topic, str):
            raise ValueError('Invalid topic')
        return topic

    @validates('scheduled_time')
    def validate_scheduled_time(self, key, scheduled_time):
        if not isinstance(scheduled_time, datetime):
            raise ValueError('Invalid scheduled time')
        return scheduled_time

    @validates('location')
    def validate_location(self, key, location):
        if not isinstance(location, str):
            raise ValueError('Invalid location')
        return location



class Project(db.Model, SerializerMixin):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    budget = db.Column(db.Integer)

    # Relationship mapping the project to related assignments
    assignments = db.relationship('Assignment', back_populates='project', cascade='all, delete-orphan')

    # Association proxy to get employees for this project through assignments
    employees = association_proxy('assignments', 'employee', creator=lambda employee_obj: Assignment(employee=employee_obj))

    def __repr__(self):
        return f'<Review {self.id}, {self.title}, {self.budget}>'


# Association Model to store many-to-many relationship with attributes between employee and project
class Assignment(db.Model, SerializerMixin):
    __tablename__ = 'assignments'

    serialize_only = ('role',)

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    # Foreign key to store the employee id
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    # Foreign key to store the project id
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    # Relationship mapping the assignment to related employee
    employee = db.relationship('Employee', back_populates='assignments')
    # Relationship mapping the assignment to related project
    project = db.relationship('Project', back_populates='assignments')

    def __repr__(self):
        return f'<Assignment {self.id}, {self.role}, {self.start_date}, {self.end_date}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-employee.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    summary = db.Column(db.String)
    # Foreign key stores the Employee id
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    # Relationship mapping the review to related employee
    employee = db.relationship('Employee', back_populates="reviews")

    def __repr__(self):
        return f'<Review {self.id}, {self.year}, {self.summary}>'
