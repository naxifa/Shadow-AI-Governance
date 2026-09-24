import json
import os
import random
import urllib.request

# ==============================================================================
# CONFIGURATION & HIPAA SAFE HARBOR NORMALIZATION
# ==============================================================================

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"

CANDIDATE_RAW_FILES = [
    os.path.join(RAW_DIR, "synthetic_clinical_queries.txt"),
    os.path.join(RAW_DIR, "asq_phi.jsonl"),
    os.path.join(RAW_DIR, "asq_phi.json"),
    "data/synthetic_clinical_queries.txt",
    "data/asq_phi.jsonl"
]

# Standardize 18 HIPAA Safe Harbor entity types into core classification categories
HIPAA_MAPPING = {
    "NAME": "NAME",
    "PATIENT": "NAME",
    "DOCTOR": "NAME",
    "PHYSICIAN": "NAME",
    "HEALTHCARE_PROVIDER": "NAME",
    "GEOGRAPHIC_LOCATION": "LOCATION",
    "LOCATION": "LOCATION",
    "HOSPITAL": "LOCATION",
    "CLINIC": "LOCATION",
    "ADDRESS": "LOCATION",
    "CITY": "LOCATION",
    "STATE": "LOCATION",
    "ZIP": "LOCATION",
    "DATE": "DATE",
    "ADMISSION_DATE": "DATE",
    "DISCHARGE_DATE": "DATE",
    "BIRTH_DATE": "DATE",
    "AGE": "AGE",
    "PHONE_NUMBER": "CONTACT",
    "PHONE": "CONTACT",
    "EMAIL_ADDRESS": "CONTACT",
    "EMAIL": "CONTACT",
    "FAX": "CONTACT",
    "MEDICAL_RECORD_NUMBER": "IDENTIFIER",
    "MRN": "IDENTIFIER",
    "HEALTH_PLAN_BENEFICIARY_NUMBER": "IDENTIFIER",
    "SOCIAL_SECURITY_NUMBER": "IDENTIFIER",
    "SSN": "IDENTIFIER",
    "ACCOUNT_NUMBER": "IDENTIFIER",
    "LICENSE_NUMBER": "IDENTIFIER"
}


# ==============================================================================
# 1. FILE RESOLUTION & SAFE DOWNLOAD
# ==============================================================================

def find_existing_raw_file():
    """Checks if any raw ASQ-PHI source file exists locally."""
    for path in CANDIDATE_RAW_FILES:
        if os.path.exists(path):
            return path
    return None


def download_asq_phi():
    """Attempts to resolve local raw data or download from GitHub mirrors."""
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # 1. Check if raw file already exists locally
    existing = find_existing_raw_file()
    if existing:
        print(f" Raw dataset already present locally at: {existing}")
        return existing
        
    print(" Attempting download of ASQ-PHI benchmark dataset from GitHub...")
    urls_to_try = [
        "https://raw.githubusercontent.com/JamesWeatherhead/asq-phi/main/data/synthetic_clinical_queries.txt",
        "https://raw.githubusercontent.com/JamesWeatherhead/asq-phi/main/synthetic_clinical_queries.txt",
        "https://raw.githubusercontent.com/JamesWeatherhead/asq-phi/main/data/asq_phi.jsonl"
    ]
    
    target_path = os.path.join(RAW_DIR, "synthetic_clinical_queries.txt")
    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f" Successfully downloaded from {url}")
            return target_path
        except Exception:
            continue

    return None


# ==============================================================================
# 2. PARSE AND EXTRACT PROMPTS + LABELS
# ==============================================================================

