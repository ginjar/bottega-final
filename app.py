from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os




app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)
# build the db
class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    done = db.Column(db.Boolean, nullable= True)

    def __init__(self, task, date, done):
        self.task = task
        self.date = date
        self.done = done

class ChoreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'task', 'date', 'done')

chore_schema = ChoreSchema()
chores_schema = ChoreSchema(many=True)

# @app.route('/chore/add', methods = ['GET'] )
# def chore_get():
    
# add new chores
@app.route('/chore/add', methods = ['POST'] )
def chore_add():
  
    task = request.json.get('task')
    date = request.json.get('date')
    done = request.json.get('done')

    new_chore = Chore(task, date, done)
    
    db.session.add(new_chore)
    db.session.commit()

    chore = Chore.query.get(new_chore.id)
    # return chore_schema.jsonify(new_chore)
    return jsonify(chore_schema.dump(chore))
  


@app.route("/chore/get", methods =['GET'])
def receive_all_chores():
    all_chores = Chore.query.all()
    
    # return chores_schema.jsonify(all_chores)
    return jsonify(chores_schema.dump(all_chores))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable = False)
    password = db.Column(db.String(144), unique=False, nullable =False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)



@app.route('/login', methods = ['POST'])
def find_user():
    username = request.json.get('username')
    password =  request.json.get('password')
    result = User.query.filter_by(username=username).first()
  
    if result :
        if result.password == password:
            return jsonify({"user_info": result.username})
        else:
            return jsonify({'message': "that is not the password", 'successful': False}),401
    else :
        return jsonify({'message': "that is not a user", 'successful': False}),401
   

@app.route('/user/add', methods = ['POST'])
def add_user():

    username = request.json.get('username')
    password =  request.json.get('password')
   
    new_user = User(username, password)

    db.session.add(new_user)
    db.session.commit()
    #return user_schema.jsonify(user)
    return jsonify(user_schema.dump(new_user))



if __name__ == "__main__":
    app.run(debug = True)
    





    

