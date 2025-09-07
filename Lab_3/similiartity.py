# lab3_full_analysis.py
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel
from nltk.translate.bleu_score import sentence_bleu

# ---------------- CONFIG ----------------
# Assuming Lab3 and Lab2 are in the same folder (Desktop)
input_csv = "/Users/jayaram/Desktop/Lab_2/diffs_rectified.csv"
output_csv = "diffs_metrics_final.csv"

# ---------------- LOAD CSV ----------------
df = pd.read_csv(input_csv).fillna("")

# ---------------- LOAD CODEBERT ----------------
print("Loading CodeBERT model...")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")
model.eval()

# ---------------- DEFINE SIMILARITY FUNCTIONS ----------------
def codebert_similarity(code1, code2):
    if not isinstance(code1, str) or not isinstance(code2, str) or len(code1.strip()) < 10 or len(code2.strip()) < 10:
        return np.nan
    try:
        inputs = tokenizer([code1, code2], return_tensors="pt", padding=True, truncation=True, max_length=256)
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        similarity = torch.nn.functional.cosine_similarity(embeddings[0], embeddings[1], dim=0)
        return similarity.item()
    except:
        return np.nan

def token_similarity(code1, code2):
    if not isinstance(code1, str) or not isinstance(code2, str):
        return np.nan
    try:
        return sentence_bleu([code1.split()], code2.split())
    except:
        return np.nan

# ---------------- COMPUTE SIMILARITIES ----------------
print("Computing Semantic Similarity...")
df['Semantic_similarity'] = df.apply(lambda row: codebert_similarity(row['Source Before'], row['Source After']), axis=1)

print("Computing Token Similarity...")
df['Token_similarity'] = df.apply(lambda row: token_similarity(row['Source Before'], row['Source After']), axis=1)

# ---------------- CLASSIFICATION ----------------
# Example thresholds, you can adjust
semantic_threshold = 0.80
token_threshold = 0.75

def classify_major_minor(sim, threshold):
    if pd.isna(sim):
        return "Unknown"
    return "Minor" if sim >= threshold else "Major"

df['Semantic_class'] = df['Semantic_similarity'].apply(lambda x: classify_major_minor(x, semantic_threshold))
df['Token_class'] = df['Token_similarity'].apply(lambda x: classify_major_minor(x, token_threshold))

# Agreement column
df['Classes_Agree'] = df.apply(
    lambda row: "YES" if row['Semantic_class'] == row['Token_class'] else "NO", axis=1
)

# ---------------- SAVE FINAL CSV ----------------
df.to_csv(output_csv, index=False)
print(f"✅ Analysis complete! Final CSV saved as {output_csv}")
