import csv
import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from tqdm import tqdm

# Increase CSV field size limit
csv.field_size_limit(sys.maxsize)

# ---- CONFIG ----
diff_csv = '/Users/jayaram/Desktop/Lab_2/diffs_full.csv'
output_csv = '/Users/jayaram/Desktop/Lab_2/diffs_rectified.csv'
model_name = "mamiksik/CommitPredictorT5"
MAX_DIFF_LINES = 50
GENERIC_MESSAGES = ['fix bug', 'bug fix', 'update', 'change', 'modify']

# ---- STEP 1: Load pre-trained model ----
print("Loading CommitPredictorT5 model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# ---- STEP 2: Read diffs CSV ----
with open(diff_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    diffs = [row for row in reader]

# ---- STEP 3: Open output CSV ----
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
        'Hash', 'Message', 'Filename',
        'Source Before', 'Source After',
        'Diff', 'LLM Inference', 'Rectified Message'
    ])

    # ---- STEP 4: Process diffs ----
    for row in tqdm(diffs, desc="Processing diffs"):
        diff_lines = row['Diff'].splitlines() if row['Diff'] else []
        input_text = '\n'.join(diff_lines[:MAX_DIFF_LINES]) if diff_lines else row['Source After']

        # Generate LLM message
        try:
            inputs = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=512)
            outputs = model.generate(inputs, max_length=64)
            llm_message = tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception:
            llm_message = row['Message']

        original_msg = row['Message'].lower().strip()
        if any(g in original_msg for g in GENERIC_MESSAGES) or not original_msg:
            rectified_message = f"{llm_message} in {row['Filename']}"
        else:
            rectified_message = row['Message']

        writer.writerow([
            row['Hash'],
            row['Message'],
            row['Filename'],
            row['Source Before'],
            row['Source After'],
            row['Diff'],
            llm_message,
            rectified_message
        ])

print(f"✅ LLM inference + smart rectifier completed. Check '{output_csv}'")
