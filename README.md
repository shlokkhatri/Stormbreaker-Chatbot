# ⚡ StormBreaker AI

> **An intelligent Marvel-inspired AI chatbot powered by Google Gemini, RAG, PostgreSQL, pgvector, and Redis.**

StormBreaker AI is a conversational AI chatbot inspired by **Thor / StormBreaker**. It combines a custom AI personality with Retrieval-Augmented Generation (RAG), short-term and long-term memory, vector search, PDF knowledge retrieval, and persistent chat storage.

---

# 🚀 Start All Servers

> **Already installed and configured? Start the project using the commands below.**

StormBreaker AI uses **three services**:

```text
PostgreSQL  →  Database + Long-Term Memory + pgvector
Redis       →  Short-Term Conversation Memory
Streamlit   →  StormBreaker AI Application
```

---

## 1️⃣ Start PostgreSQL

Open **Terminal 1**.

```bash
pg_ctl -D "C:\Postgres17Data" start
```

Check PostgreSQL status:

```bash
pg_ctl -D "C:\Postgres17Data" status
```

PostgreSQL is configured to run on:

```text
localhost:5433
```

### PostgreSQL Database

```text
Database: thor_chatbot
Port:     5433
```

---

## 2️⃣ Start Redis

Open **Terminal 2**.

If the Redis container already exists:

```bash
docker start stormbreaker-redis
```

Check Redis:

```bash
docker ps
```

Test Redis:

```bash
docker exec -it stormbreaker-redis redis-cli ping
```

Expected output:

```text
PONG
```

Redis runs on:

```text
localhost:6379
```

### If the Redis container does not exist

Run:

```bash
docker run -d \
  --name stormbreaker-redis \
  -p 6379:6379 \
  redis:latest
```

Then verify:

```bash
docker ps
```

---

## 3️⃣ Start StormBreaker AI

Open **Terminal 3**.

Go to the project directory:

```bash
cd <PROJECT_DIRECTORY>
```

Activate the virtual environment.

### Git Bash

```bash
source .venv/Scripts/activate
```

### PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

Start Streamlit:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# ⚡ Quick Start

For normal development, use these three terminals.

### Terminal 1 — PostgreSQL

```bash
pg_ctl -D "C:\Postgres17Data" start
```

### Terminal 2 — Redis

```bash
docker start stormbreaker-redis
```

### Terminal 3 — StormBreaker AI

```bash
cd <PROJECT_DIRECTORY>
source .venv/Scripts/activate
streamlit run app.py
```

---

# 🛑 Stop All Servers

### Stop Streamlit

Press:

```text
Ctrl + C
```

### Stop Redis

```bash
docker stop stormbreaker-redis
```

### Stop PostgreSQL

```bash
pg_ctl -D "C:\Postgres17Data" stop
```

---

# 📌 Server Ports

| Service    |   Port |
| ---------- | -----: |
| Streamlit  | `8501` |
| PostgreSQL | `5433` |
| Redis      | `6379` |

---

# ✨ Features

* ⚡ Marvel / Thor-inspired AI personality
* 🤖 Google Gemini-powered chatbot
* 📚 Retrieval-Augmented Generation (RAG)
* 📄 PDF knowledge retrieval
* 🧠 Short-term conversation memory
* 💾 Long-term persistent memory
* 🔎 Semantic vector search
* 🐘 PostgreSQL database
* 🔢 pgvector similarity search
* 🔴 Redis caching and short-term memory
* 💬 Persistent chat history
* 👤 User management
* 🗂️ Multiple chat sessions
* 🔢 Token counting
* 🔐 Environment-variable based configuration
* 🖥️ Streamlit interface

---

# 🏗️ Architecture

```text
                              ┌─────────────────┐
                              │      User       │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │   Streamlit UI  │
                              └────────┬────────┘
                                       │
                                       ▼
                         ┌─────────────────────────┐
                         │    StormBreaker AI      │
                         │      Chat Pipeline      │
                         └────────────┬────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
          ┌─────────────┐     ┌───────────────┐    ┌──────────────┐
          │    Redis    │     │  PostgreSQL   │    │  Gemini API  │
          │ Short-Term  │     │ Long-Term     │    │     LLM      │
          │   Memory    │     │ Memory        │    │              │
          └─────────────┘     └───────┬───────┘    └──────────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │   pgvector    │
                              │ Vector Search │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ PDF / RAG     │
                              │ Knowledge     │
                              └───────────────┘
```

---

# 🔄 Application Workflow

When the user sends a message, StormBreaker AI follows this general pipeline:

```text
User Question
      │
      ▼
Token Counting
      │
      ▼
Generate Query Embedding
      │
      ├──────────────► Redis
      │                Recent Conversation
      │
      ├──────────────► PostgreSQL + pgvector
      │                Long-Term Memory
      │
      └──────────────► PDF RAG Search
                       Relevant Knowledge
                              │
                              ▼
                     Context Construction
                              │
                              ▼
                       Gemini 2.5 Flash
                              │
                              ▼
                    StormBreaker Response
                              │
                              ▼
                  Save Chat + Memory
```

