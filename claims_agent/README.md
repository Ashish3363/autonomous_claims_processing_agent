# Insurance Claims Processing Agent

An autonomous agent that processes First Notice of Loss (FNOL) documents (PDF/TXT), extracts key information, validates it, and routes the claim based on business logic.

## Architecture

- **Ingestion**: Reads raw text from FNOL files (supports .txt and .pdf).
- **Extraction**: Uses regex and heuristics (simulating an LLM for the demo) to identify policy details, incident info, and amounts.
- **Validation**: Checks for mandatory fields and consistency (e.g., incident date within effective dates).
- **Routing**: Applies business rules with strict priority to determine the claim route.
- **Output**: Generates a structured JSON file with the extracted data, routing decision, and reasoning.

## Routing Logic & Priority

The agent evaluates claims in the following strict order. The first matching rule determines the route:

1.  **Investigation**: If the description contains fraud indicators (e.g., "staged", "fraud", "inconsistent").
2.  **Specialist Queue**: If the `Claim Type` is "injury".
3.  **Manual Review**: If any **mandatory field** is missing or empty.
4.  **Fast Track**: If `Estimated Damage` < $25,000 and all mandatory fields are present.
5.  **Manual Review**: Fallback for all other cases (e.g., high damage but no missing fields).

**Note**: Examples with missing fields will always go to *Manual Review* unless they trigger *Investigation* or *Specialist Queue* first.

## Directory Structure

```
claims_agent/
├── data/               # Dummy FNOL input files
├── src/                # Source code
│   ├── models.py       # Pydantic data models
│   ├── ingest.py       # File reading logic
│   ├── extract.py      # Field extraction (Regex/LLM-mock)
│   ├── logic.py        # Validation and Routing rules
│   └── utils.py        # Helper functions
├── main.py             # CLI entry point
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Setup & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Agent**:
    ```bash
    python main.py --file data/fnol_01.txt
    ```
    This will print the JSON output to the console.

3.  **Run All Data**:
    A script or batch file can be used to process all files in `data/`.
