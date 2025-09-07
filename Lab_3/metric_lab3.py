# metrics.py - Step 2: Structural Metrics (quiet & warning-free)
import pandas as pd
from radon.metrics import mi_visit
from radon.complexity import cc_visit
import warnings

# Suppress all warnings (including SyntaxWarnings)
warnings.filterwarnings("ignore")

# Load CSV
df = pd.read_csv("/Users/jayaram/Desktop/Lab_2/diffs_rectified.csv").fillna("")
df.columns = [c.strip() for c in df.columns]

# Initialize metric columns
for col in ['MI_Before','MI_After','CC_Before','CC_After','LOC_Before','LOC_After','MI_Change','CC_Change','LOC_Change']:
    df[col] = 0

# Compute metrics
for idx, row in df.iterrows():
    code_before = row['Source Before'] if isinstance(row['Source Before'], str) else ''
    code_after = row['Source After'] if isinstance(row['Source After'], str) else ''
    
    # MI
    try: df.at[idx,'MI_Before'] = mi_visit(code_before, True)
    except: df.at[idx,'MI_Before'] = 0
    try: df.at[idx,'MI_After'] = mi_visit(code_after, True)
    except: df.at[idx,'MI_After'] = 0

    # CC
    try: df.at[idx,'CC_Before'] = sum([f.complexity for f in cc_visit(code_before)])
    except: df.at[idx,'CC_Before'] = 0
    try: df.at[idx,'CC_After'] = sum([f.complexity for f in cc_visit(code_after)])
    except: df.at[idx,'CC_After'] = 0

    # LOC
    df.at[idx,'LOC_Before'] = len(code_before.splitlines())
    df.at[idx,'LOC_After'] = len(code_after.splitlines())

    # Changes
    df.at[idx,'MI_Change'] = df.at[idx,'MI_After'] - df.at[idx,'MI_Before']
    df.at[idx,'CC_Change'] = df.at[idx,'CC_After'] - df.at[idx,'CC_Before']
    df.at[idx,'LOC_Change'] = df.at[idx,'LOC_After'] - df.at[idx,'LOC_Before']

# Save CSV
df.to_csv("/Users/jayaram/Desktop/Lab_3/diffs_metrom.csv", index=False)
print("Structural metrics computed and saved to diffs_metrics.csv")
