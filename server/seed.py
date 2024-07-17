import datetime
from app import app
from models import db, Employee, Meeting, Employee_Meetings, Manager

with app.app_context():

    # Delete all rows in tables
    Employee_Meetings.query.delete()
    Employee.query.delete()
    Meeting.query.delete()
    Manager.query.delete()


     # Add managers
    mg1 = Manager(name = 'Trooper Wright', position = 'Installation Manager')
    mg2 = Manager(name = 'Brant Boisvert', position = 'Sound & Lighting Manager')
    mg3 = Manager(name = 'Josh Burkhaulter', position = 'Programming Manager')
    db.session.add_all([mg1, mg2, mg3])
    db.session.commit()

    # Add employees
    e1 = Employee(name="Uri Lee", hire_date=datetime.datetime(2022, 5, 17), manager=mg1)
    e2 = Employee(name="Tristan Tal", hire_date=datetime.datetime(2020, 1, 30), manager=mg1)
    e3 = Employee(name="Sasha Hao", hire_date=datetime.datetime(2021, 12, 1), manager=mg3)
    e4 = Employee(name="Taylor Jai", hire_date=datetime.datetime(2015, 1, 2), manager=mg2)
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()


    # Add meetings
    m1 = Meeting(topic="Software Engineering Weekly Update",
                 scheduled_time=datetime.datetime(
                     2023, 10, 31, 9, 30),
                 location="Building A, Room 142")
    m2 = Meeting(topic="Github Issues Brainstorming",
                 scheduled_time=datetime.datetime(
                     2023, 12, 1, 15, 15),
                 location="Building D, Room 430")
    db.session.add_all([m1, m2])
    db.session.commit()


    em1 = Employee_Meetings(role='Lead')
   

    # Many-to-many relationship between employee and project through assignment

