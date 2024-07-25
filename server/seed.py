
import datetime
from app import app
from models import db, Employee, Meeting, Project, Assignment, Review, Manager, EmployeeMeeting

with app.app_context():

    # Delete all rows in tables
    EmployeeMeeting.query.delete()
    Employee.query.delete()
    Review.query.delete()
    Meeting.query.delete()
    Project.query.delete()
    Assignment.query.delete()
    Manager.query.delete()
    db.session.commit()

    # Add managers
    mg1 = Manager(name='Trooper Wright', department='Installation')
    mg2 = Manager(name='Brant Boisvert', department='Sound & Lighting')
    mg3 = Manager(name='Josh Burkhaulter', department='Programming')
    db.session.add_all([mg1, mg2, mg3])
    db.session.commit()

    # Add employees
    e1 = Employee(name="Uri Lee", hire_date=datetime.datetime(2022, 5, 17), manager=mg1)
    e2 = Employee(name="Tristan Tal", hire_date=datetime.datetime(2020, 1, 30), manager=mg1)
    e3 = Employee(name="Sasha Hao", hire_date=datetime.datetime(2021, 12, 1), manager=mg3)
    e4 = Employee(name="Taylor Jai", hire_date=datetime.datetime(2015, 1, 2), manager=mg2)
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    # Add reviews
    uri_2023 = Review(year=2023, summary="Great web developer!", employee=e1)
    tristan_2021 = Review(year=2021, summary="Good coding skills, often late to work", employee=e2)
    tristan_2022 = Review(year=2022, summary="Strong coding skills, takes long lunches", employee=e2)
    tristan_2023 = Review(year=2023, summary="Awesome coding skills, dedicated worker", employee=e2)
    db.session.add_all([uri_2023, tristan_2021, tristan_2022, tristan_2023])
    db.session.commit()

    # Add meetings
    m1 = Meeting(topic="Software Engineering Weekly Update",
                 scheduled_time=datetime.datetime(2023, 10, 31, 9, 30),
                 location="Building A, Room 142")
    m2 = Meeting(topic="Github Issues Brainstorming",
                 scheduled_time=datetime.datetime(2023, 12, 1, 15, 15),
                 location="Building D, Room 430")
    db.session.add_all([m1, m2])
    db.session.commit()

    # Add projects
    p1 = Project(title="XYZ Project Flask server", budget=50000)
    p2 = Project(title="XYZ Project React UI", budget=100000)
    db.session.add_all([p1, p2])
    db.session.commit()

    # Many-to-many relationship between employee and meeting using EmployeeMeeting class
    em1 = EmployeeMeeting(employee_id=e1.id, meeting_id=m1.id, role="Attendee", rsvp=True)
    em2 = EmployeeMeeting(employee_id=e1.id, meeting_id=m2.id, role="Presenter", rsvp=True)
    em3 = EmployeeMeeting(employee_id=e2.id, meeting_id=m2.id, role="Attendee", rsvp=False)
    em4 = EmployeeMeeting(employee_id=e3.id, meeting_id=m2.id, role="Attendee", rsvp=True)
    em5 = EmployeeMeeting(employee_id=e4.id, meeting_id=m2.id, role="Attendee", rsvp=True)
    db.session.add_all([em1, em2, em3, em4, em5])
    db.session.commit()

    # Many-to-many relationship between employee and project through assignment
    a1 = Assignment(role='Project manager',
                    start_date=datetime.datetime(2023, 5, 28),
                    end_date=datetime.datetime(2023, 10, 30),
                    employee=e1,
                    project=p1)
    a2 = Assignment(role='Flask programmer',
                    start_date=datetime.datetime(2023, 6, 10),
                    end_date=datetime.datetime(2023, 10, 1),
                    employee=e2,
                    project=p1)
    a3 = Assignment(role='Flask programmer',
                    start_date=datetime.datetime(2023, 11, 1),
                    end_date=datetime.datetime(2024, 2, 1),
                    employee=e2,
                    project=p2)
    db.session.add_all([a1, a2, a3])
    db.session.commit()
