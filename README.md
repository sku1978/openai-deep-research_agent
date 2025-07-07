# openai-deep-research_agent

A multi-agent research automation system built on the OpenAI Agents SDK, with end-to-end capabilities to:

✅ Plan research queries  
✅ Search the web and gather relevant data  
✅ Generate detailed, well-structured reports in Markdown  
✅ Send the report via email  
✅ Provide a Gradio UI for interactive use

---

## 🚀 Project Overview

This project demonstrates how to orchestrate multiple specialized agents to perform **deep research** on any topic. The system takes a user query, plans the best web searches, retrieves and summarizes information, composes a comprehensive report, and optionally emails the result.

The system supports:

- **Agent collaboration** (planner, search, writer, email)  
- Real-time progress updates  
- Fully asynchronous execution  
- Rich UI via Gradio for interactive research sessions

---

## 🗂️ Architecture

Here’s the overall flow:

1. **User Query** →  
2. **Planner Agent** → suggests relevant web searches  
3. **Search Agent** → performs web searches & summarizes results  
4. **Writer Agent** → synthesizes a detailed Markdown report  
5. **Email Agent** → optionally sends the report via Brevo SDK  
6. **Gradio UI** → enables user-friendly interaction and visualization

All agents run asynchronously via an agent runner (`Runner`) and support OpenAI’s native tracing for debugging and observability.

---

## 🤖 Agents

### Planner Agent

- **Purpose:** Generate 3 web search queries for the user’s topic  
- **Model:** gpt-4o-mini  
- **Output:** JSON plan describing search terms & reasoning

---

### Search Agent

- **Purpose:** Execute a single web search per query and summarize results concisely  
- **Model:** gpt-4o-mini  
- **Output:** Text summaries, ~2–3 paragraphs, < 300 words

---

### Writer Agent

- **Purpose:** Compose a cohesive Markdown report from collected search summaries  
- **Model:** gpt-4o-mini  
- **Output:**  
  - Detailed Markdown report (aim for 5-10 pages)  
  - Short summary  
  - Follow-up research questions

---

### Email Agent

- **Purpose:** Send the generated report via email using Brevo’s transactional email API  
- **Model:** gpt-4o-mini  
- **Output:** Confirmation of email delivery

---

## 🖥️ User Interfaces

### 1. CLI

Each agent can run standalone for testing or development:

```bash
# Run planner agent
python planner_agent.py

# Run search agent
python search_agent.py

# Run writer agent
python writer_agent.py

# Run email agent
python email_agent.py
```

### 2. Gradio UI

Launch the interactive Gradio app:

```bash
python deep_research.py
```

This will open a browser window where you can enter a research query and watch progress updates as the research runs.

---

## 🌍 OpenAI Tracing

Each research run logs a trace URL:

```
https://platform.openai.com/traces/trace?trace_id=<trace_id>
```

View traces for debugging or performance analysis.

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/openai-deep-research_agent.git
cd openai-deep-research_agent
```

### Install Python dependencies

It’s recommended to use a virtual environment (e.g. `venv` or `conda`):

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in your repo root with these values:

```dotenv
OPENAI_API_KEY=<your_openai_api_key>

# Email configuration for Brevo SDK
BREVO_API_KEY=<your_brevo_api_key>
SENDER_EMAIL=<your_sender_email>
RECEIVER_EMAIL=<your_receiver_email>
```

> ✅ **Note:** The Gradio app uses `load_dotenv` to automatically load these values.

---

## 💻 Usage

### Run Gradio UI

```bash
python deep_research.py
```

### Example CLI Run

Run the writer agent standalone:

```bash
python writer_agent.py
```

Run the full research pipeline via the Gradio UI:

```bash
python deep_research.py
```

---

## 🧪 Running Tests

This project uses `pytest` and `pytest-asyncio`.

Run all tests:

```bash
pytest
```

---

## 📚 Project Files

| File | Description |
| ---- | ----------- |
| `deep_research.py` | Gradio web UI to run the full research pipeline interactively |
| `planner_agent.py` | Generates search plans for user queries |
| `search_agent.py` | Performs web searches and summarizes content |
| `writer_agent.py` | Synthesizes search results into a detailed report |
| `email_agent.py` | Sends the generated report via Brevo email API |
| `research_manager.py` | Orchestrates all agents end-to-end |
| `requirements.txt` | Python dependencies |

---

## ✨ Example Research Report

Here’s an excerpt of the kind of output the system generates:

```markdown
# Research Report on Renewable Energy

## Introduction
Renewable energy sources are crucial for mitigating climate change...

## Key Findings
- Solar power: ...
- Wind power: ...

## Policy Implementations
- Germany's Energiewende...
- China's massive investments...

## Challenges
- Grid integration...
- Storage solutions...

## Conclusion
Renewable energy plays a pivotal role...
```

---

## 📜 License

This project is released under the MIT License.

---

## 🙌 Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

---

Enjoy exploring deep research with AI! 🌐