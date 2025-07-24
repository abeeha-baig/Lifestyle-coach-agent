# Lifestyle-coach-agent

**Lifestyle Agent** is a smart AI assistant that scrapes lifestyle-related webpages and provides concise, human-readable summaries using GPT-4o-mini. It’s built for content curators, digital wellness bloggers, lifestyle researchers, and anyone who wants distilled insights from cluttered online content — fast.

---

## 🌟 Features

* 🔗 **Web Content Extraction**: Scrapes content from reliable URL using Firecrawl API.
* 🧠 **Intelligent Summarization**: Uses OpenAI’s `gpt-4o-mini` to generate context-aware summaries.
* 🧩 **Modular LangChain Workflow**: Easily expandable reasoning chain for prompt injection and summarization logic.
* 🔐 **Secure API Handling**: Uses Streamlit secrets for API key storage (no `.env` needed).
* 🖥️ **Streamlit UI**: Clean, minimal front-end for quick URL input and summary viewing.

---

## 🗂️ Project Structure

```
lifestyle-agent/
│
├── .streamlit/
│   └── secrets.toml              # 🔐 Stores API keys for OpenAI and Firecrawl
│
├── app/
│   ├── __init__.py
│   ├── firecrawl.py              # 🔥 Web scraping from Firecrawl API
│   ├── tools.py                  # 🧰 Utility functions
│   ├── prompt.py                 # ✍️ Prompt templates for summarization
│   └── workflow.py               # 🧠 LangChain summarization pipeline
│
├── main.py                       # 🚀 Streamlit front-end entry point
├── requirements.txt              # 📦 Project dependencies
└── README.md                     # 📘 Project description (this file)
```

---

## ⚙️ How It Works

1. **User submits a URL** in the Streamlit app.
2. 🔥 **Firecrawl** scrapes and returns structured page content.
3. 🤖 **LangChain + GPT-4o-mini** processes the content using a carefully designed prompt.
4. 📝 A clean summary appears instantly in the app.

---

## 🔐 Secrets Configuration

Use `secrets.toml` inside `.streamlit/` to store API keys:

```toml
OPENAI_API_KEY = "sk-..."
FIRECRAWL_API_KEY = "fc-..."
```

No `.env` file is required — Streamlit handles everything internally!

---

## 📦 Requirements

Make sure to install dependencies:

```bash
pip install -r requirements.txt
```

Key packages:

* `streamlit`
* `openai`
* `langchain`
* `langchain_openai`
* `requests`
* `tiktoken`

---

## 🛤️ Future Plans

* PDF export of summaries
* Multiple URL summarization
* Lifestyle-specific prompt tuning
* Integration with Notion or Google Docs
* Text-to-speech summary readout