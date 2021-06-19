# from operator import iadd
from flask import request, jsonify, Flask
from flask_restplus import Resource, fields, Namespace

from models import *
from marsh import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Users Namespace
namespace1 = Namespace('users', description='Users related operations')

# Users Schema
user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

# Users Personals List
personal_schema = PersonalListSchema()
personals_schema = PersonalListSchema(many=True)


# User Data Model
user = namespace1.model('User', {
    'FirstName': fields.String('FirstName'),
    'LastName': fields.String,
    'Email': fields.String,
    'Password': fields.String('Secured Password')
})
# Login User Data Model
login = namespace1.model('Login', {
    'Email': fields.String('User Email'),
    'Password': fields.String
})
# Personal List Data Model
personal = namespace1.model('PersonalList', {
    'Name': fields.String('University Name')
})


# User Api by Email
@namespace1.route('/<string:email>')
class userResource(Resource):
    def get(self, email):
        """
        Get user by email
        """
        user = Users.query.filter_by(Email=email).first()
        if not user:
            return {'message': 'User not found for Email: {user_id}'.format(user_id=email)}, 404

        return user_schema.dump(user)

    @namespace1.expect(user)
    @namespace1.response(204, 'User successfully Updated.')
    def put(self, email):
        """
        Updates a user by email
        """
        user = Users.query.filter_by(Email=email).first()
        if not user:
            return {'message': 'User not found for Email: {user_id}'.format(user_id=email)}, 404

        user.FirstName = request.json['FirstName']
        user.LastName = request.json['LastName']
        user.Email = request.json['Email']
        user.Password = request.json['Password']

        db.session.add(user)
        db.session.commit()

        return user_schema.dump(user)


# SignUP a User
@namespace1.route('')
class usersResource(Resource):
    def get(self):
        """
        Get all user
        """
        users = Users.query.all()
        return users_schema.dump(users), 200

    @namespace1.expect(user)
    def post(self):
        """
        Create a new User
        """
        email = request.json['Email']
        password = request.json['Password']

        user = Users.query.filter_by(Email=email).first()
        if user:
            return {'message': "The Email Address already exists"}, 400

        hashed = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = Users(FirstName=request.json['FirstName'],
                         LastName=request.json['LastName'],
                         Email=request.json['Email'],
                         Password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return user_schema.dump(new_user), 200


# Login User
@namespace1.route('/login')
class UserResource(Resource):
    @namespace1.expect(login)
    def post(self):
        """
        Login a user
        """
        email = request.json['Email']
        password = request.json['Password']

        user = Users.query.filter_by(Email=email).first()
        if not user:
            return {'message': "The Password or Email is Incorrect"}, 404
        else:
            check = bcrypt.check_password_hash(user.Password, password)
            if check:
                return user_schema.dump(user)
            else:
                return {'message': "The Password or Email is Incorrect"}, 400


# User List
@namespace1.route('/<string:email>/list')
class PersonaListsResources(Resource):
    def get(self, email):
        """
        Get all personal Lists 
        """
        uni_list = []
        user = Users.query.filter_by(Email=email).first()
        if not user:
            return {'message': "User does not exist"}, 404

        lst = PersonalList.query.filter_by(UserId=user.UserID).all()
        if not lst:
            return {'message': "There are no Lists"}, 404
        for l in lst:
            uni = University.query.filter_by(UniID=l.UniId).first()

            data = {
                'University': uni.Name,
                'Acronym': uni.Acronyms,
                'Rank': uni.Rank
            }
            uni_list.append(data)
        return jsonify(uni_list)

    @namespace1.expect(personal)
    def post(self, email):
        """
        Add to personal List
        """
        user = Users.query.filter_by(Email=email).first()
        if not user:
            return {'message': "User does not exist"}, 404

        uni_name = request.json['Name']
        uni = University.query.filter_by(Name=uni_name).first()
        if not uni:
            return {'message': "University does not exist"}, 404

        check = PersonalList.query.filter_by(
            UniId=uni.UniID).filter_by(UserId=user.UserID).first()

        if check:
            return {'message': "Already Added"}, 400
        new_list = PersonalList()
        new_list.UserId = user.UserID
        new_list.UniId = uni.UniID

        db.session.add(new_list)
        db.session.commit()

        # return personal_schema.dump(new_list)
