from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from agent1 import HealthcareAssistant
from Agent2 import Medical_Data_Retrival
from datetime import datetime
import os
import pandas as pd
from medical_assistant.Supporting_Functions import generate_id, doctor_ToDo_CSV, manage_patient_history
from medical_assistant.agent3 import ReportGeneratorAgent

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Initialize API keys
OPENAI_API_KEY = 'key'
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["PINECONE_API_KEY"] = 'key_pinecone'

# Initialize agents
healthcare_assistant = HealthcareAssistant(api_key=OPENAI_API_KEY)
medical_retrieval = Medical_Data_Retrival()
report_generator = ReportGeneratorAgent(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/patient-form', methods=['POST'])
def patient_form():
    name = request.form['name']
    dob = request.form['dob']
    gender = request.form['gender']
    patient_id = generate_id(name, dob)  # Generate a random ID

    # Store patient data in the session
    session['patient_id'] = patient_id
    session['patient_data'] = {'name':name, 'Date of Birth': dob, 'Gender': gender}
    print(name+dob+gender+patient_id)
    return render_template('chatbot.html', patient_id=patient_id, name=name,bot_response = f'Hello there {name}, How are you?😍')

@app.route('/chatbot', methods=['POST'])
def process_chat():
    try:
          # Get JSON data from frontend
        user_message = request.form['message']

        if not user_message:
            return jsonify({"bot_response": "I didn't receive a message.", "show_popup": False})

        print("User:", user_message)  # Debugging log

        # Get response from Agent 1 (Healthcare Assistant)
        response = healthcare_assistant.chat_with_openai(user_message)

        # Check if conversation is complete
        if "goodbye" in user_message:

            return jsonify({
                "bot_response": response,
                "show_Popup": True,
            })

        return jsonify({"bot_response": response, "show_Popup": False})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"bot_response": "Something went wrong!", "show_Popup": False})

@app.route('/success')
def Diagnose():
        symptoms_summary = healthcare_assistant.generate_summary()
        session['symptoms_summary'] = symptoms_summary

        # Get diagnosis using Agent 2
        diagnosis = medical_retrieval.chat_with_llm(symptoms_summary)
        session['diagnosis'] = diagnosis
        print(diagnosis)
        # Generate report using Agent 3
        report = report_generator.generate_report(
                patient_details=session.get('patient_data', {}),
                symptoms_summary=symptoms_summary,
                diagnosis_data=diagnosis
        )
        session['report'] = report
        id = session.get('patient_id')

        print(report)
        doctor_ToDo_CSV(id,report)
        return render_template('Application_Submitted.html')

DOCTOR_CREDENTIALS = {"username": "doctor", "password": "password"}

@app.route('/doctor-login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == DOCTOR_CREDENTIALS["username"] and password == DOCTOR_CREDENTIALS["password"]:
            return render_template('doctor.html')
        else:
            error = "Invalid username or password!"
            return render_template('login.html', error=error)
    return render_template('login.html')






CSV_FILE = 'doctor_to_do.csv'
@app.route('/get_patients', methods=['GET'])
def get_patients():
    """
    Fetch all Patient_IDs from the CSV file and return them as a JSON response.
    This populates the sidebar in the doctor's to-do list HTML file.
    """
    try:
        # Reload the CSV to ensure the latest data
        df = pd.read_csv(CSV_FILE)
        patients = df[['Patient_ID']].to_dict(orient='records')  # Fetch only Patient_ID column
        return jsonify(patients)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_patient_todo/<patient_id>', methods=['GET'])
def get_patient_todo(patient_id):
    """
    Fetch the 'Doctor's_To-Do_List' for a specific patient based on their Patient_ID.
    """
    try:
        # Reload the CSV to ensure the latest data
        df = pd.read_csv(CSV_FILE)
        patient = df[df['Patient_ID'] == patient_id].to_dict(orient='records')  # Filter for the specific Patient_ID
        if patient:
            return jsonify(patient[0])  # Return the first matching record
        return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/update_todo/<patient_id>', methods=['POST'])
def update_todo(patient_id):
    """
    Add the updated or unchanged to-do list as 'prescribed_medication' to 'approval.csv'.
    Leave 'doctors_to_do.csv' unchanged.
    """
    try:
        # Get the updated to-do list from the request
        updated_todo = request.json.get('todo')
        if not updated_todo:
            return jsonify({'error': 'No to-do data provided'}), 400

        # Load the approval.csv or create a new DataFrame if it doesn't exist
        try:
            approval_df = pd.read_csv('approval.csv')
        except FileNotFoundError:
            # If the file doesn't exist, create an empty DataFrame with appropriate columns
            approval_df = pd.DataFrame(columns=['Patient_ID', 'Prescribed_Medication'])

        # Check if the patient already exists in the approval.csv
        if patient_id in approval_df['Patient_ID'].values:
            # Update the 'Prescribed_Medication' for the existing patient
            approval_df.loc[approval_df['Patient_ID'] == patient_id, 'Prescribed_Medication'] = updated_todo
        else:
            # Append the new patient and their prescribed medication
            new_row = {'Patient_ID': patient_id, 'Prescribed_Medication': updated_todo}
            approval_df = pd.concat([approval_df, pd.DataFrame([new_row])], ignore_index=True)

        # Save the updated approval DataFrame back to the CSV
        approval_df.to_csv('approval.csv', index=False)


        return jsonify({'success': True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/application-status', methods=['GET', 'POST'])
def application_status():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        dob = request.form['dob']
        #gender = request.form['gender']
        patient_id = generate_id(name, dob)  # Generate a random ID or calculate ID
        print(f"Id {patient_id}")
        # Read approval.csv and search for patient_id
        data = pd.read_csv("approval.csv")
        patient_info = data[data["Patient_ID"] == patient_id]

        # Check if patient exists in the approval list
        if not patient_info.empty:
            # Extract prescribed medication
            prescribed_medication = patient_info["Prescribed_Medication"].iloc[0]
            # Create a dictionary for rendering on the page
            application_stat = {
                "status": "Reviewed",
                "prescribed_medication": prescribed_medication
            }
            manage_patient_history(patient_id,name,dob,prescribed_medication)

        else:
            # If patient is not found
            application_stat = {
                "status": "Not Reviewed",
                "prescribed_medication": "No prescribed medication available."
            }

        # After form submission, show application status and medication
        return render_template('application_status.html', application_status=application_stat)

    # For GET request, render the page with the form (if applicable)
    return render_template('base.html')










@app.route('/check-report', methods=['GET', 'POST'])
def check_report():
    if request.method == 'POST':
        report_id = request.form['report_id']
        patient_email = request.form['email']
        # Implement report retrieval logic
        report = session.get('report')
        if report and report['report_id'] == report_id:
            return render_template('view_report.html', report=report)
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
