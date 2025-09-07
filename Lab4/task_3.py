import csv

INPUT_CSV = "task_5.csv"
OUTPUT_CSV = "diff__discrepancy.csv"

with open(INPUT_CSV, "r", encoding="utf-8") as infile, \
     open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames  
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in reader:
        add_myers = int(row["add_myers"])
        rem_myers = int(row["rem_myers"])
        add_hist = int(row["add_hist"])
        rem_hist = int(row["rem_hist"])
        
        row["discrepancy"] = "Yes" if (add_myers != add_hist or rem_myers != rem_hist) else "No"
        
        writer.writerow(row)

print(f"Discrepancy CSV saved as {OUTPUT_CSV}")
