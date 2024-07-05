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

#set up classes to get picked up as the API endpoint (Index, Employees, Reviews, Meetings)
    #need <int: id> for most of them as well as ways to select and retain certain info on page or to nest deeper from an employee or something similar

#maybe not i think i like app.route better, need to set up all the other routes still then fully make front end work :)

class Index(Resource):
    def get(self):
        response_dict = {
            "Index": "hihihi"
        }

        response = make_response(response_dict, 200)

        return response

api.add_resource(Index, '/')

@app.route('/employees', methods=['GET'])
def employees():
    if request.method == 'GET':
        employees = Employee.query.all()

        return make_response(
            jsonify([employee.to_dict() for employee in employees]),
            200,
        )
    return make_response(
        jsonify({'text': 'Method not Allowed'}),
        405,
    )



if __name__ == '__main__':
    app.run(port=5555, debug=True)

