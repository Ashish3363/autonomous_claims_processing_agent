import re
import json
from .models import FNOLExtractedFields

def extract_fields(text: str) -> FNOLExtractedFields:
    """
    Extracts fields from FNOL text using a hybrid approach:
    1. Regex for structured data.
    2. Mock LLM (heuristics) for unstructured data to simulate AI behavior.
    """
    data = {}

    # --- 1. Regex Extraction ---
    # Policy Number
    # Match "Policy Number: <value>" or "Policy #: <value>"
    # Exclude matches like "Policy Information" by ensuring a separator or digit follows
    policy_match = re.search(r"Policy\s*(?:Number|#)[\s:]+([A-Z0-9-]+)", text, re.IGNORECASE)
    if policy_match:
        data["policyNumber"] = policy_match.group(1)

    # Policyholder Name (Simple heuristic: Line after "Policyholder" or matches "Policyholder: Name")
    name_match = re.search(r"Policyholder(?: Name)?[:\s]+([A-Za-z\s]+?)(?:\n|$|Effective)", text, re.IGNORECASE)
    if name_match:
        clean_name = name_match.group(1).strip()
        if "Information" not in clean_name:
            data["policyholderName"] = clean_name

    # Effective Dates
    dates_match = re.search(r"(?:Effective|Valid)\s*(?:Dates|From)?[:\s]*(\d{4}-\d{2}-\d{2}.*?\d{4}-\d{2}-\d{2})", text, re.IGNORECASE | re.DOTALL)
    if dates_match:
        data["effectiveDates"] = dates_match.group(1).strip()
        
    # Incident Date
    # Look for Date pattern specifically in Incident section or labeled as such
    inc_date_match = re.search(r"(?:Incident|Date)[:\s]*(\d{4}-\d{2}-\d{2})", text, re.IGNORECASE)
    if inc_date_match:
        data["incidentDate"] = inc_date_match.group(1)

    # Incident Time
    time_match = re.search(r"Time[:\s]*(\d{2}:\d{2})", text, re.IGNORECASE)
    if time_match:
        data["incidentTime"] = time_match.group(1)

    # Estimated Damage
    damage_match = re.search(r"(?:Estimated|Est\.?)\s*Damage[:\s]*[\$]?([\d,]+(?:\.\d{2})?)", text, re.IGNORECASE)
    if damage_match:
        try:
            data["estimatedDamage"] = float(damage_match.group(1).replace(",", ""))
        except ValueError:
            pass
            
    # Initial Estimate
    init_est_match = re.search(r"Initial\s*(?:Estimate|Est\.?)[:\s]*[\$]?([\d,]+(?:\.\d{2})?)", text, re.IGNORECASE)
    if init_est_match:
        try:
            data["initialEstimate"] = float(init_est_match.group(1).replace(",", ""))
        except ValueError:
            pass

    # Claim Type
    type_match = re.search(r"Claim\s*Type[:\s]*([A-Za-z]+)", text, re.IGNORECASE)
    if type_match:
        data["claimType"] = type_match.group(1).lower()

    # --- 2. Mock LLM / Heuristics for Unstructured Data ---
    # In a real scenario, we would send 'text' to an LLM API here.
    # For this assessment, we use advanced heuristics to fill in the gaps.
    
    # Description
    desc_match = re.search(r"Description[:\s]*([^\n]+(?:(?:\n(?!Involved|Asset|Claim)[^\n]+)*))", text, re.IGNORECASE)
    if desc_match:
        data["incidentDescription"] = desc_match.group(1).strip().replace("\n", " ")
    
    # Location
    loc_match = re.search(r"(?:Location|Loc|Place)[:\s]*([^\n]+)", text, re.IGNORECASE)
    if loc_match:
        data["incidentLocation"] = loc_match.group(1).strip()

    # Claimant
    claimant_match = re.search(r"Claimant[:\s]*([^\n]+)", text, re.IGNORECASE)
    if claimant_match:
        data["claimant"] = claimant_match.group(1).strip()
        
    # Asset Type
    # Use specific match for "Asset Type" or "Vehicle Info" etc.
    # Avoid "Asset Details" header by requiring "Type" or specific key
    asset_match = re.search(r"Asset\s*Type[:\s]+([^\n]+)", text, re.IGNORECASE)
    if asset_match:
        data["assetType"] = asset_match.group(1).strip()

    # Asset ID
    vin_match = re.search(r"(?:Asset ID|VIN)[:\s]+([A-Z0-9-]+)", text, re.IGNORECASE)
    if vin_match:
        data["assetId"] = vin_match.group(1)

    return FNOLExtractedFields(**data)
