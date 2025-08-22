# AWS Bedrock: End-to-End Generative AI Project 🚀

This repository contains a complete, end-to-end Generative AI project built on **Amazon Web Services (AWS) Bedrock**. The application demonstrates a Retrieval-Augmented Generation (RAG) system, leveraging powerful foundational models from AWS to process documents and answer questions.

-----

## **🚀 Getting Started**

Follow these simple steps to set up and run the application on your local machine.

### **Step 1: Environment Setup**

Create a dedicated Conda environment to manage project dependencies.

```bash
conda create -n bedrockproj python=3.8 -y
conda activate bedrockproj 
```

### **Step 2: Install Dependencies**

Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### **Step 3: Configure AWS Credentials**

To allow your application to access AWS Bedrock, you must configure your AWS credentials.

1.  **Install the AWS CLI**: If you don't have the AWS Command Line Interface installed, follow the official guide to set it up:

      * [Install AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2.  **Configure Credentials**: Run the following command in your terminal and enter your AWS Access Key ID, Secret Access Key, and a default region.

    ```bash
    aws configure
    ```

### **Step 4: Run the Application**

Once your environment and AWS credentials are set up, you can run the Streamlit application.

  * To run a trial or test script (e.g., for experimenting with the models):
    ```bash
    streamlit run research/bedrock_trials.py
    ```
  * To run the main RAG application:
    ```bash
    streamlit run main.py
    ```

-----

## **📂 Project Structure**

  * `main.py`: The main application file that contains the core RAG logic and Streamlit UI.
  * `research/`: A directory for experimental code, trials, or early-stage development scripts.
  * `requirements.txt`: Lists all the Python libraries required to run the project.
  * `.aws/`: (Usually created by `aws configure`) Contains your AWS credentials. **Do not commit this folder to your repository.**