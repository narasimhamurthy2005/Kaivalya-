from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import os
from googletrans import Translator
folder = "scraped_pages"
target_languages = ["te", "hi", "ta"] 
translator = Translator()
texts = []
for file in os.listdir(folder):
    if file.endswith('.txt'):
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            texts.append(f.read())
if not texts:
    print("No text files found! Check folder path.")
else:
    print(f"Found {len(texts)} text files.")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = []
for text in texts:
    chunks.extend(text_splitter.split_text(text))

print(f"Total English chunks: {len(chunks)}")
all_chunks = []  

for chunk in chunks:
    all_chunks.append(chunk)
    for lang in target_languages:
        try:
            translated_text = translator.translate(chunk, dest=lang).text
            all_chunks.append(translated_text)
        except Exception as e:
            print(f"Translation error for lang {lang}: {e}")

print(f"Total chunks including translations: {len(all_chunks)}")
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(all_chunks)
np.save('embeddings.npy', embeddings)
with open('chunks.npy', 'wb') as f:
    np.save(f, all_chunks)

print("✅ Embeddings and translated chunks saved.")
