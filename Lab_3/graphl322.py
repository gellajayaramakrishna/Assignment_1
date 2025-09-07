# token_similarity_line.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV
df = pd.read_csv("diffs_metrics_final.csv")
token_scores = df["Token_similarity"].dropna()

# Set style
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

# Plot line graph (KDE for smoothness)
plt.figure(figsize=(8, 5))
sns.kdeplot(token_scores, color="green", linewidth=2, fill=True)

# Titles and labels
plt.title("Token Similarity Score Distribution", fontsize=16, weight="bold")
plt.xlabel("Token Similarity", fontsize=13)
plt.ylabel("Density", fontsize=13)

plt.tight_layout()
plt.savefig("token_similarity_line.png", dpi=300)
plt.show()
