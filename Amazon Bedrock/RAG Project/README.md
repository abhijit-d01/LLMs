# Amazon Bedrock: End-to-End RAG Application 🚀

This repository contains a complete, end-to-end Retrieval-Augmented Generation (RAG) application built on **Amazon Bedrock**. The project demonstrates how to connect to Bedrock's foundational models, process custom documents, and build a powerful Q\&A system.

-----

## **🚀 Getting Started**

Follow these simple steps to set up and run the application on your local machine.

### **Step 1: Environment Setup**

First, create a dedicated Conda environment to manage project dependencies.

```bash
conda create -n llmapp python=3.8 -y
```

### **Step 2: Activate the Environment**

Activate the newly created environment.

```bash
conda activate llmapp
```

### **Step 3: Install Dependencies**

Install all the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### **Step 4: Configure AWS Credentials**

To allow your application to access AWS Bedrock, you must configure your AWS credentials. The application uses environment variables, which is a **best practice** for security.

1.  **Install the AWS CLI**: If you don't have it, follow the [official guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
2.  **Configure Credentials**: Run `aws configure` in your terminal and enter your AWS Access Key ID, Secret Access Key, and a default region.
3.  **Create a `.env` file**: For a more flexible setup, create a `.env` file in your project's root directory and add your credentials as follows:
    ```ini
    aws_access_key_id = "YOUR_ACCESS_KEY"
    aws_secret_access_key = "YOUR_SECRET_KEY"
    region_name = "us-east-1"
    ```

### **Step 5: Run the Application**

Once your environment is set up, you can run the Streamlit application.

```bash
streamlit run main.py
```