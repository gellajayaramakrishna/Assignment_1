from pydriller import Repository
import csv

repo_path = '/Users/jayaram/Desktop/Lab_2/blackmagic'

bug_keywords = [
    'fix', 'bug', 'error', 'issue', 'patch', 'resolve', 'crash', 'fail',
    'regression', 'correct', 'hotfix', 'defect', 'repair', 'broken',
    'fault', 'mistake', 'problem', 'glitch', 'oops', 'debug', 'adjust',
    'address', 'handle', 'bypass', 'workaround', 'prevent', 'cleanup',
    'security', 'vulnerability', 'failure', 'hang', 'leak', 'incorrect'
]

with open('bug_fix_commits.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Hash', 'Message', 'Parent Hashes', 'Is Merge?', 'Modified Files'])

    for commit in Repository(repo_path).traverse_commits():
        # Only process bug-fix commits that are not merge commits
        if any(k in commit.msg.lower() for k in bug_keywords) and not commit.merge:
            # Safely get filenames
            modified_files = []
            if commit.modified_files:
                modified_files = [mod.new_path or mod.old_path or '' for mod in commit.modified_files]
            
            writer.writerow([commit.hash, commit.msg, commit.parents, commit.merge, modified_files])

print("Bug-fixing commits saved to 'bug_fix_commits.csv'")
