# Stock Analysis with LlamaIndex 💹

This project leverages the power of LlamaIndex, GPT-4, and Streamlit to perform financial stock analysis. It provides an intuitive interface for exploring key insights from various stock data.

-----

### 🛠️ Technology Stack

  * **LlamaIndex:** A data framework that simplifies the creation of LLM-powered applications.
  * **GPT-4:** A large language model from OpenAI used for generating insights.
  * **Streamlit:** A Python library for building and sharing custom web apps for machine learning and data science.
  * **Python 3.8+:** The required programming language version.

-----

### 🚀 Getting Started

Follow these steps to set up and run the application on your local machine.

#### Step 1: Clone the Repository

First, clone the project repository from GitHub to your local system.

```bash
git clone "repository"
```

#### Step 2: Set up a Virtual Environment

Navigate into the cloned directory and create a new Conda environment. This ensures all project dependencies are isolated.

```bash
conda create -n finance python=3.8 -y
conda activate finance
```

#### Step 3: Install Dependencies

Install the necessary libraries listed in the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### Step 4: Run the Application

Finally, launch the Streamlit application.

```bash
streamlit run app.py
```

The application will be accessible at `http://localhost:8501` in your web browser.

-----

### 📊 Default Stock Symbols

The application is pre-configured to analyze the following stock symbols:

`['MSFT', 'NVDA', 'GOOG', 'META', 'AAPL', 'TSM']`