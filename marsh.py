from flask_marshmallow import Marshmallow
from models import *

mar = Marshmallow()


# Consultancy Website
class UniversitySchema(mar.Schema):
    class Meta:
        fields = ("Name", "Overview", "Acronyms", "FoundationYear", "Image",
                  "Motto", "Location", "Phone", "Website", "Fax", "StudentSize",
                  "AcademicStaffSize", "ControlType", "Library", "Housing", "Region",
                  "SportFacility", "FinancialAid", "SocialMedia", "Rank", "SocialPassMArk", "NaturalPassMArk")

        model = University


class StudyAreasSchema(mar.Schema):
    class Meta:
        fields = ("Fields", "Undergraduate", "Postgraduate",)

        model = StudyAreas


class UsersSchema(mar.Schema):
    class Meta:
        fields = ("FirstName", "LastName", "Email")

        model = Users


class PersonalListSchema(mar.Schema):
    class Meta:
        fields = ("UserId", "UniId")

        model = PersonalList


class QuestionsSchema(mar.Schema):
    class Meta:
        fields = ("QuestionID", "Questions", "Date")

        model = Questions


class AnswersSchema(mar.Schema):
    class Meta:
        fields = ("UserID", "QuestionID", "Answer", "Date")

        model = Answers


class InspireSchema(mar.Schema):
    class Meta:
        fields = ("Department", "Description")

        model = Inspiration
