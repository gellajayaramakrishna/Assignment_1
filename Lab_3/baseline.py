import pandas as pd

# === Load your Lab 2 dataset ===
csv_file = "/Users/jayaram/Desktop/Lab_2/diffs_rectified.csv"  # Make sure this is in the same folder
df = pd.read_csv(csv_file)

# === Dataset preview ===
print("Dataset Preview")
print(df.head(), "\n")

# === Total commits and files ===
total_commits = df['Hash'].nunique()  # unique commit IDs
total_files = len(df)  # each row is a file change
avg_files_per_commit = total_files / total_commits

# === Total unique files ===
unique_files = df['Filename'].nunique()

# === Top Fix Types ===
if 'LLM Inference' in df.columns:
    top_fix_types = df['LLM Inference'].value_counts().head(10)
else:
    top_fix_types = pd.Series([], dtype="int64")

# === Top Modified Files ===
top_files = df['Filename'].value_counts().head(10)

# === Most common file extensions ===
df['Extension'] = df['Filename'].apply(lambda x: x.split('.')[-1] if '.' in str(x) else 'no_ext')
ext_counts = df['Extension'].value_counts()

# === Print results ===
print(f"Total Bug-Fixing Commits: {total_commits}")
print(f"Total Modified Files: {total_files}")
print(f"Total Unique Files: {unique_files}")
print(f"Average Modified Files per Commit: {avg_files_per_commit:.2f}\n")

print("Top 10 Fix Types")
print(top_fix_types, "\n")

print("Top 10 Modified Files")
print(top_files, "\n")

print("Most Modified File Extensions")
print(ext_counts, "\n")

# === Save results to a text file ===
with open("baseline_summary.txt", "w") as f:
    f.write(f"Total Bug-Fixing Commits: {total_commits}\n")
    f.write(f"Total Modified Files: {total_files}\n")
    f.write(f"Total Unique Files: {unique_files}\n")
    f.write(f"Average Modified Files per Commit: {avg_files_per_commit:.2f}\n\n")

    f.write("Top 10 Fix Types\n")
    f.write(top_fix_types.to_string() if not top_fix_types.empty else "No Fix Type column found\n")
    f.write("\n\nTop 10 Modified Files\n")
    f.write(top_files.to_string())
    f.write("\n\nMost Modified File Extensions\n")
    f.write(ext_counts.to_string())

print("✅ Summary saved to baseline_summary.txt")
