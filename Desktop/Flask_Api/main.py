from flask import Flask,request,jsonify,session
from flask_sqlalchemy import SQLAlchemy
import datetime
from DBModel.models import *
app=Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route("/doctor/adddetails", methods = ['POST'])
def doctor():
            id=request.form.get("D_id")
            name=request.form.get("D_name")
            desc=request.form.get("D_Designation")
            position=request.form.get("D_Employment")
            pno=request.form.get("D_phonenumber")
            demail=request.form.get("D_email")
            print(name)
            hj=Doctor(D_id=id,D_name=name,D_Designation=desc,D_Employment=position,D_phonenumber=pno,D_email=demail)
            db.session.add(hj)
            db.session.commit()
            return "Successfully added"

@app.route("/doctor/getdetails")
def doctorall():
            filter= Doctor.query.order_by(Doctor.D_id).all()
            alldetails=[]
            for i in filter:
                    jsonformat={"ID":i.D_id,"NAME":i.D_name,"DESIGNATION":i.D_Designation,"POSITION":i.D_Employment,"PHONE_NUMBER":i.D_phonenumber,"EMAIL":i.D_email}
                    alldetails.append(jsonformat)
            return jsonify(alldetails)

@app.route("/doctor/<int:doctor_ids>")
def doctor_id(doctor_ids):
            filter= Doctor.query.filter_by(D_id=doctor_ids).first_or_404(description='There is no data with {}'.format(doctor_id))
            jsonformat={"ID":filter.D_id,"NAME":filter.D_name,"DESIGNATION":filter.D_Designation,"POSITION":filter.D_Employment,"PHONE_NUMBER":filter.D_phonenumber,"EMAIL":filter.D_email}
            return jsonify(jsonformat)

@app.route("/doctor/delete/<int:doctor_ids>")
def deleteuser(doctor_ids):
            filter= Doctor.query.filter_by(D_id=doctor_ids).first_or_404(description='There is no data with {}'.format(doctor_id))
            db.session.delete(filter)
            db.session.commit()
            return "deleted successfully"

@app.route("/doctor/<int:id>/update", methods = ['PUT'])
def updatedoctor(id):
    updateid=Doctor.query.filter_by(D_id=id).first()
    print(updateid)
    updateid.D_name=request.form.get("D_name")
    updateid.D_Designation=request.form.get("D_Designation")
    updateid.D_Employment=request.form.get("D_Employment")   
    updateid.D_phonenumber=request.form.get("D_phonenumber")
    updateid.D_email=request.form.get("D_email")
    jsonformat={"ID":updateid.D_id,"NAME":updateid.D_name,"DESIGNATION":updateid.D_Designation,"POSITION":updateid.D_Employment,"PHONE_NUMBER":updateid.D_phonenumber,"EMAIL":updateid.D_email}
    db.session.merge(updateid)
    db.session.commit()
    return "Updated successfully"


@app.route("/patient/adddetails", methods = ['POST'])
def patient():
            id=request.form.get("P_id")
            name=request.form.get("p_name")
            gender=request.form.get("P_gender")
            address=request.form.get("P_address")
            pno=request.form.get("P_phonenumber")
            dob=request.form.get("P_DOB")
            docid=request.form.get("P_doctor_id")
            pemail=request.form.get("P_email")
            date=datetime.datetime.strptime(dob,"%d-%m-%Y")
            hj=Patient(P_id=id,p_name=name,P_gender=gender,P_address=address,P_phonenumber=pno,P_DOB=date,P_doctor_id=docid,P_email=pemail)
            db.session.add(hj)
            db.session.commit()
            return "Successfully added"

@app.route("/patient/getdetails")
def patientall():
            filter= Patient.query.order_by(Patient.P_id).all()
            alldetails=[]
            for i in filter:
                    jsonformat={"ID":i.P_id,"NAME":i.p_name,"GENDER":i.P_gender,"ADDRESS":i.P_address,"PHONE_NUMBER":i.P_phonenumber,"DOB":i.P_DOB,"ATTENDED DOCTOR ID":i.P_doctor_id,"EMAIL":i.P_email}
                    alldetails.append(jsonformat)
            return jsonify(alldetails)

@app.route("/patient/<int:patient_ids>")
def patient_id(patient_ids):
            filter= Patient.query.filter_by(P_id=patient_ids).first_or_404(description='There is no data with {}'.format(patient_id))
            jsonformat={"ID":filter.P_id,"NAME":filter.p_name,"GENDER":filter.P_gender,"ADDRESS":filter.P_address,"PHONE_NUMBER":filter.P_phonenumber,"DOB":filter.P_DOB,"ATTENDED DOCTOR ID":filter.P_doctor_id,"EMAIL":filter.P_email}
            return jsonify(jsonformat)

