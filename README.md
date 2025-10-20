# 🧘‍♂️ Kaivalya — Multilingual Health RAG Chatbot

**Kaivalya** is a local **Retrieval-Augmented Generation (RAG)** system integrated with **GPT4All Falcon**, designed to provide **multilingual health advice** (English, Hindi, Telugu, Tamil) via **text or voice** through a **Telegram bot interface**.  
It also features a **Nearby Hospitals Finder** that provides hospital details and Google Maps links.

---

## 📚 Project Overview

Kaivalya combines web-scraped medical knowledge with powerful AI models to offer health information that is accurate, multilingual, and easy to access.  
It retrieves relevant data from health websites like [heart.org](https://www.heart.org), processes it into embeddings using **FAISS** and **SentenceTransformers**, and responds intelligently using the **GPT4All Falcon** model — all running **locally without internet dependency**.

### 🧠 Core Features:
- 💬 **Text Chat:** Ask any health-related question.
- 🎤 **Voice Chat:** Speak your query (audio → text → response).
- 🏥 **Nearby Hospitals Finder:** Provides names, addresses, and Google Maps links.
- 🌐 **Multilingual Support:** English, Hindi, Telugu, Tamil.
- 🔒 **Local Execution:** Fully offline, no external API costs.

---

## 🧩 Tech Stack

| Category | Tools / Libraries |
|-----------|-------------------|
| **Programming Language** | Python 3.10+ |
| **Web Scraping** | `requests`, `BeautifulSoup4` |
| **Translation** | `googletrans`, `deep-translator` |
| **Text Processing** | `langchain.text_splitter` |
| **Embeddings** | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| **Vector Store** | `FAISS` |
| **Language Model (LLM)** | `GPT4All Falcon (gguf)` |
| **Audio Processing** | `speech_recognition`, `pydub`, `gtts` |
| **Chat Platform** | `python-telegram-bot` |

---

## 🗂️ Project Structure

kaivalya/
│
├── scraped_pages/ # Folder containing scraped text files
│
├── scrape_helpguide.py # Script to scrape data from medical websites
├── build_embeddings.py # Splits, translates, and embeds text data
├── rag_local.py # Local RAG model + GPT Falcon integration
├── bot.py # Telegram bot (text, audio, hospital search)
│
├── chunks.npy # Saved text chunks
├── embeddings.npy # Corresponding vector embeddings
│
├── models/
│ └── gpt4all-falcon-newbpe-q4_0.gguf # Local LLM model file
│
└── README.md # Project documentation (this file)

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/kaivalya.git
cd kaivalya
2️⃣ Install Required Packages
Create a requirements.txt file and paste the following:

txt
Copy code
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
Then install dependencies:

bash
Copy code
pip install -r requirements.txt
🧠 Data Preparation Workflow
Step 1: Scrape Health Data
bash
Copy code
python scrape_helpguide.py
This script scrapes content from medical websites (e.g., heart.org) and saves the data in scraped_pages/.

Step 2: Build Embeddings
bash
Copy code
python build_embeddings.py
This script:

Splits text into small chunks (≈500 characters)

Translates them into Hindi, Telugu, and Tamil

Generates embeddings using SentenceTransformer

Saves the results as chunks.npy and embeddings.npy

Step 3: Launch the Local RAG Chatbot
bash
Copy code
python rag_local.py
Now you can chat locally:

makefile
Copy code
You: What are symptoms of a heart attack in Hindi?
Bot: हार्ट अटैक के लक्षणों में सीने में दर्द, सांस की कमी, और थकान शामिल हैं।
Step 4: Run the Telegram Bot
bash
Copy code
python bot.py
Open your Telegram bot (created via BotFather) and interact with Kaivalya.

💬 How to Interact via Telegram
Commands:

/start → Opens the main menu.

Symptoms → Advice → Choose between text or voice input.

Nearby Hospitals → Get a list of hospitals with maps.

Example:

makefile
Copy code
You: What are the symptoms of a heart attack in Hindi?
Bot: हार्ट अटैक के लक्षणों में सीने में दर्द, सांस की कमी, और थकान शामिल हैं।
🏥 Hospital Finder
When you share your location or select “Nearby Hospitals,” Kaivalya shows hospitals in your area:

Example Output:

less
Copy code
🏥 SLG Hospitals  
📍 Nizampet, Hyderabad, Telangana  
🔗 [Google Maps Link](https://share.google/AVfA5qL29nL6DQkhY)
🌐 Multilingual Support
Kaivalya can understand and respond in:

🇮🇳 English

🇮🇳 Hindi

🇮🇳 Telugu

🇮🇳 Tamil

It auto-detects the language of your question and responds in the same language.

🧠 Model Used
Model: GPT4All Falcon (gpt4all-falcon-newbpe-q4_0.gguf)
Mode: Local LLM Execution (no external API)
Embeddings: all-MiniLM-L6-v2
Vector Search: FAISS Index

🧭 Future Enhancements
🔹 Integrate dynamic hospital detection via Google Maps API

🔹 Add disease prediction from user symptoms

🔹 Include nutrition, yoga, and exercise modules

🔹 Build a web and Android interface

👨‍💻 Author
Project Name: Kaivalya
Developer: Murthy K
Model Used: GPT4All Falcon
Goal: To make multilingual AI-powered health awareness accessible to everyone, locally and privately.

⚠️ Disclaimer
Kaivalya is not a medical professional.
The information provided is for educational and awareness purposes only.
Always consult a certified doctor for medical advice.
