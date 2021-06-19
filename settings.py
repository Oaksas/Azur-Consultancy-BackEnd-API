# Flask settings
FLASK_SERVER_NAME = 'localhost:8888'
FLASK_DEBUG = True  # Do not use debug mode in production

# SQLAlchemy settings
# SQLALCHEMY_DATABASE_URI = 'postgresql://igortuckhcteup:a33837303167062edecedb60eddc4413c9acb9c33186eb914a6624e50426e5df@ec2-35-171-250-21.compute-1.amazonaws.com:5432/d2jag5hulkqnth'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/consultancy'
SQLALCHEMY_TRACK_MODIFICATIONS = False