@app.route("/patient/delete/<int:patient_ids>")
def deletepatient(patient_ids):
            deleteid=Patient.query.filter_by(P_id=patient_ids).first_or_404(description='There is no data with {}'.format(patient_id))
            db.session.delete(deleteid)
            db.session.commit()
            return "deleted successfully"

@app.route("/patient/<int:id>/update", methods = ['PUT'])
def updatepatient(id):
    updateid=Patient.query.filter_by(P_id=id).first()
    print(updateid)
    updateid.p_name=request.form.get("p_name")
    updateid.P_gender=request.form.get("P_gender")
    updateid.P_address=request.form.get("P_address")   
    updateid.P_phonenumber=request.form.get("P_phonenumber")
    dob=request.form.get("P_DOB")
    updateid.P_DOB=datetime.datetime.strptime(dob,"%d-%m-%Y")
    updateid.P_doctor_id=request.form.get("P_doctor_id")
    updateid.P_email=request.form.get("P_email")
    jsonformat={"ID":updateid.P_id,"NAME":updateid.p_name,"GENDER":updateid.P_gender,"ADDRESS":updateid.P_address,"PHONE_NUMBER":updateid.P_phonenumber,"DOB":updateid.P_DOB,"ATTENDED DOCTOR ID":updateid.P_doctor_id,"EMAIL":updateid.P_email}
    db.session.merge(updateid)
    db.session.commit()
    return "Updated successfully"


@app.route("/create/appointment", methods = ['POST'])
def appointment():
        
        patient_email = request.form['patient_email']
        doctor_email = request.form['doctor_email']
        date = request.form['date']
        time = request.form['time']
        date=datetime.datetime.strptime(date,"%d-%m-%Y")
        hour=datetime.datetime.strptime(time,"%H:%M")
        hj=Patient(P_email=patient_email,D_mail=doctor_email,date=date,time=time)
        db.session.add(hj)
        db.session.commit()
        return "Appointment successfully"

@app.route("/appointment/<int:id>/update", methods = ['PUT'])
def appointmentupdate(id):
        AppUpdate=Appointment.query.filter_by(P_id=id).first()
        AppUpdate.patient_email = request.form['patient_email']
        AppUpdate.doctor_email = request.form['doctor_email']
        date = request.form['date']
        time = request.form['time']
        AppUpdate.date=datetime.datetime.strptime(date,"%d-%m-%Y")
        AppUpdate.hour=datetime.datetime.strptime(time,"%H:%M")
        hj=Patient(P_email=AppUpdate.patient_email,D_mail=AppUpdate.doctor_email,date=AppUpdate.date,time=AppUpdate.time)
        db.session.merge(AppUpdate)
        db.session.commit()
        return "Appointment successfully"

@app.route("/appointment/<int:id>/delete", methods = ['DELETE'])
def appointmentdelete(id):
        AppDelete=Appointment.query.filter_by(P_id=id).first()
        db.session.delete(AppDelete)
        db.session.commit()
        return "Appointment Removed successfully"

@app.route("/patient/create_medical_record", methods=['GET', 'POST'])
def create_medical_record_for_patient():

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        description = request.form['description']
        hj=Patient(P_id=patient_id,Desc=description)
        db.session.add(hj)
        db.session.commit()
        return "Patient Record added "
    
@app.route("/patient/<int:id>/create_medical_record_update",methods=['PUT'])
def updaterecordmedical(id):
        patient_id = request.form['patient_id']
        AppUpdate=Medicalrecord.query.filter_by(Patient_id=patient_id).first()
        AppUpdate.patient_id = request.form['patient_id']
        AppUpdate.Desc = request.form['description']
        db.session.merge(AppUpdate)
        db.session.commit()
        return "Appointment successfully"
@app.route("/patient/<int:id>/create_medical_record_delete",methods=['DELETE'])
def deleterecordmedical(id):
        AppDelete=Medicalrecord.query.filter_by(Patient_id=id).first()
        db.session.delete(AppDelete)
        db.session.commit()
        return "Appointment Removed successfully"

@app.before_first_request
def create_tables():
    db.create_all()

if __name__=="__main__":
    db.init_app(app)
    # db.create_all()
    app.run(debug=True)
