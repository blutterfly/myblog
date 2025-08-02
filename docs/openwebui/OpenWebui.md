---
title: Open WebUI
---
# Open WebUI

This will be the front-end of LarGpt.


---

## 🔍 What is Open WebUI?

**Open WebUI** is a **self-hosted, open-source web-based user interface** for interacting with local large language models (LLMs) such as those served by [**Ollama**](https://ollama.com/). It aims to be a **ChatGPT-style interface** that’s fast, responsive, and extensible.

It supports multiple backends (e.g., Ollama, LM Studio, and others), and includes features like chat history, markdown rendering, file attachments, user management, and integration hooks—making it ideal for LLM workflows like **RAG (Retrieval-Augmented Generation)**.

---

## 🧑‍💻 Key Features (Developer-Centric)

| Feature                                   | Description                                                                                                                                                     |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🌐 **Web-based Interface**                | Built with React + TypeScript (frontend), and FastAPI + Python (backend).                                                                                       |
| 🔌 **Pluggable LLM Backend**              | Works out of the box with **Ollama**, **LM Studio**, **OpenAI API**, and can be extended to support custom models.                                              |
| 🗂 **Chat Storage**                       | Uses SQLite or PostgreSQL to store chats, configurations, and user data.                                                                                        |
| 🧵 **Multi-Session Chat**                 | Each session can target a different model with custom context. Useful for multi-user environments.                                                              |
| 🛠 **File Upload + Contextual Prompting** | Upload files (PDF, TXT, Markdown) and chat with them using built-in RAG functionality.                                                                          |
| 🧩 **Embeddings + Vector DB**             | Comes with **integrated RAG** capabilities using **local embeddings and vector store (Chroma)**. Can be swapped out with others like **FAISS** or **Weaviate**. |
| 🔐 **User Authentication**                | Support for **multi-user**, JWT-based login, and admin roles.                                                                                                   |
| 💾 **Model Download UI**                  | If using Ollama, you can pull models (like llama3, mistral, codellama) directly from the web interface.                                                         |
| 🧠 **System Prompts + Memory**            | Set persistent instructions for the assistant and control conversation memory behavior.                                                                         |
| 💡 **Plugin System**                      | (Coming soon or community-driven) Allows developers to extend capabilities using plugins.                                                                       |
| 📤 **API**                                | Offers an HTTP API to send/receive messages programmatically (great for testing, automation, and integrations).                                                 |

---

## 🧱 Architecture

### 🖥 Frontend

* **React + TypeScript**
* Supports light/dark themes
* Connects to backend via REST/WebSockets
* Responsive UI inspired by ChatGPT

### 🖧 Backend

* **Python + FastAPI**
* Handles:

  * Model integration
  * File management
  * User auth and sessions
  * Database interactions
  * Embedding + RAG
  * Chat memory

---

## 🧠 Using with Ollama

Yes, it **works natively with Ollama**:

### ✅ Ollama Integration

* Autodetects Ollama running locally at `http://localhost:11434`
* Automatically lists models from Ollama (`ollama list`)
* Supports:

  * Streaming responses
  * System prompt customization
  * Multi-turn conversation context
  * Model downloading via UI (e.g., `llama3`, `mistral`, `codellama`, `phi`)

> **Tip:** If you want to use Open WebUI with multiple models (e.g., `llama3` and `mistral`), you can launch different sessions and pick the model per session.

---

## 📚 RAG Workflow in Open WebUI

Open WebUI provides a **basic built-in RAG system**:

### 🔄 How it Works

1. Upload a document (PDF, text, CSV, etc.)
2. The backend:

   * Splits text into chunks
   * Embeds them using a local model (e.g., `all-MiniLM-L6-v2`)
   * Stores them in **Chroma** (default vector DB)
3. You can now **chat with your documents**, and it retrieves relevant chunks to feed into the prompt.

### ⚙️ Can I Customize?

Yes:

* You can change:

  * Embedding model
  * Vector database backend
  * Chunking strategy
* You can **write your own RAG pipeline** and register it using the plugin system or directly patch the backend.

---

## 🔄 Deployment Options

| Method                | Notes                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 🐳 **Docker Compose** | Easiest and most popular. Comes with prebuilt images.                                                                |
| 🧱 **Manual Install** | Clone GitHub repo, install Python deps (`pip install -r requirements.txt`), run FastAPI + React frontend separately. |
| ☁️ **Cloud Hosting**  | Host on your own server, VPS, or even internal LAN.                                                                  |

---

## 🛠 Example: Local Dev Setup with Ollama + Open WebUI

```bash
# 1. Start Ollama
ollama serve &

# 2. Clone Open WebUI
git clone https://github.com/open-webui/open-webui
cd open-webui

# 3. Build & Start
docker compose up -d --build
```

Then access:
👉 `http://localhost:3000`

---

## 🧩 Extendability Ideas for You

As a dev, you can:

* Add **custom RAG routes** using your existing PDFs or DBs
* Build **plugin hooks** to integrate knowledge bases, SQL, or API calls
* Set up **multi-tenant access** if you're offering AI tools to a group or team
* Embed WebUI inside another app using iframe or browser wrapper (e.g., Tauri)

---

## 🛠 GitHub

* **Repo**: [https://github.com/open-webui/open-webui](https://github.com/open-webui/open-webui)
* **Docs**: Available in repo
* **License**: MIT

---

## ✅ Summary: Should You Use It?

| Use Case                            | Suitability                                     |
| ----------------------------------- | ----------------------------------------------- |
| As a front-end for Ollama           | ✅ Native support                                |
| For RAG on PDFs or Markdown         | ✅ Works out of the box                          |
| For API-powered automation          | ✅ Via REST API                                  |
| For multiple users & chat history   | ✅ Supported                                     |
| For advanced RAG pipelines with DBs | ⚠️ Needs customization                          |
| For production apps                 | ✅ Self-hosted, performant                       |
| For Streamlit-style dashboards      | ❌ Use a separate front-end or iframe Open WebUI |

---

Would you like a script to **preload a document collection** into Open WebUI’s vector store, or modify it to point to your own DuckDB or knowledge base for advanced RAG?