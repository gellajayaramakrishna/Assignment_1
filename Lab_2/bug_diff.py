from pydriller import Repository
import csv

repo_path = '/Users/jayaram/Desktop/Lab_2/blackmagic'
bug_csv = 'bug_fix_commits.csv'
diff_csv = 'diffs_full.csv'

bug_fix_commits = []
with open(bug_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    reader.fieldnames = [name.strip() for name in reader.fieldnames]
    for row in reader:
        clean_row = {k.strip(): v for k, v in row.items()}
        bug_fix_commits.append(clean_row)

with open(diff_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Hash', 'Message', 'Filename', 
        'Source Before', 'Source After', 
        'Diff', 'LLM Inference', 'Rectified Message'
    ])
    repo = Repository(repo_path)
    count = 0

    for commit in repo.traverse_commits():
        if any(commit.hash == b['Hash'] for b in bug_fix_commits):
            for mod in commit.modified_files:
                try:
                    src_before = mod.source_code_before if mod.source_code_before else ""
                except Exception:
                    src_before = ""
                try:
                    src_after = mod.source_code if mod.source_code else ""
                except Exception:
                    src_after = ""
                try:
                    diff = mod.diff if mod.diff else ""
                except Exception:
                    diff = ""

                writer.writerow([
                    commit.hash,
                    commit.msg,
                    mod.filename,
                    src_before,
                    src_after,
                    diff,
                    "",  
                    ""   
                ])
                count += 1
print(f"Output saved in '{diff_csv}'.")
