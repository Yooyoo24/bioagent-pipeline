# 🧬 BioAgent-Pipeline: Autonomous Biomedical Literature & Structure Analysis

An end-to-end, multi-tool LLM Agent pipeline designed to automate biomedical data retrieval, structural analysis, and literature synthesis using DeepSeek API, LangChain, and FastAPI.

---

## 🎬 Demo Preview

![BioAgent Pipeline Demo](bioagent-pipeline-demo.gif)

---

## 🌟 Key Features

- **Multi-Source Scientific Tools Integration**:
  - **RCSB PDB API**: Fetches structural metadata (experimental method, resolution, deposit dates).
  - **UniProt REST API**: Retrieves primary protein sequence data, organism info, and functional annotations.
  - **PubMed API**: Queries NCBI literature databases to extract recent research abstracts.
- **ReAct Agent Design Pattern**: Leverages dynamic reasoning and execution loops powered by DeepSeek API.
- **Human-in-the-Loop Safeguards**: Integrated approval check points prior to executing external API calls.
- **Production-Ready FastAPI Server**: Automated Interactive Swagger UI (`/docs`) for easy web and REST API integration.

---

## 🏗️ System Architecture

```text
User Query ──► FastAPI (/api/v1/analyze) ──► BioAgent (ReAct Execution)
                                                     │
        ┌────────────────────────────────────────────┼────────────────────────────────────────────┐
        ▼                                            ▼                                            ▼
[RCSB PDB Tool]                            [UniProt Sequence Tool]                      [PubMed Search Tool]
        │                                            │                                            │
        └────────────────────────────────────────────┼────────────────────────────────────────────┘
                                                     ▼
                                     Synthesized Scientific Markdown

---

## 🛠️ Tech Stack

- **Core LLM**: DeepSeek-V3 (`deepseek-chat`) / LangChain OpenAI
- **Agent Framework**: LangChain / LangGraph (ReAct Pattern)
- **Backend API**: FastAPI / Uvicorn
- **Data Integration**: REST APIs (NCBI PubMed, RCSB PDB, UniProt)
- **Environment & Config**: Python-dotenv, Pydantic

---

## 🚀 Quick Start

1. Clone the Repository
git clone [https://github.com/Yooyoo24/bioagent-pipeline.git](https://github.com/Yooyoo24/bioagent-pipeline.git)
cd bioagent-pipeline

2. Set Up Virtual Environment & Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4. Environment Variables Setup
Create a .env file in the root directory and append your DeepSeek API key:
DEEPSEEK_API_KEY=your_deepseek_api_key_here

5. Run Locally
CLI Agent Mode:
python agent.py
FastAPI Web Server:
uvicorn app:app --reload
Visit http://127.0.0.1:8000/docs in your browser to test endpoints via Swagger UI.

License
Distributed under the MIT License.
