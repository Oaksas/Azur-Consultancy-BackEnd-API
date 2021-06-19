from flask import Flask, Blueprint
from flask_restplus import Api
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt


from settings import *
from models import *
from . import userApi, universitiesApi, questionAnswerApi


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS


db.init_app(app)
ma = Marshmallow(app)
cors = CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)


bp = Blueprint('api', __name__, url_prefix="/api")


api = Api(bp, version='1.0', title='Consultancy Website API',
          description='An API for Web Application For Consultancy Website')


api.add_namespace(userApi.namespace1)
api.add_namespace(universitiesApi.namespace2)
api.add_namespace(questionAnswerApi.namespace3)
app.register_blueprint(bp)
