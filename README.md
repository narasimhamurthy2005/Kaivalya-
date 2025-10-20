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

kaivalya/<br><br>
│<br>
├── scraped_pages/ # Folder containing scraped text files<br>
│<br>
├── scrape_helpguide.py # Scrapes data from medical websites<br>
├── build_embeddings.py # Splits, translates, and embeds text data<br>
├── rag_local.py # Local RAG model + GPT Falcon integration<br>
├── bot.py # Telegram bot (text/audio/location)<br>
│<br>
├── chunks.npy # Saved text chunks<br>
├── embeddings.npy # Corresponding vector embeddings<br>
│<br>
├── models/<br>
│ └── gpt4all-falcon-newbpe-q4_0.gguf # Local LLM model<br>
│<br>
└── README.md # Project documentation (this file)<br>
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/<your-username>/kaivalya.git<br>
cd kaivalya
---
### 2️⃣ Install Required Packages

pip install -r requirements.txt
requests
beautifulsoup4
langchain
sentence-transformers
numpy
faiss-cpu
gpt4all
googletrans==4.0.0-rc1
deep-translator
speechrecognition
pydub
gtts
python-telegram-bot==20.3

---
## Data Preparation Workflow

### Step 1: Scrape Health Data

python scrape_helpguide.py

### Step 2: Build Embeddings

python build_embeddings.py

### Step 3: Launch Local RAG Chatbot

python rag_local.py

### Step 4: Run Telegram Bot

python bot.py

## Interact via Telegram:

1. /start → Open main menu

2. “Symptoms → Advice” → Choose text/audio

3. “Nearby Hospitals” → Get hospital info

### EX:You: What are the symptoms of a heart attack in Hindi
Bot: हार्ट अटैक के लक्षणों में सीने में दर्द, सांस की कमी, और थकान शामिल हैं।

## Hospital Finder:
When you share your location or select “Nearby Hospitals,” Kaivalya shows hospitals with:

🏥 Name<br>
📍 Address<br>
🔗 Google Maps link<br>

Example:
🏥 SLG Hospitals  
📍 Nizampet, Hyderabad, Telangana  
🔗 [Google Maps Link](https://share.google/AVfA5qL29nL6DQkhY)

## Multilingual Support:

Kaivalya understands and responds in:

🇮🇳 English

🇮🇳 Hindi

🇮🇳 Telugu

🇮🇳 Tamil

## Model Used:

GPT4All Falcon (gpt4all-falcon-newbpe-q4_0.gguf)
