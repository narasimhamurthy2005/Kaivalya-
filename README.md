# 🧘‍♂️ Kaivalya — Multilingual Health RAG Chatbot

**Kaivalya** is a local **Retrieval-Augmented Generation (RAG)** system integrated with **GPT4All Falcon**, capable of providing multilingual (English, Hindi, Telugu, Tamil) health advice through **text or voice** via a **Telegram bot interface**.  
It also provides a feature to show **nearby hospitals** with Google Maps links.

---

## 📚 Project Overview

Kaivalya intelligently retrieves health-related information from scraped medical websites (like [heart.org](https://www.heart.org)) and uses **FAISS vector search** with **SentenceTransformer embeddings** to generate accurate, context-aware responses.

The bot supports:
- 💬 **Text chat** (Ask health-related questions)
- 🎤 **Voice chat** (Audio to text → RAG → speech response)
- 🏥 **Nearby hospital finder**
- 🌐 **Multilingual support:** English, Hindi, Telugu, Tamil

---

## 🧩 Tech Stack

| Category | Tools / Libraries |
|-----------|-------------------|
| **Language** | Python 3.10+ |
| **Web Scraping** | `requests`, `BeautifulSoup4` |
| **Translation** | `googletrans`, `deep-translator` |
| **Text Processing** | `langchain.text_splitter` |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Vector Store** | `FAISS` |
| **LLM** | `GPT4All Falcon (gguf)` |
| **Audio Processing** | `speech_recognition`, `pydub`, `gtts` |
| **Telegram Bot** | `python-telegram-bot` |

---

## 🗂️ Project Structure
