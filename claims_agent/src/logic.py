from typing import List
from .models import FNOLExtractedFields, RoutingOutput

FRAUD_KEYWORDS = ["fraud", "inconsistent", "staged", "suspicious"]
FASTTRACK_LIMIT = 25000.0

MANDATORY_FIELDS = [
    "policyNumber",
    "policyholderName",
    "effectiveDates",
    "incidentDate",
    "incidentDescription",
    "estimatedDamage",
    "claimType",
    "assetType",
    "initialEstimate"
]

def find_missing_fields(fields: FNOLExtractedFields) -> List[str]:
    """Identifies missing mandatory fields."""
    missing = []
    # Convert pydantic model to dict to iterate
    data = fields.model_dump()
    
    for field in MANDATORY_FIELDS:
        value = data.get(field)
        if value is None or value == "" or value == []:
            missing.append(field)
            
    return missing

def decide_route(fields: FNOLExtractedFields, missing: List[str]) -> str:
    """Determines the routing path based on business rules."""
    desc = (fields.incidentDescription or "").lower()
    claim_type = (fields.claimType or "").lower()
    est_damage = fields.estimatedDamage

    # 1. Investigation Flag
    if any(keyword in desc for keyword in FRAUD_KEYWORDS):
        return "Investigation"
    
    # 2. Specialist Queue
    if "injury" in claim_type:
        return "SpecialistQueue"
    
    # 3. Manual Review (if missing fields)
    if missing:
        return "ManualReview"
    
    # 4. Fast Track
    if est_damage is not None and est_damage < FASTTRACK_LIMIT:
        return "FastTrack"
        
    # 5. Default
    return "ManualReview"

def build_reasoning(route: str, fields: FNOLExtractedFields, missing: List[str]) -> str:
    """Generates a natural language explanation for the decision."""
    parts = []
    
    if route == "Investigation":
        found_keywords = [w for w in FRAUD_KEYWORDS if w in (fields.incidentDescription or "").lower()]
        parts.append(f"Flagged for investigation due to suspicious keywords in description: {', '.join(found_keywords)}.")
        
    elif route == "SpecialistQueue":
        parts.append("Routed to Specialist Queue because claim involves bodily injury.")
        
    elif route == "ManualReview":
        if missing:
            parts.append(f"Sent for Manual Review due to missing mandatory fields: {', '.join(missing)}.")
        else:
            parts.append("Sent for Manual Review as it did not qualify for Fast Track (damage > threshold or other criteria).")
            
    elif route == "FastTrack":
        parts.append(f"Approved for Fast Track. Estimated damage (${fields.estimatedDamage}) is under the ${FASTTRACK_LIMIT} limit and all mandatory fields are present.")
        
    return " ".join(parts)
