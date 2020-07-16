# Required Libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Creating Flask Application
app = Flask(__name__)

# Connecting MYSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/restapi'

# track modifications of objects and emit signals, 
# This requires extra memory and should be disabled if not needed.
# So disabling using config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initiating SQLAlchemy and Marshmallow objects
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Creating Task Model using SQLAlchemy
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

# Creating TaskSchema using marshmallow
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

# Generating object of TaskSchema for single object and for multiple object
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Create Operation API, save new data into DB
@app.route('/tasks', methods=['Post'])
def create_task():
  title = request.json['title']
  description = request.json['description']

  new_task= Task(title, description)

  db.session.add(new_task)
  db.session.commit()

  return task_schema.jsonify(new_task)

# Read Operation API, returns all data available into DB
@app.route('/tasks', methods=['GET'])
def get_tasks():
  all_tasks = Task.query.all()
  result = tasks_schema.dump(all_tasks)
  return jsonify(result)

# Read Operation API, returns single data by using ID
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
  task = Task.query.get(id)
  return task_schema.jsonify(task)

# Update Operation API, update existing data by using ID
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
  task = Task.query.get(id)

  title = request.json['title']
  description = request.json['description']

  task.title = title
  task.description = description

  db.session.commit()

  return task_schema.jsonify(task)

# Delete Operation API, Delete existing data by using ID
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
  task = Task.query.get(id)
  db.session.delete(task)
  db.session.commit()
  return task_schema.jsonify(task)

# Simple Checking API
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Hey There, You succesfully constructed Restful CRUD API in Flask'})

# It will run flask Application
if __name__ == "__main__":
    app.run(debug=True)