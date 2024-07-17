from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Employee_Meetings(db.Model, SerializerMixin):
    __tablename__ = 'employee_meetings'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

    employee = db.relationship('Employee', back_populates='employee_meetings')
    meeting = db.relationship('Meeting', back_populates='employee_meetings')


class Employee(db.Model, SerializerMixin):
    __tablename__ = 'employees'

    serialize_rules = ('-reviews.employee', '-meetings.employees', '-assignments.employee')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date, nullable=True)

    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))

    # Relationship mapping the employee to related manager
    manager = db.relationship('Manager', back_populates='employees')
    
    # Relationship mapping the employee to related reviews
    reviews = db.relationship('Review', back_populates='employee')

    # Relationship mapping the employee to related meetings
    employee_meetings = db.relationship('Employee_Meetings', back_populates='employee')
    meetings = db.relationship('Meeting', secondary='employee_meetings', back_populates='employees')

    def __repr__(self):
        return f'<Employee {self.id}, {self.name}, {self.hire_date}>'


class Meeting(db.Model, SerializerMixin):
    __tablename__ = 'meetings'

    serialize_rules = ('-employees.meetings',)

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String)
    scheduled_time = db.Column(db.DateTime)
    location = db.Column(db.String)

    # Relationship mapping the meeting to related employees
    employee_meetings = db.relationship('Employee_Meetings', back_populates='meeting')
    employees = db.relationship('Employee', secondary='employee_meetings', back_populates='meetings')

    def __repr__(self):
        return f'<Meeting {self.id}, {self.topic}, {self.scheduled_time}, {self.location}>'
    
    
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


class Manager(db.Model, SerializerMixin):
    __tablename__ = 'managers'

    serialize_only = ('name', 'position',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position = db.Column(db.String, nullable=False)

    employees = db.relationship('Employee', back_populates='manager')

    def __repr__(self):
        return f'<Manager {self.id}, {self.name}, {self.position}>'
