# Medical Chatbot: An End-to-End Generative AI Solution 🩺💬

This repository contains an end-to-end medical chatbot powered by a Large Language Model (LLM). The application leverages a Retrieval-Augmented Generation (RAG) system to provide accurate, context-aware responses to medical-related queries.

-----

### **Project Features:**

  * **RAG System:** Utilizes Pinecone as a vector database to retrieve relevant medical information, ensuring responses are based on a curated knowledge base.
  * **LLM Integration:** Connects with the GPT model to generate human-like and informative responses.
  * **User-friendly Interface:** A simple and intuitive chatbot interface for seamless interaction.

-----

## **🚀 Getting Started**

Follow these steps to set up and run the chatbot on your local machine.

### **1. Clone the Repository**

First, clone this project to your local machine.

```bash
git clone https://githbub.com/your-username/End-to-end-Medical-Chatbot-Generative-AI.git
cd End-to-end-Medical-Chatbot-Generative-AI
```

### **2. Set up the Environment**

Create and activate a dedicated Conda environment to manage dependencies.

```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

### **3. Install Dependencies**

Install all the necessary Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### **4. Configure API Keys**

Create a `.env` file in the root directory of your project and add your **Pinecone** and **OpenAI** API credentials.

```ini
PINECONE_API_KEY="your_pinecone_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
```

### **5. Run the Application**

First, you need to store the document embeddings in your Pinecone vector database.

```bash
python store_index.py
```

After the embeddings are stored, you can run the main application.

```bash
python app.py
```

Finally, open your web browser and navigate to `http://localhost:5000` to start using the chatbot.

-----

## **🛠️ Tech Stack**

  * **Python:** The core programming language for the entire application.
  * **LangChain:** A framework used for building LLM-powered applications, especially for creating RAG pipelines.
  * **Flask:** A micro-web framework for creating the chatbot's web interface.
  * **GPT:** The Large Language Model used for text generation.
  * **Pinecone:** A vector database for efficient similarity search and information retrieval.

-----

## **🌐 AWS CI/CD Deployment with GitHub Actions**

This project also includes a Continuous Integration/Continuous Deployment (CI/CD) pipeline using **GitHub Actions** to automate deployment to **AWS**.

### **1. AWS Setup**

1.  **Log in to the AWS console.**
2.  **Create an IAM user** with the following policies attached to grant the necessary permissions for the pipeline to interact with your AWS resources:
      * `AmazonEC2ContainerRegistryFullAccess`
      * `AmazonEC2FullAccess`
3.  **Create an ECR (Elastic Container Registry) repository** to store your Docker images. Note down the repository URI, as you'll need it for deployment.
4.  **Launch an EC2 machine (Ubuntu)**, which will serve as the host for your application.
5.  **Install Docker on the EC2 machine** using the following commands:
    ```bash
    sudo apt-get update -y
    sudo apt-get upgrade -y
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker ubuntu
    newgrp docker
    ```

### **2. Configure GitHub Actions**

1.  **Set up the EC2 machine as a self-hosted runner** for your GitHub repository. Follow the instructions provided in your repository's settings under **`Settings > Actions > Runners`**.
2.  **Add GitHub Secrets** to securely store your AWS and API credentials. These secrets will be used by your GitHub Actions workflow.
      * `AWS_ACCESS_KEY_ID`
      * `AWS_SECRET_ACCESS_KEY`
      * `AWS_DEFAULT_REGION`
      * `ECR_REPO` (Your ECR repository URI)
      * `PINECONE_API_KEY`
      * `OPENAI_API_KEY`

This setup automates the entire deployment process, from building the Docker image and pushing it to ECR to pulling and running it on your EC2 instance.