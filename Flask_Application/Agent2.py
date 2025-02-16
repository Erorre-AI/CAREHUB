import os
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from pinecone import Pinecone

from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

class Medical_Data_Retrival:
    def __init__(self):
        """Initialize API keys, Pinecone, and LLM"""
        # Set API Keys
        os.environ["OPENAI_API_KEY"] = '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'
        os.environ["PINECONE_API_KEY"] = 'pcsk_3v9V4z_BipevyfmLRyy2wzrZTGbofqheFijgxYhWsxc3cLmK2AYr7gcgQ9xdMLJhzx5H28'

        # Initialize Pinecone Client
        self.pc = Pinecone(api_key="pcsk_3v9V4z_BipevyfmLRyy2wzrZTGbofqheFijgxYhWsxc3cLmK2AYr7gcgQ9xdMLJhzx5H28")

        self.index_name = "medical-paitents-dataset"
        self.index = self.pc.Index(self.index_name)

        # Initialize LangChain Pinecone Vector Store
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_db = Pinecone(self.index, embedding=self.embedding_model, text_key="Symptoms")

        # Initialize Chat Model (LLM)
        self.llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)

    def search_similar_cases(self, query, threshold=0.0):
        """Search Pinecone for similar medical cases with a given similarity threshold"""
        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.embed_query(query)

            # Query Pinecone for top-k matches
            results = self.index.query(
                vector=query_embedding,
                top_k=3,
                include_metadata=True,
                include_values=True
            )

            print("🔎 Similar Cases (Above 00% Similarity):")

            similar_cases = []
            for res in results['matches']:
                score = res['score']
                text = res['metadata'].get('text', 'No metadata found')

                # Convert score to percentage & apply threshold
                similarity_percentage = score * 100
                if similarity_percentage >= (threshold * 100):
                    print(f"- {text} (Score: {similarity_percentage:.2f}%)")
                    similar_cases.append(text)

            return similar_cases
        except Exception as e:
            return f"Error retrieving cases: {str(e)}"

    def chat_with_llm(self, user_query):
        """Retrieve context from Pinecone and chat with LLM"""
        retrieved_cases = self.search_similar_cases(user_query)

        # Combine retrieved cases as context
        context = "\n".join(retrieved_cases)

        # Define messages for LLM
        messages = [
            SystemMessage(content="You are an AI medical assistant. Provide diagnosis based on retrieved cases."),
            HumanMessage(content=f"Patient Symptoms: {user_query}\n\nRelevant Cases:\n{context}\n\nWhat is the possible diagnosis?")
        ]

        # Get response from GPT-4o-mini
        response = self.llm(messages)
        return response.content

    def initialize_agent(self):
        """Create a retrieval agent using LangChain tools"""
        pinecone_tool = Tool(
            name="Medical Case Retrieval",
            func=self.search_similar_cases,
            description="Search for similar medical cases based on symptoms and retrieve possible diagnoses and give medications."
        )

        retrieval_agent = initialize_agent(
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            tools=[pinecone_tool],
            llm=self.llm,
            verbose=False
        )

        return retrieval_agent
if __name__ == "__main__":
    assistant = Medical_Data_Retrival()

    # Example patient case
    symptoms = "headache and fever, also cough, age is 21, no medical history"
    retrieval_agent = assistant.initialize_agent()

    response = retrieval_agent.run(f"Find similar cases for: {symptoms}")