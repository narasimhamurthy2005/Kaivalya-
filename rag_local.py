import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from gpt4all import GPT4All
from deep_translator import GoogleTranslator
embedder = SentenceTransformer("all-MiniLM-L6-v2")
chunks = np.load("chunks.npy", allow_pickle=True)
embeddings = np.load("embeddings.npy")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

print(f"✅ FAISS index loaded with {len(chunks)} chunks")
model_filename = "gpt4all-falcon-newbpe-q4_0.gguf"
model_path = os.path.join(os.getcwd(), "models")
llm = GPT4All(model_filename, model_path=model_path)
def rag_query(query, top_k=3, distance_threshold=1.0):
    """
    Query RAG system and generate answer in the explicitly requested language
    at the end of the query: English, Hindi, or Telugu.
    """
    lang_map = {
        "english": "en",
        "telugu": "te",
        "hindi": "hi"
    }
    requested_lang = "en"
    lower_query = query.lower()
    for lang_name in lang_map:
        if lower_query.endswith(f"in {lang_name}"):
            requested_lang = lang_map[lang_name]
            query = query[:-(len(f"in {lang_name}"))].strip()
            break
    query_vector = embedder.encode([query])
    distances, indices = index.search(query_vector, top_k)
    if distances[0][0] > distance_threshold:
        response_text = "🤖 I'm sorry, I don't have information on that topic."
    else:
        retrieved_chunks = [chunks[i][:500] for i in indices[0]] 
        context = "\n".join(retrieved_chunks)
        prompt = f"""You are a helpful assistant.
Use the following context to answer briefly and clearly:

Context:
{context}

Question: {query}
Answer:"""
        with llm.chat_session():
            response_text = llm.generate(prompt, max_tokens=150)
    if requested_lang != "en":
        response_text = GoogleTranslator(source="en", target=requested_lang).translate(response_text)

    return response_text
if __name__ == "__main__":
    print("🤖 RAG Chatbot is ready! Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        answer = rag_query(query)
        print("Bot:", answer, "\n")
