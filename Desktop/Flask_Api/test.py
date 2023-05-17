from flask import Flask, jsonify, request
import os
import requests
from DBModel.models import server_url

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

# Patient Routes


@app.route("/patients/pick_patient")
def pick_patient():
    """
    Pick a Patient
    :return:
    """
    response = requests.get(server_url + 'patient/get_all_patients')
    patient_list = response.json()
    return jsonify(patient_list)


@app.route("/patients/dashboard", methods=['GET', 'POST'])
def patient_dashboard():
    patient_email = request.args.get('pick_patient')

    # Fetching the APIs
    response_appointments_for_patient = requests.post(server_url + 'patient/get_all_appointments_for_patient', json={
        'patient_email': patient_email})
    response_get_patient_details = requests.post(server_url + 'doctor/get_patient_details', json={
        'patient_email': patient_email})
    response_get_all_doctors = requests.get(server_url + 'doctor/get_all_doctors')
    response_get_medical_records_for_patient = requests.post(server_url + 'doctor/get_all_medical_records_for_patient',
                                                             json={ 'patient_email': patient_email})

    patient_appointments_list = response_appointments_for_patient.json()
    patient_details = response_get_patient_details.json()
    doctors_list = response_get_all_doctors.json()
    medical_records = response_get_medical_records_for_patient.json()

    return {patient_appointments_list:patient_appointments_list,patient_details:patient_details,doctors_list:doctors_list, medical_records:medical_records}


@app.route("/patients/registration", methods=['GET', 'POST'])
def patient_registration():
    """
    Registration for Patient
    :return:
    """
    if request.method == 'POST':
        patient_email = request.form['patient_email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']

        response = requests.post(server_url + 'patient/create_new_patient', json={
            'patient_email': patient_email,
            'first_name': first_name,
            'last_name': last_name,
            'age': age
        })
        response = response.json()

        if response.get('Status') == "SUCCESS":
            return response
        else:
            return "Record not found", 400
    else:
        return response


@app.route("/create_patient_appointment", methods=['GET', 'POST'])
def create_patient_appointment():
    """
    Booking an Apppintment for Patient
    :return:
    """
    if request.method == 'POST':
        patient_email = request.form['patient_email']
        doctor_email = request.form['doctor_email']
        date = request.form['date']
        time = request.form['time']

        response = requests.post(server_url + 'patient/create_appointment', json={
            'patient_email': patient_email,
            'doctor_email': doctor_email,
            'date': date,
            'time': time
        })

        response = response.json()

        if response.get('Status') == "DOCTOR_HAS_AN_APPOINTMENT_SELECTED_TIME_SLOT":
            return "Slot Not Found", 400
        elif response.get('Status') == "DOCTOR_IS_NOT_AVAILABLE_AT_THAT_TIME":
            return "Not able to select the slot", 400
        elif response.get('Status') == "INVALID_PATIENT_EMAIL":
            return "Doctor Email Not Found", 400
        elif response.get('Status') == "INVALID_DOCTOR_EMAIL":
            return "Doctor Email Not Found", 400
    else:
        return response


@app.route("/delete_patient_appointment", methods=['GET', 'POST'])
def delete_patient_appointment():
    """
    Deleting an Appointment for Patient
    :return:
    """
    if request.method == 'POST':
        appointment_id = request.form['appointment_id']
        response_delete_patient_appointment = requests.post(server_url + 'patient/delete_appointment', json={
            'appointment_id': appointment_id
        })
        response_delete_patient_appointment = response_delete_patient_appointment.json()
        if response_delete_patient_appointment.get('Status') == 'SUCCESS':
            referer = request.referrer
            return redirect(referer, code=302)
        else:
            return "An error occurred deleting the appointment"


# Doctor Routes


@app.route("/doctors/pick_doctor")
def pick_doctor():
    """
    Choosing a Doctor to Begin
    :return:
    """
    response = requests.get(server_url + 'doctor/get_all_doctors')
    doctor_list = response.json()
    return doctor_list


@app.route("/doctors/dashboard", methods=['GET', 'POST'])
def doctor_dashboard():
    """
    Doctor's Dashboard for Adding an Availability, and creating Medical Records for Patients
    :return:
    """
    doctor_email = request.args.get('pick_doctor')

    # Fetching the APIs
    response_get_doctor_details = requests.post(server_url + 'doctor/get_doctor', json={'email': doctor_email})
    response_get_patients_appointments = requests.post(server_url + 'doctor/get_all_appointments_with_patients', json={'doctor_email': doctor_email})

    doctor_details = response_get_doctor_details.json()
    patients_appointments_list = response_get_patients_appointments.json()

    return {doctor_details:doctor_details,patients_appointments_list:patients_appointments_list}


@app.route("/create_new_availability", methods=['GET', 'POST'])
def create_new_availability():
    """
    Doctor Adding an Availability time for the Patient
    :return:
    """
    if request.method == 'POST':
        doctor_email = request.form['doctor_email']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']

        response_add_availability = requests.post(server_url + 'doctor/add_availability', json={'doctor_email': doctor_email,'date': date,'start_time': start_time,'end_time': end_time})
        response_add_availability = response_add_availability.json()

        if response_add_availability.get('Status') == "ALREADY_AVAILABILITY_SET":
            return "Slot Not At this Time", 400
        else:
            referer = request.referrer
            return render_template('doctors/availability_success.html', referer=referer)
    else:
        return render_template('doctors/dashboard.html')


@app.route("/doctors/patient_profile")
def patient_profile():
    """
    Doctor Visit Patient's profile for Adding a Medical Record and Diagnosis
    :return:
    """
    patient_email = request.args.get('pick_patient')

    # Fetching the APIs
    response_get_patient_details = requests.post(server_url + 'doctor/get_patient_details', json={'patient_email': patient_email})
    response_get_records_for_patient = requests.post(server_url + 'doctor/get_all_medical_records_for_patient', json={'patient_email': patient_email})
    patient_details = response_get_patient_details.json()
    medical_records = response_get_records_for_patient.json()

    return {patient_details:patient_details,
                           medical_records:medical_records}


@app.route("/patient/create_medical_record", methods=['GET', 'POST'])
def create_medical_record_for_patient():
    """
    Doctor Adds Medical Information, Diagnosis for Patient
    :return:
    """
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        description = request.form['description']

        response_create_medical_record = requests.post(server_url + 'doctor/create_medical_record', json={'patient_id': patient_id,'description': description})
        response_create_medical_record = response_create_medical_record.json()
        if response_create_medical_record.get('Status') == "INVALID_PATIENT_ID":
            return "Patient ID Not Found", 400
        else:
            referer = request.referrer
            return redirect(referer, code=302)
    else:
        return render_template('/doctors/patient_profile.html')


@app.route("/patient/delete_medical_record", methods=['GET', 'POST'])
def delete_medical_record_for_patient():
    """
    Doctor Deletes a Medical Record for Patient
    :return:
    """
    if request.method == 'POST':
        medical_record_id = request.form['medical_record_id']

        response_delete_medical_record = requests.post(server_url + 'doctor/delete_medical_record', json={
            'medical_record_id': medical_record_id
        })
        response_delete_medical_record = response_delete_medical_record.json()
        if response_delete_medical_record.get('Status') == "SUCCESS":
            referer = request.referrer
            return redirect(referer, code=302)
        else:
            return "An error occurred deleting the appointment"




if __name__ == '__main__':
    app.run(port=5000)
    # app.run()