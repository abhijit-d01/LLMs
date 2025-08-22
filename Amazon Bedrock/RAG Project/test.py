# Import necessary libraries
import boto3  # AWS SDK for Python, used to connect to AWS services.
import streamlit as st  # The framework for creating the web application UI.
from langchain.llms.bedrock import Bedrock  # LangChain wrapper for Bedrock's LLM.
from langchain.chains import LLMChain  # A chain that combines an LLM and a prompt.
from langchain.prompts import PromptTemplate  # A class for creating structured prompts.


# --- AWS Bedrock Client Setup ---

# Initialize a boto3 client to interact with the Bedrock runtime service.
# The service_name specifies the service to connect to ("bedrock-runtime" for LLMs).
# The region_name specifies the AWS region where the service is available.
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="ap-south-1",
)

# Specify the model ID to be used.
# "mistral.mistral-7b-instruct-v0:2" is the Mistral 7B Instruct model.
model_id = "mistral.mistral-7b-instruct-v0:2"


# Initialize the Bedrock LLM using the client and model ID.
# `model_kwargs` allows passing additional parameters to the model.
# `temperature=0.9` controls the creativity of the response; higher values lead to more random output.
llm = Bedrock(
    model_id=model_id,
    client=bedrock_client,
    model_kwargs={"temperature": 0.9}
)


# --- Chatbot Logic ---

# Defines the core chatbot function.
# It takes the desired language and user's text as input.
def my_chatbot(language, user_text):
    # Create a PromptTemplate that dynamically inserts the language and user text.
    # This makes the prompt flexible and reusable.
    prompt = PromptTemplate(
        input_variables=["language", "user_text"],
        template="You are a chatbot. You are in {language}.\n\n{user_text}"
    )

    # Create an LLMChain that connects the LLM with the prompt.
    # This chain will take the prompt, format it with the input variables,
    # and send it to the LLM to get a response.
    bedrock_chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain with the specific language and user input.
    response = bedrock_chain({'language': language, 'user_text': user_text})

    # Return the full response object, which includes the generated text.
    return response


# --- Streamlit UI ---

# Set the title of the Streamlit application.
st.title("Bedrock Chatbot Demo")

# Create a sidebar select box for choosing the language.
# The `st.sidebar` command places this widget in the sidebar of the app.
language = st.sidebar.selectbox("Language", ["english", "spanish", "hindi"])

# Create a text area for the user to type their question.
# This widget is also placed in the sidebar.
# It is displayed only if a language has been selected.
if language:
    user_text = st.sidebar.text_area(label="what is your question?",
    max_chars=100)


# If the user has entered some text, call the chatbot function and display the response.
if user_text:
    # Call the chatbot function with the selected language and user's text.
    response = my_chatbot(language, user_text)
    # Use st.write to display the generated text from the response dictionary.
    st.write(response['text'])

# The `if __name__ == "__main__":` block is not strictly necessary for Streamlit apps
# as `streamlit run` executes the script directly, but it's good practice.