def parse_asq_phi_file(source_file):
    """Parses text-delimited blocks or JSONL into standard instruction records."""
    if not source_file or not os.path.exists(source_file):
        return []

    records = []
    
    # CASE A: Standard delimited text block file
    if source_file.endswith(".txt"):
        with open(source_file, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = content.split("===QUERY===")
        for idx, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue
            parts = block.split("===PHI_TAGS===")
            query_text = parts[0].strip()
            phi_elements = []
            if len(parts) > 1:
                for line in parts[1].strip().split("\n"):
                    line = line.strip()
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            tag_obj = json.loads(line)
                            raw_type = tag_obj.get("identifier_type", "OTHER_PHI")
                            phi_elements.append({
                                "category": HIPAA_MAPPING.get(raw_type.upper(), "OTHER_PHI"),
                                "value": tag_obj.get("value", "")
                            })
                        except json.JSONDecodeError:
                            continue
            records.append({
                "id": idx + 1,
                "instruction": "Identify and redact all Protected Health Information (PHI) under HIPAA Safe Harbor regulations.",
                "input": query_text,
                "has_phi": len(phi_elements) > 0,
                "output": json.dumps(phi_elements)
            })
        return records

    # CASE B: JSONL file
    with open(source_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            query_text = item.get("query") or item.get("text") or item.get("input") or ""
            if not query_text:
                continue
            raw_entities = item.get("entities") or item.get("phi_tags") or item.get("labels") or []
            phi_elements = []
            for ent in raw_entities:
                if isinstance(ent, dict):
                    raw_type = ent.get("identifier_type") or ent.get("label") or ent.get("type") or "OTHER_PHI"
                    phi_elements.append({
                        "category": HIPAA_MAPPING.get(raw_type.upper(), "OTHER_PHI"),
                        "value": ent.get("value") or ent.get("text") or ""
                    })
            records.append({
                "id": line_num,
                "instruction": "Identify and redact all Protected Health Information (PHI) under HIPAA Safe Harbor regulations.",
                "input": query_text,
                "has_phi": len(phi_elements) > 0,
                "output": json.dumps(phi_elements)
            })
    return records


# ==============================================================================
# 3. STRATIFIED 70 / 15 / 15 PARTITIONING
# ==============================================================================

def stratified_split(records, train_pct=0.70, val_pct=0.15, seed=42):
    """Stratified partition keeping hard-negatives balanced across splits."""
    random.seed(seed)
    
    positives = [r for r in records if r["has_phi"]]
    negatives = [r for r in records if not r["has_phi"]]
    
    random.shuffle(positives)
    random.shuffle(negatives)
    
    n_pos_train = int(len(positives) * train_pct)
    n_pos_val = int(len(positives) * (train_pct + val_pct))
    
    n_neg_train = int(len(negatives) * train_pct)
    n_neg_val = int(len(negatives) * (train_pct + val_pct))
    
    train_set = positives[:n_pos_train] + negatives[:n_neg_train]
    val_set = positives[n_pos_train:n_pos_val] + negatives[n_neg_val:n_neg_val]
    test_set = positives[n_pos_val:] + negatives[n_neg_val:]
    
    random.shuffle(train_set)
    random.shuffle(val_set)
    random.shuffle(test_set)
    
    return {
        "train": train_set,
        "val": val_set,
        "test": test_set
    }


def process_and_partition():
    """Main execution pipeline."""
    print("\n" + "=" * 80)
    print("ASQ-PHI CLINICAL DATASET INGESTION & PARTITIONING PIPELINE")
    print("=" * 80)

    raw_path = download_asq_phi()
    records = parse_asq_phi_file(raw_path) if raw_path else []
    
    if not records:
        # Check if files are already generated in data/processed/
        train_p = os.path.join(PROCESSED_DIR, "train.jsonl")
        val_p = os.path.join(PROCESSED_DIR, "val.jsonl")
        test_p = os.path.join(PROCESSED_DIR, "test.jsonl")
        
        if os.path.exists(train_p) and os.path.exists(val_p) and os.path.exists(test_p):
            print(" Processed files already exist in data/processed/[cite: 1]:")
            for sp, p in [("TRAIN", train_p), ("VAL", val_p), ("TEST", test_p)]:
                with open(p, "r", encoding="utf-8") as pf:
                    count = sum(1 for _ in pf)
                print(f"  • {sp:<5} -> {count} queries verified at {p}")
            print("\nDataset ready. No download needed.")
            print("=" * 80 + "\n")
            return
            
        print(" Notice: Could not locate raw files to re-parse and download failed.")
        print(f" Place the dataset file into '{RAW_DIR}/' to rebuild splits.")
        print("=" * 80 + "\n")
        return

    total_count = len(records)
    total_pos = sum(1 for r in records if r["has_phi"])
    total_neg = total_count - total_pos
    
    print(f"\nTotal queries parsed: {total_count:,}")
    print(f"  • PHI-Positive queries : {total_pos:,}")
    print(f"  • Hard-Negative queries: {total_neg:,}")

    splits = stratified_split(records, train_pct=0.70, val_pct=0.15)
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print("\nGenerated splits:")
    for split_name, subset in splits.items():
        out_path = os.path.join(PROCESSED_DIR, f"{split_name}.jsonl")
        with open(out_path, "w", encoding="utf-8") as f:
            for row in subset:
                f.write(json.dumps(row) + "\n")
        
        pos_count = sum(1 for r in subset if r["has_phi"])
        neg_count = len(subset) - pos_count
        print(f"  • {split_name.upper():<5} -> {len(subset):>4} queries ({pos_count:>3} PHI-positive, {neg_count:>3} hard negatives) saved to {out_path}")
        
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    process_and_partition()