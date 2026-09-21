import json
import os
import random
import urllib.request

ASQ_PHI_RAW_URL = "https://raw.githubusercontent.com/JamesWeatherhead/asq-phi/main/data/synthetic_clinical_queries.txt"
RAW_FILE_PATH = "data/raw/synthetic_clinical_queries.txt"

HIPAA_MAPPING = {
    "NAME": "NAME",
    "PATIENT": "NAME",
    "DOCTOR": "NAME",
    "GEOGRAPHIC_LOCATION": "LOCATION",
    "LOCATION": "LOCATION",
    "HOSPITAL": "LOCATION",
    "DATE": "DATE",
    "AGE": "AGE",
    "PHONE_NUMBER": "CONTACT",
    "EMAIL_ADDRESS": "CONTACT",
    "MEDICAL_RECORD_NUMBER": "IDENTIFIER",
    "HEALTH_PLAN_BENEFICIARY_NUMBER": "IDENTIFIER",
    "SOCIAL_SECURITY_NUMBER": "IDENTIFIER"
}

def download_asq_phi():
    os.makedirs("data/raw", exist_ok=True)
    if not os.path.exists(RAW_FILE_PATH):
        print(f"Downloading raw ASQ-PHI benchmark from GitHub...")
        urllib.request.urlretrieve(ASQ_PHI_RAW_URL, RAW_FILE_PATH)
        print("Download complete.")
    else:
        print("Raw ASQ-PHI benchmark already present locally.")

def parse_asq_phi_file():
    records = []
    with open(RAW_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.split("===QUERY===")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        parts = block.split("===PHI_TAGS===")
        query_text = parts[0].strip()
        
        phi_elements = []
        if len(parts) > 1:
            tag_lines = parts[1].strip().split("\n")
            for line in tag_lines:
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        tag_obj = json.loads(line)
                        raw_type = tag_obj.get("identifier_type", "OTHER_PHI")
                        cleaned_cat = HIPAA_MAPPING.get(raw_type.upper(), "OTHER_PHI")
                        phi_elements.append({
                            "category": cleaned_cat,
                            "value": tag_obj.get("value", "")
                        })
                    except json.JSONDecodeError:
                        continue
        
        records.append({
            "instruction": "Extract all Protected Health Information (PHI) under HIPAA Safe Harbor regulations.",
            "input": query_text,
            "has_phi": len(phi_elements) > 0,
            "output": json.dumps(phi_elements)
        })
    return records

def process_and_partition():
    download_asq_phi()
    records = parse_asq_phi_file()
    print(f"Successfully parsed {len(records)} clinical queries.")
    
    # 70% Train, 15% Validation, 15% Test
    random.seed(42)
    random.shuffle(records)
    
    n_total = len(records)
    train_end = int(n_total * 0.70)
    val_end = int(n_total * 0.85)
    
    splits = {
        "train": records[:train_end],
        "val": records[train_end:val_end],
        "test": records[val_end:]
    }
    
    os.makedirs("data/processed", exist_ok=True)
    for split_name, subset in splits.items():
        out_path = f"data/processed/{split_name}.jsonl"
        with open(out_path, "w", encoding="utf-8") as f:
            for row in subset:
                f.write(json.dumps(row) + "\n")
        phi_pos = sum(1 for r in subset if r["has_phi"])
        print(f"  * {split_name.upper()} split -> {len(subset)} queries ({phi_pos} PHI-positive, {len(subset)-phi_pos} hard negatives) saved to {out_path}")

if __name__ == "__main__":
    process_and_partition()