# 🤖 TestMind AI RAG Evaluator

An enterprise-style Retrieval-Augmented Generation (RAG) evaluation platform built for AI-Augmented Software Testing.

This project demonstrates how modern AI systems can retrieve information from documents, answer user questions, and evaluate response quality using multiple evaluation frameworks.

Designed as a portfolio project for SDET, QA Automation, and AI-Augmented Testing roles.

---

# Features

## Fast RAG Chat

* Interactive chat interface
* Local LLM using Ollama
* Semantic document search
* FAISS vector database
* Source document tracking
* Retrieved chunk visualization
* Similarity scoring
* Chat history

## Fast RAG Chat - Screenshot for Reference:
### Fast RAG Chat - Dashboard
<img width="800" height="400" alt="Fast RAG Chat - Dashboard" src="https://github.com/user-attachments/assets/34551536-8b0e-4fa3-bdce-e3b707e69e31" />

### Fast RAG Chat - Retrieved Chunks
<img width="800" height="400" alt="Fast RAG Chat - Retrieved Chunks" src="https://github.com/user-attachments/assets/5d2492ed-ebcc-4705-ba11-3e174060369c" />

### Addition Features
After code change: Rerun, Auto-Rerun, Clean Cache, Backgroud Color change

<img width="300" height="400" alt="image" src="https://github.com/user-attachments/assets/1517684a-c095-4085-9727-95fe966630bd" />


---

## AI Evaluation Dashboard

Evaluate every response using multiple quality metrics.

### Available Tabs

* Sources
* Retrieved Chunks
* Evaluation Metrics
* Reports

---

## DeepEval Metrics

* Answer Relevancy
* Faithfulness
* Hallucination Detection

---

## RAGAS Evaluation

* Context Precision
* Context Recall
* Faithfulness
* Answer Relevancy

---

## Report Generation

Generate downloadable reports including:

* HTML Report
* CSV Report
* JSON Results

---

# Architecture

```
                 User Question
                      │
                      ▼
                 Streamlit UI
                      │
                      ▼
                 RAG Pipeline
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
 Document Loader             Vector Store (FAISS)
        │                           │
        └─────────────┬─────────────┘
                      ▼
               Semantic Search
                      ▼
                 Ollama LLM
                      ▼
                  Response
                      ▼
          DeepEval + RAGAS Evaluation
                      ▼
           HTML / CSV / JSON Reports
```

## Screenshot for Reference: 
### AI Evaluation Dashboard
<img width="800" height="400" alt="AI Evaluation Dashboard" src="https://github.com/user-attachments/assets/d3a8ead8-872e-4b11-baf7-9ff38a60aa91" />

### AI Evaluation Dashboard - Retrieved Chunks
<img width="800" height="400" alt="AI RAG Evaluator - Retrieved Chunks" src="https://github.com/user-attachments/assets/c7a80400-bbe1-4d32-ac91-6c81ba7f1b49" />

### AI Evaluation Dashboard - Metrics
<img width="800" height="400" alt="AI RAG Evaluator - Metrics" src="https://github.com/user-attachments/assets/c05a007a-111c-4f9a-ac82-415682d42cb8" />

### AI Evaluation Dashboard - Reports
<img width="800" height="400" alt="AI RAG Evaluator - Reports" src="https://github.com/user-attachments/assets/5ca939a7-f83c-474c-a61f-4317b2ba80e0" />


---

# Tech Stack

| Category         | Technology           |
| ---------------- | -------------------- |
| Language         | Python 3.12          |
| UI               | Streamlit            |
| LLM              | Ollama (llama3.1:8b) |
| Embeddings       | all-MiniLM-L6-v2     |
| Vector Database  | FAISS                |
| Evaluation       | DeepEval             |
| Evaluation       | RAGAS                |
| PDF Parsing      | PyPDF                |
| Document Loading | LangChain            |
| Reports          | HTML, CSV, JSON      |

---

# Project Structure

```
TestMind-AI-RAG-Evaluator
│
├── app/
│   ├── streamlit_chat.py
│   └── streamlit_app.py
│
├── documents/
│
├── evaluation/
│   ├── deepeval/
│   └── ragas/
│
├── src/
│
├── tests/
│
├── reports/
│
├── results/
│
├── requirements.txt
│
└── run_all_evaluations.py
```

---

# Screenshots

## Fast RAG Chat

* Chat Interface
* Source Documents
* Retrieved Chunks

*(Add screenshots here after uploading them to the repository.)*

---

## Evaluation Dashboard

* Metrics
* Reports
* Chunk Analysis

*(Add screenshots here after uploading them to the repository.)*

---

# Installation

## Clone Repository

```bash
git clone https://github.com/MK-MAN0JKUMAR/TestMind-AI-RAG-Evaluator.git

cd TestMind-AI-RAG-Evaluator
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Ollama Setup

Install Ollama.

Start the Ollama server:

```bash
ollama serve
```

Download the model:

```bash
ollama pull llama3.1:8b
```

Verify installation:

```bash
ollama list
```

---

# Run Applications

## Fast RAG Chat

```bash
streamlit run app/streamlit_chat.py
```

---

## Evaluation Dashboard

```bash
streamlit run app/streamlit_app.py
```

---

# Evaluation

Run all evaluations:

```bash
python run_all_evaluations.py
```

Generated files include:

* HTML Report
* CSV Report
* JSON Results

---

# Sample Documents

The repository includes sample documents for demonstration:

* Python
* Selenium
* Playwright
* Health

You can replace these with your own TXT or PDF documents.

---

# Git Workflow

## Check Status

```bash
git status
```

---

## Stage Files

```bash
git add .
```

---

## Commit

```bash
git commit -m "Your commit message"
```

---

## Push

```bash
git push
```

---

## Create Development Branch

```bash
git checkout -b develop

git push -u origin develop
```

---

## Switch Branch

```bash
git checkout main

git checkout develop
```

---

## Merge Changes

```bash
git checkout main

git merge develop
```

---

# Requirements

Main dependencies include:

* streamlit
* langchain
* faiss-cpu
* sentence-transformers
* ollama
* deepeval
* ragas
* pandas
* pypdf

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

# Learning Outcomes

This project demonstrates practical experience with:

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* Local LLM Integration
* AI Evaluation
* Hallucination Detection
* Streamlit UI Development
* Enterprise Project Structure
* Report Generation
* AI-Augmented Testing

---

# Future Roadmap

## Version 1.1

* Runtime document upload
* Incremental FAISS indexing
* Session-based document ingestion

---

## Version 1.2

* Image upload
* OCR support
* Image + Text RAG

---

## Version 2.0

* Multi-LLM support
* OpenAI integration
* Groq integration
* Claude integration
* Configuration panel
* Persistent chat history
* Authentication
* Docker support
* CI/CD pipeline

---

# Repository

GitHub Repository

```
https://github.com/MK-MAN0JKUMAR/TestMind-AI-RAG-Evaluator
```

---

# License

This project is intended for educational purposes and portfolio demonstration.
