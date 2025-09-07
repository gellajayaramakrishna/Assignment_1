# semantic_similarity_bar.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load CSV
df = pd.read_csv("diffs_metrics_final.csv")
semantic_scores = df["Semantic_similarity"].dropna()

# Define bins for grouping similarity scores
bins = np.arange(0, 1.05, 0.1)  # Bins of width 0.1
labels = [f"{round(b,1)}-{round(b+0.1,1)}" for b in bins[:-1]]

# Categorize scores into bins
binned = pd.cut(semantic_scores, bins=bins, labels=labels, include_lowest=True)
count_data = binned.value_counts().sort_index()

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(x=count_data.index, y=count_data.values, palette="Blues_d")

# Titles and labels
plt.title("Semantic Similarity Score Distribution", fontsize=18, weight="bold")
plt.xlabel("Semantic Similarity Range", fontsize=14)
plt.ylabel("Number of Commits", fontsize=14)

# Add values on top of bars
for i, val in enumerate(count_data.values):
    plt.text(i, val + 5, str(val), ha='center', fontsize=12)

plt.tight_layout()
plt.savefig("semantic_similarity_bar.png", dpi=300)
plt.show()
