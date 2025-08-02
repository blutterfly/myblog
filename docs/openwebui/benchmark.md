# Benchmark

```bash
pip install gputil
```

Then run this performance benchmark script to gather CPU, RAM, and GPU info:

### ✅ Performance Benchmark Script (Python)

```python
import platform
import psutil
import GPUtil

def benchmark_system():
    print("🖥 CPU:", platform.processor())
    print("💾 RAM:", round(psutil.virtual_memory().total / (1024**3), 2), "GB")

    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f"\n🖼 GPU Name: {gpu.name}")
        print(f"📦 Total Memory: {round(gpu.memoryTotal / 1024, 2)} GB")
        print(f"📈 Used Memory: {round(gpu.memoryUsed / 1024, 2)} GB")
        print(f"🔧 Driver Version: {gpu.driver}")
        print(f"🧬 UUID: {gpu.uuid}")

benchmark_system()
```

---

## 🔍 RAG Demo Pipeline (Ollama + Chroma + LangChain)

Here’s a simplified RAG pipeline using **Ollama**, **Chroma**, and **LangChain**.

### 📁 Folder Structure

```
rag_demo/
├── app.py
├── docs/
│   └── sample.txt
└── requirements.txt
```

### 📦 requirements.txt

```txt
langchain
chromadb
unstructured
ollama
tqdm
```

### 🧠 app.py (RAG Pipeline)

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# 1. Load Document
loader = TextLoader("docs/sample.txt")
docs = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 3. Embed + Store
embedding = OllamaEmbeddings(model="nomic-embed-text")  # download via ollama
db = Chroma.from_documents(chunks, embedding)

# 4. Create QA Chain
retriever = db.as_retriever()
llm = Ollama(model="llama3:70b")  # or use "mistral:instruct"
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 5. Ask Questions
while True:
    q = input("🔍 Ask: ")
    if q.lower() in ["exit", "quit"]: break
    print("🧠 Answer:", qa_chain.run(q))
```

---

## 🦙 Ollama Model Setup

To prepare for this demo:

```bash
# Run Ollama server
ollama serve &

# Pull required models
ollama pull llama3:70b
ollama pull mistral:instruct
ollama pull nomic-embed-text
```

---

## 🚀 Final Notes

| Component | Model              | Notes                                            |
| --------- | ------------------ | ------------------------------------------------ |
| LLM       | `llama3:70b`       | Needs 64GB+ VRAM or will offload to CPU (slower) |
| LLM       | `mistral:instruct` | Lightweight, faster, great for QA                |
| Embedding | `nomic-embed-text` | Lightweight, accurate                            |
| DB        | `Chroma`           | Fast local vector store                          |

Would you like this RAG demo zipped and pre-filled with README and sample docs?

