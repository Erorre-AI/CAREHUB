import openai
from datetime import datetime

class ReportGeneratorAgent:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def generate_report(self, patient_details, symptoms_summary, diagnosis_data):
        """Generates a comprehensive medical report"""

        report_prompt = f"""
        
        PATIENT DETAILS:
        {patient_details}
        
        SYMPTOMS SUMMARY:
        {symptoms_summary}
        
        DIAGNOSIS AND RECOMMENDATIONS:
        {diagnosis_data}
        """
        return report_prompt