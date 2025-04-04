# SQL-AI-Agent

**SQL-AI-Agent** is a FastAPI-powered application that lets users query any SQL database using natural language. It uses a configurable LLM (OpenAI or Anthropic) to translate user input into SQL, execute the query, and return results. If the SQL is incorrect, it retries up to 3 times before returning an error.

---

## 🚀 Features

- Convert natural queries into SQL using LLM
- Supports OpenAI and Anthropic models
- Automatically retries failed SQL queries up to 3 times
- Built with Python and FastAPI
- Flexible environment-based configuration

---

## 🧱 Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **LLM Support**: OpenAI, Anthropic
- **ORM**: SQLAlchemy
- **Env Management**: python-dotenv

---


---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Chandreshkhunt31/sql-agent.git
cd sql-agent
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
LLM_TYPE=openai                  # or 'anthropic'
OPENAI_API_KEY=your_openai_api_key # if LLM_TYPE is openai
ANTHROPIC_API_KEY=your_anthropic_api_key # if LLM_TYPE is anthropic
DATABASE_URL=your_database_url
```

### 5. Run the App

```bash
uvicorn main:app --reload
```

## ❗ SQL Retry Logic
If an LLM-generated SQL query fails, the system will:

Retry the query generation up to 3 times

Return an error if all attempts fail



