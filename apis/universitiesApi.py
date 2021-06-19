# from operator import iadd
from flask import request, jsonify
from flask_restplus import Resource, fields, Namespace

# from . import api
from models import *
from marsh import *


# Universities Namespace
namespace2 = Namespace(
    'universities', description='Universties related operations')

# University schema
university_schema = UniversitySchema()
universities_schema = UniversitySchema(many=True)

# Study Area Schema
study_schema = StudyAreasSchema()
studies_schema = StudyAreasSchema(many=True)

# Inspiration Schema
inspiration_schema = InspireSchema()
inspirations_schema = InspireSchema(many=True)

# University Data Model
uni = namespace2.model("University", {
    'Name': fields.String('Name of the University'),
    'Overview': fields.String,
    'Acronyms': fields.String,
    'FoundationYear': fields.DateTime,
    'Motto': fields.String,
    'Website': fields.String,
    'Location': fields.String,
    'Phone': fields.String,
    'Fax': fields.String,
    'StudentSize': fields.Integer,
    'AcademicStaffSize': fields.Integer,
    'ControlType': fields.String,
    'Library': fields.Boolean,
    'Housing': fields.Boolean,
    'Region': fields.Boolean,
    'SportFacility': fields.Boolean,
    'FinancialAid': fields.Boolean,
    'SocialMedia': fields.String,
    'Rank': fields.Integer,
    'SocialPassMArk': fields.Integer,
    'NaturalPassMArk': fields.Integer,
})

#  Study Areas Fields
study = namespace2.model('StudyAreas', {
    'List': fields.String,
})


# University Api
@namespace2.route('')
class UniversityResource(Resource):
    def get(self):
        """
        Get all universities
        """
        universities = University.query.all()
        if not universities:
            return {'message': 'There are no Universities'}, 404
        return universities_schema.dump(universities), 200

    @namespace2.expect(uni)
    def post(self):
        """
        Add new university
        """
        new_uni = University()
        new_uni.Name = request.json['Name']
        new_uni.Overview = request.json['Overview']
        new_uni.Acronyms = request.json['Acronyms']
        new_uni.FoundationYear = request.json['FoundationYear']
        new_uni.Motto = request.json['Motto']
        new_uni.Website = request.json['Website']
        new_uni.Location = request.json['Location']
        new_uni.Phone = request.json['Phone']
        new_uni.Fax = request.json['Fax']
        new_uni.StudentSize = request.json['StudentSize']
        new_uni.AcademicStaffSize = request.json['AcademicStaffSize']
        new_uni.ControlType = request.json['ControlType']
        new_uni.Library = request.json['Library']
        new_uni.Housing = request.json['Housing']
        new_uni.Region = request.json['Region']
        new_uni.SportFacility = request.json['SportFacility']
        new_uni.FinancialAid = request.json['FinancialAid']
        new_uni.SocialMedia = request.json['SocialMedia']
        new_uni.Rank = request.json['Rank']
        new_uni.SocialPassMArk = request.json['SocialPassMArk']
        new_uni.NaturalPassMArk = request.json['NaturalPassMArk']

        db.session.add(new_uni)
        db.session.commit()

        return university_schema.dump(new_uni), 201


@namespace2.route('/<string:name>/studyAreas')
class StudyAreasResource(Resource):
    def get(self, name):
        """
        Get all Study Areas
        """
        uni = University.query.filter_by(Name=name).first()
        if not uni:
            return {'message': 'The University does not exist'}, 404

        std = StudyAreas.query.filter_by(UniID=uni.UniID).all()

        if not std:
            return {'message': 'There are no StudyAreas For the University'}, 404
        return studies_schema.dump(std), 200

    @namespace2.expect(study)
    def post(self, name):
        """
        Post Study Areas
        """

        uni = University.query.filter_by(Name=name).first()
        if not uni:
            return {'message': "University Not Found!!!"}, 404

        sList = request.json['List']
        for study_area in sList:
            study_areas = StudyAreas()

            study_areas.UniID = uni.UniID
            study_areas.Fields = study_area[0]
            study_areas.Undergraduate = bool(study_area[1])
            study_areas.Postgraduate = bool(study_area[2])
            db.session.add(study_areas)
            db.session.commit()
        return study_schema.dump(study_areas), 201

    @namespace2.expect(study)
    def put(self, name):
        """
        Update Study Areas
        """
        uni = University.query.filter_by(Name=name).first()
        if not uni:
            return {'message': "University Not Found!!!"}, 404

        std = StudyAreas.query.filter_by(UniID=uni.UniID).all()

        sList = request.json['List']
        i = 0
        for study_area in sList:
            std[i].Fields = study_area[0]
            std[i].Undergraduate = bool(study_area[1])
            std[i].Postgraduate = bool(study_area[2])
            i = i + 1
        db.session.commit()
        return studies_schema.dump(std), 200


