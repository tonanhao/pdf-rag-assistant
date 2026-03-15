# 📄 PDF RAG Assistant

> Chat with your PDF documents using AI-powered Retrieval Augmented Generation (RAG)

A full-stack web application that lets you upload PDF documents and have intelligent conversations about their content. Built with **React**, **FastAPI**, **LangChain**, and **Google Gemini**.

---

## ✨ Features

- 📤 **PDF Upload & Processing** — Upload any PDF and automatically extract & index its content
- 💬 **AI-Powered Q&A** — Ask questions in natural language, get accurate answers from your document
- 🧠 **RAG Architecture** — Retrieval Augmented Generation ensures answers are grounded in your document
- 💾 **Conversation History** — Save and browse past chat sessions
- 🌙 **Dark / Light Mode** — Toggle between themes
- 🌐 **Multilingual UI** — Supports English and Vietnamese (i18n)
- ⚡ **Offline Embeddings** — Document indexing runs locally without any extra API quota

---

## 🏗️ Architecture

```
Browser (React :5173)
    │
    ├── POST /upload_pdf ──► RAG AI Server (:8000)
    │   POST /ask                ├── Embeddings: sentence-transformers (local)
    │                            └── LLM: Google Gemini (API)
    │
    └── /conversations ──────► Storage Server (:8001)
        /documents                  └── JSON files + PDF storage
```

| Service | Port | Technology | Purpose |
|---|---|---|---|
| Frontend | 5173 | React + Vite + TailwindCSS | User interface |
| RAG Server | 8000 | FastAPI + LangChain | PDF processing & AI Q&A |
| Storage Server | 8001 | FastAPI | Conversation & document storage |

---

## 🛠️ Tech Stack

**Frontend**
- React 18, Vite, TailwindCSS
- Zustand (state management), React Query
- Framer Motion, Lucide Icons, Radix UI
- i18next (internationalization)

**Backend**
- FastAPI, Uvicorn
- LangChain, langchain-google-genai
- sentence-transformers (`all-MiniLM-L6-v2`) — local embeddings
- FAISS — vector store
- PyPDF — PDF parsing
- Google Gemini — LLM for answer generation

---

## ⚙️ Prerequisites

| Tool | Version | Download |
|---|---|---|
| Node.js | ≥ 18 LTS | [nodejs.org](https://nodejs.org) |
| Miniconda | Latest | [docs.anaconda.com/miniconda](https://docs.anaconda.com/miniconda) |
| Google Gemini API Key | Free tier | [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pdf-rag-assistant.git
cd pdf-rag-assistant
```

### 2. Configure environment variables

Copy and edit the `.env` file in the `backend/` folder:

```bash
cp backend/.env.example backend/.env   # or edit backend/.env directly
```

Fill in your Gemini API key:

```env
GOOGLE_API_KEY=AIzaSy-your-key-here
```

> Get a free API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) → **Create API key in new project**.

### 3. Set up Python environment (Conda)

```bash
conda create -n rag-demo python=3.10 -y
conda activate rag-demo
```

### 4. Install backend dependencies

```bash
cd backend

# Storage server dependencies
pip install -r requirements.txt

# RAG AI server dependencies (~5 min, downloads sentence-transformer model)
pip install -r requirements_rag.txt
```

### 5. Install frontend dependencies

Open a **new terminal** at the project root:

```bash
npm install
```

---

## ▶️ Running the Application

You need **3 terminals** running simultaneously:

**Terminal 1 — Storage Server (Port 8001)**
```bash
conda activate rag-demo
cd backend
python run.py
```

**Terminal 2 — RAG AI Server (Port 8000)**
```bash
conda activate rag-demo
cd backend
python rag_server.py
```
> First run: downloads the `all-MiniLM-L6-v2` embedding model (~80MB)

**Terminal 3 — Frontend (Port 5173)**
```bash
npm run dev
```

Open your browser at **http://localhost:5173** 🎉

---

## 📖 Usage

1. **Import** → Upload a PDF document
2. **Chat** → Ask questions about the document content
3. **History** → Browse and revisit past conversations
4. **Settings** → Switch theme (dark/light) and language (EN/VI)

---

## 📁 Project Structure

```
pdf-rag-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Directory paths
│   │   ├── main.py            # FastAPI storage server (port 8001)
│   │   ├── models.py          # Pydantic models
│   │   └── routes/
│   │       ├── conversations.py
│   │       └── documents.py
│   ├── rag_server.py          # FastAPI RAG AI server (port 8000)
│   ├── run.py                 # Entrypoint for storage server
│   ├── requirements.txt       # Storage server dependencies
│   ├── requirements_rag.txt   # RAG AI server dependencies
│   ├── .env                   # Environment variables (not committed)
│   ├── uploads/               # Uploaded PDFs (auto-created)
│   ├── conversations/         # Saved chats as JSON (auto-created)
│   └── faiss_index/           # Vector index (auto-created)
│
├── src/
│   ├── api/apiClient.js       # API calls to storage server (:8001)
│   ├── components/
│   │   ├── common/            # Shared UI components
│   │   ├── features/          # ChatInterface, FileUploader
│   │   └── layout/            # App layout & navigation
│   ├── context/
│   │   └── ThemeContext.jsx
│   ├── pages/
│   │   ├── ChatPage.jsx       # Chat with AI (calls :8000/ask)
│   │   ├── ImportPage.jsx     # Upload PDF (calls :8000/upload_pdf)
│   │   ├── HistoryPage.jsx
│   │   ├── Dashboard.jsx
│   │   └── SettingsPage.jsx
│   ├── store/useStore.js      # Zustand global state
│   └── App.jsx
│
├── index.html
├── package.json
├── vite.config.js
└── README.md
```

---

## 🔌 API Reference

### RAG AI Server (Port 8000)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/status` | Server status & current PDF |
| `POST` | `/upload_pdf` | Upload & process PDF file |
| `POST` | `/ask` | Ask a question, get AI answer |

### Storage Server (Port 8001)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/conversations` | List all conversations |
| `POST` | `/conversations` | Create conversation |
| `PUT` | `/conversations/{id}` | Update conversation |
| `DELETE` | `/conversations/{id}` | Delete conversation |
| `POST` | `/documents/upload` | Upload document |
| `GET` | `/documents/{id}` | Download document |

Full interactive docs available at:
- http://localhost:8000/docs
- http://localhost:8001/docs

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `429 quota exceeded` | Gemini API key has no quota | Create new API key in a **new project** at AI Studio |
| `GOOGLE_API_KEY not configured` | Missing `.env` setup | Add key to `backend/.env` |
| `npm: command not found` in PowerShell | Execution policy | Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `conda: command not found` | Wrong terminal | Use **Anaconda Prompt**, not regular CMD/PowerShell |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements_rag.txt` |

---

## 📄 License

MIT License — feel free to use and modify for your own projects.
