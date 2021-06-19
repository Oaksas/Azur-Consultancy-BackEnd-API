from flask import request, jsonify
from flask_restplus import Resource, fields, Namespace

from models import *
from marsh import *

# Questions and Answers Namespace
namespace3 = Namespace(
    'questions', description='Questions and Answers related operations')


question_schema = QuestionsSchema()
questions_schema = QuestionsSchema(many=True)

answer_schema = AnswersSchema()
answers_schema = AnswersSchema(many=True)

# Questions Data Model
questions = namespace3.model('Questions', {
    'Email': fields.Integer,
    'Questions': fields.String,
    'Date': fields.DateTime
})

#  Answers for the Questions
answers = namespace3.model('Answers', {
    'Email': fields.Integer,
    'Answer': fields.String,
    'Date': fields.DateTime
})


@namespace3.route('')
class QuestionsResource(Resource):
    def get(self):
        """
        Get all questions
        """
        qes = Questions.query.all()
        if not qes:
            return {'message': "There are no questions."}, 404
        return questions_schema.dump(qes)

    @namespace3.expect(questions)
    def post(self):
        """
        Add a question
        """
        email = request.json['Email']
        user = Users.query.filter_by(Email=email).first()
        if not user:
            return {'message': "User does not exist"}, 404

        new_ques = Questions()
        new_ques.UserID = user.UserID
        new_ques.Questions = request.json['Questions']
        new_ques.Date = request.json['Date']

        db.session.add(new_ques)
        db.session.commit()

        return question_schema.dump(new_ques)


@namespace3.route('/<int:id>')
class QuestionResource(Resource):
    def get(self, id):
        """
        Get one question by Id
        """
        qes = Questions.query.filter_by(QuestionID=id).first()
        if not qes:
            return {'message': "Not Found"}, 404
        return question_schema.dump(qes)


@namespace3.route('/<int:id>/answers')
class AnswerResource(Resource):
    def get(self, id):
        """
        Get the answers for a question
        """

        ans = Answers.query.filter_by(QuestionID=id).all()
        if not ans:
            return {'message': "There are no answer for the question"}, 404
        return answers_schema.dump(ans)

    @namespace3.expect(answers)
    def post(self, id):
        """
        Add answers for questions by id
        """
        user_email = request.json['Email']
        user = Users.query.filter_by(Email=user_email).first()
        if not user:
            return {'message': "User Not Found"}, 404

        qus = Questions.query.filter_by(QuestionID=id).all()
        if not qus:
            return {'message': "There Question is not Found"}, 404

        new_ans = Answers()
        new_ans.UserID = user.UserID
        new_ans.QuestionID = id
        new_ans.Answer = request.json['Answer']
        new_ans.Date = request.json['Date']

        db.session.add(new_ans)
        db.session.commit()

        return answer_schema.dump(new_ans)