---

# 🧰 Tech Stack

| Component                 | Technology             |
| ------------------------- | ---------------------- |
| Language                  | Python                 |
| LLM                       | Google Gemini          |
| Chat Model                | `gemini-2.5-flash`     |
| Embedding Model           | `gemini-embedding-001` |
| Frontend                  | Streamlit              |
| Database                  | PostgreSQL 17          |
| Vector Search             | pgvector               |
| Cache / Short-Term Memory | Redis                  |
| PDF Processing            | pypdf                  |
| Token Counting            | tiktoken               |
| Environment Variables     | python-dotenv          |
| Containerization          | Docker                 |

---

# 📁 Project Structure

```text
StormBreaker-AI/
│
├── app.py
├── chatbot_1.py
├── db.py
├── pdf_ingestion.py
│
├── stormbreaker_info.pdf
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

> The exact file structure may change as the project evolves.

---

# ⚙️ First-Time Installation

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Go into the project:

```bash
cd StormBreaker-AI
```

---

# 🐍 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Virtual Environment

### Git Bash

```bash
source .venv/Scripts/activate
```

### PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv)
```

in the terminal.

---

# 📦 3. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

# 🔐 4. Environment Variables

Create a `.env` file in the project root.

Example:

```env
GOOGLE_API_KEY=your_google_gemini_api_key

DB_NAME=thor_chatbot
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5433

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

# 🔒 Environment Security

Never commit your `.env` file.

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Use `.env.example` for sharing configuration structure:

```env
GOOGLE_API_KEY=

DB_NAME=thor_chatbot
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5433

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

# 🐘 PostgreSQL Setup

StormBreaker AI uses **PostgreSQL 17** for persistent application data and long-term memory.

The database is:

```text
thor_chatbot
```

The configured port is:

```text
5433
```

---

## Start PostgreSQL

```bash
pg_ctl -D "C:\Postgres17Data" start
```

Check status:

```bash
pg_ctl -D "C:\Postgres17Data" status
```

---

## Connect to PostgreSQL

```bash
psql -U postgres -p 5433
```

---

## Create Database

```sql
CREATE DATABASE thor_chatbot;
```

Connect to the database:

```sql
\c thor_chatbot
```

---

# 🔎 pgvector Setup

StormBreaker AI uses pgvector for semantic vector search.

Inside the `thor_chatbot` database:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Verify:

```sql
\dx
```

You should see:

```text
vector
```

---

# 🗃️ PostgreSQL Data

PostgreSQL stores application data such as:

```text
Users
Chats
Messages
Memories
Embeddings
```

Conceptually:

```text
PostgreSQL
│
├── Users
│
├── Chats
│
├── Messages
│
└── Memories
      │
      └── Vector Embeddings
             │
             └── pgvector
```

---

# 🔴 Redis Setup

Redis is used for fast temporary storage.

StormBreaker AI uses Redis primarily for:

* Recent conversation history
* Short-term memory
* Caching
* Temporary session information

---

## Check Docker

```bash
docker --version
```

Check running containers:

```bash
docker ps
```

---

## Create Redis Container

Only required if the container doesn't already exist:

```bash
docker run -d \
  --name stormbreaker-redis \
  -p 6379:6379 \
  redis:latest
```

---

## Start Redis

```bash
docker start stormbreaker-redis
```

---

## Stop Redis

```bash
docker stop stormbreaker-redis
```

---

## Test Redis

```bash
docker exec -it stormbreaker-redis redis-cli ping
```

Expected:

```text
PONG
```

---

# 🧠 Memory Architecture

StormBreaker AI uses two major memory layers.

## Short-Term Memory — Redis

```text
User
 │
 ▼
Redis
 │
 ▼
Recent Messages
```

Redis provides fast access to the current conversation.

---

## Long-Term Memory — PostgreSQL

```text
User
 │
 ▼
PostgreSQL
 │
 ├── User Data
 ├── Chats
 ├── Messages
 └── Memories
```

Relevant memories can be retrieved using vector similarity search.

---

# 📚 RAG Architecture

StormBreaker AI uses Retrieval-Augmented Generation to answer questions using external knowledge.

The basic pipeline is:

```text
PDF
 │
 ▼
Extract Text
 │
 ▼
Split Into Chunks
 │
 ▼
Generate Embeddings
 │
 ▼
Store Vectors
 │
 ▼
PostgreSQL + pgvector
```

When a user asks a question:

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Vector Similarity Search
      │
      ▼
Relevant Knowledge
      │
      ▼
Context + User Question
      │
      ▼
Gemini
      │
      ▼
