import os
from sentence_transformers import SentenceTransformer, util
import torch, pickle

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_documents(base_path):
    documents = []

    for folder in ["hackerrank", "claude", "visa"]:
        folder_path = os.path.join(base_path, folder)

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                        chunks = text.split("\n\n")[:5]
                        documents.extend(chunks)

                except:
                    continue
    print(f"Loaded {len(documents)} chunks")
    return documents

def build_embeddings(documents):
    if os.path.exists("embeddings.pkl"):
        print("Loading cached embeddings...")
        with open("embeddings.pkl", "rb") as f:
            return pickle.load(f)

    print("Building embeddings (first time only)...")
    embeddings = model.encode(documents, convert_to_tensor=True)

    with open("embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

    return embeddings


def retrieve(query, documents, doc_embeddings):
    query_embedding = model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    top_k = 5
    top_results = torch.topk(scores, k=top_k)

    best_idx = top_results.indices[0].item()
    best_score = top_results.values[0].item()

    if best_score < 0.52:
        return "", best_score

    return documents[best_idx][:300], best_score