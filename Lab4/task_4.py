import pandas as pd
import matplotlib.pyplot as plt

csv_path = "task_5.csv"
df = pd.read_csv(csv_path)

def get_file_type(path):
    if not isinstance(path, str):
        return "Other files"
    path = path.lower()
    if path.endswith(".py") or "src" in path:
        return "Source Code files"
    elif "test" in path:
        return "Test Code files"
    elif "readme" in path:
        return "README files"
    elif "license" in path:
        return "LICENSE files"
    else:
        return "Other files"

df['file_type'] = df['new_path'].fillna(df['old_path']).apply(get_file_type)

df['mismatches'] = df['discrepancy'].apply(lambda x: 1 if str(x).strip().lower() == "yes" else 0)
df['matches'] = df['discrepancy'].apply(lambda x: 1 if str(x).strip().lower() == "no" else 0)

summary = df.groupby('file_type').agg(
    matches=('matches', 'sum'),
    mismatches=('mismatches', 'sum')
).reset_index()
summary['total'] = summary['matches'] + summary['mismatches']
summary['mismatch_rate'] = (summary['mismatches'] / summary['total']) * 100

plt.style.use('ggplot')

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Discrepancy Analysis by File Type", fontsize=16, fontweight='bold')

axes[0,0].bar(summary['file_type'], summary['mismatches'], color='tomato')
for i, v in enumerate(summary['mismatches']):
    axes[0,0].text(i, v+0.5, str(v), ha='center', fontweight='bold')
axes[0,0].set_title("Number of Mismatches by File Type")
axes[0,0].set_ylabel("Mismatches")

axes[0,1].bar(summary['file_type'], summary['mismatch_rate'], color='skyblue')
for i, v in enumerate(summary['mismatch_rate']):
    axes[0,1].text(i, v+0.5, f"{v:.1f}%", ha='center', fontweight='bold')
axes[0,1].set_title("Mismatch Rate by File Type")
axes[0,1].set_ylabel("Mismatch Rate (%)")

for idx, row in summary.iterrows():
    sizes = [row['matches'], row['mismatches']]
    labels = ['Matches', 'Mismatches']
    colors = ['#90ee90', '#ff6f69']
    ax = axes[1, idx] if idx < 2 else axes[1, 1]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    ax.set_title(f"{row['file_type']}")

plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()
