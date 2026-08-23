import json
import os
import sys
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.retrieval import embed_text
from app.db.client import supabase

DATA_FILE = "/Users/rishii/SIH-2026/data/indian_standards_master_catalog.json"

def extract_year(text: str) -> str | None:
    match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
    if match:
        return match.group(1)
    return None

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: Data file not found at {DATA_FILE}")
        return

    with open(DATA_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return

    for item in data:
        is_number = item.get("is_number", "")
        year = item.get("year", "")
        standard_id = f"{is_number}:{year}" if year else is_number
        
        title = item.get("title", "")
        
        keywords = item.get("keywords", [])
        tender_spec_snippet = item.get("tender_spec_snippet", "")
        scope = ", ".join(keywords) + " " + tender_spec_snippet
        
        revision = item.get("revision", "")
        reaffirmed_year = item.get("reaffirmed_year", "")
        latest_amendments = item.get("latest_amendments", [])
        
        # Build latest_version
        latest_version = f"{revision}" if revision else ""
        if reaffirmed_year:
            if latest_version:
                latest_version += f", Reaffirmed {reaffirmed_year}"
            else:
                latest_version = f"Reaffirmed {reaffirmed_year}"
                
        if latest_amendments:
            amendments_str = ", ".join(latest_amendments)
            if latest_version:
                latest_version += f" - {amendments_str}"
            else:
                latest_version = amendments_str
                
        # Extract amendment_date
        amendment_date = None
        if latest_amendments:
            last_amendment = latest_amendments[-1]
            extracted = extract_year(last_amendment)
            if extracted:
                amendment_date = extracted
                
        qco_details = item.get("qco_details", {})
        is_mandatory_qco = qco_details.get("is_mandatory", False)
        
        print(f"Processing {standard_id}...")
        
        text_to_embed = f"Title: {title}\nScope/Keywords: {scope}"
        try:
            embedding = embed_text(text_to_embed)
        except RuntimeError as e:
            print(f"Failed to embed {standard_id}: {e}")
            continue

        standard_record = {
            "standard_id": standard_id,
            "title": title,
            "scope": scope,
            "embedding": embedding,
            "latest_version": latest_version,
            "amendment_date": amendment_date,
            "is_mandatory_qco": is_mandatory_qco
        }

        try:
            if supabase is None:
                raise RuntimeError("Supabase client is not initialized.")
            supabase.table("standards").upsert(standard_record).execute()
        except Exception as e:
            print(f"Failed to upsert standard {standard_id}: {e}")
            continue
            
        # References
        references_to_insert = []
        for ref in item.get("normative_references", []):
            ref_id = ref.get("is_number") if isinstance(ref, dict) else str(ref)
            if not ref_id:
                continue
            references_to_insert.append({
                "standard_id": standard_id,
                "referenced_id": ref_id,
                "referenced_title": ref.get("title") if isinstance(ref, dict) else None,
                "relationship_type": ref.get("relationship", "normative") if isinstance(ref, dict) else "normative"
            })
            
        for ref in item.get("allied_standards", []):
            ref_id = ref.get("is_number") if isinstance(ref, dict) else str(ref)
            if not ref_id:
                continue
            references_to_insert.append({
                "standard_id": standard_id,
                "referenced_id": ref_id,
                "referenced_title": ref.get("title") if isinstance(ref, dict) else None,
                "relationship_type": ref.get("relationship", "allied") if isinstance(ref, dict) else "allied"
            })
            
        if references_to_insert:
            try:
                supabase.table("standard_references").upsert(references_to_insert).execute()
            except Exception as e:
                print(f"Failed to upsert references for {standard_id}: {e}")

    print("Ingestion completed successfully.")

if __name__ == "__main__":
    main()
