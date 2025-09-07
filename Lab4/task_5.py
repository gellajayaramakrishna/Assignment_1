import os, csv, subprocess
from pydriller import Repository

# Paths
REPO_FOLDER = "/Users/jayaram/Desktop/Lab4"
OUTPUT_CSV = "task_5.csv"
repos = ["black", "butterknife", "scikit-learn"]

def get_diff_stats(repo, commit, parent, algo):
    """Return added/removed line counts (no raw diff)"""
    result = subprocess.run(
        ["git", "-C", repo, "diff", parent, commit, f"--diff-algorithm={algo}", "-w", "--ignore-blank-lines"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    ).stdout

    added = sum(1 for line in result.splitlines() if line.startswith('+') and not line.startswith('+++'))
    removed = sum(1 for line in result.splitlines() if line.startswith('-') and not line.startswith('---'))
    return added, removed

# Open CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "repo", "old_path", "new_path", "commit_sha", "parent_sha",
        "commit_message", "add_myers", "rem_myers", "add_hist", "rem_hist", "discrepancy"
    ])

    # Process repos
    for repo_name in repos:
        repo_path = os.path.join(REPO_FOLDER, repo_name)
        print(f"Processing {repo_name}...")

        for commit in Repository(repo_path).traverse_commits():
            if not commit.parents:
                continue  # skip root commits (no parent)

            parent = commit.parents[0]
            for mod in commit.modified_files:
                old_path, new_path = mod.old_path or "", mod.new_path or ""

                # Get counts only
                add_myers, rem_myers = get_diff_stats(repo_path, commit.hash, parent, "myers")
                add_hist, rem_hist = get_diff_stats(repo_path, commit.hash, parent, "histogram")

                discrepancy = "Yes" if (add_myers != add_hist or rem_myers != rem_hist) else "No"

                # Write row
                writer.writerow([
                    repo_name,
                    old_path,
                    new_path,
                    commit.hash,
                    parent,
                    commit.msg.replace("\n", " ")[:100],  # truncate msg
                    add_myers, rem_myers, add_hist, rem_hist, discrepancy
                ])

print(f"✅ Slim CSV saved to {OUTPUT_CSV}")
