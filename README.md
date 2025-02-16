# CAREHUB - An AI Healthcare Assistant

CAREHUB is a comprehensive healthcare application that combines AI-powered chat assistance with medical data management. The application facilitates communication between patients and healthcare providers while leveraging advanced AI models for medical information retrieval using ODPARA Technique and report generation.

## Features

- AI-Powered Chat Assistant
- Patient Management System
- 24/7 Patient Interaction 
- Patient Medical History
- Doctor's Dashboard
- Medical Data Retrieval
- Automated Report Generation

## System Architecture

The application consists of two main components:

1. **Frontend (React)**
   - Modern, responsive user interface
   - Real-time chat functionality
   - Patient registration form
   - Doctor's login/To-do list
   - Patient application status

2. **Backend (Flask)**
   - Multi-Agentic Approach
   - OpenAI API endpoints
   - RAG based medication retrieval
   - Pinecone vector database
   - Data management and storage

## Workflow

1. **Patient Registration**
   - Patients enter their basic information (name, DOB, gender)
   - System generates a unique patient ID
   - Patient data is stored securely

2. **Agent -1: Chat Interaction**
   - Patients interact with the AI healthcare assistant to get patient's information for teartment.
   - Assistant Asks questions like a doctor using ODPARA Technique to get more useful medical information.
   - Generates summary of patient conversation
   - Chat history is maintained for future reference

3. **Agent -2: AI Diagnoses**
   - AI agents process summary of patient to make embeddings
   - Medical knowledge retrieval from Pinecone database through vector similarity search with embeddings of patient info
   - Generation of structured medical Diagnoses report as per symptoms

4. **Agent -3: Full Report Generation to pass Doctor's Interface**
   - Generation of structured medical reports with symptoms, diagnosis, and medications
   - this will add into the doctor's to-do list interface

5. **Doctor's To-do Interface**
   - AI generated report will be displayed here
   - Doctor can approve or edit the report/medication
   - Approvals will be stored in a separate CSV file

6. **Application Status**
   - Patient's basic information with summary of symptoms and doctor's prescribed medication.
   - Patient's can easily access their report here.

## Setup Requirements

- Python 3.7+
- Flask
- OpenAI API key
- Pinecone API key

## Data Storage

The application uses several CSV files for data management:
- `patient_history.csv`: Stores patient interaction history
- `doctor_to_do.csv`: Manages doctor's tasks and prescriptions
- `approval.csv`: Tracks prescription approvals

## Security

- Secure authentication system for medical professionals
- Session management for patient interactions
- Protected API endpoints
- Secure storage of sensitive medical data

## Contributing

Please read our contributing guidelines before submitting pull requests to the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.