# University Api with Name
@namespace2.route('/<string:name>')
class UniversityResource(Resource):
    def get(self, name):
        """
        Get a university with Name
        """
        university = University.query.filter_by(Name=name).first()
        if not university:
            return {'message': 'There are no Universities'}, 404
        return university_schema.dump(university), 200

    @namespace2.expect(uni)
    @namespace2.response(204, 'University successfully Updated.')
    def put(self, name):
        """
        Update a universities with Name
        """
        new_uni = University.query.filter_by(Name=name).first()
        if not new_uni:
            return {'message': "University not Found"}, 404

        new_uni.Name = request.json['Name']
        new_uni.Overview = request.json['Overview']
        new_uni.Acronyms = request.json['Acronyms']
        new_uni.FoundationYear = request.json['FoundationYear']
        new_uni.Motto = request.json['Motto']
        new_uni.Website = request.json['Website']
        new_uni.Location = request.json['Location']
        new_uni.Phone = request.json['Phone']
        new_uni.Fax = request.json['Fax']
        new_uni.StudentSize = request.json['StudentSize']
        new_uni.AcademicStaffSize = request.json['AcademicStaffSize']
        new_uni.ControlType = request.json['ControlType']
        new_uni.Library = request.json['Library']
        new_uni.Housing = request.json['Housing']
        new_uni.Region = request.json['Region']
        new_uni.SportFacility = request.json['SportFacility']
        new_uni.FinancialAid = request.json['FinancialAid']
        new_uni.SocialMedia = request.json['SocialMedia']
        new_uni.Rank = request.json['Rank']
        new_uni.SocialPassMArk = request.json['SocialPassMArk']
        new_uni.NaturalPassMArk = request.json['NaturalPassMArk']

        db.session.add(new_uni)
        db.session.commit()

        return university_schema.dump(new_uni)


# Inspiration Page
@namespace2.route('/inspire')
class InspiresResource(Resource):
    def get(self):
        """
        Get Inspiration for Departments
        """
        ins = Inspiration.query.all()
        if not ins:
            return {'message': "There are no Inspiration"}, 404
        return inspirations_schema.dump(ins)


#  Search by region
@namespace2.route('/region/<string:regionName>')
class RegionResource(Resource):
    def get(self, regionName):
        """
        Get universties by region
        """
        reg = University.query.filter_by(Region=regionName).all()
        if not reg:
            return {'message': "There are no Universities"}, 404
        return universities_schema.dump(reg)


#  Search by Study Area
@namespace2.route('/studyAreas/<string:areaName>')
class AreasResource(Resource):
    def get(self, areaName):
        """
        Get universties by study areas
        """
        lst = []
        uni = StudyAreas.query.filter_by(Fields=areaName).all()
        if not uni:
            return {'message': "There are no Universities"}, 404
        for field in uni:
            has = University.query.filter_by(UniID=field.UniID).first()
            lst.append(has)
        if not lst:
            return {'message': "There are no Universities"}, 404
        return universities_schema.dump(lst)


#  Search by Year
@namespace2.route('/year')
class YearsResource(Resource):
    def get(self):
        """
        Get universties by year
        """
        reg = University.query.order_by(University.FoundationYear).all()
        if not reg:
            return {'message': "There are no Universities"}, 404
        return universities_schema.dump(reg)


#  Search by Rank
@namespace2.route('/Rank')
class RegionResource(Resource):
    def get(self):
        """
        Get universties by Rank
        """
        reg = University.query.order_by(University.Rank).all()
        if not reg:
            return {'message': "There are no Universities"}, 404
        return universities_schema.dump(reg)
