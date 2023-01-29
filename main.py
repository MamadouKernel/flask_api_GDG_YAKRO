from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy

#creation de notre application

app = Flask(__name__)

#configuration de la base de données

app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://{user}:{password}@{host}/{db}".format(
    user = "root",
    password = "",
    host = "localhost",
    db ="bienseloger"
)
with app.app_context():

    #initialisation de sqlalchemy
    db = SQLAlchemy(app)
    #creation des tables

    class User(db.Model):
        def __int__(self,name,username,email,password):
            self.name =name
            self.username = username
            self.email = email
            self.password = password
                
        id=db.Column(db.Integer,primary_key=True)
        name = db.Column(db.String(255))
        username = db.Column(db.String(255))
        email = db.Column(db.String(255))
        password = db.Column(db.String(255))

        def __repr__(self):
            return '<User %r>' % self.name
    


#migration de la base de données

    db.create_all()

#creation des routes
@app.route('/',methods=['GET'])
def index():
    return jsonify({'message':'Welcome to the page'})


@app.route('/api/users',methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'],username=data['username'],email=data['email'],password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'user created'})

@app.route('/api/users',methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users':output})

@app.route('/api/users/<user_id>',methods=['GET'])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'no user found'})
    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['password'] = user.password
    return jsonify({'user':user_data})

@app.route('/api/users/<user_id>',methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'no user found'})
    data = request.get_json()
    user.name = data['name']
    user.username = data['username']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message':'user updated'})

@app.route('/api/users/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message':'no user found'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message':'user deleted'})

if __name__ == '__main__':
    app.run(debug=True)