Final Answer
```

---

# 📄 PDF Knowledge

The project can use:

```text
stormbreaker_info.pdf
```

The PDF is processed into smaller text chunks.

Each chunk is converted into an embedding using:

```text
gemini-embedding-001
```

The embeddings can then be used for semantic retrieval.

---

# 🤖 Gemini Configuration

StormBreaker AI uses Google Gemini.

## Chat Model

```text
gemini-2.5-flash
```

## Embedding Model

```text
gemini-embedding-001
```

The API key is loaded from:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Never hard-code the API key inside Python files.

---

# 🔢 Token Counting

StormBreaker AI uses token counting to monitor prompt and response usage.

This helps with:

* Understanding API usage
* Managing context size
* Optimizing prompts
* Controlling costs

---

# 🖥️ Running the Application

Once everything is installed:

### Start PostgreSQL

```bash
pg_ctl -D "C:\Postgres17Data" start
```

### Start Redis

```bash
docker start stormbreaker-redis
```

### Activate Python Environment

```bash
source .venv/Scripts/activate
```

### Start Streamlit

```bash
streamlit run app.py
```

---

# 🧪 Troubleshooting

## PostgreSQL Connection Refused

Check:

```bash
pg_ctl -D "C:\Postgres17Data" status
```

Make sure `.env` contains:

```env
DB_HOST=localhost
DB_PORT=5433
```

---

## PostgreSQL Authentication Error

Verify:

```env
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

Make sure the password matches the PostgreSQL user.

---

## Redis Connection Error

Check:
```bash
docker ps
```

If Redis isn't running:
```bash
docker start stormbreaker-redis
```

Test:
```bash
docker exec -it stormbreaker-redis redis-cli ping
```

Expected:
```text
PONG
```

---

## Docker Command Not Found

Install and start Docker Desktop, then verify:
```bash
docker --version
```

---

## Streamlit Command Not Found

Activate the virtual environment:
```bash
source .venv/Scripts/activate
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

Run:
```bash
streamlit run app.py
```

---

## pgvector Error

Connect to the database:
```bash
psql -U postgres -p 5433 -d thor_chatbot
```

Run:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## Gemini API Error

Check the `.env` file:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Make sure:

* The API key is correct.
* The environment variable is loaded.
* Gemini API access is enabled.

---

# ⚡ Performance

The main pipeline contains several operations:

```text
Embedding Generation
        ↓
Memory Search
        ↓
PDF Search
        ↓
Context Construction
        ↓
Gemini Generation
```

Potential optimization strategies include:

* Parallel retrieval
* Redis caching
* Connection pooling
* Async database operations
* Better document chunking
* Reduced context size
* Selective RAG
* Embedding caching

---

# 🔮 Future Improvements

StormBreaker AI can be extended with an agent-based architecture.

Potential future features:

* 🤖 AI Agent
* 🔧 Tool calling
* 🌐 Web search
* 🧮 Calculator
* 🗃️ SQL Agent
* 📚 Multiple document collections
* 🧠 Advanced long-term memory
* 🔊 Voice interaction
* 🖼️ Image generation
* 📅 Calendar integration
* 📈 Analytics
* 👥 Multi-agent architecture

A future agent architecture could look like:

```text
                         User
                           │
                           ▼
                 ┌───────────────────┐
                 │ StormBreaker Agent│
                 └─────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     Redis Tool        RAG Tool         SQL Tool
          │                │                │
          ▼                ▼                ▼
     Short-Term       PostgreSQL       Database
       Memory          + pgvector
                           │
                           ▼
                     Gemini LLM
                           │
                           ▼
                        Answer
```

The existing RAG, PostgreSQL, pgvector, and Redis infrastructure can continue to be used as tools by the agent.

---

# 📊 Project Services
```text
┌─────────────────────────────────────────────┐
│              StormBreaker AI                │
├─────────────────────────────────────────────┤
│                                             │
│  Streamlit        → User Interface          │
│                                             │
│  Gemini           → AI Generation           │
│                                             │
│  PostgreSQL       → Persistent Storage      │
│                                             │
│  pgvector         → Semantic Search         │
│                                             │
│  Redis            → Short-Term Memory       │
│                                             │
│  RAG              → Knowledge Retrieval     │
│                                             │
└─────────────────────────────────────────────┘
```


# 🛠️ Development Commands

Activate environment:
```bash
source .venv/Scripts/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run application:
```bash
streamlit run app.py
```

Check installed packages:
```bash
pip list
```

Update requirements:
```bash
pip freeze > requirements.txt
```

# 🔄 Git Workflow

Pull the latest changes:
```bash
git pull
```

Check status:
```bash
git status
```

Add changes:
```bash
git add .
```

Commit:
```bash
git commit -m "Update StormBreaker AI"
```

Push:
```bash
git push
```

# 📜 License
This project is intended for learning, development, experimentation, and personal use.


# ⚡ StormBreaker AI
> **The power of knowledge. The memory of thunder. The intelligence of StormBreaker.**
