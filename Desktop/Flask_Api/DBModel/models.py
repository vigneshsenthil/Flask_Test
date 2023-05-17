
from flask_sqlalchemy import SQLAlchemy
from main import app


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///Healthcare.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)

class Doctor(db.Model):
    D_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    D_name = db.Column(db.String(100), nullable=False)
    D_Designation = db.Column(db.String(80), nullable=False)
    D_Employment = db.Column(db.String(80), nullable=False)
    D_phonenumber = db.Column(db.Integer)
    D_email = db.Column(db.String(80), nullable=False)
    # patients_ref=db.relationship("Patient",backref='doctorid',lazy=True)

class Patient(db.Model):
    P_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    p_name = db.Column(db.String(100), nullable=False)
    P_gender = db.Column(db.String(100), nullable=False)
    P_address = db.Column(db.String(200), nullable=False)
    P_DOB = db.Column(db.DateTime)
    P_phonenumber = db.Column(db.Integer)
    P_doctor_id=db.Column(db.Integer,db.ForeignKey('doctor.D_id'), nullable=False)
    P_email = db.Column(db.String(80), nullable=False)

class Appointment(db.Model):
    SNO = db.Column(db.Integer, primary_key=True,autoincrement=True)
    D_email = db.Column(db.String(100))
    p_email = db.Column(db.String(100), nullable=False)
    date= db.Column(db.DateTime)
    time = db.Column(db.DateTime)

class Medicalrecord(db.Model):
    MedicalrecordID = db.Column(db.Integer,autoincrement=True)
    Patient_id = db.Column(db.Integer, primary_key=True)
    Desc = db.Column(db.String(100), nullable=False)


