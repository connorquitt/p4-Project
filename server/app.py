from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Employee, Meeting, Project, Assignment, employee_meetings, Review, Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if request.method == 'GET':
        employees = Employee.query.all()

        return make_response(
            jsonify([employee.to_dict() for employee in employees]),
            200,
        )
    
    elif request.method == 'POST':
        new_employee = Employee(
            name = request.form.get('name'),
            hire_date = request.form.get('hire_date'),
            manager_id = request.form.get('manager_id'),
        )
        db.session.add(new_employee)
        db.session.commit()

        response = make_response(new_employee.to_dict(), 201)
        return response

        
    return make_response(
        jsonify({'text': 'Method not Allowed'}),
        405,
    )

@app.route('/employees/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def employee_by_id(id):
    employee = Employee.query.filter(Employee.id == id).first()
    
    if employee == None:
        response_body = {
            "message": "This employee does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)
        return response

    elif request.method == 'GET':
        response = make_response(employee.to_dict(), 200)
        return response
    
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(employee, attr, request.form.get(attr))
        db.session.add(employee)
        db.session.commit()

        response = make_response(employee.to_dict(), 200)
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(employee)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }

        response = make_response(response_body, 200)
        return response
    
@app.route('/managers', methods=['GET', 'POST'])
def managers():
    if request.method == 'GET':
        managers = Manager.query.all()

        return make_response(
            jsonify([manager.to_dict for manager in managers]), 200
        )
    
    elif request.method == 'POST':
        new_manager = Manager(
            name=request.form.get('name'),
            position=request.form.get('position'),
            employees=request.form.get('employees'),
        )

        db.session.add(new_manager)
        db.session.commit()

        return make_response(new_manager.to_dict, 201)

@app.route('/managers/<int:id>', methods=['GET', 'PATCH', 'DELETE']) 
def manager_by_id(id):
    manager = Manager.query.filter(Manager.id == id).first()

    if manager == None:
        response_body = {
            "message": "Manager not found in our database, please try again"
        }

        return make_response(response_body, 404)
    
    else:
        if request.method == 'GET':
            return make_response(manager.to_dict(), 200)
        
        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(manager, attr, request.form.get(attr))
            db.session.add(manager)
            db.session.commit()

            return make_response(manager.to_dict(), 201)
        
        elif request.method == 'DELETE':
            db.session.delete(manager)
            db.session.commit()

            response_body = {
            "delete_successful": True,
            "message": "Review deleted."
        }
            return make_response(response_body, 200)
            
                


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

    if request.method == 'GET':
        reviews = Review.query.all()

        return make_response(
            jsonify([review.to_dict() for review in reviews]), 200
        )

    elif request.method == 'POST':
        new_review = Review(
            year=request.form.get("year"),
            summary=request.form.get("summary"),
            employee_id=request.form.get("employee_id"),
        )

        db.session.add(new_review)
        db.session.commit()

        review_dict = new_review.to_dict()

        response = make_response(
            review_dict,
            201
        )

        return response

@app.route('/reviews/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.filter(Review.id == id).first()

    if review == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(review, attr, request.form.get(attr))

            db.session.add(review)
            db.session.commit()

            review_dict = review.to_dict()

            response = make_response(
                review_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(review)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Review deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'GET':
        projects = Project.query.all()
        return make_response(
            jsonify([project.to_dict() for project in projects]), 200
        )
    
    elif request.method == 'POST':
        new_project = Project(
            title=request.form.get('title'),
            budget=request.form.get('budget')
        )
        db.session.add(new_project)
        db.session.commit()
        return make_response(new_project.to_dict(), 201)

@app.route('/projects/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def projects_by_id(id):
    project = Project.query.filter(Project.id == id).first()
    if project is None:
        response_body = {"message": "Project not found in our database, please try again"}
        return make_response(response_body, 404)
    
    if request.method == 'GET':
        return make_response(project.to_dict(), 200)
        
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(project, attr, request.form.get(attr))
        db.session.add(project)
        db.session.commit()
        return make_response(project.to_dict(), 200)
        
    elif request.method == 'DELETE':
        db.session.delete(project)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Project deleted."
        }
        return make_response(response_body, 200)


@app.route('/meetings', methods=['GET', 'POST'])
def meetings():
    if request.method == 'GET':
        meetings = Meeting.query.all()
        return make_response(
            jsonify([meeting.to_dict() for meeting in meetings]), 200
        )
    
    elif request.method == 'POST':
        new_meeting = Meeting(
            topic=request.form.get('topic'),
            scheduled_time=request.form.get('scheduled_time'),
            location=request.form.get('location')
        )
        db.session.add(new_meeting)
        db.session.commit()
        return make_response(new_meeting.to_dict(), 201)

@app.route('/meetings/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def meetings_by_id(id):
    meeting = Meeting.query.filter(Meeting.id == id).first()
    if meeting is None:
        response_body = {"message": "Meeting not found in our database, please try again"}
        return make_response(response_body, 404)
    
    if request.method == 'GET':
        return make_response(meeting.to_dict(), 200)
        
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(meeting, attr, request.form.get(attr))
        db.session.add(meeting)
        db.session.commit()
        return make_response(meeting.to_dict(), 200)
        
    elif request.method == 'DELETE':
        db.session.delete(meeting)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Meeting deleted."
        }
        return make_response(response_body, 200)


@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    if request.method == 'GET':
        assignments = Assignment.query.all()
        return make_response(
            jsonify([assignment.to_dict() for assignment in assignments]), 200
        )
    
    elif request.method == 'POST':
        new_assignment = Assignment(
            role=request.form.get('role'),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),
            employee_id=request.form.get('employee_id'),
            project_id=request.form.get('project_id')
        )
        db.session.add(new_assignment)
        db.session.commit()
        return make_response(new_assignment.to_dict(), 201)

@app.route('/assignments/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def assignments_by_id(id):
    assignment = Assignment.query.filter(Assignment.id == id).first()
    if assignment is None:
        response_body = {"message": "Assignment not found in our database, please try again"}
        return make_response(response_body, 404)
    
    if request.method == 'GET':
        return make_response(assignment.to_dict(), 200)
        
    elif request.method == 'PATCH':
        for attr in request.form:
            setattr(assignment, attr, request.form.get(attr))
        db.session.add(assignment)
        db.session.commit()
        return make_response(assignment.to_dict(), 200)
        
    elif request.method == 'DELETE':
        db.session.delete(assignment)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Assignment deleted."
        }
        return make_response(response_body, 200)





if __name__ == '__main__':
    app.run(port=5555, debug=True)

