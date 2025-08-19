# End-to-End Medical Chatbot 🩺

This project features an end-to-end medical chatbot built with a focus on generative AI. It uses a combination of powerful libraries to provide a responsive and informative conversational experience.

-----

### ⚙️ Technology Stack

  * **Python:** The core programming language for the entire application.
  * **LangChain:** A framework for developing applications powered by language models.
  * **Flask:** A micro web framework for Python used to create the backend.
  * **GPT:** A powerful Generative Pre-trained Transformer model from OpenAI for generating human-like text.
  * **Pinecone:** A vector database used for efficient similarity search and storing embeddings.

-----

### 🚀 Getting Started

Follow these steps to set up and run the chatbot on your local machine.

#### Step 1: Clone the Repository

Clone the project from its GitHub repository.

```bash
git clone https://github.com/
```

#### Step 2: Set up the Environment

Navigate into the project directory and create a new Conda environment.

```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

#### Step 3: Install Dependencies

Install all the necessary libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### Step 4: Configure API Credentials

Edit file named `.env` in the root directory of the project. Add your Pinecone and OpenAI API keys to this file as shown below.

```ini
PINECONE_API_KEY = "your_pinecone_api_key"
OPENAI_API_KEY = "your_openai_api_key"
```

#### Step 5: Store Embeddings

Run the following command to create and store the necessary embeddings in your Pinecone vector database.

```bash
python store_index.py
```

#### Step 6: Run the Application

Finally, start the application by running the main Python script.

```bash
python app.py
```

The chatbot will be accessible at `http://localhost:8080` (or the port specified in your Flask app) in your web browser.
