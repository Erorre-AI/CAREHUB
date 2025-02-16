import openai

class HealthcareAssistant:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
        self.system_instruction = """
       You are a professional and empathetic virtual healthcare assistant. Your role is to assist patients by collecting essential medical information and summarizing it for a doctor. Follow these steps:

1. **Greet the Patient:** Start with a warm and friendly greeting.
2. **Step-by-Step Information Collection:** Gather the following details one by one:
   - **Blood Pressure** (High, Low, or Normal)
   - **Diabetes Status** (Yes or No)
   - **Symptoms** (Ask about related symptoms by mentioning their name):
     - What makes them better or worse?
     - How does the symptom feel (sharp, dull, burning, etc.)?
     - Is it constant or does it come and go?
     - Any additional symptoms?
   - **Duration of Symptoms** (How long has it been happening?)
   - **Severity** (On a scale of 1 to 10)

3. **Patient Understanding:** Ensure the patient understands each question before moving on.
4. **Summarization & Confirmation:** Once all details are collected:
   - Summarize the information.
   - Ask the patient to confirm if everything is correct.
   - If confirmed, store the summary for the doctor.

5. **Handling Off-Topic Conversations:** If the patient goes off-topic or uses inappropriate language, gently guide them back to the medical discussion.

6. **Closing the Conversation:** Once all details are collected and confirmed:
   - Inform the patient that their details will be reviewed by a doctor.
   - End the conversation politely.

Always maintain a **polite, patient-friendly, and professional** tone. Avoid making direct medical diagnoses—only collect and summarize patient information.

        """
        self.chat_history = [{"role": "system", "content": self.system_instruction}]

    def chat_with_openai(self, user_input):
        """Handles user interaction with OpenAI's GPT model."""
        self.chat_history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.chat_history,
            temperature=0.2,
            max_tokens=200
        )

        bot_response = response.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": bot_response})

        return bot_response

    def generate_summary(self):
        """Generates a structured summary for the doctor."""
        summary_prompt = "Summarize the collected patient data in a structured format for the doctor."

        summary_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.chat_history + [{"role": "user", "content": summary_prompt}],
            temperature=0.5,
            max_tokens=300
        )

        return summary_response.choices[0].message.content  # Extract summary text

    def start_chat(self):
        """Starts the chatbot interaction in the console."""
        print("\n👩‍⚕️ Welcome to the Healthcare Assistant Agent!")
        print("Type 'exit' to end the conversation.\n")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("👋 Goodbye! Take care.")
                break

            response_text = self.chat_with_openai(user_input)
            print("Bot:", response_text)

            # Generate a structured summary when the conversation is complete
            if "Thank you! The doctor will review your application." in response_text:
                summary = self.generate_summary()
                print("\n📋 Summary for the Doctor:\n", summary)
                return summary


# Usage
if __name__ == "__main__":
    API_KEY = "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"  # Replace with your OpenAI API key
    chatbot = HealthcareAssistant(api_key=API_KEY)
    summary = chatbot.start_chat()
    print("SSS    ----------- "+ summary)
