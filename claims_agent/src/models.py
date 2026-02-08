from pydantic import BaseModel
from typing import List, Optional

class FNOLExtractedFields(BaseModel):
    policyNumber: Optional[str] = None
    policyholderName: Optional[str] = None
    effectiveDates: Optional[str] = None
    incidentDate: Optional[str] = None
    incidentTime: Optional[str] = None
    incidentLocation: Optional[str] = None
    incidentDescription: Optional[str] = None
    claimant: Optional[str] = None
    thirdParties: Optional[str] = None
    contactDetails: Optional[str] = None
    assetType: Optional[str] = None
    assetId: Optional[str] = None
    estimatedDamage: Optional[float] = None
    claimType: Optional[str] = None
    attachments: Optional[List[str]] = None
    initialEstimate: Optional[float] = None

class RoutingOutput(BaseModel):
    extractedFields: FNOLExtractedFields
    missingFields: List[str]
    recommendedRoute: str
    reasoning: str
