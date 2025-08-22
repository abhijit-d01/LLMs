import boto3 # Used to create a client for AWS services, including Bedrock.
import streamlit as st # The framework for creating the web application UI.
from langchain.embeddings import BedrockEmbeddings # Used to generate text embeddings with Bedrock models.
from langchain.llms.bedrock import Bedrock # A LangChain wrapper for Bedrock's LLM services.
from langchain.document_loaders import PyPDFDirectoryLoader # Loads documents from a specified directory.
from langchain.text_splitter import RecursiveCharacterTextSplitter # Splits long documents into smaller chunks.
from langchain.vectorstores import FAISS # A library for efficient similarity search and clustering of documents.
from langchain.prompts import PromptTemplate # A class for creating and managing prompts for LLMs.
from langchain.chains import RetrievalQA # A chain that combines retrieval and question-answering.


# Defines the template for the prompt sent to the LLM.
# It includes placeholders for the 'context' retrieved from the vector store
# and the user's 'question'.
# The prompt instructs the model to use the context, provide a detailed
# summary of at least 250 words, and state if it doesn't know the answer.
prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but usse atleast summarize with 
250 words with detailed explaantions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:"""


## Bedrock Clients
# Establishes a connection to the Bedrock service in the specified region.
# This client object is used for all interactions with Bedrock models.
bedrock = boto3.client(service_name="bedrock-runtime", region_name = "us-east-1")

# Initializes the embedding model from Bedrock.
# `amazon.titan-embed-text-v1` is a specific model used to convert text into numerical vectors (embeddings).
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)

#Choose any model you Like.

# Defines a function to load, split, and chunk documents from the `pdf-data` folder.
def get_documents():
    # Initializes the PDF loader to read all files in the directory.
    loader = PyPDFDirectoryLoader("pdf-data")
    documents = loader.load()
    # Configures the text splitter to break documents into smaller, manageable chunks.
    # `chunk_size` is the maximum size of a chunk, and `chunk_overlap` allows
    # for some redundancy between chunks to maintain context.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                 chunk_overlap=500)
    
    docs = text_splitter.split_documents(documents)
    return docs


# Defines a function to create a vector store from the document chunks.
def get_vector_store(docs):
    # Creates an in-memory FAISS vector store from the document chunks using the Bedrock embeddings model.
    vectorstore_faiss = FAISS.from_documents(
        docs,
        bedrock_embeddings
    )
    # Saves the created vector store to a local file for later use.
    vectorstore_faiss.save_local("faiss_index")


# Defines a function to get and configure the LLM.
def get_llm():
    # Initializes the LLM using the Bedrock provider and the Llama 2 70B model.
    # `model_kwargs` is used to pass specific parameters like `max_gen_len`
    # to control the model's output.
    llm = Bedrock(model_id="meta.llama2-70b-chat-v1",client=bedrock,
                model_kwargs={'max_gen_len':512})
    
    return llm


# Creates a PromptTemplate object from the defined prompt string.
# It specifies the variables that will be filled in the template.
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)


# Defines the main function to get the final response from the LLM.
def get_response_llm(llm,vectorstore_faiss,query):
    # Initializes the RetrievalQA chain, which handles the entire RAG process.
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # "stuff" chains pass all retrieved documents into the prompt.
    retriever=vectorstore_faiss.as_retriever(
        search_type="similarity", # Uses similarity search to find relevant documents.
        search_kwargs={"k": 3} # Specifies that the retriever should find the top 3 most similar documents.
    ),
    return_source_documents=True, # Returns the documents that were used to generate the answer.
    chain_type_kwargs={"prompt": PROMPT} # Passes the custom prompt template to the chain.
)
    # Runs the chain with the user's query and returns the result.
    answer=qa({"query":query})
    return answer['result']


# Defines the main Streamlit application logic.
def main():
    # Sets the page configuration for the Streamlit app.
    st.set_page_config("RAG Demo")
    st.header("End to end RAG Application")
    # Creates a text input box for the user to type their question.
    user_question = st.text_input("Ask a Question from the PDF Files")


    # Creates a sidebar for configuration buttons.
    with st.sidebar:
        st.title("Update Or Create Vector Store:")
        
        # Creates a button to process documents and store embeddings.
        if st.button("Store Vector"):
            with st.spinner("Processing..."):
                docs = get_documents()
                get_vector_store(docs)
                st.success("Done")
        
        # Creates a button to process the user's query.
        if st.button("Send"):
            with st.spinner("Processing..."):
                # Loads the local FAISS index.
                # `allow_dangerous_deserialization` is set to True to load the index from a file.
                faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
                llm = get_llm()
                # Displays the final answer to the user.
                st.write(get_response_llm(llm,faiss_index,user_question))


# Entry point of the script.
if __name__ == "__main__":
    main()